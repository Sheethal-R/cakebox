from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib.auth.models import User
from myapp.models import Cakebox
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages



class CakeForm(forms.ModelForm):
    class Meta:
        model= Cakebox
        fields='__all__'
        widgets={
                
                "name":forms.TextInput(attrs={"class":"form-control"}),
                "flavour":forms.TextInput(attrs={"class":"form-control"}),
                "price":forms.NumberInput(attrs={"class":"form-control"}),
                "shape":forms.TextInput(attrs={"class":"form-control"}),
                "weight":forms.NumberInput(attrs={"class":"form-control"}),
                "image":forms.FileInput(attrs={"class":"form-control"}),
                "layer":forms.NumberInput(attrs={"class":"form-control"})
                 }

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=User       
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={"first_name":forms.TextInput(attrs={"class":"form-control"}),
                 "last_name":forms.TextInput(attrs={"class":"form-control"}),
                 "email":forms.EmailInput(attrs={"class":"form-control"}),
                 "username":forms.TextInput(attrs={"class":"form-control"}),
                "password1":forms.PasswordInput(attrs={"class":"form-control"}) 
                }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

   
class CakeboxCreateView(View):
    def get(self,request,*args,**kwargs):
        form=CakeForm()
        return render(request,"cake-add.html",{"form":form})
   
    def post(self,request,**kwargs):
        form=CakeForm(data=request.POST,files=request.FILES)
        if form.is_valid():
           print(form.cleaned_data)
           Cakebox.objects.create(**form.cleaned_data)
           messages.success(request,"cake has been credited successfully")

           return redirect("cake-list")
        messages.error(request,"failed to create todo")
        return render(request,"cake-add.html",{"form":form})

class CakeboxListView(View):
    def get(self,request,*args,**kwargs):
        qs=Cakebox.objects.all()
        return render(request,"cake-list.html",{"cakes":qs})

class  CakeboxDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakebox.objects.get(id=id)
        return render(request,"cake-detail.html",{"cakes":qs})
         

class CakeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ca=Cakebox.objects.get(id=id)
        form=CakeForm(instance=ca)
        messages.success(request,"cake has been changed")
        return render(request,"cake-edit.html",{"form":form}) 
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        ca=Cakebox.objects.get(id=id)
        form=CakeForm(instance=ca,data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect("cake-detail",pk=id)
        return render(request,"cake-edit.html",{"form":form})  

    
class CakeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Cakebox.objects.get(id=id).delete()
        messages.success(request,"cake has been removed successfully")
        return redirect("cake-list")
    

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"account has been created successfully")
            return redirect("signin")
            return render(request,"register.html",{"form":form})
    
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            
            if usr:
                login(request,usr)
                return redirect("cake-list")
        return render(request,"login.html",{"form":form})    

def signout_view(request,*args,**kwargs): 
    logout(request)
    return redirect("signin")         
