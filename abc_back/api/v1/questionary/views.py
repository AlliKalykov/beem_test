from __future__ import annotations

from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from abc_back.api.pagination import DefaultPageNumberPagination
from abc_back.api.views import MultiSerializerViewSetMixin
from abc_back.questionary.models import AboutMe, GiftCertificateOrder, Question

from .serializers import AboutMeSerializer, GiftCertificateOrderSerializer, QuestionSerializer


class AboutMeViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
):
    queryset = AboutMe.objects.none()
    pagination_class = DefaultPageNumberPagination

    serializer_classes = {
        "list": AboutMeSerializer,
        "create": AboutMeSerializer,
    }

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        about_me = serializer.save()
        user_about_me = request.session.get("about_me", [])
        user_about_me.append(about_me.id)
        request.session["about_me"] = user_about_me
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request, *args, **kwargs):
        user_about_me = request.session.get("about_me", [])
        about_me = AboutMe.objects.filter(pk__in=user_about_me)
        page = self.paginate_queryset(about_me)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(about_me, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GiftCertificateOrderViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
):
    queryset = GiftCertificateOrder.objects.none()
    pagination_class = DefaultPageNumberPagination

    serializer_classes = {
        "list": GiftCertificateOrderSerializer,
        "create": GiftCertificateOrderSerializer,
    }

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gift_certificate_order = serializer.save()
        user_gift_certificate_order = request.session.get("gift_certificate_order", [])
        user_gift_certificate_order.append(gift_certificate_order.id)
        request.session["gift_certificate_order"] = user_gift_certificate_order
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request, *args, **kwargs):
        user_gift_certificate_order = request.session.get("gift_certificate_order", [])
        gift_certificate_order = GiftCertificateOrder.objects.filter(pk__in=user_gift_certificate_order)
        page = self.paginate_queryset(gift_certificate_order)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(gift_certificate_order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionViewSet(
    MultiSerializerViewSetMixin, viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
):
    queryset = Question.objects.none()
    pagination_class = DefaultPageNumberPagination

    serializer_classes = {
        "list": QuestionSerializer,
        "create": QuestionSerializer,
    }

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = serializer.save()
        user_question = request.session.get("question", [])
        user_question.append(question.id)
        request.session["question"] = user_question
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request: Request, *args, **kwargs):
        user_question = request.session.get("question", [])
        question = Question.objects.filter(pk__in=user_question)
        page = self.paginate_queryset(question)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
