# INF II Demo(s) 

# Database Setup 
You can setup a mongo db instance as a standalone server on your own physical machine, or use a container for that.

## Setup for running the demo with containers 

1. Install [Docker Desktop](https://www.docker.com/get-started/) 
2. Install [python](https://www.python.org/)
    1. generate virtual environment in this folder via ```python -m venv .venv```
    1. install dependencies in the new venv (using a new terminal window) ```pip install -r requirements.txt```
3. Initialize mongodb, mongo express and the xeokit viewer using ```docker compose up -d```
4. cd into the app directory ```cd .\app\```
5. run fastapi app via uvicorn using ```uvicorn main:app --reload```
6. Service is available on [http://127.0.0.1:8000](http://127.0.0.1:8000)
7. API Documentation is available under [/docs](http://127.0.0.1:8000/docs)

