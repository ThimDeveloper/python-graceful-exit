import asyncio
import inspect
import signal
import time
from typing import Callable, Coroutine, Union


class TerminationGuard(object):
    def __init__(
        self,
        main_coroutine: Union[Callable, Coroutine],
        exit_handler: Union[Callable, Coroutine],
        loop: asyncio.AbstractEventLoop
    ):
        self._main = main_coroutine
        self._exit_handler = exit_handler
        self._loop = loop

    def __enter__(self):
        return self._main

    def __exit__(self, type, value, traceback):
        print("Handling exception")
        self._loop.run_until_complete(self._exit_handler())
        self._loop.close()
        print("Exception has been handled")
        print(type)
        print(value)
        print(traceback)
        return True


class MainApp:
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("Received:", signum)
        self.shutdown = True

    async def exit_handler(*args, **kwargs):
        print("processing exit handler coroutine")
        await asyncio.sleep(2)
        print("DONE: processing exit handler coroutine")

    async def run(self):
        while not self.shutdown:
            print("Running app")
            await asyncio.sleep(5)
        else:
            await self.exit_handler()






def main():
    app = MainApp()
    app.start()
    # This boolean flag should flip to false when a SIGINT or SIGTERM comes in...
    while not app.shutdown:
        app.run()
    else:
        print("gracefully shutting down")


if __name__ == "__main__":
    main()
