import pytest
from model_bakery import baker


# address fixtures
from address.models import Country, City, Street


@pytest.fixture
def country_factory():
    """
    Country factory
    """
    def factory(*args, **kwargs):
        return baker.make(Country, *args, **kwargs)

    return factory


@pytest.fixture
def city_factory():
    """
    City factory
    """
    def factory(*args, **kwargs):
        return baker.make(City, *args, **kwargs)

    return factory


@pytest.fixture
def street_factory():
    """
    Street factory
    """
    def factory(*args, **kwargs):
        return baker.make(Street, *args, **kwargs)

    return factory
