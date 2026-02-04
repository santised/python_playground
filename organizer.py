import pandas as pd
import sys

keep_columns = [
    "Effective Date",
    "Amount",
    "Description",
    "Transaction Category",
]

exclude_labels = ["Transfers"]


def bills_organizer(path_to_spreadsheet):
    truncated_path = path_to_spreadsheet.split("/")[-1]
    print(f"\nReading from {truncated_path}\n")
    # Insanely powerful ability to both read a csv, keep specific columns, and sort alphabetically
    # from within one function call.
    new_csv = pd.read_csv(path_to_spreadsheet, usecols=keep_columns)

    updated_csv = new_csv[
        ~new_csv["Transaction Category"].str.contains("|".join(exclude_labels))
    ]

    alphabetized_csv = updated_csv.sort_values(
        by=[
            "Transaction Category",
            "Effective Date",
        ]
    )

    # Return a copy of the csv that removes the rows from the column "Designator" that match the labels within
    # "exclude_labels". Note that this is in fact making a csv that match the labels of the list, but inverts the
    # matching behavior: ~
    # updated_csv = csv_pd[~csv_pd["Designator"].str.contains("|".join(exclude_labels))]

    # alphabetized_csv = new_csv.sort_values("Designator")

    print("Placed here: {0}".format(path_to_spreadsheet))
    print(alphabetized_csv)
    alphabetized_csv.to_csv("{0}".format(path_to_spreadsheet), index=False)
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
