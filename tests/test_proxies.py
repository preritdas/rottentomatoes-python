"""Test that all proxies used are working."""
from rottentomatoes.proxies import PROXIES, get_working_proxies_threaded


def test_all_proxies_working():
    assert all(proxy in PROXIES for proxy in get_working_proxies_threaded(PROXIES))
