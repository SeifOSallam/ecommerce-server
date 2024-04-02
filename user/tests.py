from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


# Create your tests here.
class SignUpTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create(
            username="testUser",
            first_name="existing",
            last_name="user",
            email="user@test.com",
            password="aA1!testuser",
        )
        return super().setUpTestData()

    def test_sign_up_missing_username(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "first_name": "test",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_missing_first_name(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_missing_last_name(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_missing_email(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "test",
                "last_name": "test",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_missing_email(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "test",
                "last_name": "test",
                "email": "test@test.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_username(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "te st",
                "first_name": "test",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "te#st",
                "first_name": "test",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_invalid_first_name_length(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "te",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "testtesttesttesttest",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_first_name_format(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "td23ts",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "td  ts",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "first_name": "td@ts",
                "last_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_last_name_length(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "te",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "testtesttesttesttest",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_first_name_format(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "td23ts",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "td  ts",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "td@ts",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_email(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_invalid_password(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1adftest",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA!adtest",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aadfa1test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data), 1)

        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_existing_username(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": self.test_user.username,
                "last_name": "test",
                "first_name": "test",
                "email": "test2@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_existing_email(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test2",
                "last_name": "test",
                "first_name": "test",
                "email": self.test_user.email,
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(len(response.data), 1)

    def test_sign_up_successful(self):
        response = self.client.post(
            reverse("sign_up"),
            {
                "username": "test",
                "last_name": "test",
                "first_name": "test",
                "email": "test@test.com",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse("login"),
            {
                "username": "test",
                "password": "aA1!test",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertEqual(len(response.data), 2)


class LoginTests(APITestCase):
    test_user_password = "aA1!testuser"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.test_user = User.objects.create(
            username="loginTestUser",
            first_name="existing",
            last_name="user",
            email="user@test.com",
            password=make_password(cls.test_user_password),
        )
        return super().setUpTestData()

    def test_login_to_existing_user(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.test_user.username,
                "password": self.test_user_password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertEqual(len(response.data), 2)

    def test_login_to_non_existing_user(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "nonexistingusername",
                "password": self.test_user_password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(len(response.data), 1)

    def test_login_wrong_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": self.test_user.username,
                "password": "wrongpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)
        self.assertEqual(len(response.data), 1)
