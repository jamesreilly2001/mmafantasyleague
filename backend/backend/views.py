from django.shortcuts import render, redirect
import pyrebase

from firebase_admin import auth
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse



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

def postsignup(request):
 
 name=request.POST.get('name')
 email=request.POST.get('email')
 passw=request.POST.get('pass')
 
 
 try:
   user=authe.create_user_with_email_and_password(email,passw)
   uid = user['localId']
   unique_name = str(name)
   data={"name":name,"email":email,"status":"1"}
   encoded_email = email.replace('.', ',')
   database.child("users").child(encoded_email).child("details").set(data)
   request.session['name'] = name
   request.session['email'] = email
   print(name)
   request.session.save()
   

 except: 
   message="Unable to create account try again"
   return render(request,"signup.html",{"messg":message})

 return render(request,"signIn.html")

def signIn(request): 

    return render(request,"signIn.html")

def logout(request):
    if 'uid' in request.session:
        email = request.session.get('email')
        print(f"User ID in session: {request.session['uid']}")
        print(email)
        request.session.clear()  # clear the session
        print(f"User ID in session after clearing: {request.session.get('uid')}")
        print(email)
        messages.success(request, "You have been logged out.")
    else:
        messages.warning(request, "You were not logged in.")
    return redirect('signIn')

def signUp(request):

  return render(request, "signUp.html")

def home(request): 
  if 'uid' in request.session:
    return render(request,"welcome.html")
  else:
    message="You are logged out"
    return render(request,"signIn.html", {"messg":message})


def postsign(request):
  email = request.POST.get('email')
  passw = request.POST.get("pass")

  try: 
    user = authe.sign_in_with_email_and_password(email,passw)
    
  except:
    message="Invalid Credentials."
    return render(request,"signIn.html", {"messg":message})
  session_id=user['idToken']
  request.session['uid']=str(session_id)
  request.session['email'] = email
  request.session['name'] = user['displayName']  # <--- add this line
  print(user['displayName'])
  return render(request, "welcome.html", {"e":email})


# Define the view for the UFC Fight Night form
def choosefighters(request):
  
  return render(request, "choosefighters.html")


def save_choices(request):
    if 'uid' in request.session:
        name=request.session.get('name')
        email=request.session.get('email')
        encoded_email = email.replace('.', ',')
        print(name)
        print(email)
        print
        if request.method == 'POST':
            andradre_blanchfield = request.POST.get('andradre-blanchfield')
            wright_pauga = request.POST.get('wright-pauga')
            parisian_pogues = request.POST.get('parisian-pogues')
            knight_prachnio = request.POST.get('knight-prachnio')
            miller_hernandez = request.POST.get('miller-hernandez')
            sadykhov_elder = request.POST.get('sadykhov-elder')
            lansberg_silva = request.POST.get('lansberg-silva')
            emmers_askhabov = request.POST.get('emmers-askhabov')
            preux_lins = request.POST.get('preux-lins')
            fletcher_gorimbo = request.POST.get('fletcher-gorimbo')
            carpenter_ronderos = request.POST.get('carpenter-ronderos')
            # Check if all fighters have been selected
            if '' in [andradre_blanchfield, wright_pauga, parisian_pogues, knight_prachnio, miller_hernandez, sadykhov_elder, lansberg_silva, emmers_askhabov, preux_lins, fletcher_gorimbo, carpenter_ronderos]:
                message = "Please select fighters for all fights"
                return render(request, "choosefighters.html", {"messg": message})
            else:
                # Save the selected fighters to the database
                data={
                    'andradre-blanchfield': andradre_blanchfield,
                    'wright-pauga': wright_pauga,
                    'parisian-pogues': parisian_pogues,
                    'knight-prachnio': knight_prachnio,
                    'miller-hernandez': miller_hernandez,
                    'sadykhov-elder': sadykhov_elder,
                    'lansberg-silva': lansberg_silva,
                    'emmers-askabov': emmers_askhabov,
                    'preux-lins': preux_lins,
                    'fletcher-gorimbo': fletcher_gorimbo,
                    'carpenter-ronderos': carpenter_ronderos,
                }
                database.child("users").child(encoded_email).child("fighter selections").set(data)

                message = "Fighter choices saved"
                return render(request, "choosefighters.html", {"messg": message})
        else:
            message = "Invalid request method"
            return render(request, "choosefighters.html", {"messg": message})
    else:
        message = "You are logged out, to continue log back in!"
        return render(request, "signIn.html", {"messg": message})
  
