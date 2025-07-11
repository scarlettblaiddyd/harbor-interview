# Document Date Visualizer

This repo is Scarlett Blaiddyd's submission for the Harbour interview process. It consists of a FastAPI python backend and a Vue.js typescript frontend.

## Overview

The python backend (`src/backend`) uses spacy - a natural language processing library - to extract dates from the provided .docx files and try to infer some context. It's not the smartest at figuring out what a sentence means, but if the surrounding text is concise (i.e. Submit Report By 10/12/2025) it can pick it up correctly.

The typescript frontend (surprise surprise, in `src/frontend`) uses Vue with the `fullcalendar` package to display and populate a calendar, and the `@harbour-enterprises/superdoc` package to display .docx files. You can select an event from the calendar and click the "view event source" button to have superdoc jump you right to where in the document an event was found.

## Hosting

The backend is hosted on https://render.com/ (at https://date-extraction-api.onrender.com) using the free tier. Since it's in free tier, they will put it to sleep after a period of inactivity, so it can take a minute or so for the service to spin up. If you see the loading spinner for a long time, assume that's the issue, as an alert will display if there was actually an error when processing your docx files.

The frontend is hosted right here on github via github pages. https://scarlettblaiddyd.github.io/harbor-interview/

## Development

Docker is set up to make testing easier. From the project root, `docker-compose up --build` should build the containers and get both the front and backends running. You can check out the FastAPI docks at localhost:8000/docs, and the frontend is served at localhost:5173

<span style="color:red">
KNOWN ISSUE: For some reason, bun and vite really haven't been playing nice with docker.
</span>

I know that it kind of defeats the purpose of docker, but installing dependencies with

```
cd src/frontend
bun install
```

and then letting docker copy the existing `node_modules` folder into the container seems to fix it? Sorry, 30 mins of troubleshooting didn't produce a fix so I'm just gonna submit this as it
(-‿-")
