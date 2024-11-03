# Rossum Test Task

This is a Django-based project for the Rossum test task, designed to run in a Docker container. The project includes a simple API endpoint that connects to Rossum, retrieves data based on queue and annotation IDs, transforms it, and sends the result to a PostBin URL.

## Prerequisites

- **Docker**: Make sure Docker is installed on your system.
- **PostBin**: Create a new PostBin URL by visiting [https://www.postb.in/](https://www.postb.in/). You’ll need this URL to send transformed data as part of the task.

## Environment Configuration

The project requires a few environment variables to interact with Rossum and PostBin. Here’s a summary of what each variable is used for:

- **ROSSUM_USERNAME**: Your Rossum account username.
- **ROSSUM_PASSWORD**: Your Rossum account password.
- **ROSSUM_DOMAIN**: The domain for your Rossum instance, such as `mspas.rossum.app`.
- **POSTBIN_URL**: The PostBin URL where the transformed data will be sent.

You can set these variables in the Dockerfile.

## How to Build and Run the Project

1. **Build and Start the Container**:

   To build and start the project, simply run:

```bash
docker-compose up --build
```

This command will:
- Build the Docker image.
- Set up the Django application with all necessary dependencies.
- Run migrations and create a superuser for accessing the endpoint.

## Environment Setup

Make sure you update the following environment variables if needed:

- `ROSSUM_USERNAME` and `ROSSUM_PASSWORD` should be set to your Rossum credentials.
- `ROSSUM_DOMAIN` should match your Rossum domain (e.g., `mspas.rossum.app`).
- `POSTBIN_URL` should be set to a new PostBin URL created from [https://www.postb.in/](https://www.postb.in/).

If you're using a different `queue_id` or `annotation_id`, update them in the request as described below.

## Testing the Endpoint

Once the container is up and running, you can test the endpoint using `curl`.

### Sample Test Command

```bash
curl -u myUser123:secretSecret -X GET "http://localhost:8000/export/?queue_id=1404916&annotation_id=4788316"
```
- Replace 1404916 and 4788316 with your specific Rossum queue_id and annotation_id.

- Update `myUser123` and `secretSecret` in the curl command if you have customized the superuser credentials in the Dockerfile.

### Response

If everything is set up correctly, you should receive a JSON response with the result of the operation.

## Configuration Notes

If you’re running the project with different Rossum credentials or a new PostBin URL, update the following lines in the Dockerfile:

```dockerfile
ENV ROSSUM_USERNAME='your_rossum_username'
ENV ROSSUM_PASSWORD='your_rossum_password'
ENV POSTBIN_URL='your_postbin_url'
```
After updating, rebuild the Docker image:

```bash
docker-compose up --build
```

## Additional Information

- **Queue and Annotation IDs**: The IDs used in the test (`queue_id=1404916` and `annotation_id=4788316`) are from the `mspas.rossum.app` instance. If you have different IDs, make sure to change them in the curl command.
- **PostBin URL**: Create a new PostBin URL if needed, and set it in the environment variable `POSTBIN_URL`.

## Testing

Once the container is up and running, you can run tests using the following command:

```bash
docker-compose run web python manage.py test
```
This command will:
- Start a temporary container based on the `web` service defined in `docker-compose.yml`.
- Run Django’s test suite using `python manage.py test`.
- Exit after the tests complete, without affecting the running `web` container.

> **Note**: Ensure that the container are already up (using `docker-compose up`).

If you need to re-run tests frequently, you can keep the main container running and simply use the `docker-compose run` command each time to test any changes.
