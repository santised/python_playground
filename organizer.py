import pandas as pd
import sys


class expense_organizer:
    def __init__(self, path_to_spreadsheet):
        truncated_path = path_to_spreadsheet.split("/")[-1]
        self.spreadsheet = truncated_path
        print(f"\nReading from {truncated_path}\n")

        self.keep_columns = [
            "Effective Date",
            "Amount",
            "Description",
            "Transaction Category",
        ]

        self.grocery_search = [
            "WHOLEFDS",
            "NATURAL GROCERS",
            "COSTCO",
            "KING SOOPERS",
            "Murdochs",  # dog food
            "CHUCK",  # dog food
        ]

        self.reccurring_expense_search = [
            "LONGMONT CLIMBING COL",
            "CITI",
            "CHASE",
            "USAA CREDIT CARD",
            "BOULDER COUNTY BOMBER",
            "THE NEST",
            "Spotify",
            "Netflix",
            "T-MOBILE",
            "GEICO",
            "Airborne",
            "InstaMed",
            "XCEL",
            "CITYOFLONGMONT",  # Utilities
            "Nextlight",
            "CU PARKING REMOTE",  # Utilities
        ]

        self.dog_food_expense_label = ["CHUCK", "MURDOCHS"]

        self.coffee_expense_label = [
            "Ziggis",
            "Brewing Market",
            "Dutch Bros",
            "Ozo Coffee",
            "Cavegirl",
        ]

        self.payroll_search = [
            "GUSTO",
            "PAYROLL",
        ]

        self.exclude_labels = ["Transfers"]
        self.reduced_csv = self.format_new_csv()

    def format_new_csv(self):
        new_csv = pd.read_csv(self.spreadsheet, usecols=self.keep_columns)

        # Return a copy of the csv that removes the rows from the column "Designator" that match the labels within
        # "exclude_labels". Note that this is in fact making a csv that match the labels of the list, but inverts the
        # matching behavior: ~
        new_csv = new_csv[
            ~new_csv["Transaction Category"].str.contains("|".join(self.exclude_labels))
        ]

        # Change values to positive values
        new_csv["Amount"] = new_csv["Amount"].abs()

        # The date column is just text and so sorting it means 1/27 comes before 1/3, change to date time.
        new_csv["Effective Date"] = pd.to_datetime(new_csv["Effective Date"])

        # Now chnage date time to just be month/day
        new_csv["Effective Date"] = new_csv["Effective Date"].dt.strftime("%m/%d")

        return new_csv

    def bills_organizer(self):
        # Blanket reset a column to be "other expenses"
        new_csv.loc[new_csv["Description"].notna(), "Transaction Category"] = "Expenses"

        # Search for groceries and apply that label
        grocery_pattern = "|".join(self.grocery_search)
        new_csv.loc[
            new_csv["Description"].str.contains(grocery_pattern, case=False, na=False),
            "Transaction Category",
        ] = "Groceries"

        # Search for recurring expenses and apply the correct label
        recurring_pattern = "|".join(self.reccurring_expense_search)
        new_csv.loc[
            new_csv["Description"].str.contains(
                recurring_pattern, case=False, na=False
            ),
            "Transaction Category",
        ] = "Recurring"

        # Search for income
        payroll_pattern = "|".join(self.payroll_search)
        new_csv.loc[
            new_csv["Description"].str.contains(payroll_pattern, case=False, na=False),
            "Transaction Category",
        ] = "INCOME"

        coffee_pattern = "|".join(self.coffee_expense_label)
        new_csv.loc[
            new_csv["Description"].str.contains(coffee_pattern, case=False, na=False),
            "Sub-category",
        ] = "Coffee"

        dog_pattern = "|".join(self.dog_food_expense_label)
        new_csv.loc[
            new_csv["Description"].str.contains(dog_pattern, case=False, na=False),
            "Sub-category",
        ] = "Dog Food"

        new_csv.loc[
            new_csv["Description"].str.contains("Flagstaff", case=False, na=False),
            "Sub-category",
        ] = "Flagstaff"

        new_csv.loc[
            new_csv["Description"].str.contains("CU Parking", case=False, na=False),
            "Sub-category",
        ] = "Parking"

        new_csv.loc[
            new_csv["Description"].str.contains("Gusto", case=False, na=False),
            "Sub-category",
        ] = "Gusto"

        # Sort the spreadsheet
        sorted_csv = new_csv.sort_values(
            by=[
                "Transaction Category",
                "Effective Date",
            ]
        )

        grocery_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("Groceries"), "Amount"
        ].sum()

        recurring_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("Recurring"), "Amount"
        ].sum()

        expense_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("Expenses"), "Amount"
        ].sum()

        income_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("INCOME"), "Amount"
        ].sum()

        parking_total = sorted_csv.loc[
            sorted_csv["Sub-category"].str.contains("Parking"), "Amount"
        ].sum()

        dog_food_total = sorted_csv.loc[
            sorted_csv["Sub-category"].str.contains("Dog Food"), "Amount"
        ].sum()

        coffee_total = sorted_csv.loc[
            sorted_csv["Sub-category"].str.contains("Coffee"), "Amount"
        ].sum()

        gusto_income_total = sorted_csv.loc[
            sorted_csv["Sub-category"].str.contains("Gusto"), "Amount"
        ].sum()

        print("Total expenses:", expense_total)
        print("Grocery Total: ", grocery_total)
        print("Recurring Total: ", recurring_total)
        print("Income Total: ", income_total)
        print("Parking Total: ", parking_total)
        print("Dog Food Total: ", dog_food_total)
        print("Coffee Total: ", coffee_total)
        print("GUSTO Income Total: ", gusto_income_total)
        print(
            "Left after expenses: ",
            (income_total + 4332.47)
            - (grocery_total + expense_total + recurring_total),
        )

        # print("Placed here: {0}".format(path_to_spreadsheet))
        # print(sorted_csv)
        sorted_csv.to_csv("expense.csv", index=False)
        # alphabetized_csv.to_csv("{0}".format(path_to_spreadsheet), index=False)
        return 0


#
# ███╗   ███╗ █████╗ ██╗███╗   ██╗
# ████╗ ████║██╔══██╗██║████╗  ██║
# ██╔████╔██║███████║██║██╔██╗ ██║
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
#
if __name__ == "__main__":
    path_to_spreadsheet = sys.argv[1]
    bills_organizer(path_to_spreadsheet)
