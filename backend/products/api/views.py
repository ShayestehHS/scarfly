from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from products.api.serializers import ProductDetailSerializer
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
