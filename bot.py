import discord
import os
import requests

from dotenv import load_dotenv

load_dotenv()


google_key = os.getenv("GOOGLE_API")
if not google_key:
    raise ValueError("ERROR: API KEY is missing. Check your .env file.")
token = os.getenv("TOKEN")
if not token:
    raise ValueError("ERROR: Bot token is missing. Check your .env file.")


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents = intents)

#function to fech query data
def fetch_fact_check(query):
    api_url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={google_key}"
    response = requests.get(api_url)

    
    if response.status_code != 200:
        return f"Error: Unable to fetch data (status {response.status_code})"

    data = response.json()
    if "claims" not in data or not data["claims"]:
        return "No fact-check results found for this claim."

    # Extract the first fact-check result
    fact = data["claims"][0]
    text = fact.get("text", "No claim text available.")
    review = fact.get("claimReview", [{}])[0]
    
    source = review.get("publisher", {}).get("name", "Unknown source")
    rating = review.get("textualRating", "No rating available")
    review_url = review.get("url", "No URL available")

    return f"**Claim:** {text}\n**Source:** {source}\n**Rating:** {rating}\n[More Info]({review_url})"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$factcheck'):
        # populate query with message content exluding "$factcheck"
        query = message.content[len("$factcheck "):].strip()

        if not query:
            await message.channel.send("Erm, please provide a claim.")
            return
        
        await message.channel.send(f'Query is: {query}')
        
        await message.channel.send("Searching..")
        result = fetch_fact_check(query)
        await message.channel.send(result)
client.run(token)

