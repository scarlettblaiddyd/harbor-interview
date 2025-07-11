from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pathlib import Path
import tempfile
import dateparser
from dateparser.search import search_dates
import datefinder
import spacy
from docx import Document
from models import ExtractedEventResponse

nlp = spacy.load("en_core_web_sm")

# This function was written mostly by AI, I'm not very familiar with NLP
# It seems to produce usable results, and is certainly better than my earlier implementation
def extract_title(sentence: str) -> str:
    doc = nlp(sentence)

    skip_words = {
        "i", "we", "you", "he", "she", "it", "they", "them",
        "day", "time", "today", "tomorrow", "tonight",
        "am", "pm",
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
    }

    skip_words = {w.lower() for w in skip_words}  # ensure all lowercase

    # 1. Prefer meaningful noun chunks
    for chunk in doc.noun_chunks:
        chunk_words = chunk.text.strip().lower().split()
        if (
            chunk.root.pos_ in ("NOUN", "PROPN") and
            not any(w in skip_words for w in chunk_words) and
            not any(ent.label_ == "DATE" and ent.start <= chunk.start < ent.end for ent in doc.ents)
        ):
            return chunk.text.title()

    # 2. Try VERB + NOUN combo
    for i, token in enumerate(doc):
        if token.pos_ == "VERB":
            for j in range(i + 1, len(doc)):
                next_token = doc[j]
                # Inside the VERB + NOUN logic block
                if (
                    next_token.pos_ == "NOUN" and
                    next_token.text.lower() not in skip_words and
                    not any(ent.label_ == "DATE" and next_token.i >= ent.start and next_token.i < ent.end for ent in doc.ents)
                ):
                    return f"{token.text.title()} {next_token.text.title()}"

    # 3. Fallback: first 2–3 significant tokens (excluding dates, skip words)
    keywords = []
    for token in doc:
        if (
            not token.is_stop and not token.is_punct and
            token.text.lower() not in skip_words and
            not any(ent.label_ == "DATE" and token.i >= ent.start and token.i < ent.end for ent in doc.ents)
        ):
            keywords.append(token.text.title())
        if len(keywords) >= 3:
            break

    return " ".join(keywords) if keywords else "Untitled"


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://scarlettblaiddyd.github.io/harbor-interview"], # or * for later
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)

@app.get('/')
async def root():
    return {'message': 'Boop'}

@app.post('/upload', response_model=ExtractedEventResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    events = []

    for file in files:
        # Save temp file on server for processing w/ docx
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

    
        # Extract text from the .docx file
        doc = Document(tmp_path)

        # Search each paragraph individually for a date using NLP
        # This approach is much slower than just parsing for date objects
        # But provides much more useful information
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        for paragraph in paragraphs:
            spacy_doc = nlp(paragraph)

            for ent in spacy_doc.ents:
                if ent.label_ in ("DATE", "TIME"):
                    parsed = dateparser.parse(ent.text)
                    if not parsed:
                        continue

                    title = extract_title(paragraph)

                    events.append({
                        "date": parsed.strftime("%m/%d/%Y"),
                        "title": title,
                        "context": paragraph,
                        "document": file.filename
                    })
        # Delete temporary file
        Path(tmp_path).unlink()

    return {"events": events}


