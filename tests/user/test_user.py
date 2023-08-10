import pytest

from user.models import User


@pytest.mark.django_db
def test_create_user_api(client):
    """
    Create user with API post request
    """
    count = User.objects.count()
    data = {
        "username": "test",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "test@test.ru",
        "phone_number": "987654321"
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    assert User.objects.count() == count + 1
    reply = response.json()
    assert reply["username"] == data["username"]


@pytest.mark.django_db
def test_create_user_exists(client, user_factory):
    """
    Create already existing user
    """
    user = user_factory()
    data = {
        "username": user.username,
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": user.email,
        "phone_number": user.phone_number
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply['username'] == ['user with this username already exists.']
    assert reply['email'] == ['A user with that email already exists.']
    assert reply['phone_number'] == ['A user with that phone number already exists.']


@pytest.mark.django_db
def test_create_user_less_info(client):
    """
    Create user with not all required information
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321"
    }
    data_copy = data.copy()
    for field in data:
        data_copy.pop(field)
        response = client.post("/api/v1/users/", data=data_copy, format="json")
        assert response.status_code == 400
        assert response.json() == {field: ['This field is required.']}
        data_copy = data.copy()


@pytest.mark.django_db
def test_create_user_null_info(client):
    """
    Create user with null required information
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321"
    }
    data_copy = data.copy()
    for field in ["username", "email", "phone_number"]:
        data_copy[field] = None
        response = client.post("/api/v1/users/", data=data_copy, format="json")
        assert response.status_code == 400
        assert response.json() == {field: ['This field may not be null.']}
        data_copy = data.copy()


@pytest.mark.django_db
def test_create_user_blank_info(client):
    """
    Create user with blank required information
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321"
    }
    data_copy = data.copy()
    for field in ["username", "email", "phone_number"]:
        data_copy[field] = ""
        response = client.post("/api/v1/users/", data=data_copy, format="json")
        assert response.status_code == 400
        assert response.json() == {field: ['This field may not be blank.']}
        data_copy = data.copy()


@pytest.mark.parametrize(
    ["post_type", "result_type"],
    (("private entity", "private entity"), ("legal entity", "legal entity")),
)
@pytest.mark.django_db
def test_create_user_type(client, post_type, result_type):
    """
    Creates users with different types
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "type": post_type
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply["type"] == result_type


@pytest.mark.django_db
def test_create_user_invalid_type(client):
    """
    Creation of user with invalid type
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "type": "invalid"
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {"type": ['"invalid" is not a valid choice.']}


@pytest.mark.django_db
def test_create_user_no_type(client):
    """
    Creation of user with default type
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply["type"] == "private entity"


@pytest.mark.django_db
def test_create_user_email_validation(client):
    """
    Creation of user with invalid email
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email",
        "phone_number": "987654321",
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {"email": ["Enter a valid email address."]}


@pytest.mark.parametrize(
    ["password", "expected_reply"],
    (("93825647895217321596227862362245821005",
      {"password": ["This password is entirely numeric."]}),
     ("strpas1",
      {"password": ["This password is too short. It must contain at least 8 characters."]}),
     ("password",
      {"password": ["This password is too common."]})),
)
@pytest.mark.django_db
def test_create_user_password_validation(client, password, expected_reply):
    """
    Creation of user with invalid password
    """
    data = {
        "username": "username",
        "password": password,
        "repeat_password": password,
        "email": "email@email.ru",
        "phone_number": "987654321",
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == expected_reply


@pytest.mark.django_db
def test_create_user_password_repeat_differs(client):
    """
    Creation of user with different repeat_password
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "VeryStrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {"password": ["Passwort fields does not correspond."]}


@pytest.mark.django_db
def test_create_user_no_country(client):
    """
    Creation of user with no country
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] is None


@pytest.mark.django_db
def test_create_user_with_country(client, country_factory):
    """
    Creation of user with country
    """
    country = country_factory()
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": country.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country.id


@pytest.mark.django_db
def test_create_user_country_dont_exist(client):
    """
    Creation of user with absent country
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": 1
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {'country': ['Invalid pk "1" - object does not exist.']}


@pytest.mark.django_db
def test_create_user_city_with_country(client, country_factory, city_factory):
    """
    Creation of user with city and country
    """
    country = country_factory()
    city = city_factory(country=country)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": country.id,
        "city": city.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country.id
    assert reply['city'] == city.id


@pytest.mark.django_db
def test_create_user_city_without_country(client, country_factory, city_factory):
    """
    Creation of user with city and without country
    """
    country = country_factory()
    city = city_factory(country=country)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "city": city.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country.id
    assert reply['city'] == city.id


@pytest.mark.django_db
def test_create_user_with_country_city_not_correspond(client, country_factory, city_factory):
    """
    Creation of user with city and improper country
    """
    country1 = country_factory()
    country2 = country_factory()
    city = city_factory(country=country1)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": country2.id,
        "city": city.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country1.id


@pytest.mark.django_db
def test_create_user_city_not_exist(client,):
    """
    Creation of user with absent city
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "city": 99
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {'city': ['Invalid pk "99" - object does not exist.']}


@pytest.mark.django_db
def test_create_user_street_with_city_country(client,
                                              country_factory,
                                              city_factory,
                                              street_factory):
    """
    Creation of user with street, city and country
    """
    country = country_factory()
    city = city_factory(country=country)
    street = street_factory(city=city)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": country.id,
        "city": city.id,
        "street": street.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country.id
    assert reply['city'] == city.id
    assert reply['street'] == street.id


@pytest.mark.django_db
def test_create_user_street_without_city_country(client,
                                                 country_factory,
                                                 city_factory,
                                                 street_factory):
    """
    Creation of user with city and without city and country
    """
    country = country_factory()
    city = city_factory(country=country)
    street = street_factory(city=city)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "street": street.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country.id
    assert reply['city'] == city.id
    assert reply['street'] == street.id


@pytest.mark.django_db
def test_create_user_street_country_city_not_correspond(client,
                                                        country_factory,
                                                        city_factory,
                                                        street_factory):
    """
    Creation of user with street, improper city and improper country
    """
    country1 = country_factory()
    country2 = country_factory()
    country3 = country_factory()
    city1 = city_factory(country=country1)
    city2 = city_factory(country=country2)
    street = street_factory(city=city1)
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "country": country3.id,
        "city": city2.id,
        "street": street.id
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 201
    reply = response.json()
    assert reply['country'] == country1.id
    assert reply['city'] == city1.id


@pytest.mark.django_db
def test_create_user_street_not_exist(client,):
    """
    Creation of user with absent street
    """
    data = {
        "username": "username",
        "password": "StrongPassword1!",
        "repeat_password": "StrongPassword1!",
        "email": "email@email.ru",
        "phone_number": "987654321",
        "street": 99
    }
    response = client.post("/api/v1/users/", data=data, format="json")
    assert response.status_code == 400
    reply = response.json()
    assert reply == {'street': ['Invalid pk "99" - object does not exist.']}


@pytest.mark.django_db
def test_list_users_no_token(client):
    """
    Get user list info without token
    """
    response = client.get("/api/v1/users/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_list_users_wrong_token(client, user_factory, token_factory):
    """
    Get user list info with wrong token
    """
    user = user_factory(is_staff=True)
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token wrong{token.key}")
    response = client.get("/api/v1/users/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Invalid token."}


@pytest.mark.django_db
def test_list_users_admin(client, user_factory, token_factory):
    """
    Get user list info with admin token
    """
    admin = user_factory(is_staff=True)
    token = token_factory(user=admin)
    users = user_factory(_quantity=5)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(users) + 1 == len(data)


@pytest.mark.django_db
def test_list_users_user(client, user_factory, token_factory):
    """
    Get user list info with user token
    """
    user = user_factory(is_staff=False)
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get("/api/v1/users/")
    assert response.status_code == 403
    data = response.json()
    assert data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_retrieve_users_no_token(client, user_factory):
    """
    Get particular user info without token
    """
    user = user_factory()
    response = client.get(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_retrieve_users_wrong_token(client, user_factory, token_factory):
    """
    Get particular user info with wrong token
    """
    user = user_factory(is_staff=True)
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token wrong{token.key}/")
    response = client.get(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Invalid token."}


@pytest.mark.django_db
def test_retrieve_users_user_token(client, user_factory, token_factory):
    """
    Get particular user info with user token
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get(f"/api/v1/users/{user.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id


@pytest.mark.django_db
def test_retrieve_users_user_not_exist(client, user_factory, token_factory):
    """
    Get particular absent user info
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.get("/api/v1/users/999/")
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Not found.'}


@pytest.mark.django_db
def test_destroy_users_no_token(client, user_factory):
    """
    Delete particular user without token
    """
    user = user_factory()
    response = client.delete(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_destroy_users_wrong_token(client, user_factory, token_factory):
    """
    Delete particular user with wrong token
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token wrong{token.key}/")
    response = client.delete(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Invalid token."}


@pytest.mark.django_db
def test_destroy_users_user_token(client, user_factory, token_factory):
    """
    Delete particular user with users token
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.delete(f"/api/v1/users/{user.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_destroy_users_other_user_token(client, user_factory, token_factory):
    """
    Delete particular user with other users token
    """
    user = user_factory()
    token = token_factory(user=user)
    user2 = user_factory()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.delete(f"/api/v1/users/{user2.id}/")
    assert response.status_code == 403
    data = response.json()
    assert data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_destroy_users_user_not_exist(client, user_factory, token_factory):
    """
    Delete absent particular user
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.delete("/api/v1/users/999/")
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Not found.'}


@pytest.mark.django_db
def test_put_not_allowed(client, user_factory):
    """
    Tests not allowed PUT method
    """
    user = user_factory()
    response = client.put(f"/api/v1/users/{user.id}/", data={}, format="json")
    assert response.status_code == 405
    data = response.json()
    assert data == {'detail': 'Method "PUT" not allowed.'}


@pytest.mark.django_db
def test_update_users_no_token(client, user_factory):
    """
    Update particular user info without token
    """
    user = user_factory()
    response = client.patch(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_update_users_wrong_token(client, user_factory, token_factory):
    """
    Update particular user info with wrong token
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token wrong{token.key}/")
    response = client.patch(f"/api/v1/users/{user.id}/")
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Invalid token."}


@pytest.mark.django_db
def test_update_users_other_user_token(client, user_factory, token_factory):
    """
    Update particular user info with other users token
    """
    user = user_factory()
    token = token_factory(user=user)
    user2 = user_factory()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch(f"/api/v1/users/{user2.id}/")
    assert response.status_code == 403
    data = response.json()
    assert data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_update_users_user_token(client, user_factory, token_factory):
    """
    Update particular user info with users token
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"username": "username"},
                            format="json")
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == "username"


@pytest.mark.django_db
def test_update_users_user_not_exist(client, user_factory, token_factory):
    """
    Update absent particular user info
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch("/api/v1/users/999/",
                            data={"username": "username"},
                            format="json")
    assert response.status_code == 404
    data = response.json()
    assert data == {'detail': 'Not found.'}


@pytest.mark.django_db
def test_update_users_unique_fields(client, user_factory, token_factory):
    """
    Update particular user unique fields to already existing values
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    user2 = user_factory()

    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"username": user2.username},
                            format="json")
    assert response.status_code == 400
    data = response.json()
    assert data == {'username': ['user with this username already exists.']}

    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"email": user2.email},
                            format="json")
    assert response.status_code == 400
    data = response.json()
    assert data == {'email': ['A user with that email already exists.']}

    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"phone_number": user2.phone_number},
                            format="json")
    assert response.status_code == 400
    data = response.json()
    assert data == {'phone_number': ['A user with that phone number already exists.']}


