from fastapi import FastAPI

from app.api.routes import experiment


app = FastAPI()

app.include_router(experiment.router)


@app.get("/")
def get_home():
    return {"hello": "world"}
