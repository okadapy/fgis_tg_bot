import asyncio
import multiprocessing
import subprocess
from app.database.requests import create_tables
from sys import stdout


async def main():
    await create_tables()
    ap = subprocess.Popen(["python", "start_arshin.py"])
    qp = subprocess.Popen(["python", "start_quasar.py"])

    qp.wait()
    ap.wait()


asyncio.run(main())
