import requests
import os

from dotenv import load_dotenv

API_KEY = os.getenv("GOOGLE_API")
query = "Interest rates are at an all time high"
url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={API_KEY}"


response = requests.get(url)
data = response.json()

print(response.status_code)  # Should be 200 if successful
print(response.text)  # See full error message
print(data)
