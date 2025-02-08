import pytest


@pytest.fixture(scope='function', autouse=True)
def test_function(record_xml_attribute):
    record_xml_attribute("assertions", "REQ-1234")
    record_xml_attribute("classname", "custom_classname")
    record_xml_attribute("name", "custom_name")
    record_xml_attribute("func", "custom_func")
    print("hello world")
    assert True