from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers import RegistrationSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def index(request) -> Response:
    """Index page."""
    return Response({"message": "Simple forecasts service"})


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request) -> Response:
    """Register new user."""
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        account = serializer.save()
        data["status"] = "new user has been created"
        data["email"] = account.email
        data["username"] = account.username
        token = Token.objects.get(user=account).key
        data["auth_token"] = token
    else:
        data = serializer.errors
    return Response(data)
