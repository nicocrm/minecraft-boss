from os import path

import repository


def test_list_servers():
    repo = repository.Repository(path.dirname(__file__))
    result = list(repo.list_servers())
    assert len(result) == 1
    assert result[0].name == "s1"
    assert result[0].description == "A server powered by Casa!"
