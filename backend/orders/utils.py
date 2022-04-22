import uuid

from requests import post as requests_post
from json import dumps as json_dumps
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.response import Response


def get_authority(amount, description, mobile, email: None):
    req_data = {
        "merchant_id": settings.ZP_MERCHANT,
        "amount": int(amount),
        "callback_url": settings.CALLBACK_URL,
        "description": description,
        "metadata": {"mobile": mobile, 'email': email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests_post(url=settings.ZP_API_REQUEST, data=json_dumps(req_data), headers=req_header)

    if len(req.json()['errors']) != 0:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        raise APIException({"code": e_code, "message": e_message, 'request data': req_data})

    authority = req.json()['data']['authority']
    return authority


def verify(authority, amount) -> bool:
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req_data = {
        "merchant_id": settings.ZP_MERCHANT,
        "amount": amount,
        "authority": authority
    }
    req = requests_post(url=settings.ZP_API_VERIFY, data=json_dumps(req_data), headers=req_header)
    if len(req.json()['errors']) != 0:
        # e_code = req.json()['errors']['code']
        # e_message = req.json()['errors']['message']
        # return Response({f"Error code= {e_code}": f"Message: {e_message}"}, status.HTTP_400_BAD_REQUEST)
        return False

    t_status = req.json()['data']['code']
    if t_status != 100:
        if t_status == 101:
            # return Response({'Submitted': str(req.json()['data']['message'])}, status.HTTP_204_NO_CONTENT)
            return True
        else:
            # return Response({'Failed': str(req.json()['data']['message'])}, status.HTTP_400_BAD_REQUEST)
            return False
    # return Response({'Success': str(req.json()['data']['ref_id'])})
    return True


def get_payment_id(user_id, product_id):
    payment_id = f"{user_id}-{product_id}-{str(uuid.uuid4())[:8]}"
    return payment_id
