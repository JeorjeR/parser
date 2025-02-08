import pytest

def snake_to_pascal(snake_str):
    # Разделяем строку по символу подчеркивания
    components = snake_str.split('_')
    # Преобразуем каждую часть в PascalCase (первая буква заглавная)
    pascal_str = ''.join(component.capitalize() for component in components)
    return pascal_str

@pytest.fixture(scope='function', autouse=True)
def test_function(record_xml_attribute, request):
    parent = request.path.parts[-2: -1][0]
    parent_str = snake_to_pascal(parent)

    func = request.path.stem
    func_str = snake_to_pascal(func)

    record_xml_attribute("classname", parent_str)
    print("hello world")
    assert True