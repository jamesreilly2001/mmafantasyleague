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
      message="You are logged out, to continue log back in!"
      return render(request,"signIn.html", {"messg":message})




def logout(request):
  if 'uid' in request.session:
     try:
       del request.session['uid']
     except KeyError:
       pass
     return render(request, 'logout.html')

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
   database.child("users").child(name).child("details").set(data)
 except:
   message="Unable to create account try again"
   return render(request,"signup.html",{"messg":message})

 return render(request,"signIn.html")

   

def createleague(request): 
    email = request.session.get("email")
    return render(request,"createleague.html",{"email": email})


def postcreateleague(request):
  if 'uid' in request.session:
    id_token = request.session['uid']
    try:
        leaguename = request.POST.get('leaguename')
        uniquecode = request.POST.get('uniquecode')
        owner = request.session.get("email")
        members = [owner]
        data = {"leaguename": leaguename, "owner": owner, "members": members, "uniquecode": uniquecode}
        database.child("leagues").push(data)
        print(uniquecode)
        print(leaguename)
        return redirect('choosefighters',)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
  else:
        message="You are logged out, to continue log back in!"
        return render(request,"signIn.html", {"messg":message})


def joinleague(request): 
    email = request.session.get("email")   
    return render(request,"joinleague.html",{"email": email})



def postjoinleague(request):
  if 'uid' in request.session:
    id_token = request.session['uid']
    try:
        uniquecode = request.POST.get('uniquecode')
        email = request.session.get("email")
        leagues = database.child("leagues").get().val() # get the league information dictionary
        league_found = False
        for key, league in leagues.items():# iterate over the key-value pairs in the dictionary
          print(key)
          if league['uniquecode'] == uniquecode:
            members = league['members']
            members.append(email)
            database.child("leagues").child(key).update({"members": members})
            league_found = True
            break
        if league_found:
          return redirect('choosefighters',)
        else:
          message="The unique code you entered does not match any existing leagues. Please try again or create a new league."
          return render(request, "joinleague.html", {"messg":message})
    except:
        message="Unable to join the league. Please try again later."
        return render(request, "joinleague.html", {"messg":message})
  else:
    message="You are logged out, please log back in to join a league."
    return render(request, "signIn.html", {"messg":message})




def trying(request): 

    return render(request,"trying.html")