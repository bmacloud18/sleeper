import os
import logging
import random
from jose import jwt
from datetime import datetime, timedelta, timezone

from openai import OpenAI

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from dotenv import load_dotenv
load_dotenv()

import psycopg
from psycopg import Connection
from psycopg_pool import ConnectionPool
# from psycopg.rows import dict_row
DB_URL = os.environ.get('DB_URL')
pool: ConnectionPool = None


from util import get_token, verify_token
# TOKEN_NAME = os.environ.get('TOKEN_NAME')
# API_SECRET = os.environ.get('API_SECRET')
# ALGORITHM = "HS256"

# EXP_TIME = 900 # < 15 minutes left

# setup FastAPI backend application, allowing CORS requests from domain
app = FastAPI()

def get_db():
    with pool.connection() as con:
        yield con

@app.on_event("startup")
def startup():
    global pool
    pool = ConnectionPool(DB_URL, min_size=1, max_size=10)

@app.on_event("shutdown")
def shutdown():
    pool.close()

@app.post("/inconspicuousroute")
def get_token_route():
    get_token()


@app.get("/")
def get_home(valid: bool = Depends(verify_token), connection: Connection = Depends(get_db)):
    return {"message": "home point hit"}