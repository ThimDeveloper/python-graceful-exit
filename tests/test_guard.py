import signal
import pytest
from graceful_exit.module import GracefulExit
from tests.mocks.app import MockApp


async def main():
    app = MockApp()
    async with GracefulExit[MockApp](
        app=app, exit_handler=app.exit_handler
    ) as wrapped_app:
        await wrapped_app.run()


def test_create_main_app() -> None:
    app = MockApp()
    assert app is not None


class TestSynchronousContextManager:
    def test_sig_int_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGINT, raise_after_iterations=5)
        assert app.called_exit_handler == False
        try:
            with GracefulExit[MockApp](
                app=app, exit_handler=app.exit_handler_sync
            ) as wrapped_app:
                wrapped_app.run_sync()
        finally:
            assert app.called_exit_handler == True

    def test_sig_term_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        assert app.called_exit_handler == False
        try:
            with GracefulExit[MockApp](
                app=app, exit_handler=app.exit_handler_sync
            ) as wrapped_app:
                wrapped_app.run_sync()
        finally:
            assert app.called_exit_handler == True


@pytest.mark.asyncio
class TestAsynchronousContextManager:
    async def test_sig_int_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGINT, raise_after_iterations=5)
        assert app.called_exit_handler == False
        try:
            async with GracefulExit[MockApp](
                app=app, exit_handler=app.exit_handler
            ) as wrapped_app:
                await wrapped_app.run()
        finally:
            assert app.called_exit_handler == True

    async def test_sig_term_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        assert app.called_exit_handler == False
        try:
            async with GracefulExit[MockApp](
                app=app, exit_handler=app.exit_handler
            ) as wrapped_app:
                await wrapped_app.run()
        finally:
            assert app.called_exit_handler == True
