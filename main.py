import asyncio

from fastapi import FastAPI, Request
from database.crud import Database

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield

app = FastAPI(lifespan=lifespan)
db = Database()


@app.get("/get_version")
async def get_version():
    return {"version": "0.0.1"}


@app.post("/check_by_key")
async def check_by_key(request: Request):
    data = await request.json()
    key = data.get("key")
    if not key:
        return {"status": False}
    try:
        license_data = await db.get_license(key)
    except Exception as e:
        return {"status": False}
    if not license_data:
        return {"status": False}
    return {"status": True}


@app.post("/get_hwid")
async def bind_by_hardware(request: Request):
    data = await request.json()
    key = data.get("key")
    hwid = data.get("hwid")
    if not hwid:
        return {"status": False}
    try:
        hwid_data = await db.get_hwid(key)
    except Exception as e:
        print(e)
        return {"status": False}
    if hwid_data is None:
        await db.set_hwid(key, hwid)
        return {"status": True}
    if hwid != hwid_data:
        return {"status": False}
    return {"status": True}
