import asyncio
import time
import signal
from graceful_exit.customer_logger.custom_logging import get_logger

logger = get_logger("MockApp")


class MockApp:
    def __init__(
        self,
        exit_signal_type: signal.Signals = signal.SIGTERM,
        raise_after_iterations: int = 0,
        sleep_time: float = 0.01,
    ) -> None:
        self.iterations = 0
        self.raise_after_iterations = raise_after_iterations
        self.called_exit_handler = False
        self.exit_signal_type = exit_signal_type
        self.sleep_time = sleep_time
        self.exit_sleep_time = 1

    def raise_signal_after_number_iterations(self, iterations: int) -> None:
        if iterations >= self.raise_after_iterations:
            logger.debug("Raising exit signal")
            signal.raise_signal(self.exit_signal_type)

    def exit_handler_sync(self, *args, **kwargs):
        logger.debug("processing exit handler sync", status="STARTED")
        time.sleep(self.exit_sleep_time)
        self.called_exit_handler = True
        logger.debug("processing exit handler sync", status="DONE")

    def run_sync(self):
        while True:
            logger.debug("Running app", iterations=self.iterations)
            time.sleep(self.sleep_time)
            self.iterations += 1
            self.raise_signal_after_number_iterations(self.iterations)

    async def exit_handler(self, *args, **kwargs):
        logger.debug("processing exit handler async", status="STARTED")
        await asyncio.sleep(self.exit_sleep_time)
        self.called_exit_handler = True
        logger.debug("processing exit handler async", status="DONE")

    async def run(self):
        while True:
            logger.debug("Running app", iterations=self.iterations)
            await asyncio.sleep(self.sleep_time)
            self.iterations += 1
            self.raise_signal_after_number_iterations(self.iterations)
