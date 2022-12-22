from outline_vpn.outline_vpn import OutlineVPN
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.models import *
from src.db import *

client = OutlineVPN(api_url="https://34.235.115.252:62280/Kbi7e6u53KhnSYLwfZIleA")

app = FastAPI()

@app.get("/create_key", response_model=User)
async def read_item(username: str = None):
    key = client.create_key(key_name=username)
    sql = 'INSERT INTO USER (id, name, age) values(?, ?, ?)'
    data = [
        (key.key_id, key.name, 21)]
    with con:
        con.executemany(sql, data)
    json_object = {"id" : key.key_id,
                   "username" : key.name,
                   "password" : key.password,
                   "access_url" : key.access_url}
    json_compatible_item_data = jsonable_encoder(json_object)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/retrieve_key", response_model=User)
async def root(username: str = None, password : str = None):
    sql = 'SELECT * FROM USER WHERE username = ? and password = ?'
    with con:
        con.executemany(sql,(username,password))
    return None