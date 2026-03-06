import asyncio

from fastapi import FastAPI

from database.crud import Database

app = FastAPI()
db = Database()


@app.get("/get_version")
async def get_version():
    return {"version": "0.0.1"}


@app.post("/check_by_key")
async def check_by_key(data):
    license_data = await db.get_license(data.key)
    if license_data and license_data["is_active"]:
        return {"status": True}
    return {"status": False}


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
