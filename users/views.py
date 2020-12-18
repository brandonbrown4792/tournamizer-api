from users.models import User
from users.serializers import UserSerializer
from users.managers import UserManager
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class UserViewSet(viewsets.ModelViewSet):
    """
    User view model with custom create to return token to user on creation
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)