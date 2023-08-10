import pytest
from django.db import IntegrityError
from user.models import User
from address.models import Country, City, Street


@pytest.mark.django_db
def test_create_user(user_factory):
    """
    Create one User
    """
    user = user_factory()

    assert User.objects.filter(id=user.pk).exists()


@pytest.mark.django_db
def test_create_users(user_factory):
    """
    Create many Users
    """
    user_factory(_quantity=3)

    assert User.objects.count() == 3


@pytest.mark.django_db
def test_update_user(user_factory):
    """
    Update User
    """
    user = user_factory()

    user_db = User.objects.get(id=user.pk)
    user_db.username = 'update'
    user_db.email = 'update@update.com'
    user_db.phone_number = '987654321'
    user_db.type = 'legal entity'
    user_db.save()

    updated_user = User.objects.get(id=user.pk)
    assert updated_user.username == 'update'
    assert updated_user.email == 'update@update.com'
    assert updated_user.phone_number == '987654321'
    assert updated_user.type == 'legal entity'


@pytest.mark.django_db
def test_delete_user(user_factory):
    """
    Delete User
    """
    user = user_factory()
    User.objects.get(id=user.pk).delete()

    assert not User.objects.filter(id=user.pk).exists()


@pytest.mark.django_db
def test_user_username_unique_constraint(user_factory):
    """
    User username should be unique
    """
    user = user_factory()

    try:
        user_factory(username=user.username)
        assert False
    except IntegrityError:
        assert True


@pytest.mark.django_db
def test_user_email_unique_constraint(user_factory):
    """
    User email should be unique
    """
    user = user_factory()

    try:
        user_factory(email=user.email)
        assert False
    except IntegrityError:
        assert True


@pytest.mark.django_db
def test_user_phone_number_unique_constraint(user_factory):
    """
    User phone number should be unique
    """
    user = user_factory()

    try:
        user_factory(phone_number=user.phone_number)
        assert False
    except IntegrityError:
        assert True


@pytest.mark.django_db
def test_user_setnull_delete_country(user_factory, country_factory):
    """
    User should not automatically delete with its Country, country field should be set null
    """
    country = country_factory()
    user = user_factory(country=country)

    Country.objects.get(id=country.pk).delete()
    updated_user = User.objects.get(id=user.id)
    assert updated_user
    assert updated_user.country is None


@pytest.mark.django_db
def test_user_setnull_delete_city(user_factory, country_factory, city_factory):
    """
    User should not automatically delete with its City, city field should be set null
    """
    country = country_factory()
    city = city_factory(country=country)
    user = user_factory(country=country, city=city)

    City.objects.get(id=city.pk).delete()
    updated_user = User.objects.get(id=user.id)
    assert updated_user
    assert updated_user.city is None


@pytest.mark.django_db
def test_user_setnull_delete_street(user_factory, country_factory, city_factory, street_factory):
    """
    User should not automatically delete with its Street, street field should be set null
    """
    country = country_factory()
    city = city_factory(country=country)
    street = street_factory(city=city)
    user = user_factory(country=country, city=city, street=street)

    Street.objects.get(id=street.pk).delete()
    updated_user = User.objects.get(id=user.id)
    assert updated_user
    assert updated_user.street is None
