import pytest


@pytest.mark.description('Чтение поля json_connection')
@pytest.mark.usefixtures('description')
def test_read_json_connection():
    __doc__ = 'Подготовка объектов'
    assert True, 'Чтение поля json_connection'