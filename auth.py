# auth.py
from fastapi import APIRouter, HTTPException, Request, Depends, Header
from fastapi.responses import JSONResponse
from database import fetch_single_row, register_user
import jwt
import datetime

SECRET_KEY = "11223344"

router = APIRouter()

# Helper function to validate JWT token
def validate_token(authorization: str = Header(...)):
    try:
        # Check if the header starts with "Bearer " and extract the token
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["data"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login")
async def login(request: Request):
    data = await request.json()
    query = "SELECT id, email,name,coins,cell,city,address,is_admin FROM public.user WHERE email = %s AND password = %s;"
    params = (data["email"], data["password"])
    row = fetch_single_row(query, params)

    if row is not None:
        # Create the JWT token
        token = jwt.encode({"data": row}, SECRET_KEY, algorithm="HS256")
        # token_string = token.decode("utf-8")
        response_data = {"success": True, "data": {
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "coins": row[3],
            "cell": row[4],
            "city": row[5],
            "address": row[6],
            "is_admin": row[7],
        }, "token": token, "message": "User Logged In Successfully!"}
        return response_data
    else:
        # Invalid credentials, return error response
        error_response = {"success": False, "message": "Invalid Credentials"}
        return JSONResponse(status_code=401, content=error_response)


@router.post("/register")
async def register(request: Request):
    data = await request.json()
    query = "SELECT * FROM public.user WHERE email = %s or cell = %s;"
    params = (data["email"], data["cell"])
    row = fetch_single_row(query, params)

    if row is not None:
        return {"success": False, "message": "User has already been register please login again!"}
    else:
        query = "INSERT into public.user (email,password,name,coins,cell,city,address,is_admin)VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        params = (data["email"], data["password"], data["name"], data["coins"], data["cell"], data["city"], data["address"],
                  data["is_admin"])
        response = register_user(query, params)
        return response

@router.post("/checktoken")
async def check_token(data: dict = Depends(validate_token)):
    return {"success": True, "data": data, "message": "Token is valid"}
