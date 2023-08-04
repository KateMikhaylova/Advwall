import pytest
from django.db import IntegrityError, DataError

from address.models import Country, City, Street


@pytest.mark.django_db
def test_create_country(country_factory):
    """
    Create one Country
    """
    country = country_factory()

    assert Country.objects.filter(id=country.pk).exists()


@pytest.mark.django_db
def test_create_countries(country_factory):
    """
    Create many Countries
    """
    country_factory(_quantity=5)

    assert Country.objects.count() == 5


@pytest.mark.django_db
def test_update_country(country_factory):
    """
    Update Country
    """
    country = country_factory()
    country_db = Country.objects.get(id=country.pk)
    country_db.name = 'test'
    country_db.save()

    assert Country.objects.get(id=country.pk).name == 'test'


@pytest.mark.django_db
def test_delete_country(country_factory):
    """
    Delete Country
    """
    country = country_factory()
    Country.objects.get(id=country.pk).delete()

    assert not Country.objects.filter(id=country.pk).exists()


@pytest.mark.django_db
def test_country_name_unique_constraint(country_factory):
    """
    Country name should be unique
    """
    country = country_factory()

    try:
        country_factory(name=country.name)
        assert False
    except IntegrityError:
        assert True


@pytest.mark.django_db
def test_country_max_length_constraint(country_factory):
    """
    Country name max length should be 100
    """
    country_factory(name='l'*100)
    try:
        country_factory(name='l'*101)
        assert False
    except DataError:
        assert True


@pytest.mark.django_db
def test_create_city(city_factory):
    """
    Create one City
    """
    city = city_factory()

    assert City.objects.filter(id=city.pk).exists()


@pytest.mark.django_db
def test_create_cities(city_factory):
    """
    Create many Cities
    """
    city_factory(_quantity=5)

    assert City.objects.count() == 5


@pytest.mark.django_db
def test_update_city(city_factory):
    """
    Update City
    """
    city = city_factory()
    city_db = City.objects.get(id=city.pk)
    city_db.name = 'test'
    city_db.save()

    assert City.objects.get(id=city.pk).name == 'test'


@pytest.mark.django_db
def test_delete_city(city_factory):
    """
    Delete City
    """
    city = city_factory()
    City.objects.get(id=city.pk).delete()

    assert not City.objects.filter(id=city.pk).exists()


@pytest.mark.django_db
def test_delete_city_with_country(city_factory):
    """
    City should automatically delete with its Country
    """
    city = city_factory()
    Country.objects.get(id=city.country.pk).delete()

    assert not City.objects.all().exists()


@pytest.mark.django_db
def test_city_max_length_constraint(city_factory):
    """
    City name max length should be 100
    """
    city_factory(name='l'*100)
    try:
        city_factory(name='l'*101)
        assert False
    except DataError:
        assert True


@pytest.mark.django_db
def test_create_street(street_factory):
    """
    Create one Street
    """
    street = street_factory()

    assert Street.objects.filter(id=street.pk).exists()


@pytest.mark.django_db
def test_create_streets(street_factory):
    """
    Create many Streets
    """
    street_factory(_quantity=5)

    assert Street.objects.count() == 5


@pytest.mark.django_db
def test_update_street(street_factory):
    """
    Update Street
    """
    street = street_factory()
    street_db = Street.objects.get(id=street.pk)
    street_db.name = 'test'
    street_db.save()

    assert Street.objects.get(id=street.pk).name == 'test'


@pytest.mark.django_db
def test_delete_street(street_factory):
    """
    Delete Street
    """
    street = street_factory()
    Street.objects.get(id=street.pk).delete()

    assert not Street.objects.filter(id=street.pk).exists()


@pytest.mark.django_db
def test_delete_street_with_city(street_factory):
    """
    Street should automatically delete with its City
    """
    street = street_factory()
    City.objects.get(id=street.city.pk).delete()

    assert not Street.objects.all().exists()


@pytest.mark.django_db
def test_delete_street_with_country(street_factory):
    """
    Street should automatically delete with its Country
    """
    street = street_factory()
    Country.objects.get(id=street.city.country.pk).delete()

    assert not Street.objects.all().exists()


@pytest.mark.django_db
def test_street_max_length_constraint(street_factory):
    """
    Street name max length should be 100
    """
    street_factory(name='l'*100)
    try:
        street_factory(name='l'*101)
        assert False
    except DataError:
        assert True
