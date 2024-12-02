from rest_framework import serializers

from abc_back.pages.models import AboutUs, Delivery, GiftCertificate


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class GiftCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCertificate
        fields = "__all__"
