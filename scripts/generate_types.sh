#!/bin/bash

echo "Generating OpenAPI Schema..."
PYTHONPATH=./src/backend python3 scripts/generate_openapi.py

echo "Generating Typescript Types..."
openapi-typescript scripts/openapi.json -o src/frontend/src/models/index.ts

echo "Cleaning Up..."
rm scripts/openapi.json

echo "Finished!"