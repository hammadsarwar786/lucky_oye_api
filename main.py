# main.py
from fastapi import FastAPI
from auth import router as auth_router
from notification import router as notifi
from fastapi.middleware.cors import CORSMiddleware
# CORS configuration


app = FastAPI()

origins = ["*"]
# laptop_ip = "52.0.41.103"
laptop_ip = "127.0.0.1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins  + [f"http://{laptop_ip}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# baseurl/api/notification
# baseurl/api/socket/notification
app.include_router(notifi, prefix="/api", tags=["notification"])

# baseurl/api/login
# baseurl/api/signup
app.include_router(auth_router, prefix="/api", tags=["authentication"])


# Run the server
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)