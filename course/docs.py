from drf_yasg import openapi
from rest_framework import status

SUBSCRIBE_VIEW_SCHEMA = {
    "operation_id": "subscribe to course",
    "operation_description": """subscribe to course""",
    "responses": {
        status.HTTP_200_OK: openapi.Response(
            "Success",
            openapi.Schema(
                title="Success",
                type=openapi.TYPE_OBJECT,
                properties=dict(
                    message=openapi.Schema(type=openapi.TYPE_STRING, example="string"),
                ),
            ),
        ),
    },
}
