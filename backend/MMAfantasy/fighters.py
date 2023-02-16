import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyD-_zfDFYhcZUDpTTaKS7I0YJahMaqiCLs",
  'authDomain': "mma-fantasy-league-94b6e.firebaseapp.com",
  'databaseURL': "https://mma-fantasy-league-94b6e-default-rtdb.firebaseio.com",
  'projectId': "mma-fantasy-league-94b6e",
  'storageBucket': "mma-fantasy-league-94b6e.appspot.com",
  'messagingSenderId': "837434946169",
  'appId': "1:837434946169:web:7a0210a7c523225e629aa8",
  'measurementId': "G-DRKKN38R7H"
}


firebase=pyrebase.initialize_app(firebaseConfig)
# Define the data for each fighter
db = firebase.database()
data = {
        'name': 'Jessica Andradre',
        'age': 31,
        'record': '24-9-0',
        'weight_class': 'Flyweight',
        'points':3
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Andradre v Blanchfield").child("Jessica Andradre").set(data)


data = {
        'name': 'Erin Blanchfield',
        'age': 23,
        'record': '10-1-0',
        'weight_class': 'Flyweight',
        'points':4
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Andradre v Blanchfield").child("Erin Blanchfield").set(data)

data = {
        'name': 'Jordan Wright',
        'age': 31,
        'record': '12-4-0 (1 NC)',
        'weight_class': 'Lightheavyweight',
        'points':3
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Wright v Pauga").child("Jordan Wright").set(data)


data = {
        'name': 'ZAC PAUGA',
        'age': 45,
        'record': '6-1-0',
        'weight_class': 'Lightheavyweight',
        'points':4
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Wright v Pauga").child("Zac Pauga").set(data)