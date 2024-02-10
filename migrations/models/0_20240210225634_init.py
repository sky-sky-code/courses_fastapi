from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "courses" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "direction" VARCHAR(128) NOT NULL,
    "value" DOUBLE PRECISION NOT NULL,
    "exchanger_id" INT NOT NULL REFERENCES "courses" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "exchanger" (
    "uid" UUID NOT NULL  PRIMARY KEY,
    "exchanger" VARCHAR(16) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
