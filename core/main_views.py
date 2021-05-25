from django.shortcuts import render, redirect
import os
from pathlib import Path
import numpy as np
import json

def neh(request):
    if "instance" in request.session:
        context = {
            "instance": request.session['instance']
        }
        return render(request, "neh.html", context=context)
    else:
        return redirect("/")
