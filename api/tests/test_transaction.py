""" CRUD tests for TransactionRecord """
import string
import random
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import ServiceType


def generate_random_transaction_data() -> dict:
    """ Helper to generate transaction data """
    return {
        "service_type": random.choice(list(ServiceType)),
        "provider": random.choice(["idemia", "usps"]),
        "csp": "login.gov",
        "cost": random.randrange(0, 200) / 100,
        "result": random.choice([True, False]),
    }


def post_record_to_view(view_name, client):
    """ POST to the url with a randomly generated record """
    url = reverse(view_name)
    record = generate_random_transaction_data()
    return client.post(url, record)


class TransactionRecordCRUDTest(APITestCase):
    """ Test crud operations on TransactionRecord objects """

    def test_create_transaction_succeed(self):
        """ Test that a transaction record can be created """
        response = post_record_to_view("transactionrecord-list", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_transaction_fail(self):
        """ Test that bad request bodies are rejected """
        url = reverse("transactionrecord-list")
        response = self.client.post(url, None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_transaction_succeed(self):
        """ Test that we can GET a previously created record """
        # Generate a record
        response = post_record_to_view("transactionrecord-list", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Read the record
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_read_transaction_fail(self):
        """ Test that GET with an invalid record id fails """
        url = reverse("transactionrecord-detail", args=["invalid"])
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_transaction_succeed(self):
        """ Test that we can update the record result """
        # Generate a record
        response = post_record_to_view("transactionrecord-list", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the record result
        new_result = random.choice([True, False])
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        patch_response = self.client.patch(url, data={"result": new_result})

        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()["result"], new_result)

    def test_update_transaction_fail(self):
        # Generate a record
        response = post_record_to_view("transactionrecord-list", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt incorrect modification of the record
        new_service_type = "".join(random.choices(string.ascii_lowercase, k=10))
        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        patch_response = self.client.put(url, data={"service_type": new_service_type})

        self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_transaction_fail(self):
        """ Test that deleting a record is not possible """
        # Generate a record
        response = post_record_to_view("transactionrecord-list", self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse("transactionrecord-detail", args=[response.json()["record_uuid"]])
        get_response = self.client.delete(url)

        self.assertEqual(get_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
