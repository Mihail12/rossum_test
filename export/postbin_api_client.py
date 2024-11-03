import json

import requests  # type: ignore


class PostBinClient:
    def __init__(self, url: str):
        """
        Initialize the client with the PostBin URL.

        :param url: The endpoint URL for PostBin.
        """
        self.url = url
        self.headers = {"X-Status": "Awesome", "Content-Type": "application/json"}

    def send_data(self, annotation_id: str, transformed_base64_xml: str) -> dict:
        """
        Send the transformed XML data as a POST request to the PostBin URL.

        :param annotation_id: The annotation ID to be sent.
        :param transformed_base64_xml: The base64-encoded XML content.
        :return: A JSON with 'success' key indicating if the POST request was successful.
        """
        payload = {"annotationId": annotation_id, "content": transformed_base64_xml}

        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": response.json()}
        except requests.RequestException as e:
            return {"success": False, "error": str(e)}
