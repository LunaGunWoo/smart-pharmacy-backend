from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from . import serializers
from .models import Medicine
from reviews.serializers import ReviewSerializer
from reviews.models import Review


class Medicines(APIView):

    def get(self, request):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = settings.PAGE_SIZE
            start = (page - 1) * page_size
            end = start + page_size
            medicines = Medicine.objects.all()[start:end]
            serializer = serializers.MedicineTinySerializer(
                medicines,
                many=True,
            )
        except:
            return redirect(f"{request.path}?page=1")
        return Response(serializer.data)


class MedicineDetail(APIView):

    def get_object(self, pk):
        try:
            return Medicine.objects.get(pk=pk)
        except Medicine.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        medicine = self.get_object(pk)
        serializer = serializers.MedicineDetailSerializer(medicine)
        return Response(serializer.data)


class MedicineReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Medicine.objects.get(pk=pk)
        except Medicine.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
            page_size = settings.PAGE_SIZE
            start = (page - 1) * page_size
            end = start + page_size
            all_reviews = Review.objects.all()[start:end]
            medicine = self.get_object(pk)
            serializer = serializers.ReviewSerializer(
                all_reviews,
                many=True,
            )
        except:
            return redirect(f"{request.path}?page=1")
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
            )
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

    def push_test(self, request):
        pass
