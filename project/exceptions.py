from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # If the error is a dict with 'message' and possibly other keys, return as is
    if isinstance(response.data, dict):
        # If the dict has only one key and it's a list or string, keep old behavior
        if len(response.data) == 1:
            value = next(iter(response.data.values()))
            if isinstance(value, list) and value:
                return Response({"message": value[0]}, status=response.status_code)
            elif isinstance(value, str):
                return Response({"message": value}, status=response.status_code)
        # If the dict has 'message' and 'status', return the whole dict
        if "message" in response.data and "status" in response.data:
            return Response(response.data, status=response.status_code)
        # Otherwise, return the whole dict
        return Response(response.data, status=response.status_code)

    return Response({"message": "Something went wrong"}, status=response.status_code)
