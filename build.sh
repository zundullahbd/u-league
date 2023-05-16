#!/bin/bash

# Build the project
echo "Building the project..."
python3 -m pip install -r requirements.txt

echo "Make Migration..."
python3 manage.py makemigrations 
python3 manage.py migrate 

echo "Collect Static Files..."
python3 manage.py collectstatic --noinput
