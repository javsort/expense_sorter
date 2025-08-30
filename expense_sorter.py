import csv
import os
from os.path import isfile, exists
import json
import datetime

EXPENSE_CLASSES = ["New", "Reg Expense", "Income", "Investment", "Savings", "Dumb Shit", "Family / Friends", "Bar/Drinks", "Food/Coffee", "Subscription", "Other"]

PARTNER = {
    "Name": "",
    "Expense Class": EXPENSE_CLASSES[0],
    "Comment": "",
    "Tags": "",
    "Charges": []
}

CHARGE = {
    "Amount": 0,
    "Date": "",             # Value Date
    "Date Registered": ""   # Booking Date
}

def get_listed_exp_classes():
    ret_str = ""

    for x in range(len(EXPENSE_CLASSES)):
        curr_class = EXPENSE_CLASSES[x]

        if curr_class == EXPENSE_CLASSES[0]:
            continue

        ret_str += f" {x} - {curr_class} \n"

    ret_str = f" 0 - Skip \n{ret_str}"

    return ret_str

def summarize_partner(partner):
    partner_str = ""

    return partner_str

def review_classes(expense_dict):

    print(f"\n\nWe detected some new unclassified partners, please review: \n")
    expenseUpdatedClasses = expense_dict

    for key, data in expense_dict.items():
        if data['Expense Class'] == EXPENSE_CLASSES[0]:
            while True:
                print(summarize_partner(data))
                print(f"We detected the partner: '{key}' hasn't been set an expense class. Please choose one out of the following:\n{get_listed_exp_classes()}")
                chosen_class = input()

                print(f"Chosen class selected: {chosen_class}")

                match chosen_class:
                    case "0":      # Skip
                        print(f"Skiping... \n")
                        break
                    case "1":       # Regular Expense
                        data["Expense Class"] = EXPENSE_CLASSES[1]
                        break
                    case "2":       # Income
                        data["Expense Class"] = EXPENSE_CLASSES[2]
                        break
                    case "3":       # Investment
                        data["Expense Class"] = EXPENSE_CLASSES[3]
                        break
                    case "4":       # Savings
                        data["Expense Class"] = EXPENSE_CLASSES[4]
                        break
                    case "5":       # Dumb Shit
                        data["Expense Class"] = EXPENSE_CLASSES[5]
                        break
                    case "6":       # Fam / Friends
                        data["Expense Class"] = EXPENSE_CLASSES[6]
                        break
                    case "7":       # Bar
                        data["Expense Class"] = EXPENSE_CLASSES[7]
                        break
                    case "8":       # Food
                        data["Expense Class"] = EXPENSE_CLASSES[8]
                        break
                    case "9":       # Food
                        data["Expense Class"] = EXPENSE_CLASSES[9]
                        break
                    case "10":       # Other
                        data["Expense Class"] = EXPENSE_CLASSES[10]
                        break
                    case _:
                        print(f"Please choose a valid class.")
                        continue
                
            print(f"Expense Class updated successfully :)")


    return expenseUpdatedClasses

def main():
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

            partners_grouped_expenses = []

            for expense in data['expenses']:
                this_charge = CHARGE.copy()
                this_charge['Date'] = expense['Value Date']
                this_charge['Date Registered'] = expense['Booking Date']
                this_charge['Amount'] = expense['Amount (EUR)']

                partners_grouped_expenses.append(this_charge)

            expense_dict[partner]["Charges"] = partners_grouped_expenses
            #print(f"Partner: {partner}, Count: {data['count']}")

        print(f"New partners added to dictionary: {new_dict_partners}")

    print(f"{json.dumps(expense_dict, indent=4)}")

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