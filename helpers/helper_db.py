from psycopg import AsyncCursor, AsyncConnection
from helpers.helper_config import get_config

__asyncConnection: AsyncConnection = None


async def _connect(user: str, password: str) -> None:
    global __asyncConnection
    config = get_config()
    __asyncConnection = await AsyncConnection.connect(
        dbname=config.db_name,
        user=user,
        password=password,
        host=config.db_host,
        port=config.db_port,
    )


async def connect_submitter():
    config = get_config()
    await _connect(config.db_user_submitter, config.db_password_submitter)


async def connect_notifier():
    config = get_config()
    await _connect(config.db_user_notifier, config.db_password_notifier)


async def disconnect() -> None:
    global __asyncConnection
    await __asyncConnection.close()
    __asyncConnection = None


def get_cursor() -> AsyncCursor:
    global __asyncConnection
    return __asyncConnection.cursor()


async def commit() -> None:
    global __asyncConnection
    await __asyncConnection.commit()
