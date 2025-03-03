import requests
import config
from datetime import datetime
import sys
from logging_config import logger

def update_clickup_custom_field(task_id, custom_field_id, value):
    """Update a custom field in a ClickUp task"""
    url = f'{config.CLICKUP_ENDPOINT}task/{task_id}/field/{custom_field_id}'
    payload = {'value': str(value)}
    response = requests.post(url, json=payload, headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to update ClickUp custom field: {response.status_code} - {response.content}')
        return None
    return response.json()

def checkin_to_cickup():
    """Check in tasks to ClickUp"""

    action = sys.argv[1].lower() if len(sys.argv) > 1 else None
    field_names = {
        'checkin': 'Check In',
        'checkout': 'Check Out'
    }

    # Validate and get the correct field name
    custom_field_name = field_names.get(action)
    if not custom_field_name:
        logger.info('Invalid action. Use "checkin" or "checkout".')
        sys.exit(1)

    # Get the Space ID
    response = requests.get(f'{config.CLICKUP_ENDPOINT}team/{config.CLICKUP_TEAM_ID}/space', headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to fetch ClickUp tasks: {response.status_code} - {response.content}')
        return None

    clickup_spaces = response.json().get('spaces', [])
    space_id = next((item['id'] for item in clickup_spaces if "Staff Daily Task/WFH" in item['name']), None)

    if not space_id:
        logger.info('Space ID not found.')
        return

    #Get folder ID
    response = requests.get(f'{config.CLICKUP_ENDPOINT}space/{space_id}/folder', headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to fetch ClickUp tasks: {response.status_code} - {response.content}')
        return None

    clickup_folders = response.json().get('folders', [])
    folder_name = datetime.now().strftime("%B %Y")
    folder_id = next((item['id'] for item in clickup_folders if folder_name in item['name']), None)

    if not folder_id:
        logger.info('Folder ID not found.')
        return
    
    #Get List ID
    response = requests.get(f'{config.CLICKUP_ENDPOINT}folder/{folder_id}/list', headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to fetch ClickUp tasks: {response.status_code} - {response.content}')
        return None

    clickup_lists = response.json().get('lists', [])
    list_name = datetime.now().strftime("%d.%m.%Y")
    list_id = next((item['id'] for item in clickup_lists if list_name in item['name']), None)

    if not list_id:
        logger.info('Folder ID not found.')
        return
    
    #Get Task ID
    response = requests.get(f'{config.CLICKUP_ENDPOINT}list/{list_id}/task', headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to fetch ClickUp tasks: {response.status_code} - {response.content}')
        return None

    clickup_tasks = response.json().get('tasks', [])
    task_name = config.NAME
    task_id = next((item['id'] for item in clickup_tasks if task_name in item['name']), None)

    if not task_id:
        logger.info('Task ID not found.')
        return
    
    #Get Custom Field ID
    response = requests.get(f'{config.CLICKUP_ENDPOINT}task/{task_id}', headers=config.clickup_headers)
    if not response.ok:
        logger.info(f'Failed to fetch ClickUp tasks: {response.status_code} - {response.content}')
        return None

    custom_fields = response.json().get('custom_fields', [])
    custom_field_id = next((item['id'] for item in custom_fields if custom_field_name in item['name']), None)

    if not custom_field_id:
        logger.info(f'Custom Field ID not found for {custom_field_name}.')
        return
    update_clickup_custom_field(task_id, custom_field_id, "true")

    if action == 'checkin':
        custom_field_id = next((item['id'] for item in custom_fields if "Location" in item['name']), None)
        update_clickup_custom_field(task_id, custom_field_id, 1)

    logger.info(f'Successfully updated ClickUp task with ID {task_id} with custom field {custom_field_name} for action {action}.')

if __name__ == '__main__':
    checkin_to_cickup()
