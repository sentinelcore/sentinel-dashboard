from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ FastAPI is running from debug_test!"}
