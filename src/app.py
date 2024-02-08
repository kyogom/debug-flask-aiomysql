import asyncio
import aiomysql
from flask import Flask, jsonify
import asyncio
import os
from aiomysql import create_pool

pool = None


async def create_or_get_pool():
    global pool
    if pool:
        return pool
    pool = await create_pool(
        host=os.getenv("DB_HOST"),
        port=3306,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_DATABASE"),
        autocommit=True,
        charset="utf8mb4",
        pool_recycle=300,
        loop=asyncio.get_event_loop(),
    )
    return pool


async def create_app():
    app = Flask(__name__)

    @app.route("/api/users", methods=["GET"])
    async def _():
        pool = await create_or_get_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute("SELECT 10")
                result = await cur.fetchone()
        return jsonify(result)

    return app


async def main():
    app = await create_app()
    return app


app = asyncio.run(main())
