from django.shortcuts import render, redirect
import os
from pathlib import Path
import numpy as np
import json


BASE_DIR = Path(__file__).resolve().parent

# Create your views here.
def  index(request):
    return render(request, "index.html")

def create_instance(request):
    if request.method=="POST":
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        instance_name = request.POST.get("instance_name","").replace(" ", "-")
        instance_data = request.POST.get("instance_data","")
        instance_structure = request.POST.get("instance_structure","jobs-machines")

        json_file = f"{BASE_DIR}/user_data/{instance_name}.json"

        with open(f"{BASE_DIR}/user_data/{instance_name}.txt", 'w') as data_file:
            data_file.write(instance_data)

        # fill the metadata file 
        metadata = {
            'instance_structure': instance_structure,
            'instance_name': instance_name,
            'type':'CREATED'
        }
        
        with open(json_file, 'w') as destination:
            destination.write(json.dumps(metadata))
        
        request.session['instance'] = instance_name
        return redirect("/main")

def main(request):
    if "instance" in request.session:
        context = {
            "instance": request.session['instance']
        }
        return render(request, "main.html", context=context)
    else:
        return redirect("/")


def generate_instance(request):
    if request.method =="POST":
        # get params 
        instance_name = request.POST.get("instance_name","").replace(" ", "-")
        jobs_num = int(request.POST.get("jobs_num",10))
        machines_num = int(request.POST.get("machines_num",10))
        instance_structure = request.POST.get("instance_structure","jobs-machines")
        generation_method = request.POST.get("generation_method","uniform")
        
        data_file =f"{BASE_DIR}/user_data/{instance_name}.txt" 
        json_file = f"{BASE_DIR}/user_data/{instance_name}.json"


        if instance_structure=="jobs-machines":
            shape = (jobs_num,machines_num)
        else:
            shape = (machines_num,jobs_num)
        if generation_method=="uniform":
            instance = np.random.random_integers(5,80,shape)
        np.savetxt(data_file,instance,delimiter=" ", fmt="%d")

        # fill the metadata file 
        metadata = {
            'instance_structure': instance_structure,
            'instance_name': instance_name,
            'type':'GENERATED'
        }
        
        with open(json_file, 'w') as destination:
            destination.write(json.dumps(metadata))

        request.session['instance'] = instance_name
        return redirect("/main")
    else:
        return redirect("/")

def select_instance(request):
    if request.method == 'POST':
        instance_name = request.POST.get("instance_name","").replace(" ", "-")
        instance_structure = request.POST.get("instance_structure","jobs-machines")
        data_file =f"{BASE_DIR}/user_data/{instance_name}.txt"
        json_file = f"{BASE_DIR}/user_data/{instance_name}.json"

        file = request.FILES['instance']
        with open(data_file, 'w') as destination:
            for chunk in file.chunks():
                destination.write(chunk.decode('utf-8'))
        
        # fill the metadata file 
        metadata = {
            'instance_structure': instance_structure,
            'instance_name': instance_name,
            'type':'UPLOADED'
        }

        
        with open(json_file, 'w') as destination:
            destination.write(json.dumps(metadata))

        request.session['instance'] = instance_name
        return redirect("/main")
    else:
        return redirect("/")

def logout(request):
    if request.method =="GET":
        if "instance" in request.session:
            instance =  request.session['instance']
            data_file =f"{BASE_DIR}/user_data/{instance}.txt"
            json_file = f"{BASE_DIR}/user_data/{instance}.json"
            os.remove(json_file)
            os.remove(data_file)
            del request.session["instance"]
            return redirect("/")
        else:
            return redirect("/")