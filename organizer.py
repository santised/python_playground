import pandas as pd
import sys
import matplotlib.pyplot as plotLib


class expense_organizer:
    def __init__(self, path_to_spreadsheet):
        truncated_path = path_to_spreadsheet.split("/")[-1]
        self.spreadsheet = truncated_path
        print(f"\nReading from {truncated_path}\n")

        # All class arrays are small pattern matches..
        # These are the columns of interest
        self.keep_columns = [
            "Effective Date",
            "Amount",
            "Description",
            "Transaction Category",
        ]

        # Grocery stores
        self.grocery_search = [
            "WHOLEFDS",
            "NATURAL GROCERS",
            "COSTCO",
            "SAFEWAY",
            "KING SOOPERS",
            "Murdochs",  # dog food
            "CHUCK",  # dog food
        ]

        # These are recurring expenses like utlities and subscriptions
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

        # This is used to sub-categorize expenses
        self.dog_food_sub_category = ["CHUCK", "MURDOCHS"]

        self.coffee_sub_category = [
            "Ziggis",
            "Brewing Market",
            "Dutch Bros",
            "Ozo Coffee",
            "Cavegirl",
            "Babettes",
        ]

        # Income
        self.payroll_search = [
            "GUSTO",
            "PAYROLL",
        ]

        self.items_to_exclude = ["Transfers"]

        # Only a few of the columns are relevant and so they're reduced here and
        # certain columns are formatted; the date field is set to a proper date-time field
        # for better sorting, and expenses are set to positive values.
        # This is done so that I can copy and paste into another spreadsheet.
        # FIX: Can I finalize the format so that I can copy the entire csv into the other?
        # Can I upload a csv directly into Proton?
        self.organized_csv = self.format_new_csv()
        self.finalized_csv = self.bills_sorting()

    def format_new_csv(self):
        new_csv = pd.read_csv(self.spreadsheet, usecols=self.keep_columns)

        # Return a copy of the csv that removes the rows from the column "Designator" that match the labels within
        # "items_to_exclude". Note that this is in fact making a csv that match the labels of the list, but inverts the
        # matching behavior: ~
        new_csv = new_csv[
            ~new_csv["Transaction Category"].str.contains(
                "|".join(self.items_to_exclude)
            )
        ]

        # Change expense values to positive values to be able to copy it directly into another csv
        new_csv["Amount"] = new_csv["Amount"].abs()

        # The date column is just text and so sorting it means 1/27 comes before 1/3, change to date time.
        new_csv["Effective Date"] = pd.to_datetime(new_csv["Effective Date"])

        # Now chnage date time to just be month/day
        new_csv["Effective Date"] = new_csv["Effective Date"].dt.strftime("%m/%d")

        # Return the formatted csv
        return new_csv

    def bills_sorting(self):
        # Blanket reset a column to be "other expenses"
        self.organized_csv.loc[
            self.organized_csv["Description"].notna(), "Transaction Category"
        ] = "Expenses"

        # Search for groceries and apply that label
        grocery_pattern = "|".join(self.grocery_search)
        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                grocery_pattern, case=False, na=False
            ),
            "Transaction Category",
        ] = "Groceries"

        # Search for recurring expenses and apply the correct label
        recurring_pattern = "|".join(self.reccurring_expense_search)
        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                recurring_pattern, case=False, na=False
            ),
            "Transaction Category",
        ] = "Recurring"

        # Search for income
        payroll_pattern = "|".join(self.payroll_search)
        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                payroll_pattern, case=False, na=False
            ),
            "Transaction Category",
        ] = "INCOME"

        coffee_pattern = "|".join(self.coffee_sub_category)
        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                coffee_pattern, case=False, na=False
            ),
            "Sub-category",
        ] = "Coffee"

        dog_pattern = "|".join(self.dog_food_sub_category)
        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                dog_pattern, case=False, na=False
            ),
            "Sub-category",
        ] = "Dog Food"

        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                "Flagstaff", case=False, na=False
            ),
            "Sub-category",
        ] = "Flagstaff"

        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                "CU Parking", case=False, na=False
            ),
            "Sub-category",
        ] = "Parking"

        self.organized_csv.loc[
            self.organized_csv["Description"].str.contains(
                "Gusto", case=False, na=False
            ),
            "Sub-category",
        ] = "Gusto"

        # Sort the spreadsheet
        return self.organized_csv.sort_values(
            by=[
                "Transaction Category",
                "Effective Date",
            ]
        )

    def sum_category_totals(self, sorted_csv):
        grocery_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("Groceries"),
            "Amount",
        ].sum()

        recurring_total = sorted_csv.loc[
            sorted_csv["Transaction Category"].str.contains("Recurring"),
            "Amount",
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
        # alphabetized_csv.to_csv("{0}".format(path_to_spreadsheet), index=False)
        return 0

    def export_csv(self):
        self.finalized_csv.to_csv("expense.csv", index=False)

    def graph_expenses(self):
        income_total = self.finalized_csv.loc[
            self.finalized_csv["Transaction Category"].str.contains("INCOME"), "Amount"
        ].sum()

        # finalized_csv is sorted by Transaction categories i.e. Groceries, Income, Expenses and sorts each Category
        # by date. I only want to graph by date.
        expenses = self.finalized_csv[
            self.finalized_csv["Transaction Category"] != "INCOME"
        ].sort_values("Effective Date")

        # cumsum produces a running total of "Amount"
        expenses["Remaining"] = income_total - expenses["Amount"].cumsum()

        #  collapses the "remaining" values at a given date and mi
        daily_min = expenses.groupby("Effective Date")["Remaining"].min().reset_index()

        bars = plotLib.bar(daily_min["Effective Date"], daily_min["Remaining"])

        for bar, value in zip(bars, daily_min["Remaining"]):
            plotLib.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"${value:.2f}",
                ha="center",
                va="bottom",
            )
        plotLib.xlabel("Date")
        plotLib.ylabel("Money Remaining")
        plotLib.show()

    def stack_graphs(self):
        expenses = self.finalized_csv[
            self.finalized_csv["Transaction Category"] != "INCOME"
        ].sort_values("Effective Date")

        pivot = (
            expenses.groupby(["Effective Date", "Transaction Category"])["Amount"]
            .sum()
            .unstack(fill_value=0)
        )
        pivot.plot(kind="bar", stacked=True)
        plotLib.xlabel("Date")
        plotLib.ylabel("Amount")
        plotLib.show()


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
    bo = expense_organizer(path_to_spreadsheet)
    bo.sum_category_totals(bo.finalized_csv)
    bo.export_csv()
    bo.graph_expenses()
