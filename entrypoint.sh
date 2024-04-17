#!/bin/bash

# Pull the latest changes from Git
git pull

# Migrate the database
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

# Start your application
python3 app.py