from aiohttp import request

from helpers.helper_config import Config, get_config
from helpers.helper_logger import get_logger

from abc import (
    ABC,
    abstractmethod,
)

from constants.urls import URL_TELEGRAM_API


class RequestBase(ABC):
    config: Config
    method_name: str

    def __init__(self, method_name: str) -> None:
        self.config = get_config()
        self.method_name = method_name
        super().__init__()

    @abstractmethod
    def get_json(self) -> dict:
        pass

    async def send(self) -> None:
        async with request(
                'POST',
            f'{URL_TELEGRAM_API}{self.config.bot_token}/{self.method_name}',
            json=self.get_json()
        ) as response:
            get_logger().debug(f'Sent request: {response.request_info}')
            if response.status == 403:
                get_logger().warn(f'Failed to send request: {await response.json(encoding="UTF-8")}')
            elif response.status != 200:
                get_logger().error(f'Failed to send request: {await response.json(encoding="UTF-8")}')
            response.close()
