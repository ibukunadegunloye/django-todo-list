from django.shortcuts import render, redirect 
from .models import List
from .forms import ListForm
from django.contrib import messages
from .serializers import TodoSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)

        if form.is_valid():
            form.save()
            all_items = List.objects.all
            messages.success (request, ('Item has been successfully added to List!'))
            return render(request, 'home.html', {'all_items':all_items})

    else:
        all_items = List.objects.all
        return render(request, "home.html", {'all_items':all_items})


def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success (request, ('Item has been deleted!'))
    return redirect(home)


def cross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect(home)



def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect(home)


def edit(request, list_id):
    if request.method == 'POST':
        item = List.objects.get()
        form = ListForm(request.POST or None)

        if form.is_valid():
            form.save()
            all_items = List.objects.all
            messages.success (request, ('Item has been successfully added to List!'))
            return render(request, 'home.html', {'all_items':all_items})

    else:
        all_items = List.objects.all
        return render(request, "home.html", {'all_items':all_items})

# API views
@api_view(['GET','POST'])
def getlist(request):
    if request.method == 'GET':
        item = List.objects.all()
        serializer = TodoSerializer(item, many=True)  
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def getlistdetail(request, id):

    try:
        item = List.objects.get(pk=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = TodoSerializer(item) 
        return Response(serializer.data)
        
    elif request.method == 'PUT':
        serializer = TodoSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

