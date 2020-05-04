import json
from users.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from users.api.serializers import UserSerializer
from requests.auth import HTTPBasicAuth
import base64

class UserRegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"full_name": "John Doe", "email": "john@gmail.com", "password": "123"}
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_registration(self):
        data = {"full_name": "John Doe", "email": "", "password": "123"}
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UsersTestCase(APITestCase):
    def setUp(self):
        self.password = "123"
        self.user = User.objects.create(full_name="John Doe",
                                        email="john@gmail.com",
                                        password=self.password,
                                        is_admin=True,
                                        is_staff=True)
                                        
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_list_authenticated(self):
        response = self.client.get(reverse("users-list"))
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user_authenticated(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.pk}))
        usr = User.objects.get(pk=self.user.pk)
        serialized = UserSerializer(usr)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bad_user_retrieve(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_update_authenticated(self):
        data = {"full_name": "John Doe Junior", "email": "john@gmail.com", "password": "123"}
        response = self.client.put(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        usr = User.objects.get(pk=self.user.pk)
        serialized = UserSerializer(usr)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {"full_name": "John Doe Junior", "email": "john@gmail.com", "password": "123"}
        response = self.client.put(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_bad_update(self):
        data = {"full_name": "John Doe Junior", "email": "", "password": "123"}
        response = self.client.put(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_partial_update_authenticated(self):
        data = {"full_name": "John Doe Junior"}
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        usr = User.objects.get(pk=self.user.pk)
        serialized = UserSerializer(usr)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_partial_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {"full_name": "John Doe Junior"}
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_bad_partial_update(self):
        data = {"full_name": ""}
        response = self.client.patch(reverse("users-detail", kwargs={"pk": self.user.pk}),
                                                           data=json.dumps(data),
                                                           content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_delete_authenticated(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("users-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_bad_delete(self):
        response = self.client.get(reverse("users-detail", kwargs={"pk": 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
