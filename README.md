A boilterplate for creating backend API using FastAPI

to run

bash scripts/dev.sh

to test

`python -m pytest`

## Access Swagger Documentation

> <http://localhost:8080/docs>

## Access Redocs Documentation

> <http://localhost:8080/redoc>

## Project structure

Files related to application are in the `app` or `tests` directories.
Application parts are:

    
    |---Fast-API stuff
    ├── api                 - web related stuff.
    │   └── routes          - web routes.
    ├── core                - application configuration, startup events, logging.
    ├── models              - pydantic models for this application.
    ├── services            - logic that is not just crud related.
    ├── main-aws-lambda.py  - [Optional] FastAPI application for AWS Lambda creation and configuration.
    └── main.py             - FastAPI application creation and configuration.
    |
    ├── data             - where you persist data locally
    │   ├── interim      - intermediate data that has been transformed.
    │   ├── processed    - the final, canonical data sets for modeling.
    │   └── raw          - the original, immutable data dump.
    │
    └── tests            - pytest
