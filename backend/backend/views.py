from django.shortcuts import render

import pyrebase
from django.contrib import auth 

config ={
  'apiKey': "AIzaSyD-_zfDFYhcZUDpTTaKS7I0YJahMaqiCLs",
  'authDomain': "mma-fantasy-league-94b6e.firebaseapp.com",
  'projectId': "mma-fantasy-league-94b6e",
  'storageBucket': "mma-fantasy-league-94b6e.appspot.com",
  'messagingSenderId': "837434946169",
  'appId': "1:837434946169:web:7a0210a7c523225e629aa8",
  'measurementId': "G-DRKKN38R7H",
  'databaseURL': "",
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()

def signIn(request): 

    return render(request,"signIn.html")

def postsign(request):
  email = request.POST.get('email')
  passw = request.POST.get("pass")
  try: 
    user = authe.sign_in_with_email_and_password(email,passw)
  except:
    message="Invalid Credentials."
    return render(request,"signIn.html", {"messg":message})
  print(user['idToken'])
  session_id=user['idToken']
  request.session['uid']=str(session_id)
  return render(request, "welcome.html",{"e":email})

def logout(request):
  auth.logout(request)
  return render(request, 'signin.html')

def signUp(request):

  return render(request, "signUp.html")
