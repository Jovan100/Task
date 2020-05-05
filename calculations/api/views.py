from rest_framework.viewsets import ViewSet
from calculations.api.serializers import CalculationsSerializer
from calculations.models import Calculations
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status

class AddView(ViewSet):

    def add(self, request, numbers):
        if isinstance(request.data['num'], int):
            numbers.append(request.data['num'])
        elif isinstance(request.data['num'], str):
            nums = [int(x) for x in request.data['num'].split(',')]
            numbers.extend(nums)
        request.session['numbers'] = numbers

    def create(self, request, *args, **kwargs):
        try:
            numbers = request.session['numbers']
            self.add(request, numbers)
        except KeyError:
            numbers = []
            self.add(request, numbers)

        return Response(data=request.session['numbers'], status=status.HTTP_201_CREATED)


class CalculateView(ViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            calc = sum(request.session['numbers'])
            calculations = request.session['calculations']
            calculations.append(calc)
            request.session['calculations'] = calculations
            return Response(data=calc, status=status.HTTP_201_CREATED)
        except KeyError:
            try:
                calc = sum(request.session['numbers'])
                request.session['calculations'] = [calc]
                return Response(data=calc, status=status.HTTP_201_CREATED)
            except KeyError:
                message = 'There are no numbers.'
                return Response(data=message, status=status.HTTP_404_NOT_FOUND)

    def list(self, request, all=None, **kwargs):
        if all == 'all':
            try:
                return Response(data=request.session['calculations'], status=status.HTTP_200_OK)
            except KeyError:
                message = 'There are no calculations.'
                return Response(data=message, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ResetView(ViewSet):
    def create(self, request, *args, **kwargs):
        try:
            data = {}
            data['numbers'] = request.session['numbers']
            try:
                data['calculations'] = request.session['calculations']
            except KeyError:
                data['calculations'] = []
            serialized = CalculationsSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                del request.session['numbers']
                del request.session['calculations']
                return Response(data=serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            message = 'There are no numbers to add.'
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class HistoryView(ViewSet):
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Calculations.objects.all()
        history = get_object_or_404(queryset, pk=pk)
        serialized = CalculationsSerializer(history)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = Calculations.objects.all()
        serialized = CalculationsSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
