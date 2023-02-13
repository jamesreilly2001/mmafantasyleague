from django.shortcuts import render, redirect
import pyrebase
from MMAfantasy import models
from django.contrib import auth

config ={
  'apiKey': "AIzaSyD-_zfDFYhcZUDpTTaKS7I0YJahMaqiCLs",
  'authDomain': "mma-fantasy-league-94b6e.firebaseapp.com",
  'projectId': "mma-fantasy-league-94b6e",
  'storageBucket': "mma-fantasy-league-94b6e.appspot.com",
  'messagingSenderId': "837434946169",
  'appId': "1:837434946169:web:7a0210a7c523225e629aa8",
  'measurementId': "G-DRKKN38R7H",
  'databaseURL': "https://mma-fantasy-league-94b6e-default-rtdb.firebaseio.com/",
}

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()

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
  request.session['email'] = email
  request.session.save()
  
  print(email)

  
  return render(request, "welcome.html",{"e":email})


def choosefighters(request):
    if 'uid' in request.session:
       id_token = request.session['uid']

       try:
           email = request.session.get("email")
           print(email)
           return render(request, "choosefighters.html", {"email": email})
       except Exception as e:
           print(str(e))
           return redirect('signIn')
       else:
           return redirect('signIn')




def logout(request):
  try:
    del request.session['uid']
  except KeyError:
    pass
  return render(request, 'signin.html')

def signUp(request):

  return render(request, "signUp.html")

def postsignup(request):
 
 name=request.POST.get('name')
 email=request.POST.get('email')
 passw=request.POST.get('pass')
 
 try:
   user=authe.create_user_with_email_and_password(email,passw)
   uid = user['localId']
   data={"name":name,"status":"1"}
   database.child("users").child(uid).child("details").set(data)
 except:
   message="Unable to create account try again"
   return render(request,"signup.html",{"messg":message})

 return render(request,"signIn.html")


def createleague(request):
    if 'uid' in request.session:
        id_token = request.session['uid']
        try:
            email = request.session.get("email")
            print(email)
            return render(request, "createleague.html", {"email": email})
        except Exception as e:
            print(str(e))
            return redirect('signIn')
    else:
        return redirect('signIn')

def post_create_league(request):
    name = request.POST.get('name')
    owner = request.session['uid']
    members = [owner]
    data = {"name": name, "owner": owner, "members": members}
    database.child("leagues").push(data)
    return redirect('choosefighters')

def joinleague(request):
    if 'uid' in request.session:
        id_token = request.session['uid']
        try:
            email = request.session.get("email")
            print(email)
            leagues = database.child("leagues").get().val()
            return render(request, "joinleague.html",{"email": email} )
        except Exception as e:
            print(str(e))
            return redirect('signIn')
    else:
        return redirect('signIn')

def post_join_league(request):
    league_id = request.POST.get('league_id')
    user = request.session['uid']
    league = database.child("leagues").child(league_id).get().val()
    league["members"].append(user)
    database.child("leagues").child(league_id).set(league)
    return redirect('choosefighters')
