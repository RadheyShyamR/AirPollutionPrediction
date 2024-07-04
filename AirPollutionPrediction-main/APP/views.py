from django.shortcuts import render, redirect
from . models import UserPersonalModel
from . forms import UserPersonalForm, UserRegisterForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
import numpy as np
import joblib


def Landing_1(request):
    return render(request, '1_Landing.html')

def Register_2(request):
    form = UserRegisterForm()
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created. ' + user)
            return redirect('Login_3')

    context = {'form':form}
    return render(request, '2_Register.html', context)


def Login_3(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home_4')
        else:
            messages.info(request, 'Username OR Password incorrect')

    context = {}
    return render(request,'3_Login.html', context)

def Home_4(request):
    return render(request, '4_Home.html')

def Teamates_5(request):
    return render(request,'5_Teamates.html')

def Domain_Result_6(request):
    return render(request,'6_Domain_Result.html')

def Problem_Statement_7(request):
    return render(request,'7_Problem_Statement.html')
    

def Per_Info_8(request):
    if request.method == 'POST':
        fieldss = ['firstname','lastname','age','address','phone','city','state','country']
        form = UserPersonalForm(request.POST)
        if form.is_valid():
            print('Saving data in Form')
            form.save()
        return render(request, '4_Home.html', {'form':form})
    else:
        print('Else working')
        form = UserPersonalForm(request.POST)    
        return render(request, '8_Per_Info.html', {'form':form})
    
Model = joblib.load('C:/Users/jayak/OneDrive/Desktop/Air Pollution with Diseases/ITPML14-FINAL CODING/DEPLOYMENT_3_ML/PROJECT/APP/RFC1.pkl')
# to change
    #"C:\Users\jayak\OneDrive\Desktop\Air Pollution with Diseases\ITPML14-FINAL CODING\DEPLOYMENT_3_ML\PROJECT\APP\RFC1.pkl"
def Deploy_9(request): 
    if request.method == "POST":
        int_features = [x for x in request.POST.values()]
        int_features = int_features[1:]
        print(int_features)
        final_features = [np.array(int_features, dtype=object)]
        print(final_features)
        prediction = Model.predict(final_features)
        print(prediction)
        output = prediction[0]
        print(output)
        if output == 0:
            return render(request, 'result.html', {"prediction_text":"Good:AQI Range: 0-50 Air Quality: Air is considered satisfactory, and air pollution poses little or no risk. This level is generally safe for all individuals."})
        elif output == 1:
            return render(request, 'result.html', {"prediction_text":"Moderate:AQI Range: 51-100 Description: Air quality is acceptable, but sensitive individuals may experience minor health effects.Potential Diseases:1.Respiratory 2.infections Aggravation of 3.asthma Bronchitis"})
        elif output == 2:
            return render(request, 'result.html', {"prediction_text":"Poor:AQI Range: 201-300 Description: Health alert; everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects.Potential Diseases:1.Exacerbation of asthma 2.Increased risk of respiratory infections 3.Aggravation of cardiovascular diseases 4.Reduced lung function"})
        elif output == 3:
            return render(request, 'result.html', {"prediction_text":"Satisfactory:AQI Range: 101-200 Description: Air quality is still acceptable, but there may be a moderate health concern, especially for sensitive individuals Potential Diseases:Increased risk of respiratory infections Aggravation of chronic respiratory diseases (e.g., chronic obstructive pulmonary disease or COPD)Cardiovascular diseases (in susceptible individuals)"})
        elif output == 4:
            return render(request, 'result.html', {"prediction_text":"Poor (201-300 AQI):Description: Health alert: everyone may experience more serious health effects.Potential Diseases:Severe health effects for the entire population.Increased risk of respiratory infections.Aggravation of chronic respiratory diseases (e.g., chronic obstructive pulmonary disease or COPD).Cardiovascular diseases in susceptible individuals.Precautions: Everyone should avoid prolonged outdoor exertion, and sensitive groups should avoid outdoor activities"})
        elif output == 5:
            return render(request, 'result.html', {"prediction_text":"Description: Health warnings of emergency conditions; the entire population is more likely to be affected.Potential Diseases:Severe health effects for everyone.Increased risk of respiratory infections.Aggravation of chronic respiratory diseases.Cardiovascular diseases in susceptible individuals.Precautions: Everyone should avoid any outdoor exertion, and sensitive groups should remain indoors. The air quality is hazardous, and measures should be taken to protect against prolonged exposure"})

    else:
        return render(request, '9_Deploy.html')


def Per_Database_10(request):
    models = UserPersonalModel.objects.all()
    return render(request, '10_Per_Database.html', {'models':models})


def Logout(request):
    logout(request)
    return redirect('Landing_1')
