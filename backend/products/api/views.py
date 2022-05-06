from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from products.api.serializers import ListProductSerializer, ProductDetailSerializer
from products.models import Product


class RetrieveProductAPIView(RetrieveAPIView):
    """
    URL: https://scarfly.ir/products/retrieve/<int:pro_code>/
    GET:
        Response:
            1. HTTP 401:
                { "detail": message } => (CommonProblem: Invalid token. Solution: Delete 'Authorization' from header)
            2. HTTP 404:
                { "detail": "Not found." } => (CommonProblem: Invalid product id)
            3. HTTP 200:
                {
                    "pk" : value,
                    "name": value,
                    "image": Image_url,
                    "pro_code": value,
                    "sell_price": value,
                    "description": value
                }
    """
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'pro_code'


class ListProductAPIView(ListAPIView):
    """
    URL: https://scarfly.ir/api/products/list/
    URL: https://scarfly.ir/api/products/list/?productID=1&productID=2&..
    GET:
        Response:
            1. HTTP 404:
                { "detail": "Not found." } => (CommonProblem: Invalid product id)
            2. HTTP 200:
                {
                    "count": 4,
                    "next": null,
                    "previous": null,
                    "results": [
                        {
                            "pk": 1,
                            "name": "",
                            "image": "",
                            "pro_code": 1,
                            "sell_price": 59000,
                            "description": ""
                        },
                        {},
                        {},
                        {}
                    ]
                }
    """
    serializer_class = ListProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        list_product_id = [int(pro_id) for pro_id in self.request.GET.getlist('productID')]
        qs = Product.objects.filter(is_available=True)

        if list_product_id:
            qs = qs.filter(pro_code__in=list_product_id)
        return qs

    def list(self, request, *args, **kwargs):
        response = super(ListProductAPIView, self).list(request, *args, **kwargs)

        if response.data.get('count') == 0:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return response
