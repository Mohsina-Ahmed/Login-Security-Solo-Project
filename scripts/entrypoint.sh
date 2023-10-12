#!/bin/sh

set -e # exit if errors happen anywhere

# Load environment variables from the .env file using python-dotenv
#python -m dotenv -f .env
python -m dotenv.cli -f .env run flask run

flask init-db
flask run --host=0.0.0.0
