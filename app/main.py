from fastapi import FastAPI

app = FastAPI(title="DevSecOps Demo API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/echo/{msg}")
def echo(msg: str):
    return {"message": msg}
