# auth.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from database import fetch_single_row
import jwt
import datetime

SECRET_KEY = "11223344"

router = APIRouter()

@router.post("/login")
async def login(request: Request):
    data = await request.json()
    query = "SELECT email,name,credit FROM public.user WHERE email = %s AND password = %s;"
    params = (data["email"], data["password"])
    row = fetch_single_row(query, params)

    if row is not None:
        # User logged in successfully, return success response with data
        # Set the expiration time to 1 hour from now
        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        # Create the JWT token
        token = jwt.encode({"data": row, "exp": expiration_time}, SECRET_KEY, algorithm="HS256")
        # Convert the token to a string (by default, it's bytes)
        # token_string = token.decode("utf-8")
        response_data = {"success": True, "data": row, "token" : token, "message": "User Logged In Successfully!"}
        return response_data
    else:
        # Invalid credentials, return error response
        error_response = {"success": False, "message": "Invalid Credentials"}
        return JSONResponse(status_code=401, content=error_response)