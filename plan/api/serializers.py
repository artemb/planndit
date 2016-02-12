from rest_framework import serializers
from plan.externals import routing
from plan.models import Route, Vehicle, Order, Location, OrderItem


class LocationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=False)

    class Meta:
        model = Location
        fields = ('id', 'address', 'latitude', 'longitude', 'is_valid')


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ('id', 'name')


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=False)

    def update(self, instance, validated_data):
        instance.key = validated_data.get('key', instance.key)
        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance

    def create(self, validated_data):
        item = OrderItem.objects.create(**validated_data)
        return item

    class Meta:
        model = OrderItem
        fields = ('id', 'key', 'value')


class OrderSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    orderitem_set = OrderItemSerializer(many=True)
    distance = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    def get_distance(self, order):
        if order.distance is None:
            return '0mi'
        miles = order.distance * 0.000621371192
        return '{:.2f}mi'.format(miles)

    def get_duration(self, order):
        if order.duration is None:
            return
        minutes, seconds = divmod(order.duration, 60)
        hours, minutes = divmod(minutes, 60)
        return '{:02d}:{:02d}'.format(hours, minutes)
        # if hours > 0:
        #     return '{:d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
        # else:
        #     return '{:02d}:{:02d}'.format(minutes, seconds)

    def update(self, instance, validated_data):
        instance.reference = validated_data.get('reference', instance.reference)
        instance.commentary = validated_data.get('commentary', instance.reference)
        location = validated_data.get('location', instance.reference)
        old_valid = instance.location.is_valid
        old_location = instance.location.id
        instance.location = Location.objects.filter(id=location['id'])[0]
        now_valid = instance.location.is_valid
        now_location = instance.location.id
        if old_valid != now_valid:
            if now_valid:
                orders = instance.route.orders.filter(location__is_valid=True)
                number = orders.count() - 1
                order = orders.last()
                order.order += 1
                order.save()
                instance.order = number
            else:
                instance.order = 0
                orders = instance.route.orders.filter(location__is_valid=True)
                order = orders.last()
                order.order -= 1
                order.save()
        if old_location != now_location:
            routing.calculate_distance(instance.route)

        instance.save()

        # delete
        orderitem_ids = [item['id'] for item in validated_data['orderitem_set']]
        for item in instance.orderitem_set.all():
            if item.id not in orderitem_ids:
                item.delete()

        # create or update
        for item in validated_data['orderitem_set']:
            OrderItem(id=item['id'], key=item['key'], value=item['value'], order=instance).save()

        return instance

    class Meta:
        model = Order
        fields = ('id', 'order', 'reference', 'commentary', 'distance', 'duration', 'location', 'orderitem_set')


class RouteSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()
    invalid_orders = serializers.SerializerMethodField()
    vehicle = VehicleSerializer(read_only=True)
    status = serializers.StringRelatedField()

    def get_invalid_orders(self, obj):
        ser = OrderSerializer(many=True, read_only=True)
        return ser.to_representation(obj.orders.filter(location__is_valid=False))

    def get_orders(self, obj):
        ser = OrderSerializer(many=True, read_only=True)
        return ser.to_representation(obj.orders.filter(location__is_valid=True))

    def create(self, validated_data):
        route = Route.objects.create(**validated_data)
        route.vehicle = Vehicle.objects.all()[0]  # todo with until date check
        location = route.vehicle.location
        Order.objects.create(reference='Vehicle location', location=location, route=route, order=0)
        Order.objects.create(reference='Vehicle location', location=location, route=route, order=1)
        route.save()
        return route

    class Meta:
        model = Route
        fields = ('id', 'orders', 'invalid_orders', 'vehicle', 'date', 'status')
