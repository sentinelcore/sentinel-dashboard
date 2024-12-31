from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ FastAPI is running!"}

@app.get("/test")
async def test():
    return {"status": "✅ Test route works!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
