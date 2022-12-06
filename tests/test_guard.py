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
        with GracefulExit[MockApp](
            app=app, exit_handler=app.exit_handler_sync
        ) as wrapped_app:
            wrapped_app.run_sync()

        assert app.called_exit_handler == True

    def test_sig_term_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        assert app.called_exit_handler == False
        with GracefulExit[MockApp](
            app=app, exit_handler=app.exit_handler_sync
        ) as wrapped_app:
            wrapped_app.run_sync()

        assert app.called_exit_handler == True

    def test_without_exit_handler(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        with GracefulExit[MockApp](app=app) as wrapped_app:
            wrapped_app.run_sync()
        assert app.called_exit_handler == False

    @pytest.mark.xfail
    def test_without_app(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        with GracefulExit[MockApp]() as wrapped_app:
            wrapped_app.run_sync()
        assert app.called_exit_handler == False


@pytest.mark.asyncio
class TestAsynchronousContextManager:
    async def test_sig_int_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGINT, raise_after_iterations=5)
        assert app.called_exit_handler == False
        async with GracefulExit[MockApp](
            app=app, exit_handler=app.exit_handler
        ) as wrapped_app:
            await wrapped_app.run()

        assert app.called_exit_handler == True

    async def test_sig_term_handling(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        assert app.called_exit_handler == False
        async with GracefulExit[MockApp](
            app=app, exit_handler=app.exit_handler
        ) as wrapped_app:
            await wrapped_app.run()

        assert app.called_exit_handler == True

    async def test_without_exit_handler(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        async with GracefulExit[MockApp](app=app) as wrapped_app:
            await wrapped_app.run()
        assert app.called_exit_handler == False

    @pytest.mark.xfail
    async def test_without_app(self) -> None:
        app = MockApp(exit_signal_type=signal.SIGTERM, raise_after_iterations=5)
        async with GracefulExit[MockApp]() as wrapped_app:
            await wrapped_app.run()
        assert app.called_exit_handler == False
