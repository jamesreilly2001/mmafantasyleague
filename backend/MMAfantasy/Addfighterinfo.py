import json
from firebase_admin import credentials, firestore, initialize_app

# Replace [YOUR_FIREBASE_PROJECT_ID] and [YOUR_FIREBASE_AUTH_KEY_FILE_PATH] with your actual Firebase project ID and authentication key file path
firebase_project_id = 'mma-fantasy-league-94b6e'
cred = credentials.Certificate("C:\\Users\\user\\Downloads\\mma-fantasy-league-94b6e-firebase-adminsdk-g34f1-4d142578ad.json")

# Initialize the app with a service account, granting admin privileges
initialize_app(cred, {
  'projectId': firebase_project_id,
})

# Get a reference to the Firestore database
db = firestore.client()

# Define the data for each fighter
fighters = [
    {
        'name': 'Islam Makhachev',
        'age': 31,
        'record': '23-1-0',
        'weight_class': 'Lightweight'
    },
    {
        'name': 'Alexander Volkanovski',
        'age': 34,
        'record': '25-1-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Yair Rodríguez',
        'age': 30,
        'record': '15-3-0',
        'weight_class': 'Lightweight'
    },
    {
        'name': 'Josh Emmett',
        'age': 37,
        'record': '18-2-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Jack Della Maddalena',
        'age': 26,
        'record': '13-2-0',
        'weight_class': 'Welterweight'
    },
    {
        'name': 'Randy Brown',
        'age': 32,
        'record': '16-4-0',
        'weight_class': 'Welterweight'
    },
    {
        'name': 'Justin Tafa',
        'age': 29,
        'record': '5-3-0',
        'weight_class': 'Heavyweight'
    },
    {
        'name': 'Parker Porter',
        'age': 37,
        'record': '13-7-0',
        'weight_class': 'Heavyweight'
    },
    {
        'name': 'Jimmy Crute',
        'age': 26,
        'record': '12-3-0',
        'weight_class': 'Light Heavyweight'
    },
    {
        'name': 'Alonzo Menifield',
        'age': 35,
        'record': '13-3-0',
        'weight_class': 'Light Heavyweight'
    },
    {
        'name': 'Tyson Pedro',
        'age': 31,
        'record': '9-3-0',
        'weight_class': 'Light Heavyweight'
    },
    {
        'name': 'modestas bukauskas',
        'age': 28,
        'record': '13-5-0',
        'weight_class': 'Light Heavyweight'
    },
    {
        'name': 'Joshua Culibao',
        'age': 28,
        'record': '10-1-1',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Melsik Baghdasaryan',
        'age': 31,
        'record': '7-1-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Shannon Ross',
        'age': 33,
        'record': '13-6-0',
        'weight_class': 'Flyweight'
    },
    {
        'name': 'Kleydson Rodrigues',
        'age': 27,
        'record': '7-2-0',
        'weight_class': 'Flyweight'
    },
    {
        'name': 'Jamie Mullarkey',
        'age': 28,
        'record': '15-5-0',
        'weight_class': 'Lightweight'
    },
    {
        'name': 'Francis prado',
        'age': 20,
        'record': '11-0-0',
        'weight_class': 'Lightweight'
    },
    {
        'name': 'Jack Jenkins',
        'age': 29,
        'record': '10-2-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Don Shainis',
        'age': 34,
        'record': '12-4-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Loma Lookboonme',
        'age': 27,
        'record': '7-3-0',
        'weight_class': 'Women Strawweight'
    },
    {
        'name': 'Elise Reed',
        'age': 30,
        'record': '6-2-0',
        'weight_class': 'Women Strawweight'
    },
    {
        'name': 'Shane Young',
        'age': 29,
        'record': '13-6-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Blake Bilder',
        'age': 32,
        'record': '7-0-1',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Zubaira Tukhugov',
        'age': 32,
        'record': '20-5-1',
        'weight_class': 'Lightweight'
    },
    {
        'name': 'Elves Brenner',
        'age': 25,
        'record': '13-3-0',
        'weight_class': 'Lightweight'
    }

]

# Loop through each fighter, and send the data to Firebase Realtime Database
for fighter in fighters:
    fighter_id = fighter['name'].lower().replace(' ', '_')
    doc_ref = db.collection(u'fighters').document(fighter_id)
    doc_ref.set(fighter)
    print(f'Successfully inserted data for fighter {fighter_id}')
