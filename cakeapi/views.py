from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from myapp.models import Cakebox
from rest_framework import serializers
from rest_framework.decorators import action
 

class CakeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Cakebox
       # exclude=("id",)
        fields='__all__'


class CakeView(ViewSet):
    #localhost:8000/api/
    def list(self,request,*args,**kwargs):
        qs=Cakebox.objects.all()

        if "flavour" in request.query_params:
            fla=request.query_params.get("flavour")
            qs=qs.filter(flavour=fla)

        if "shape" in request.query_params:
            sha=request.query_params.get("shape")
            qs=qs.filter(shape=sha)    

        if "price" in request.query_params:
            pri=request.query_params.get("price")
            qs=qs.filter(price=pri)
            
        #deserialization
        serializer=CakeSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    def create(self,request,*args,**kwargs):
        #serialization
        serializer=CakeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakebox.objects.get(id=id)
        serializer=CakeSerializer(qs)
        return Response(data=serializer.data)
    

    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake_obj=Cakebox.objects.get(id=id)
        serializer=CakeSerializer(instance=cake_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    
    def destroy(self,request,*args,**kwargs):
    
        id=kwargs.get("pk")
        try:
            Cakebox.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")
        

    @action(methods=["get"],detail=False)
    def flavour(self,request,*args,**kwargs):
        qs=Cakebox.objects.all().values_list("flavour",flat=True).distinct()
        return Response(data=qs)
    


