from fastapi import FastAPI

from app.api.routes import experiment, auth


app = FastAPI()

app.include_router(experiment.router)
app.include_router(auth.router)


@app.get("/")
def get_home():
    return {"hello": "world"}
