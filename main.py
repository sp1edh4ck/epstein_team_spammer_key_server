import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from database.crud import Database

db = Database()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/get_version")
async def get_version():
    return {"version": "0.0.1"}


@app.get("/check_by_key")
async def check_by_key(data):
    key = data.get("key")
    logger.info(f"Checking key: {key}")
    if not key:
        return {"status": False}
    license_data = await db.get_license(key)
    if not license_data:
        return {"status": False}
    return {"status": True}


@app.post("/bind_by_hardware")
async def bind_by_hardware(data):
    license_data = await db.get_license(data.key)
    if not license_data or not license_data["is_active"]:
        return {"status": False}
    current_hardware = license_data.get("hardware_id")
    hardware_id = f"{data.pc_id}_{data.uuid_system}"
    if current_hardware and current_hardware != hardware_id:
        return {"status": False}
    if not current_hardware:
        await db.bind_hardware(data.key, hardware_id)
    return {"status": True}


async def main():
    await db.connect()


if __name__ == "__main__":
    asyncio.run(main())
