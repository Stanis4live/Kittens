import os
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from exhibition.models import Breed, Kitten


@pytest.fixture(scope='session', autouse=True)
def set_env():
    os.environ['SKIP_MIGRATION_DATA'] = 'True'

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    return User.objects.create_user(username='Bob', email='owner@example.com', password='testpassword')

@pytest.fixture
def authenticate_user(api_client, create_user):
    response = api_client.post(reverse('token_obtain_pair'), {
        'username':'Bob',
        'password':'testpassword'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

@pytest.fixture
def create_breed():
    return Breed.objects.create(name='Scottish')

@pytest.fixture
def create_kitten(create_user, create_breed):
    return Kitten.objects.create(
        owner=create_user,
        breed=create_breed,
        color='grey',
        age_months=3,
        description='little kitten'
    )

@pytest.mark.django_db
def test_get_kittens_list(api_client, authenticate_user):
    url = reverse('kittens-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_kitten(api_client, authenticate_user, create_breed):
    url = reverse('manage-kittens-list')
    data = {
        'breed': create_breed.id,
        'color': 'grey',
        'age_months': 3,
        'description': 'little kitten'
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_get_kitten(api_client, authenticate_user, create_kitten):
    url = reverse('kittens-detail', kwargs={'pk': create_kitten.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_kitten(api_client, authenticate_user, create_kitten):
    url = reverse('manage-kittens-detail', kwargs={'pk': create_kitten.id})
    data = {
        'color': 'black',
        'age_months': 144,
        'description': 'big kitten'
    }
    response = api_client.patch(url, data=data)
    assert response.status_code == status.HTTP_200_OK
    create_kitten.refresh_from_db()
    assert create_kitten.color == 'black'

@pytest.mark.django_db
def test_update_other_kitten_fail(api_client, authenticate_user, create_breed):
    another_user = User.objects.create_user(
        username='another_user',
        email='another_user@example.com',
        password='password1'
    )
    another_kitten = Kitten.objects.create(
        owner=another_user,
        breed=create_breed,
        color='white',
        age_months=5,
        description='Cute kitten'
    )
    url = reverse('manage-kittens-detail', kwargs={'pk': another_kitten.id})
    data = {
        'color': 'black',
        'age_months': 144,
    }
    response = api_client.patch(url, data=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    another_kitten.refresh_from_db()
    assert another_kitten.color == 'white'

@pytest.mark.django_db
def test_delete_kitten(api_client, authenticate_user, create_kitten):
    url = reverse('manage-kittens-detail', kwargs={'pk': create_kitten.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_delete_other_kitten_fail(api_client, authenticate_user, create_breed):
    another_user = User.objects.create_user(
        username='another_user',
        email='another_user@example.com',
        password='password1'
    )
    another_kitten = Kitten.objects.create(
        owner=another_user,
        breed=create_breed,
        color='white',
        age_months=5,
        description='Cute kitten'
    )
    url = reverse('manage-kittens-detail', kwargs={'pk': another_kitten.id})
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Kitten.objects.filter(id=another_kitten.id).exists()

@pytest.mark.django_db
def test_get_breeds_list(api_client, authenticate_user, create_breed):
    url = reverse('breed-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_rate_other_kitten_success(api_client, authenticate_user, create_user, create_breed):
    another_user = User.objects.create_user(
        username='another_user',
        email='another_user@example.com',
        password='password1'
    )
    another_kitten = Kitten.objects.create(
        owner=another_user,
        breed=create_breed,
        color='white',
        age_months=5,
        description='Cute kitten'
    )
    url = reverse('rating-create')
    data = {
        'kitten': another_kitten.id,
        'score': 5
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    another_kitten.refresh_from_db()
    assert another_kitten.rating_scores.count() == 1
    assert another_kitten.rating_scores.first().score == 5

@pytest.mark.django_db
def test_rate_own_kitten_fail(api_client, authenticate_user, create_kitten):
    url = reverse('rating-create')
    data = {
        'kitten': create_kitten.id,
        'score': 5
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_get_kittens_by_breed_filter(api_client, authenticate_user, create_breed, create_user):
    print(f"Database being used for tests: {settings.DATABASES['default']['NAME']}")
    assert 'test_' in settings.DATABASES['default']['NAME'], "Tests should be using a test database"
    another_breed = Breed.objects.create(name='Pers')
    persian_kitten = Kitten.objects.create(
        owner=create_user,
        breed=another_breed,
        color='black',
        age_months=5,
        description='Funny kitten'
    )
    scottish_kitten = Kitten.objects.create(
        owner=create_user,
        breed=create_breed,
        color='grey',
        age_months=3,
        description='Scottish kitten'
    )

    url = reverse('kittens-list') + '?breed=scott'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == scottish_kitten.id

    url = reverse('kittens-list') + f'?breed_id={another_breed.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == persian_kitten.id





