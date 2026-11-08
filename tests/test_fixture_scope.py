import pytest


@pytest.fixture(scope="function")
def function_fixture() -> str:
    print("\nFUNCTION FIXTURE")
    return "function"


@pytest.fixture(scope="module")
def module_fixture() -> str:
    print("\nMODULE FIXTURE")
    return "module"


@pytest.mark.usefixtures("function_fixture", "module_fixture")
def test_first() -> None:
    print("FIRST TEST")


@pytest.mark.usefixtures("function_fixture", "module_fixture")
def test_second() -> None:
    print("SECOND TEST")


@pytest.mark.usefixtures("function_fixture", "module_fixture")
def test_third() -> None:
    print("THIRD TEST")
