import csv
import os
from os.path import isfile, exists
import json
import argparse

EXPENSE_CLASSES = ["New", "Expense", "Income", "Investment", "Savings", "Dumb Shit", "Family and Friends", "Other"]

PARTNER = {
    "Name": "",
    "Expense Class": EXPENSE_CLASSES[0],
    "Comment": "",
    "Tags": "",
    "Charges": []
}

def review_classes(expense_dict):
    expenseUpdatedClasses = expense_dict

    for key, data in expense_dict.items():
        if data['Expense Class'] == EXPENSE_CLASSES[0]:
            print(f"gotta change it!")

    return expenseUpdatedClasses

def main():
    #parser = argparse.ArgumentParser(description="Expense sorter script.")
    #parser.add_argument("-f", "--filepath", type=str, help="The name of the CSV file")
    #args = parser.parse_args()

    # There are supposed to be under a folder named /data. It's not in the repo for obvious reasons
    path_to_folder = os.path.join(os.getcwd(), "data", "finance_files")
    library = os.path.join(os.getcwd(), "data", "dictionary.json")

    path_to_data = os.path.join(os.getcwd(), "data")
    path_to_csvs = f"{path_to_data}/finance_files"

    # Create and check if necessary data is present
    if not exists(path_to_data):
        os.mkdir(path_to_data)

    if not exists(path_to_csvs):
        os.mkdir(path_to_csvs)

    if not os.listdir(path_to_csvs):
        print(f"The folder where CSVs are pulled from is empty. Please ensure your file is here and that it follows the guidelines.\nPath: '{path_to_csvs}'")
        return 

    expense_dict = {}
    new_partners_detected = False
    new_dict_partners = 0
     
    # Load up or create library
    if isfile(library):
        with open(library, "r") as file:
            expense_dict = json.load(file)
            print(f"Loaded {len(expense_dict)} entries from the expense dictionary.")
    else:
        expense_dict = {}
        print("No existing expense  dictionary found. Starting fresh.")

    # Walk the folder and get all available files
    available_csvs = []
    for root, folder, files in os.walk(path_to_csvs):
        for file in files:
            full_file_path = os.path.join(root, file)
            available_csvs.append(full_file_path)

    # Go over each csv
    for csv_file in available_csvs:
        sorted_expenses = {}
    
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)

            # Print column headers
            print(f" {' | '.join(reader.fieldnames)} ")

            # Start sorting rows based on the partner name
            for row in reader:
                if row["Partner Name"] in sorted_expenses:
                    sorted_expenses[row["Partner Name"]]["count"] += 1
                    sorted_expenses[row["Partner Name"]]["expenses"].append(row)
                else:
                    sorted_expenses[row["Partner Name"]] = {"count": 1, "expenses": [row]}

        print(f"Total unique accounts: {len(sorted_expenses)}")
        # After the csv is read, compare to dictionary to check if already there or not:
        for partner, data in sorted_expenses.items():
            print(f"\n - Partner: {partner}\nData:{data}")

            if partner not in expense_dict:
                new_partners_detected = True
                expense_dict[partner] = PARTNER.copy()

            expense_dict[partner]["Name"] = partner

            for expense in data['expenses']:
                og_curr = expense['Original Currency']
                partner_name = expense['Partner Name']

                #print(f"Expense: {expense}")


            expense_dict[partner]["Charges"] = [expense["Amount (EUR)"] for expense in data["expenses"]]

            #print(f"Partner: {partner}, Count: {data['count']}")

        print(f"New partners added to dictionary: {new_dict_partners}")

    # Ensure the directory for the library file exists
    os.makedirs(os.path.dirname(library), exist_ok=True)

    if new_partners_detected and len(expense_dict) > 0:
        expense_dict = review_classes(expense_dict)
    
    # Store back dictionary
    with open(library, "w") as file:
        json.dump(expense_dict, file, indent=4)
        print(f"Saved {len(expense_dict)} entries to the expense dictionary.")

if __name__ == "__main__":
    main()