import asyncio
from os import path

import pytest
from ..repository import Repository


def test_list_servers():
    repo = Repository(path.dirname(__file__))

    async def consume_generator(gen):
        return [server async for server in gen]

    result = list(asyncio.run(consume_generator(repo.list_servers())))
    assert len(result) == 3
    assert set([f.name for f in result]) == set(["s1", "another_server", "third_server"])
    s1 = [f for f in result if f.name == "s1"][0]
    assert s1.name == "s1"
    assert s1.description == "A server powered by Casa!"
    assert s1.mods == ["mod1"]
    assert not s1.is_running


def test_start_server_ok():
    repo = Repository(path.dirname(__file__))
    result = asyncio.run(repo.start_server("s1"))
    assert result.name == "s1"


def test_start_server_ko():
    repo = Repository(path.dirname(__file__))
    with pytest.raises(Exception):
        asyncio.run(repo.start_server("fail"))
