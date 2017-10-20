from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from crccloud.models import Client

# Serializers define the API representation.
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

# class ProjectSerializer(serializers.ModelSerializer):
# 
#     manager = CustomUserSerializer()
#     created_by = CustomUserSerializer()
#     client = ClientSerializer()
# 
#     info_project = InfoSerializer(many=True, read_only=True)
# 
#     class Meta:
#         model = Project
#         fields = ('__all__')

class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
#from rest_framework import rest_framework.urls
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