@pytest.mark.django_db
def test_update_users_email_validation(client, user_factory, token_factory):
    """
    Update particular user with invalid email
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"email": "email"},
                            format="json")
    assert response.status_code == 400
    data = response.json()
    assert data == {'email': ['Enter a valid email address.']}


@pytest.mark.django_db
def test_update_users_null_fields(client, user_factory, token_factory):
    """
    Update particular user info with null fields
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    for field in ['username', 'email', 'phone_number']:
        response = client.patch(f"/api/v1/users/{user.id}/", data={field: None}, format="json")
        assert response.status_code == 400
        data = response.json()
        assert data == {field: ['This field may not be null.']}


@pytest.mark.django_db
def test_update_users_blank_fields(client, user_factory, token_factory):
    """
    Update particular user info with blank fields
    """
    user = user_factory()
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    for field in ['username', 'email', 'phone_number']:
        response = client.patch(f"/api/v1/users/{user.id}/", data={field: ""}, format="json")
        assert response.status_code == 400
        data = response.json()
        assert data == {field: ['This field may not be blank.']}


@pytest.mark.django_db
def test_update_users_type(client, user_factory, token_factory):
    """
    Update particular user type
    """
    user = user_factory(type='private entity')
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch(f"/api/v1/users/{user.id}/",
                            data={"type": "legal entity"},
                            format="json")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == 'legal entity'


@pytest.mark.django_db
def test_update_users_type_invalid(client, user_factory, token_factory):
    """
    Update particular user type to invalid value
    """
    user = user_factory(type='private entity')
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = client.patch(f"/api/v1/users/{user.id}/", data={"type": "invalid"}, format="json")
    assert response.status_code == 400
    data = response.json()
    assert data == {'type': ['"invalid" is not a valid choice.']}


@pytest.mark.django_db
def test_update_users_password_patch(client, token_factory):
    """
    Update particular user password
    """
    data = {
                "username": "test",
                "password": "StrongPassword1!",
                "repeat_password": "StrongPassword1!",
                "email": "test@test.ru",
                "phone_number": "987654321"
            }
    response = client.post("/api/v1/users/", data=data, format="json")
    reply = response.json()
    user = User.objects.get(id=reply['id'])
    old_hash = user.password
    token = token_factory(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    new_password = "VeryStrongPassword1!"
    patch_data = {"current_password": data['password'],
                  "password": new_password,
                  "repeat_password": new_password}
    response = client.patch(f"/api/v1/users/{reply['id']}/", data=patch_data, format="json")
    assert response.status_code == 200
    user = User.objects.get(id=reply['id'])
    new_hash = user.password
    assert old_hash != new_hash
