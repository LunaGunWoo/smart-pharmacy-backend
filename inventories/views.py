from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from medicines.models import Medicine
from receipts.models import Receipt, PastMedicine
from .serializers import InventorySerializer
from .models import Inventory


class Inventories(APIView):
    permission_classes = [IsAuthenticated]

    def get_medicine(self, pk):
        try:
            return Medicine.objects.get(pk=pk)
        except Medicine.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request):
        my_inventories = Inventory.objects.filter(owner=request.user)
        serializer = InventorySerializer(
            my_inventories,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            medicine_pk = request.data.get("medicine")
            if medicine_pk:
                try:
                    medicine_pk = int(medicine_pk)
                except:
                    raise exceptions.ParseError
            else:
                return Response(
                    {"medicine": ["이 필드는 필수 항목입니다."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            medicine = self.get_medicine(medicine_pk)
            inventory = serializer.save(
                medicine=medicine,
                owner=request.user,
            )
            serializer = InventorySerializer(inventory)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class InventoriesPurchase(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_inventories = Inventory.objects.filter(owner=request.user)
        receipt = Receipt.objects.create(owner=request.user)
        for my_inventory in my_inventories:
            receipt.past_medicine.add(
                PastMedicine.objects.create(
                    receipt=receipt,
                    medicine=my_inventory.medicine,
                    quantity=my_inventory.quantity,
                    price_per_medicine_at_purchase=my_inventory.medicine.price,
                )
            )
            my_inventory.delete()
        return Response(status=status.HTTP_200_OK)


class InventoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise exceptions.NotFound

    def put(self, request, pk):
        inventory = self.get_object(pk)
        if inventory.owner != request.user:
            raise exceptions.PermissionDenied
        serializer = InventorySerializer(
            inventory,
            data=request.data,
        )
        if serializer.is_valid():
            inventory = serializer.save()
            serializer = InventorySerializer(inventory)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        inventory = self.get_object(pk)
        if inventory.owner != request.user:
            raise exceptions.PermissionDenied
        inventory.delete()
        return Response(status=status.HTTP_200_OK)
