from django.shortcuts import render, redirect
import os
from pathlib import Path
# Create your views here.
def  index(request):
    return render(request, "index.html")
def create_instance(request):
    if request.method=="POST":
        # Build paths inside the project like this: BASE_DIR / 'subdir'.
        BASE_DIR = Path(__file__).resolve().parent
        instance_name = request.POST.get("instance_name","").replace(" ", "-")
        instance_data = request.POST.get("instance_data","")
        with open(f"{BASE_DIR}/data/{instance_name}.txt", 'w') as data_file:
            data_file.write(instance_data)
            request.session['instance'] = instance_name
        return redirect("/main")
def main(request):
    if "instance" in request.session:
        context = {
            "instance": request.session['instance']
        }
    return render(request, "main.html", context=context)