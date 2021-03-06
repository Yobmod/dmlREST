from rest_framework.generics import (ListAPIView,
									RetrieveAPIView,
									RetrieveUpdateAPIView,
									CreateAPIView,
									DestroyAPIView,
									)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from django.contrib.auth import get_user_model
#from django.db.models import Q

#from .permissions import IsOwnerOrReadOnly
from .serializers import (UserCreateSerializer,
							UserLoginSerializer,
							)

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
		queryset = User.objects.all()
		serializer_class = UserCreateSerializer
		permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
		serializer_class = UserLoginSerializer
		permission_classes = [AllowAny]

		def post(self, request, *args, **kwargs):
			data = request.data
			serializer = UserLoginSerializer(data=data)
			if serializer.is_valid(raise_exception=True):
				new_data = Response(new_data, status=HTTP_200_OK)
			return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
