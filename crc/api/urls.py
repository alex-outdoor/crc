from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from crccloud.models import Client, Bid, Respondent, Methodology, Deliverable

class CustomSerializer(serializers.ModelSerializer):

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

# Serializers define the API representation.
class ClientSerializer(CustomSerializer):
    class Meta:
        model = Client
        fields = ('__all__')

class MethodologySerializer(CustomSerializer):
    class Meta:
        model = Methodology
        fields = ('__all__')

class DeliverableSerializer(CustomSerializer):
    class Meta:
        model = Deliverable
        fields = ('__all__')

class RespondentSerializer(CustomSerializer):
    methodologies = MethodologySerializer(many=True, read_only=True)
    
    class Meta:
        model = Respondent
        fields = ('__all__')
        
class BidSerializer(CustomSerializer):
    respondents = RespondentSerializer(many=True, read_only=True)
    deliverables = DeliverableSerializer(many=True, read_only=True)
    client = ClientSerializer(many=False, read_only=True)
    
    class Meta:
        model = Bid
        fields = ('__all__')

class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class BidsViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet)
router.register(r'bid', BidsViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
