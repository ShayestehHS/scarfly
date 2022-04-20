from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializsers import LoginRegisterSerializer, RetrieveUserSerializer, UpdateUserSerializer
from accounts.permissions import OnlyAccountOfUser

USER = get_user_model()


class Login(APIView):
    """
    URL: https://scarfly.ir/accounts/login/
    POST:
        DATA: { "phone_number" : value }
            * Length of phone_number: 13
            * phone_number must start with `+989`
            * Type of phone_number value should be string
        Response:
            1: HTTP 400:
                { "detail": message } => (CommonProblem: Invalid phone_number)
            2: HTTP 401:
                { "detail": message } => (CommonProblem: Some token(invalid/valid) is set in header)
            3: HTTP 200:
                { "access": token, "refresh":token }
    """
    permission_classes = [~IsAuthenticated]
    serializer_class = LoginRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        res = Response(serializer.data, status.HTTP_200_OK)
        res.set_cookie('access', res.data['access'], httponly=True)
        res.set_cookie('refresh', res.data['refresh'], httponly=True)
        return res


class Register(CreateAPIView):
    """
    URL: https://scarfly.ir/accounts/register/
    POST:
        DATA: { "phone_number" : value }
            * Length of phone_number should be 13 character
            * phone_number must start with `+989`
            * Type of phone_number value should be string
        Response:
            1: HTTP 400:
                { "detail": message } => (CommonProblem: Invalid phone_number format)
                { "duplicated": message } => (CommonProblem: Duplicated phone number)
                { "phone_number": [ message ] } => (CommonProblem: Invalid phone_number)
            2: HTTP 401:
                { "detail": message } => (CommonProblem: Some token(invalid/valid) is set in header)
            3: HTTP 201:
                {
                    "access": token,
                    "refresh":token,
                    "access_expiration": UNIX time,
                    "refresh_expiration": UNIX time,
                }
    """
    serializer_class = LoginRegisterSerializer
    permission_classes = [~IsAuthenticated]

    def post(self, request, *args, **kwargs):
        res = super(Register, self).post(request, *args, **kwargs)
        res.set_cookie('access', res.data['access'])
        res.set_cookie('refresh', res.data['refresh'])
        return res


class Verify(APIView):
    """
    URL: https://scarfly.ir/accounts/verify/
    GET:
        Response:
            1: HTTP 401:
                { "detail": message } => (CommonProblem: User is not authenticated)
            2: HTTP 200:
                {'detail': 'user is authenticated'}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'detail': 'user is authenticated'})


class RetrieveUpdateUserAPIView(RetrieveUpdateAPIView):
    """GET:
        Response:
            1: HTTP 401:
                { "detail": message } => (CommonProblem: User is not authenticated)
            2: HTTP 200
                {
                    "first_name": "Value",
                    "last_name": "Value",
                    "phone_number": "+989876543210"
                }
    PUT/PATCH:
        DATA:
            {"first_name":"Value", "last_name":"Value"}
        Response:
            1. HTTP 401:
                { "detail": message } => (CommonProblem: User is not authenticated)
            2: HTTP 200:
                {"first_name":"Value", "last_name":"Value"}
    """
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "POST":
            return RetrieveUserSerializer
        return UpdateUserSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
