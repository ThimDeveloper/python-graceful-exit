import pytest
from graceful_exit.helpers import wrap_in_system_exit


def test_wraps_function_call_in_system_exit() -> None:
    def test_fn(x):
        return x

    with pytest.raises(SystemExit):
        wrap_in_system_exit(test_fn(42))


def test_wraps_coroutine_call_in_system_exit() -> None:
    async def test_fn(x):
        return x

    with pytest.raises(SystemExit):
        wrap_in_system_exit(test_fn(42))
