from django.shortcuts import render
from rest_framework import viewsets
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['Post'])
def incoming_data(request):
    token = request.headers.get('CL-X-TOKEN')
    if not token:
        return  Response({'message': 'Un Aunthenticate'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        account = Account.objects.get(app_secret_token = token)
    except Account.DoesNotExist:
        return Response({'message': 'Un Aunthenticate'}, status=status.HTTP_401_UNAUTHORIZED)

    data = request.data
    destinations = account.destinations.all()

    for destination in destinations:
        headers =destination.headers
        url = destination.url
        method = destination.http_method
        if method == 'GET':
            response = requests.get(url, headers=headers, params= data)
        else:
            response = requests.request(method, url, headers=headers, json= data)

    return Response({"message": "Data processed successfully"})


