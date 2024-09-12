# Capstone_PV_API

## environment set-up

### dev environment

To set up for local development, type the following command into bash.

```bash
# create virtual environment and name it ".venv"
python -m venv .venv

# activate the environment
source .venv/Scripts/activate

# make sure that we are not using global python environment
which python

# install the required package
pip install -r requirements.txt

# run the api in dev mode
fastapi dev ./app/main.py

```

> Whenever install a package using `pip install`, we need to run `pip freeze > requirements.txt` to keep track of the packages used in this project

> Sometimes package is not resolve automatically. If you are using vscode, add this line of code into `.vscode/settings.json`: 
`{"python.analysis.extraPaths": ["./.venv"]}`


### run the container app

Make sure docker desktop is up and running, then type `docker compose up -d` to run the containerized application. The API will be accepting request at port `8080`.
