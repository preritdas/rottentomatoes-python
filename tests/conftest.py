"""Fixtures."""
import pytest

from rottentomatoes.standalone import _request


@pytest.fixture(scope="session")
def happy_gilmore_content():
    return _request("happy gilmore")


@pytest.fixture(scope="session")
def top_gun_mav_content():
    return _request("top gun")


@pytest.fixture(scope="session")
def forrest_gump_content():
    return _request("forrest gump")
