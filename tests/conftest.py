import dataclasses
import enum

import pytest


class TestTypes(enum.StrEnum):
    API = 'api'
    INTEGRATION = 'integration'
    UNIT = 'unit'

@dataclasses.dataclass
class TestDescription:
    class_name: str
    name: str


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

    tests_root_path_idx = request.path.parts.index('tests')
    test_type = request.path.parts[tests_root_path_idx + 2].split('_')[1]
    test_functional_name = snake_to_pascal(request.path.parts[tests_root_path_idx + 1].split('_')[1])
    test_type = TestTypes(test_type)

    if test_type == TestTypes.API:
        test_description = description_api_tests(request)
    elif test_type == TestTypes.UNIT:
        test_description =  description_unit_test(request)
    else:
        test_description = description_integration_tests(request)

    record_xml_attribute("classname", f'{test_type}.{test_functional_name}')

    if test_description:
        if test_description.name:
            record_xml_attribute("name", test_description.class_name)


def description_api_tests(request) -> TestDescription:
    parent = request.path.parts[-2: -1][0]
    parent_str = snake_to_pascal(parent)
    name = request.node.function.__doc__.splitlines()[0].strip()

    return TestDescription(
        class_name=parent_str,
        name=name,
    )


def description_integration_tests(request) -> TestDescription | None:
    ...


def description_unit_test(request) -> TestDescription | None:
    ...