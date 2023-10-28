#import os
import json
import requests
from flask import Flask, jsonify

# Replace 'YOUR_API_KEY' with your actual API key
api_keys = [
    "YOUR_API_KEY",
    "YOUR_API_KEY",
    "YOUR_API_KEY",
    "YOUR_API_KEY",
    "YOUR_API_KEY",
    "YOUR_API_KEY",
    "YOUR_API_KEY"
]

# Define the News API endpoint
api_endpoint = "https://newsapi.org/v2/everything"
topics = ["Machine Learning", "Artificial Intelligence", "Code for AI", "Technology", "AI WebApps", "AI Algorithms", "Science"]

app = Flask(__name__)

# Define the JSON filename
json_filename = "news_data.json"

# Initialize an empty list or load an existing JSON file if available
try:
    with open(json_filename, "r") as json_file:
        data = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

@app.route('/get_articles', methods=['GET'])
def get_articles():
    return jsonify(data)

def fetch_articles():
    new_data = []

    for topic in topics:
        for api_key in api_keys:
            # Make a request to the API
            params = {
                "apiKey": api_key,
                "q": topic,
                "language": "en",
                "pageSize": 100
            }
            response = requests.get(api_endpoint, params=params)

            if response.status_code == 200:
                articles = response.json().get("articles", [])

                # Iterate through the articles and add new ones to the list
                for article in articles:
                    if article not in data:
                        new_data.append(article)

                # API request was successful, break out of the loop
                break
            else:
                print(f"API request with key '{api_key}' for topic '{topic}' failed. Trying the next key.")

    # Extend the existing list with new data
    if new_data:
        data.extend(new_data)

        # Save the updated list to the JSON file
        with open(json_filename, "w") as json_file:
            json.dump(data, json_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

