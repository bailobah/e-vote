from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer

class LoginSerializer(RestAuthLoginSerializer):
    email = None



