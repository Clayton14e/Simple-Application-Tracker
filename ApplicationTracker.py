import json
import csv
from tabulate import tabulate
import datetime

# Opening Data file definition
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Saving Data file definition
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
# Adding to Data file

def add_data_to_json(file_path, new_data):
    data = load_json(file_path)
    
    for entry in data:
        if entry["name"].lower() == new_data["name"].lower():
            entry.update(new_data)
            break
    else:
        data.append(new_data)
    
    save_json(file_path, data)
    print(tabulate(data, headers="keys", tablefmt="grid"))
    return data

# Export Data Definition
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

# Search by Name Definition
def search_entry_by_name(file_path, name):
    data = load_json(file_path)
    for entry in data:
        if entry["name"].lower() == name.lower():
            print(tabulate([entry], headers="keys", tablefmt="grid"))
            return
    print("Entry not found.")

# Count Entries by Day Definition (Currently a search method)
def count_entries_by_day(file_path, day):
    data = load_json(file_path)
    for entry in data:
        if entry["day"].lower() == day.lower():
            print(tabulate([entry], headers="keys", tablefmt="grid"))
            return
    print("No Entries found.")

# Display Histograph with Data
def display_histograph():
    print("data")

# Main
def main():
    file_path = "data.json"
    while True:
        choice = input("Choose an option: (1) Add Entry (2) View Data Table (3) Search Entry by Name (4) Exit: ").strip()
        
        # Add Entry
        if choice == '1':
            name = input("Enter name: ")
            position = input("Enter position: ")
            selected = input("Is selected? (yes/no): ").strip().lower() == 'yes'
            today = datetime.date.today()
            day = today.weekday()
            
            # Switch day from int to string before adding
            if day == 0:
                day = 'Monday'
            elif day == 1:
                day = 'Tuesday'
            elif day == 2:
                day = 'Wednesday'
            elif day == 3:
                day = 'Thursday'
            elif day == 4:
                day = 'Friday'
            elif day == 5:
                day = 'Saturday'
            elif day == 6:
                day = 'Sunday'
            
            if not selected:
                status = input("Choose status (rejected/no response/new entry): ").strip().lower()
            else:
                status = input("Choose status (offer/interview/rejected): ").strip().lower()
            
            new_entry = {
                "name": name,
                "position": position,
                "status": status,
                "day": day
            }
            add_data_to_json(file_path, new_entry)
        
        # View Table
        elif choice == '2':
            data = load_json(file_path)
            if data:
                print(tabulate(data, headers="keys", tablefmt="grid"))
            else:
                print("No data available.")
        
        # Search Entry by name
        elif choice == '3':
            name = input("Enter name to search: ")
            search_entry_by_name(file_path, name)
        
        # Exit
        elif choice == '4':
            break
        
        # Catch invalid input
        else:
            print("Invalid choice. Please try again.")

    export_choice = input("Do you want to export the data to a spreadsheet? (yes/no): ").strip().lower()
    if export_choice == 'yes':
        export_to_csv(load_json(file_path), "data.csv")

if __name__ == "__main__":
    main()