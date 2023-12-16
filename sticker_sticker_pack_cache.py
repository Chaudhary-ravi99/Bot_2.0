import json

# Function to add data to the JSON file


def add_data_to_json(user_id, sticker_pack_link):
    try:
        # Load existing data or create an empty dictionary
        with open('sticker_sticker_pack_cache.json', 'r') as file:
            json_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_data = {}

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

    # Write the updated data back to the file
    with open('sticker_sticker_pack_cache.json', 'w') as file:
        json.dump(json_data, file, indent=2)


def get_user_data(user_id):
    try:
        # Load existing data or create an empty dictionary
        with open('sticker_sticker_pack_cache.json', 'r') as file:
            json_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
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






def delete_data_from_json(username, data_to_delete):
    try:
        # Load existing data or create an empty dictionary
        with open('sticker_sticker_pack_cache.json', 'r') as file:
            json_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        json_data = {}

    # Check if the username exists
    if username in json_data:
        # Remove specific data from the list
        json_data[username] = [item for item in json_data[username] if item not in data_to_delete]

        # Write the updated data back to the file
        with open('data.json', 'w') as file:
            json.dump(json_data, file, indent=2)
    else:
        print(f"Username '{username}' not found.")

# Example usernames and data
#username1 = 'Username'
#data1 = ['data1', 'data2', 'data3']
#data_to_delete = ['data2']

#add_data_to_json(username1, data1)
#delete_data_from_json(username1, data_to_delete)

#result_data = get_data_by_username(username1)
#print(f"Data for {username1}: {result_data}")
