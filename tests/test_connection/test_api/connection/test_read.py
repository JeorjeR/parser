import pytest


@pytest.mark.metadata(
    author="John Doe",
    description="This test checks if the login feature works correctly",
    environment="Staging",
)
def test_read_json_connection():
    assert False, 'Чтение поля json_connection'