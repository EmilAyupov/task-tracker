import pytest


@pytest.fixture(scope="function")
def function_fixture():
    print("\nFUNCTION FIXTURE")
    return "function"


@pytest.fixture(scope="module")
def module_fixture():
    print("\nMODULE FIXTURE")
    return "module"


def test_first(function_fixture, module_fixture):
    print("FIRST TEST")


def test_second(function_fixture, module_fixture):
    print("SECOND TEST")


def test_third(function_fixture, module_fixture):
    print("THIRD TEST")
