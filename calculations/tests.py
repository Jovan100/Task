import json
from calculations.models import Calculations
from users.models import User
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from calculations.api.serializers import CalculationsSerializer


class CalculationsTestCase(APITestCase):
    def setUp(self):
        self.password = "123"
        self.email = "john@gmail.com"
        self.user = User.objects.create(full_name="John Doe",
                                        email=self.email,
                                        password=self.password)
        self.admin = User.objects.create(full_name="John Doe Junior",
                                        email="johnjr@gmail.com",
                                        password=self.password,
                                        is_staff=True,
                                        is_admin=True)
        self.data1 = {"num": [1, 2, 3]}
        self.sum1 = sum(self.data1['num'])
        self.data2 = {"num": "4, 5, 6"}
        self.sum2 = self.sum1 + sum(int(x) for x in self.data2['num'].split(','))
        self.client.force_authenticate(user=self.user)

    def test_add_number_int_authenticated(self):
        data = {"num": 1}
        response = self.client.post('/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_list_authenticated(self):
        response = self.client.post('/add/', self.data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data1['num'])

    def test_add_number_string_authenticated(self):
        data = {"num": "1, 2, 3"}
        response = self.client.post('/add/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, [int(x) for x in data['num'].split(',')])

    def test_add_bad_string(self):
        data = {'num': 'test'}
        response = self.client.post('/add/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_number_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post('/add/', self.data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_calculate_authenticated(self):
        self.client.post('/add/', self.data1, format='json')
        response = self.client.get(reverse("calculate"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.sum1)

    def test_all_calculations_authenticated(self):
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        response = self.client.get(reverse("calculate", kwargs={"all": "all"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [self.sum1, self.sum2])

    def test_no_calculations(self):
        response = self.client.get(reverse("calculate", kwargs={"all": "all"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_bad_all_calculations(self):
        self.client.post('/add/', self.data1, format='json')
        response = self.client.get(reverse("calculate", kwargs={"all": "test"}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_unauthenticated(self):
        self.client.force_authenticate(user=None)
        self.client.post('/add/', self.data1, format='json')
        response = self.client.get(reverse("calculate"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reset_authenticated(self):
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        response = self.client.post(reverse("reset"))
        calculation = Calculations.objects.get(pk=response.data['id'])
        serialized = CalculationsSerializer(calculation)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serialized.data)

    def test_bad_reset(self):
        response = self.client.post(reverse("reset"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_unauthenticated(self):
        self.client.force_authenticate(user=None)
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("reset"))
        response = self.client.post(reverse("reset"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_history_retrieve_authenticated(self):
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        test_calc = self.client.post(reverse("reset"))
        calculation = Calculations.objects.get(pk=test_calc.data['id'])
        serialized = CalculationsSerializer(calculation)
        response = self.client.get(reverse("history", kwargs={"pk": test_calc.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)

    def test_history_retrieve_unauthenticated(self):
        self.client.force_authenticate(user=None)
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post(reverse("reset"))
        response = self.client.get(reverse("history", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_history_list_admin_authenticated(self):
        self.client.force_authenticate(user=self.admin)
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        test_calc1 = self.client.post(reverse("reset"))
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        test_calc2 = self.client.post(reverse("reset"))
        calculation1 = Calculations.objects.get(pk=test_calc1.data['id'])
        serialized1 = CalculationsSerializer(calculation1)
        calculation2 = Calculations.objects.get(pk=test_calc2.data['id'])
        serialized2 = CalculationsSerializer(calculation2)
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [serialized1.data, serialized2.data])

    def test_history_list_user_unauthenticated(self):
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        self.client.post(reverse("reset"))
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        self.client.post(reverse("reset"))
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_history_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        self.client.post(reverse("reset"))
        self.client.post('/add/', self.data1, format='json')
        self.client.get(reverse("calculate"))
        self.client.post('/add/', self.data2)
        self.client.get(reverse("calculate"))
        self.client.post(reverse("reset"))
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
