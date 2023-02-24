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

#### FILL THIS ALGORITHM TO GENERATE POINTS FOR EACH FIGHTER IN EACH FIGHT####### 

fighter1_points = 5
fighter2_points = 5

# Get the last 5 fight results for each fighter
fighter1_last_5 = ['w', 'w', 'w', 'w', 'w']
fighter2_last_5 = ['w', 'l', 'w', 'w', 'w']

# Add 1 point for each loss in the last 5 fights
fighter1_points += fighter1_last_5.count('l')
fighter2_points += fighter2_last_5.count('l')

# Determine which fighter has worse takedown accuracy
fighter1_takedown_accuracy = 0.7
fighter2_takedown_accuracy = 0.6

if fighter1_takedown_accuracy < fighter2_takedown_accuracy:
    fighter1_points += 1
else:
    fighter2_points += 1

# Determine which fighter has worse strike accuracy
fighter1_strike_accuracy = 0.8
fighter2_strike_accuracy = 0.75

if fighter1_strike_accuracy < fighter2_strike_accuracy:
    fighter1_points += 1
else:
    fighter2_points += 1

# Print the final results
print("Fighter 1 points:", fighter1_points)
print("Fighter 2 points:", fighter2_points)


blanchfield = {
        'points': fighter1_points,
        
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Andradre v Blanchfield").child("Erin Blanchfield").set(blanchfield)

andradre = {
        'points': fighter2_points,
        
    }

# Loop through each fighter, and send the data to Firebase Realtime Database
db.child("Fight cards").child("UFC FIGHT NIGHT: Andradre v Blanchfield ").child("Main Card").child("Fights").child("Andradre v Blanchfield").child("Jessica Andradre").set(andradre)
