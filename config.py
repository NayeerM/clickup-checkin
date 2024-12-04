import json

def load_config(config_file='config.json'):
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    return config_data

# Load the configuration data
config = load_config()

CLICKUP_API_KEY = config['CLICKUP_API_KEY']
CLICKUP_ENDPOINT = 'https://api.clickup.com/api/v2/'
CLICKUP_TEAM_ID = config['CLICKUP_TEAM_ID']
NAME = config['Name']

clickup_headers = {
    'Authorization': CLICKUP_API_KEY,
    'Content-Type': 'application/json'
}