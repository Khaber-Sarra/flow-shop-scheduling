from django.shortcuts import render, redirect
import os
from pathlib import Path
import numpy as np
import json
from .opt.loader import loader
from .opt.neh import neh
from .opt.Chen import Chen
import time

BASE_DIR = Path(__file__).resolve().parent

def neh_view(request):
    if request.method =="GET":
        if "instance" in request.session:
            instance = request.session['instance']
            context = {
                "instance": instance
            }
            start = request.GET.get("start", None)
            if start:
                machines_in_rows = False        
                instance_info = json.loads(open(f"{BASE_DIR}/user_data/{instance}.json",'r').read())
                if instance_info['instance_structure'] !="jobs-machines":
                    machines_in_rows = True                 
                loaded_instance = loader(f"{BASE_DIR}/user_data/{instance}.txt",machines_in_rows=machines_in_rows)
                shape = loaded_instance.shape
                nb_jobs = shape[1]
                if  machines_in_rows:
                    nb_jobs = shape[0]  
                start =time.time()
                result =neh(loaded_instance,nb_jobs)
                end = time.time()
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(result[0].tolist())
            return render(request, "neh.html", context=context)
        else:
            return redirect("/")

def chen_view(request):
    if request.method =="GET":
        if "instance" in request.session:
            instance = request.session['instance']
            context = {
                "instance": instance
            }
            start = request.GET.get("start", None)
            if start:
                machines_in_rows = False        
                instance_info = json.loads(open(f"{BASE_DIR}/user_data/{instance}.json",'r').read())
                if instance_info['instance_structure'] !="jobs-machines":
                    machines_in_rows = True                 
                loaded_instance = loader(f"{BASE_DIR}/user_data/{instance}.txt",machines_in_rows=machines_in_rows)
                shape = loaded_instance.shape
                nb_jobs = shape[1]
                if  machines_in_rows:
                    nb_jobs = shape[0]  
                start =time.time()
                result =neh(loaded_instance,nb_jobs)
                end = time.time()
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(result[0].tolist())
            return render(request, "neh.html", context=context)
        else:
            return redirect("/")

