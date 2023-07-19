import asyncio

import pytest

from .fixtures import *  # noqa: F403, F401


@pytest.fixture(scope="session")
def event_loop():
    """This overwrites pytest-asyncio's default event_loop fixture.

    pytest-asyncio provides a event_loop fixture it uses in the background.
    The default fixture has a function scope which causes problems in some
    cases.
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
