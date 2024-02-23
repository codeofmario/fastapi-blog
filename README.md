# Architecture of a FastAPI Rest API with JWT Authentication

## TECH STACK
- Python
- FastAPI
- Posgresql
- Redis
- Minio/S3


## START PROJECT
### run docker compose
```console
sudo docker-compose up -d
```

### install project dependencies
```console
poetry install
```

### run server
```console
poetry run uvicorn main:app --reload
```

Visit the [Swagger docs](http://localhost:8000/docs)
