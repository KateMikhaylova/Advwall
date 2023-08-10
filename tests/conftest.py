import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
# address fixtures
from address.models import Country, City, Street
from user.models import User



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


@pytest.fixture
def user_factory():
    """
    User factory
    """
    def factory(*args, **kwargs):
        return baker.make(User, *args, **kwargs)

    return factory


@pytest.fixture
def token_factory():
    """
    Token factory
    """
    def factory(*args, **kwargs):
        return baker.make(Token, *args, **kwargs)

    return factory


@pytest.fixture
def client():
    """
    Returns api client to perform requests
    :return:
    """
    return APIClient()
