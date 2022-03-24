from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.serializsers import LoginRegisterSerializer, RetrieveUserSerializer

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


class RetrieveUserAPIView(RetrieveAPIView):
    """
    First case: User is authenticated
        URL: https://scarfly.ir/accounts/retrieve/<str:any_thing>/
    Second case: User is not authenticated
        URL: https://scarfly.ir/accounts/retrieve/<str:phone_number>/
    GET:
        Response:
            1: HTTP 404:
                { "detail": "Not found." }
            2: HTTP 200
                {
                    "first_name": "Value",
                    "last_name": "Value",
                    "phone_number": "+989876543210"
                }
    """
    serializer_class = RetrieveUserSerializer
    lookup_field = 'phone_number'
    queryset = USER.objects.all()

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        return super(RetrieveUserAPIView, self).get_object()
