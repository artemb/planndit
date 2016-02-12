from rest_framework import viewsets, permissions
from plan.api.serializers import RouteSerializer, OrderSerializer, OrderItemSerializer, VehicleSerializer
from plan.models import Route, Order, OrderItem, Vehicle


class RouteViewset(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    filter_fields = ('date',)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user.account)


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class VehicleViewset(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


