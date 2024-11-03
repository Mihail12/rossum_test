import os

from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from export.invoice_transformer import RossumInvoiceTransformer
from export.postbin_api_client import PostBinClient
from export.rossum_api_client import RossumAPIClient
from export.serializers import ExportRequestSerializer

ROSSUM_USERNAME = os.getenv("ROSSUM_USERNAME")
ROSSUM_PASSWORD = os.getenv("ROSSUM_PASSWORD")
POSTBIN_URL = os.getenv("POSTBIN_URL")
ROSSUM_DOMAIN = os.getenv("ROSSUM_DOMAIN")


@api_view(["GET"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def export_view(request):
    # Validate input parameters using the serializer
    serializer = ExportRequestSerializer(data=request.GET)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    queue_id = serializer.validated_data["queue_id"]
    annotation_id = serializer.validated_data["annotation_id"]

    # Initialize Rossum API client with credentials
    api_client = RossumAPIClient(username=ROSSUM_USERNAME, password=ROSSUM_PASSWORD, domain=ROSSUM_DOMAIN)
    result = {"success": False}
    # Authenticate with Rossum API
    if api_client.authenticate():
        xml_content = api_client.get_export_xml(queue_id=queue_id, annotation_id=annotation_id)

        if xml_content:
            # Initialize transformer with the retrieved XML content
            transformer = RossumInvoiceTransformer(xml_content)
            output_base64 = transformer.transform_base64()

            post_bin_client = PostBinClient(url=POSTBIN_URL)
            result = post_bin_client.send_data(annotation_id=annotation_id, transformed_base64_xml=output_base64)
            success = result.get("success", False)
            result = {"success": success}

    return JsonResponse(result)
