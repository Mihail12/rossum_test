import requests  # type: ignore


class RossumAPIClient:
    def __init__(self, username: str, password: str, domain: str):
        """
        Initialize the API client with authentication credentials.

        :param username: Rossum API username.
        :param password: Rossum API password.
        :param domain: Rossum API domain
        """
        self.username = username
        self.password = password
        self.domain = domain
        self.token = None

    def authenticate(self) -> bool:
        """
        Authenticate with the Rossum API and store the token.

        :return: True if authentication was successful, False otherwise.
        """
        auth_url = f"https://{self.domain}/api/v1/auth/login"
        payload = {"username": self.username, "password": self.password}
        response = requests.post(auth_url, json=payload)

        if response.status_code == 200:
            self.token = response.json().get("key")
            return True
        else:
            print("Authentication failed:", response.json())
            return False

    def get_export_xml(self, queue_id: str, annotation_id: str) -> str:
        """
        Fetch the XML export data from Rossum for a specific queue and application ID.

        :param queue_id: ID of the queue in Rossum.
        :param annotation_id: ID of the application to fetch data for.
        :return: XML content as a string if successful, None otherwise.
        """
        if not self.token:
            raise Exception("Not authenticated. Please call authenticate() first.")

        export_url = f"https://{self.domain}/api/v1/queues/{queue_id}/export"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"status": "to_review", "format": "xml", "id": annotation_id}
        response = requests.get(export_url, headers=headers, params=params)

        if response.status_code == 200:
            return response.content
        else:
            print("Failed to fetch XML data:", response.json())
            return ""
