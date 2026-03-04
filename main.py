from fastapi import FastAPI


app = FastAPI()


@app.get("/home")
def get_gome():
    return {"hello": "world"}
