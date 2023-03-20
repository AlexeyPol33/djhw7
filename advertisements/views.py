from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework
from rest_framework import filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Advertisement, Favorites
from .serializers import AdvertisementSerializer, FavoritesSerializer
from .permissions import IsOwnerPermissin
from .filters import AdvertisementFilter
from rest_framework.response import Response


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset=Advertisement.objects.all()
    serializer_class=AdvertisementSerializer
    filter_backends=[rest_framework.DjangoFilterBackend,filters.SearchFilter]
    filterset_class=AdvertisementFilter
    


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update",'destroy']:
            permission_classes = [IsOwnerPermissin|IsAdminUser]
        else:
            return []
        return [permission() for permission in permission_classes]
    
class FavoritesViewSer(ModelViewSet):
    
    def list(self, request):
        
        queryset = Favorites.objects.filter(user=request.user)
        serializer = FavoritesSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list','retrieve',"create","partial_update"]:
            permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            permission_classes = [IsOwnerPermissin]
      
        return [permission() for permission in permission_classes]
    