def points_earned(request):
    if 'uid' in request.session:
        email = request.session.get('email')
        encoded_email = email.replace('.', ',')
        fighters_selected = database.child("users").child(encoded_email).child("fighter selections").get().val()
        print(fighters_selected)
        # Define a dictionary of the points awarded for each fighter in each match
        total_points = 0
        if 'andradre-blanchfield' in fighters_selected and fighters_selected['andradre-blanchfield'] == "Erin Blanchfield":
          total_points = total_points + 4
          secondfight = "Win"
        else:
          secondfight = "Loss"
          
        if 'wright-pauga' in fighters_selected and fighters_selected['wright-pauga'] == "Jordan Wright":
          total_points = total_points + 4
          firstfight = "Win"
        else:
          firstfight = "Loss"
        if 'parisian-pogues' in fighters_selected and fighters_selected['parisian-pogues'] == "Jamal Pogues":
          total_points = total_points + 4
          thirdfight = "Win"
        else:
          thirdfight="Loss"
        if 'knight-prachnio' in fighters_selected and fighters_selected['knight-prachnio'] == "Marchin Prachnio":
            total_points = total_points + 4
            fourthfight="WIN"
        else:
          fourthfight="Loss"
        if 'miller-hernandez' in fighters_selected and fighters_selected['miller-hernandez'] == "Alexander Hernandez":
          total_points = total_points + 4
          fifthfight="Win"
        else:
          fifthfight="Loss"
        if 'sadykhov-elder' in fighters_selected and fighters_selected['sadykhov-elder'] == "Nazim Sadykhov":
            total_points = total_points + 4
            sixthfight="Win"
        else:
            sixthfight="Loss"
        if 'lansberg-silva' in fighters_selected and fighters_selected['lansberg-silva'] == "Mayra Bueno Silva":
          total_points = total_points + 4
          seventhfight="Win"
        else:
          seventhfight="Loss"
        if 'emmers-askabov' in fighters_selected and fighters_selected['emmers-askabov'] == "Jamall Emmers":
            total_points = total_points + 4
            eightfight="Win"
        else:
            eightfight="Loss"
        if 'preux-lins' in fighters_selected and fighters_selected['preux-lins'] == "Philipe Lins":
          total_points = total_points + 4
          ninthfight="Win"
        else:
          ninthfight="Loss"
        if 'fletcher-gorimbo' in fighters_selected and fighters_selected['fletcher-gorimbo'] == "AJ Fletcher":
            total_points = total_points + 4
            tenthfight="Win"
        else:
            tenthfight="Loss"
        if 'carpenter-ronderos' in fighters_selected and fighters_selected['carpenter-ronderos'] == "Clayton Carpenter":
          total_points = total_points + 4
          eleventhfight="Win"
        else:
          eleventhfight="Loss"
        

        print(total_points)
        return render(request, "points_earned.html", {'total_points': total_points, 'firstfight': firstfight, 'secondfight': secondfight, 'thirdfight': thirdfight, 'fourthfight': fourthfight, 'fifthfight': fifthfight, 'sixthfight': sixthfight, 'seventhfight': seventhfight, 'eightfight': eightfight, 'ninthfight': ninthfight, 'tenthfight': tenthfight, 'eleventhfight': eleventhfight })
    else:
        message = "You are logged out, to continue log back in!"
        return render(request, "signIn.html", {"messg": message})



def fighter_selection(request):
    if 'uid' in request.session:
        email = request.session.get('email')
        encoded_email = email.replace('.', ',')
        fighters_selected = database.child("users").child(encoded_email).child("fighter selections").get().val()
        return render(request, "fighter_selection.html", {'fighters_selected': fighters_selected})
    else:
        message = "You are logged out, to continue log back in!"
        return render(request, "signIn.html", {"messg": message})


def leaguetable(request):
  if 'uid' in request.session:
    id_token = request.session['uid']
    email = request.session.get("email")
    encoded_email = email.replace('.', ',')
    try:
      leagues = database.child("leagues").get().val()
      leagues_dict = dict(leagues)  # Convert to a dictionary
      data = []
      for league_id, league in leagues_dict.items():
          if 'members' in league and email in league['members']:
              print('User is a member of league:', league['leaguename'])
              league_data = {'name': league['leaguename'], 'members': []}
              for member in league['members']:
                  if member is None:
                      continue
                  print('Processing member:', member)
                  member_data = {'name': member, 'fighter_selections_link': None}
                  member_encoded_email = member.replace('.', ',')
                  if database.child("users").child(member_encoded_email).child("fighter selections").get().val() is not None:
                      member_data['fighter_selections_link'] = reverse('membersselections')
                  league_data['members'].append(member_data)
              data.append(league_data)
      if not data:
        message="You are not part of any leagues, join or create a league."
        return render(request, "welcome.html", {"messg":message})
        
      return render(request, 'leaguetable.html', {'data': data})
      
    except:
      message="You are not part of any leagues, join or create a league."
      print( database.child("users").child(encoded_email).child("fighter selections").get().val() )
      return render(request, "joinleague.html", {"messg":message})
  else:
    message="You are logged out, to continue log back in!"
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
        database.child("leagues").child(leaguename).set(data)
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
                print("League key:", key)
                print("League unique code:", league['uniquecode'])
                print("League members:", league['members'])
                if league['uniquecode'] == uniquecode:
                    if email in league['members']: # check if the user is already a member of the league
                        message = "You are already a member of this league."
                        return render(request, "joinleague.html", {"messg": message})
                    else:
                        members = league['members']
                        members.append(email)
                        database.child("leagues").child(key).update({"members": members})
                        league_found = True
                        break
            if league_found:
                print("League found. Redirecting to leaguetable.")
                return redirect('leaguetable')
            if not league_found:
                message="The unique code you entered does not match any existing leagues. Please try again or create a new league."
                return render(request, "joinleague.html", {"messg":message})
        except Exception as e:
            print("Exception:", e)
            message="The unique code you entered does not match any existing leagues. Please try again or create a new league."
            return render(request, "joinleague.html", {"messg":message})
    else:
        message="You are logged out, please log back in to join a league."
        return render(request, "signIn.html", {"messg":message})



def membersselections(request):
  
  return render(request, "membersselections.html")