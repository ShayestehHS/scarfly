from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from orders.api.serializers import OrderCreateSerializer, OrderDetailUpdateSerializer
from orders.models import Order
from orders.permissions import OnlyOrderOfUser


class CreateOrderAPIView(CreateAPIView):
    """
    URL: https://scarfly.ir/orders/create/
    POST:
        DATA: {
                'product_id': 1(String),
                'address': value(String),
                'postal_code': value(String),
                }
        RETURN:
            1: HTTP 400:
                { "detail": message } => (CommonProblem: Not matched `product_id`)
                { "product": message} => (CommonProblem: Not matched `product_id`)
            2: HTTP 401:
                { "detail": message }  => (CommonProblem: User is not authenticated)
            3: HTTP 500:
                { "detail" : { "code": value, "message": value } } => (CommonProblem: Invalid data was sent to payment server)
                { "duplicated" : message } => (CommonProblem: Fail to create unique payment_id)
            3: HTTP 201:
                {
                    "product": {
                        "id": 2,
                        "name": "شال بچگانه"
                    },
                    "address": "asdf",
                    "postal_code": "1737863549",
                    "authority": "A00000000000000000000000000328961379",
                    "payment_id": "1-2-6c27425f",
                    "status": "1",
                    "offer_key": null,
                    "timestamp": "2022-03-28T13:25:58.205702+04:30"
                }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateOrderAPIView(RetrieveUpdateAPIView):
    """
    URL: https://scarfly.ir/orders/pk/
    URL: https://scarfly.ir/orders/authority/
    GET:
        Response:
            1. HTTP 404:
                { "detail": message } => (CommonProblem: Invalid authority/pk)
            2. HTTP 401:
                { "detail": message } => (CommonProblem: User is not authenticated)
            3. HTTP 200:
                {
                    "id": order_id,
                    "product": {
                        "id": product_id,
                        "name": product_name
                    },
                    "timestamp": "2022-02-21T10:41:35.649315+03:30",
                    "is_paid": false,
                    "authority": "123abc",
                    "payment_id": "1-2-13213",
                    "status": "3",
                    "offer_key": null,
                    "user": user_id
                }
    """
    permission_classes = [IsAuthenticated, OnlyOrderOfUser]
    queryset = Order.objects.all()
    serializer_class = OrderDetailUpdateSerializer

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        lookup_value = self.kwargs.get('lookup')
        if lookup_value is not None:
            if len(lookup_value) > 4:  # Ignore empty fields.
                filter['authority'] = lookup_value
            else:
                filter['pk'] = lookup_value

        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj
