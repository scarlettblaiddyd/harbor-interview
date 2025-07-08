from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from pathlib import Path
import tempfile
import re
import dateparser
from docx import Document

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/upload')
async def upload_files(files: List[UploadFile] = File(...)):
    all_dates = []

    for file in files:
        # Save temp file on server for processing w/ docx
        suffix = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

    
        # Extract text from the .docx file
        doc = Document(tmp_path)
        text = "\n".join([p.text for p in doc.paragraphs])

        # Find dates using regex
        # Asked chatGPT for a slightly more robust date amtcher. Still not happy with this but I can test a bit more now
        pattern = r"\b(?:\d{1,2}/\d{1,2}/\d{4}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:st|nd|rd|th)?(?:, \d{4})?)\b"
        matches = re.finditer(pattern, text)

        print("Document: " + file.filename)
        for match in matches:
            raw_date = match.group(0)
            parsed_date = dateparser.parse(raw_date)
            if not parsed_date:
                continue

            print("Found date: " + parsed_date.strftime("%m/%d/%Y"))

            # Extract a little context around the match
            # TODO: Strip newlines out of context?
            # TODO: NLP to extract context and/or a title?
            context_start = max(0, match.start() - 30)
            context_end = min(len(text), match.end() + 30)
            context = text[context_start:context_end].strip()


            # TODO: Add a title field?
            # TODO: Can I define/export this event format somewhere for use by the frontend?
            # Need to look into (maybe FastAPI does it automatically?)
            all_dates.append({
                "date": parsed_date.strftime("%m/%d/%Y"),
                "context": context,
                "document": file.filename
            })

        # Optional: delete temporary file
        Path(tmp_path).unlink()

    return {"dates": all_dates}


