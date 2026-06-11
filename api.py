from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "Retail AI Running"
    }


@app.get("/health")
def health():
    return {
        "healthy": True
    }