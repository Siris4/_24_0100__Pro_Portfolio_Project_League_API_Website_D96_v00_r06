import requests
import os

# Load API key from environment variables
API_KEY = os.getenv('RIOT_API_KEY')
BASE_URL = 'https://{region}.api.riotgames.com'


# Function to get live game data using PUUID
def get_live_game_by_puuid(region='na1'):
    # Fetch PUUID from environment
    puuid = os.getenv('ENCRYPTED_PUUID')

    if not puuid:
        print("PUUID not found in environment variables!")
        return None

    # Construct the URL
    url = f'{BASE_URL.format(region=region)}/lol/spectator/v5/active-games/by-summoner/{puuid}'

    # Debugging: Print out the PUUID and constructed URL to ensure they are valid
    print(f"PUUID: {puuid}")
    print(f"Constructed Request URL: {url}")

    headers = {'X-Riot-Token': API_KEY}

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")

        # Handle successful response (status code 200)
        if response.status_code == 200:
            live_game_data = response.json()
            print("Live game data found:")
            return live_game_data
        elif response.status_code == 404:
            print("The summoner is not currently in a live game.")
        elif response.status_code == 401:
            print("Unauthorized - Check your API key.")
        elif response.status_code == 429:
            print("Rate limit exceeded - Please try again later.")
        else:
            print(f"Unexpected error: {response.status_code}")
    except OSError as e:
        print(f"OSError: {e}")
    return None


# Test the function by fetching live game data for a summoner's PUUID
if __name__ == "__main__":
    region = "na1"  # Replace with the appropriate region
    live_game_data = get_live_game_by_puuid(region)

    if live_game_data:
        print(f"Live Game Data: {live_game_data}")
