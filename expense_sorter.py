import csv
import os
from os.path import isfile
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
    parser = argparse.ArgumentParser(description="Expense sorter script.")
    parser.add_argument("-f", "--filepath", type=str, help="The name of the CSV file")
    args = parser.parse_args()

    path_to_folder = os.path.join(os.getcwd(), "data", "finance_files")
    library = os.path.join(os.getcwd(), "data", "dictionary.json")

    csv_file = args.filepath

    sorted_expenses = {}
    expense_dict = {}
    new_partners_detected = False
    new_dict_partners = 0
    
    if isfile(library):
        with open(library, "r") as file:
            expense_dict = json.load(file)
            print(f"Loaded {len(expense_dict)} entries from the expense dictionary.")

    else:
        expense_dict = {}
        print("No existing expense  dictionary found. Starting fresh.")


    with open(os.path.join(path_to_folder, csv_file), "r") as file:
        reader = csv.DictReader(file)
        
        # Print column headers
        print(f" {' | '.join(reader.fieldnames)} ")
        
        # Print rows
        for row in reader:
            if row["Partner Name"] in sorted_expenses:
                sorted_expenses[row["Partner Name"]]["expenses"].append(row)
                sorted_expenses[row["Partner Name"]]["count"] += 1

            else:
                sorted_expenses[row["Partner Name"]] = {"expenses": [row], "count": 1}

            printed_line = " | ".join(row.values()) 
            #print(printed_line)

    print(f"Total unique accounts: {len(sorted_expenses)}")
    for partner, data in sorted_expenses.items():

        if partner not in expense_dict:
            new_partners_detected = True
            expense_dict[partner] = PARTNER.copy()

        expense_dict[partner]["Name"] = partner

        for expense in data['expenses']:
            og_curr = expense['Original Currency']
            partner_name = expense['Partner Name']

            if len(og_curr) > 0 and og_curr != "EUR":
                print(expense)

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