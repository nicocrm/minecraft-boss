import asyncio
from os import path

import pytest
from repository import Repository


def test_list_servers():
    repo = Repository(path.dirname(__file__))

    async def consume_generator(gen):
        return [server async for server in gen]

    result = list(asyncio.run(consume_generator(repo.list_servers())))
    assert len(result) == 1
    assert result[0].name == "s1"
    assert result[0].description == "A server powered by Casa!"
    assert result[0].mods == ["mod1"]
    assert not result[0].is_running


def test_start_server_ok():
    repo = Repository(path.dirname(__file__))
    result = asyncio.run(repo.start_server("s1"))
    assert result.name == "s1"


def test_start_server_ko():
    repo = Repository(path.dirname(__file__))
    with pytest.raises(Exception):
        asyncio.run(repo.start_server("fail"))
