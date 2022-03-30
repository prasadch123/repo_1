from django.shortcuts import render,redirect
import pickle
import numpy as np
import joblib
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login

# Load the Random Forest CLassifier model
#filename = 'diabetes-prediction-rfc-model.pkl'#
#classifier = pickle.load(open(filename, 'rb'))

def register_view(request):
        form = CreateUserForm()
        context = {'form': form}
        if request.method == "POST":
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        return render(request,'register.html',context)


def login_view(request):
        if request.method=="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')


def home(request):
	return render(request,'index.html')


def predict(request):
    if request.method == "POST":
        classifier=joblib.load('finalized_model.sav')

        preg = int(request.POST.get('pregnancies'))
        glucose = int(request.POST.get('glucose'))
        bp = int(request.POST.get('bloodpressure'))
        st = int(request.POST.get('skinthickness'))
        insulin = int(request.POST.get('insulin'))
        bmi = float(request.POST.get('bmi'))
        dpf = float(request.POST.get('dpf'))
        age = int(request.POST.get('age'))
        
        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        my_prediction = classifier.predict(data)
        
        return render(request,'result.html', {'prediction':my_prediction})


def index(request):
    return render(request,'index2.html')




