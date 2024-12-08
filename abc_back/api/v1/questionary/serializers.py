from __future__ import annotations

from rest_framework import serializers

from abc_back.questionary.models import AboutMe, GiftCertificateOrder, Question


class AboutMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutMe
        fields = ["id", "fio", "email", "phone", "address", "about_yourself", "created_at"]
        read_only_fields = ["id", "created_at"]


class GiftCertificateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCertificateOrder
        fields = ["id", "buyer_fio", "buyer_email", "addressee_name", "summa", "addressee_message", "created_at"]
        read_only_fields = ["id", "created_at"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "name", "email", "question", "created_at"]
        read_only_fields = ["id", "created_at"]
