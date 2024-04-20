#!/bin/bash


# Exit immediately if any command fails
set -e

# Pull the latest changes from Git
git pull origin master

flask db upgrade

# Start your application
exec python3 app.py