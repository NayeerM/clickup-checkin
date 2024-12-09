import json
import os
from dotenv import load_dotenv

load_dotenv()

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data

# Load the configuration data
config = load_config()

NAME = config['Name']

CLICKUP_ENDPOINT = 'https://api.clickup.com/api/v2/'

CLICKUP_API_KEY = os.getenv('CLICKUP_API_KEY')
if CLICKUP_API_KEY is None:
    raise KeyError("CLICKUP_API_KEY")

CLICKUP_TEAM_ID = os.getenv('CLICKUP_TEAM_ID')
if CLICKUP_TEAM_ID is None:
    raise KeyError("CLICKUP_TEAM_ID")

clickup_headers = {
    'Authorization': CLICKUP_API_KEY,
    'Content-Type': 'application/json'
}