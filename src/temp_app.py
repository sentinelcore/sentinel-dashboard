from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ FastAPI is running!"}

@app.get("/test")
async def test():
    return {"status": "✅ Test route works!"}
