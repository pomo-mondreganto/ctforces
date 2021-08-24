from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


def serialize(obj, token_type):
    serializer = URLSafeTimedSerializer(secret_key=settings.SECRET_KEY)
    result = serializer.dumps(obj=obj, salt=token_type)
    return result


def deserialize(string, token_type, max_age=None):
    serializer = URLSafeTimedSerializer(secret_key=settings.SECRET_KEY)
    try:
        result = serializer.loads(string, salt=token_type, max_age=max_age)
        return result
    except BadSignature:
        return None
    except SignatureExpired:
        return None
