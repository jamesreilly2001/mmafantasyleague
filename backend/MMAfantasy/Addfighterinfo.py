import requests
import json
from MMAfantasy import models



# Replace [YOUR_FIREBASE_PROJECT_ID] and [YOUR_FIREBASE_AUTH_KEY] with your actual Firebase project ID and authentication key
firebase_project_id = 'mma-fantasy-league-94b6e'
firebase_auth_key = '73a7ce5de6e25f7cac604eac438e25841edadccd'

# Define the data for each fighter
fighters = [
    {
        'name': 'Conor McGregor',
        'age': 32,
        'record': '22-5-0',
        'weight_class': 'Featherweight'
    },
    {
        'name': 'Jon Jones',
        'age': 34,
        'record': '26-1-0',
        'weight_class': 'Light Heavyweight'
    },
    {
        'name': 'Khabib Nurmagomedov',
        'age': 32,
        'record': '29-0-0',
        'weight_class': 'Lightweight'
    }
]

# Loop through each fighter, and send the data to Firebase Realtime Database
for fighter in fighters:
    fighter_id = fighter['name'].lower().replace(' ', '_')
    endpoint_url = f'https://{firebase_project_id}.firebaseio.com/fighters/{fighter_id}.json'
    headers = {
        'Authorization': f'Bearer {firebase_auth_key}',
        'Content-Type': 'application/json'
    }
    data = json.dumps(fighter)
    response = requests.post(endpoint_url, headers=headers, data=data)
    if response.status_code != 200:
        print(f'Error inserting data for fighter {fighter_id}: {response.text}')
    else:
        print(f'Successfully inserted data for fighter {fighter_id}')
