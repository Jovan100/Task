from rest_framework.viewsets import ViewSet
from calculation.api.serializers import CalculationsSerializer
from calculation.models import Calculations
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
import array as arr

class AddView(ViewSet):
    def add(self, request, numbers):
        if isinstance(request.data['num'], int):
            numbers.append(request.data['num'])
        elif isinstance(request.data['num'], str):
            numbers.extend(list(map(int, request.data['num'].split(','))))
        else:
            numbers.extend(request.data['num'])
        request.session['numbers'] = numbers

    def create(self, request, *args, **kwargs):
        try:
            numbers = request.session['numbers']
            self.add(request, numbers)
        except (KeyError, AttributeError):
            numbers = []
            self.add(request, numbers)

        return Response(status=201)


class CalculateView(ViewSet):
    def retrieve(self, request, *args, **kwargs):
        try:
            calc = sum(request.session['numbers'])
            calculations = request.session['calculations']
            calculations.append(calc)
            request.session['calculations'] = calculations
            return Response(data=calc, status=201)
        except KeyError:
            try:
                calc = sum(request.session['numbers'])
                request.session['calculations'] = [calc]
                return Response(data=calc, status=201)
            except:
                message = 'There are no numbers.'
                return Response(data=message, status=404)

    def list(self, request, all=None, **kwargs):
        if all == 'all':
            try:
                return Response(data=request.session['calculations'], status=200)
            except KeyError:
                message = 'There aro no calculations.'
                return Response(data=message, status=404)
        else:
            return Response(status=400)

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
                return Response(data=serialized.data, status=201)
            else:
                return Response(status=400)
        except KeyError:
            message = 'There are no numbers to add.'
            return Response(data=message, status=400)

class HistoryView(ViewSet):
    def retrieve(self, request, pk=None, **kwargs):
        queryset = Calculations.objects.all()
        history = get_object_or_404(queryset, pk=pk)
        serialized = CalculationsSerializer(history)
        return Response(serialized.data, status=200)

    def list(self, request, *args, **kwargs):
        queryset = Calculations.objects.all()
        serialized = CalculationsSerializer(queryset, many=True)
        return Response(serialized.data, status=200)
