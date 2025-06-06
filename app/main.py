from fastapi import FastAPI, Request, HTTPException, Depends
from app.limiter import is_allowed


app = FastAPI()

def get_client_ip(request: Request) -> str:
    return request.client.host

def check_rate_limit(request: Request):
    ip = get_client_ip(request)
    result = is_allowed(ip)
    if not result["allowed"]:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "retry_after": result["retry_after"]
            }
        )
    return result

@app.get("/")
def root():
    return {"message": "Rate limiter is working!"}

@app.get("/api/data")
def get_data(rate_info=Depends(check_rate_limit)):
    return {
        "message": "Here is your data!",
        "rate_limit_info": rate_info
    }

@app.get("/rate-limit/status")
def status(request: Request):
    ip = get_client_ip(request)
    result = is_allowed(ip)
    return result
