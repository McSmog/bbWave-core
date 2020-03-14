from fastapi import FastAPI

app = FastAPI()

@app.get("/audio/")
async def list_audio():
    return {"list" : "yes"}