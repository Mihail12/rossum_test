import base64
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from export.serializers import ExportRequestSerializer

# Sample data for the test
SAMPLE_QUEUE_ID = "123456"
SAMPLE_ANNOTATION_ID = "654321"
SAMPLE_XML_CONTENT = """<export><data>Sample XML Data</data></export>"""
SAMPLE_TRANSFORMED_XML = (
    """<InvoiceRegisters><Invoices><Payable>Sample Transformed Data</Payable></Invoices></InvoiceRegisters>"""
)
SAMPLE_BASE64_XML = base64.b64encode(SAMPLE_TRANSFORMED_XML.encode("utf-8")).decode("utf-8")
SAMPLE_POSTBIN_RESPONSE = {"success": True}
BASIC_AUTH_USERNAME = "test_user"
BASIC_AUTH_PASSWORD = "test_password"


class ExportViewTestCase(TestCase):
    def setUp(self):
        # Create a test user with the Basic Auth credentials
        self.user = User.objects.create_user(username=BASIC_AUTH_USERNAME, password=BASIC_AUTH_PASSWORD)

        self.client = APIClient()
        # Set the Authorization header with Basic Auth credentials
        credentials = f"{BASIC_AUTH_USERNAME}:{BASIC_AUTH_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {encoded_credentials}")

    @patch("export.views.RossumAPIClient")
    @patch("export.views.PostBinClient")
    def test_export_view_success(self, MockPostBinClient, MockRossumAPIClient):
        # Mock RossumAPIClient behavior
        mock_api_client = MockRossumAPIClient.return_value
        mock_api_client.authenticate.return_value = True
        mock_api_client.get_export_xml.return_value = SAMPLE_XML_CONTENT

        # Mock RossumInvoiceTransformer behavior
        with patch("export.views.RossumInvoiceTransformer") as MockTransformer:
            mock_transformer_instance = MockTransformer.return_value
            mock_transformer_instance.transform_base64.return_value = SAMPLE_BASE64_XML

            # Mock PostBinClient behavior
            mock_postbin_client = MockPostBinClient.return_value
            mock_postbin_client.send_data.return_value = SAMPLE_POSTBIN_RESPONSE

            # Make a request to the export_view
            response = self.client.get(
                reverse("export_view"),
                {"queue_id": SAMPLE_QUEUE_ID, "annotation_id": SAMPLE_ANNOTATION_ID},
            )

            # Assertions
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), SAMPLE_POSTBIN_RESPONSE)

            # Verify RossumAPIClient methods were called
            mock_api_client.authenticate.assert_called_once()
            mock_api_client.get_export_xml.assert_called_once_with(
                queue_id=SAMPLE_QUEUE_ID, annotation_id=SAMPLE_ANNOTATION_ID
            )

            # Verify transformer transform method was called
            mock_transformer_instance.transform_base64.assert_called_once()

            # Verify PostBinClient send_data was called with the correct arguments
            mock_postbin_client.send_data.assert_called_once_with(
                annotation_id=SAMPLE_ANNOTATION_ID,
                transformed_base64_xml=SAMPLE_BASE64_XML,
            )

    @patch("export.views.RossumAPIClient")
    def test_export_view_authentication_failure(self, MockRossumAPIClient):
        # Mock RossumAPIClient behavior for failed authentication
        mock_api_client = MockRossumAPIClient.return_value
        mock_api_client.authenticate.return_value = False

        # Make a request to the export_view
        response = self.client.get(
            reverse("export_view"),
            {"queue_id": SAMPLE_QUEUE_ID, "annotation_id": SAMPLE_ANNOTATION_ID},
        )

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])


class ExportRequestSerializerTestCase(TestCase):
    def test_serializer_with_valid_data(self):
        # Valid input data
        valid_data = {"queue_id": "123456", "annotation_id": "654321"}

        # Initialize the serializer with valid data
        serializer = ExportRequestSerializer(data=valid_data)

        # Validate the serializer
        self.assertTrue(serializer.is_valid(), "Serializer should be valid with correct data.")
        self.assertEqual(
            serializer.validated_data,
            valid_data,
            "Validated data should match input data.",
        )

    def test_serializer_with_invalid_data(self):
        # Missing 'annotation_id'
        invalid_data = {"queue_id": "123456"}

        # Initialize the serializer with invalid data
        serializer = ExportRequestSerializer(data=invalid_data)

        # Validate the serializer
        self.assertFalse(
            serializer.is_valid(),
            "Serializer should be invalid when 'annotation_id' is missing.",
        )
        self.assertIn("annotation_id", serializer.errors, "'annotation_id' should be in errors.")

        # Missing both 'queue_id' and 'annotation_id'
        invalid_data_empty = {}
        serializer_empty = ExportRequestSerializer(data=invalid_data_empty)

        self.assertFalse(
            serializer_empty.is_valid(),
            "Serializer should be invalid when data is empty.",
        )
        self.assertIn("queue_id", serializer_empty.errors, "'queue_id' should be in errors.")
        self.assertIn(
            "annotation_id",
            serializer_empty.errors,
            "'annotation_id' should be in errors.",
        )
