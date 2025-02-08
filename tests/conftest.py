import pytest


@pytest.fixture(scope='function', autouse=True)
def add_in_report(record_property):
    record_property("example_key", 1)
    record_property("example_key1", 1)
    record_property("example_key2", 1)
