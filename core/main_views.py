from django.shortcuts import render, redirect
import os
from pathlib import Path
import pandas as pd
import numpy as np
import json
from core.opt.loader import loader
from core.opt.neh import neh
from core.opt.Chen import Chen
from core.opt.bb import bb
from core.opt.ts import tabu_search
from core.opt.AG import AG
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
                nb_machines = shape[0]
                if  machines_in_rows:
                    nb_jobs = shape[0]
                    nb_machines = shape[1]
                start =time.time()
                result =neh(loaded_instance,nb_jobs,nb_machines)
                end = time.time()
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[2]
                context["chart_data"] = json.dumps(result[1].tolist())
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
                loaded_instance = read_instance(instance)
                shape = loaded_instance.shape
                start =time.time()
                result =Chen(loaded_instance)
                end = time.time()
                results = format_result(result[0],loaded_instance)    
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(results.tolist())
            return render(request, "chen.html", context=context)
        else:
            return redirect("/")

def format_result(sol,data):
    results = np.zeros((data.shape[0],data.shape[1]+1),dtype=int)
    # formatting the result 
    for idx in range(len(sol)):
        results[idx] = data.iloc[sol[idx]].append(pd.Series([sol[idx]]))
    return results

def read_instance(instance):
    machines_in_rows = False        
    instance_info = json.loads(open(f"{BASE_DIR}/user_data/{instance}.json",'r').read())
    if instance_info['instance_structure'] !="jobs-machines":
        machines_in_rows = True                 
    loaded_instance = loader(f"{BASE_DIR}/user_data/{instance}.txt",machines_in_rows=machines_in_rows)
    return loaded_instance

def breach_and_bounds_view(request):
    if request.method =="GET":
        if "instance" in request.session:
            instance = request.session['instance']
            context = {
                "instance": instance
            }
            start = request.GET.get("start", None)
            if start:
                loaded_instance = read_instance(instance)
                shape = loaded_instance.shape
                start =time.time()
                result =bb(loaded_instance)
                end = time.time()
                results = format_result(result[0],loaded_instance)    
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(results.tolist())
            return render(request, "bb.html", context=context)
        else:
            return redirect("/")
def tabu_search_view(request):
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
                nb_machines = shape[0]
                if  machines_in_rows:
                    nb_jobs = shape[0]
                    nb_machines = shape[1]
                start =time.time()
                result =tabu_search(loaded_instance,3,nb_jobs,nb_machines)
                end = time.time()
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(result[0].tolist())
            return render(request, "tabu_search.html", context=context)
        else:
            return redirect("/")

def ag_view(request):
    if request.method =="GET":
        if "instance" in request.session:
            instance = request.session['instance']
            context = {
                "instance": instance
            }
            start = request.GET.get("start", None)
            if start:
                loaded_instance = read_instance(instance)
                shape = loaded_instance.shape
                start =time.time()
                result =AG(loaded_instance)
                end = time.time()
                results = format_result(result[0],loaded_instance)    
                context["execution_time"] = round(end-start,3)
                context['makespan'] = result[1]
                context["chart_data"] = json.dumps(results.tolist())
            return render(request, "ag.html", context=context)
        else:
            return redirect("/")