from fastapi import FastAPI

from app.api.routes import experiment


app = FastAPI()

app.include_router(experiment.router)


@app.get("/home")
def get_gome():
    return {"hello": "world"}
