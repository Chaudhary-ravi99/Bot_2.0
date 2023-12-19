import requests
import json
import base64
import os
# GitHub repository information



repo_name = os.getenv('REPO_NAME')
github_token = os.getenv('UPLOAD_API_CODE')
repo_owner = 'jinix6'
file_path = 'sticker_sticker_pack_cache.json'



def add_data_to_github(user_id, sticker_pack_link):
    # Fetch existing data from GitHub
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}',
                            headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 200:
        json_data = json.loads(base64.b64decode(response.json()['content']).decode('utf-8'))
        sha = response.json().get('sha')  # Check if 'sha' is present in the response
    else:
        json_data = {}
        sha = None

    # Check if the user_id already exists
    if user_id in json_data:
        # Check if the data for user_id is a list
        if isinstance(json_data[user_id], list):
            # Append new data to the existing list
            json_data[user_id].append(sticker_pack_link)
        else:
            # If not a list, convert it to a list with the existing data and the new data
            json_data[user_id] = [json_data[user_id], sticker_pack_link]
    else:
        # Add a new entry for the user_id and data (as a list)
        json_data[user_id] = [sticker_pack_link]

    # Update the file on GitHub
    encoded_content = base64.b64encode(json.dumps(json_data, indent=2).encode('utf-8')).decode('utf-8')
    update_data = {
        'message': 'Update sticker pack data',
        'content': encoded_content,
    }

    if sha is not None:
        update_data['sha'] = sha  # Add 'sha' only if it's available in the response

    update_response = requests.put(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}',
                                   headers={'Authorization': f'token {github_token}'},
                                   json=update_data)

    print(f"GitHub API URL: {update_response.url}")
    print(f"GitHub API Response: {update_response.text}")

    if update_response.status_code != 200:
        print(f"Failed to update data on GitHub. Status code: {update_response.status_code}")


# Function to get user data from GitHub
def get_user_data_from_github(user_id):
    # Fetch existing data from GitHub
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}',
                            headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 200:
        json_data = json.loads(base64.b64decode(response.json()['content']).decode('utf-8'))
    else:
        json_data = {}

    # Check if the user_id exists
    if user_id in json_data:
        # Ensure the data is a list, convert if necessary
        user_data = json_data[user_id]
        if not isinstance(user_data, list):
            user_data = [user_data]
        return user_data
    else:
        return None

# Function to delete data from GitHub
def delete_data_from_github(username, data_to_delete):
    # Fetch existing data from GitHub
    response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}',
                            headers={'Authorization': f'token {github_token}'})
    
    if response.status_code == 200:
        json_data = json.loads(base64.b64decode(response.json()['content']).decode('utf-8'))
    else:
        json_data = {}

    # Check if the username exists
    if username in json_data:
        # Remove specific data from the list
        json_data[username] = [item for item in json_data[username] if item not in data_to_delete]

        # Update the file on GitHub
        encoded_content = base64.b64encode(json.dumps(json_data, indent=2).encode('utf-8')).decode('utf-8')
        update_data = {
            'message': 'Update sticker pack data',
            'content': encoded_content,
            'sha': response.json()['sha']
        }

        update_response = requests.put(f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}',
                                       headers={'Authorization': f'token {github_token}'},
                                       json=update_data)

        if update_response.status_code != 200:
            print(f"Failed to update data on GitHub. Status code: {update_response.status_code}")
    else:
        print(f"Username '{username}' not found.")