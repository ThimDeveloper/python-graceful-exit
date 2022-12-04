import asyncio
import time
from graceful_exit.module import GracefulExit
from graceful_exit.helpers import wrap_in_system_exit
from graceful_exit.logging.custom_logging import get_logger

logger = get_logger("Docker")


class App:
    def exit_handler_sync(self, *args, **kwargs):
        logger.debug("processing exit handler sync", status="STARTED")
        time.sleep(5)
        logger.debug("processing exit handler sync", status="DONE")

    def run_sync(self):
        while True:
            logger.debug("Running app")
            time.sleep(2)

    async def exit_handler(self, *args, **kwargs):
        logger.debug("processing exit handler async", status="STARTED")
        await asyncio.sleep(5)
        logger.debug("processing exit handler async", status="DONE")

    async def run(self):
        while True:
            logger.debug("Running app")
            await asyncio.sleep(2)


async def main():
    app = App()
    async with GracefulExit[App](app=app, exit_handler=app.exit_handler) as app:
        await app.run()


if __name__ == "__main__":
    wrap_in_system_exit(asyncio.run(main()))
