from __future__ import annotations

from rest_framework import serializers

from abc_back.pages.models import AboutUs, Contact, Delivery, GiftCertificate


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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
