import asyncio

from processors.processor import Processor
from helpers.helper_db import connect_submitter, disconnect
from helpers.helper_config import read_config
from aiohttp import request
from helpers.helper_config import get_config
from constants.request_methods import REQUEST_METHOD_GET_UPDATES
from constants.urls import URL_TELEGRAM_API
from processors.processor import Processor
from helpers.helper_logger import get_logger


# CONST
DEFAULT_STEP = 3
SLEEP_ON_ERROR = 5


class Listener():
    __step = DEFAULT_STEP
    __offset = 0

    def __init__(self, processor: Processor) -> None:
        config = get_config()
        self.processor = processor
        self.bot_token = config.bot_token

    async def listen(self):
        get_logger().info('Started listening to tg updates.')
        while True:
            await self.requestUpdates()
            await asyncio.sleep(self.__step)

    async def requestUpdates(self):
        try:
            async with request('GET', (f'{URL_TELEGRAM_API}{self.bot_token}'
                                    f'/{REQUEST_METHOD_GET_UPDATES}?offset={self.__offset + 1}'))\
                    as response:
                responseObject = await response.json(encoding='UTF-8')
                if (
                        'ok' in responseObject 
                        and responseObject['ok'] 
                        and 'result' in responseObject 
                        and (type(responseObject['result']) is list)
                    ):
                    offset = self.processor.process(
                        responseObject['result'], self.__offset)
                    self.__offset = offset
                    return
                
                get_logger().warn('Unexpected tg response', responseObject)
                if 'error_code' in responseObject and responseObject['error_code'] == 429:
                    await asyncio.sleep(SLEEP_ON_ERROR)
        
        except Exception as e:
            get_logger().exception(e)
            await asyncio.sleep(SLEEP_ON_ERROR)


async def start():
    read_config()
    get_logger().info('Started submitter')
    await connect_submitter()
    processor = Processor()
    updater = Listener(processor,)
    await updater.listen()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        asyncio.run(disconnect())
