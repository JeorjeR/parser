import pytest

@pytest.fixture(scope='function', autouse=True)
def description(request):
    try:
        mark = request.node.get_closest_marker("description").args[0]
    except:
        return
    if mark:
        request.node.function.__doc__ = f'{mark}\n{__doc__ or ""}'

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
    name = request.node.function.__doc__.splitlines()[0].strip()

    func = request.path.stem
    func_str = snake_to_pascal(func)

    #record_xml_attribute("classname", parent_str)
    #record_xml_attribute("name", name)