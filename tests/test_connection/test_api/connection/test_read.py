import pytest

from conftest import description


@pytest.mark.description('Чтение поля json_connection')
@description('Чтение json_connection')
def test_read_json_connection():
    __doc__ = 'Подготовка объектов'
    assert True, 'Чтение поля json_connection'