import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from store.models import Collection
from rest_framework.test import APIClient
from rest_framework import status

class TestCreateCollection:
    #Arrange,Act,Assert(AAA)
    # @pytest.mark.skip
    @pytest.mark.django_db
    def test_if_user_is_anonymous_returns_401(self,create_collection):
        response = create_collection({'title':'a'})
        #Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_if_user_is_not_admin_returns_403(self,authenticate,create_collection):
        authenticate(is_staff=False)
        response = create_collection({'title':'a'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_if_data_is_invalid_returns_400(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response = create_collection({'title':''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    @pytest.mark.django_db
    def test_if_data_is_valid_returns_201(self,authenticate,create_collection):
        authenticate(is_staff=True)
        response = create_collection({'title':'ram'})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


class TestRetrieveCollection:
    @pytest.mark.django_db
    def test_if_collection_exists_returns_200(self, api_client, authenticate):
        authenticate(is_staff=True) 
        collection = baker.make(Collection)
        response = api_client.get(f'/store/collections/{collection.id}/')
        assert response.status_code == status.HTTP_200_OK

    