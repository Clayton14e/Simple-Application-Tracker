import json
import csv
from tabulate import tabulate

def add_data_to_json(file_path, new_data):
    try:
        # Load existing data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty, start with an empty list
        data = []
    
    # Check if entry exists by name and update if found
    for entry in data:
        if entry["name"].lower() == new_data["name"].lower():
            entry.update(new_data)
            break
    else:
        # Append new data if name not found
        data.append(new_data)
    
    # Write updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    # Display updated JSON data as a table
    print(tabulate(data, headers="keys", tablefmt="grid"))
    
    return data

def export_to_csv(data, file_path):
    if not data:
        print("No data to export.")
        return
    
    keys = data[0].keys()
    with open(file_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Data exported to {file_path}")

data_list = []
while True:
    # Collect user input
    name = input("Enter Company: ")
    position = input("Enter Position: ")
    status = input("Enter Status: ")

    new_entry = {
        "name": name,
        "position": position,
        "status": status
    }

    data_list = add_data_to_json("data.json", new_entry)
    
    # Ask if user wants to add more data
    another = input("Do you want to add another entry? (yes/no): ").strip().lower()
    if another != 'yes':
        break

# Ask if user wants to export to CSV
export_choice = input("Do you want to export the data to a spreadsheet? (yes/no): ").strip().lower()
if export_choice == 'yes':
    export_to_csv(data_list, "data.csv")
