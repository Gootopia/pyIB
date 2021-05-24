# clientportal_websockets.py

from overrides import overrides
from ib.watchdog import Watchdog
import asyncio
import websockets
from lib.certificate import Certificate, CertificateError
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from enum import Enum


class ClientPortalWebsocketsError(Enum):
    Ok = 0
    Unknown = 1
    Invalid_Certificate = 2


    # TODO: Document ClientPortalWebsockets class
class ClientPortalWebsockets(Watchdog):
    """
    Interactive Brokers ClientPortal Interface (Websocket).
    Refer to https://interactivebrokers.github.io/cpwebapi/RealtimeSubscription.html for API documentation
    NOTE: Websocket usage also requires the UI to send the /tickle endpoint. See Websocket Ping Session docs.
    """
    def __init__(self):
        super().__init__(autostart=True, timeout_sec=5, name='WebSocket')
        self.url_websockets = 'wss://localhost:5000/v1/api/ws'
        # Base used by all endpoints
        logger.log('DEBUG', f'Clientportal (Websockets) Started with endpoint: {self.url_websockets}')

    @overrides
    def watchdog_task(self):
        super().watchdog_task()
        # TODO: Add periodic call to websocket 'tic'

    async def establish_connection(self):
        """ Create the websocket establish_connection """
        result = Certificate.get_certificate()

        if result.error != CertificateError.Ok:
            logger.log('DEBUG', f'Problems obtaining certificate: {result.error}')
            return ClientPortalWebsocketsError.Invalid_Certificate

        logger.log('DEBUG', f'Attempting connection to "{self.url_websockets}"')

        try:
            async with websockets.connect(self.url_websockets, ssl=result.ssl_context) as ws:
                logger.log('DEBUG', f'Connected to "{self.url_websockets}')
                await ws.send('smd+265598+{"fields":["31","83"]}')
                while True:
                    response = await ws.recv()
                    print(f'{response}')
        except websockets.InvalidURI:
            pass
        except websockets.InvalidHandshake:
            pass
        except Exception as e:
            pass
        finally:
            logger.log('DEBUG', f'Connection "{self.url_websockets}" broken')

    def loop(self):
        with ThreadPoolExecutor(max_workers=1) as executor:
            logger.log('DEBUG', f'Starting websockets thread')
            future = executor.submit(asyncio.get_event_loop().run_until_complete(self.establish_connection()))
            logger.log('DEBUG', f'Completed websockets thread')


if __name__ == '__main__':
    print("=== IB Client Portal Websockets ===")
