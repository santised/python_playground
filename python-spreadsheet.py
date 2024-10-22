import pandas as pd
import sys

# Columns to keep
keep_columns = [
    "SparkFun Part Number",
    "Part Description",
    "BOM Quantity",
    "Primary Vendor",
    "Primary Vendor Part Number",
    "Primary Vendor Cost",
    "Alternate Manufacturer",
    "Alternate Manufactuerer Part Number",
]

# This is all for now I suppose
remove_rows = ["FD", "TP"]


def bom_assembly_update(path_to_spreadsheet, arg):
    print(f"Reading from: {path_to_spreadsheet}\n")
    if arg == "0":
        # Insanely powerful ability to both read a csv and keep specific columns from it within one function call.
        new_csv = pd.read_csv(path_to_spreadsheet, usecols=keep_columns)
        # Without the "index = False" line there is an extra column added in column "A" listing the index.
        # of the rows.
        new_csv.to_csv("Updated_Sparkle_BOM.csv", index=False)
    if arg == "1":
        # Read in the given csb, can be position or BOM csv.
        csv_pd = pd.read_csv(path_to_spreadsheet)
        # So we're checking the "Designator" column and checking if a row/s
        # within contain the given strings. We don't want those (!) so return the rest
        # into swapped.
        swapped_csv = csv_pd[
            ~csv_pd["Designator"].str.contains(remove_rows[0])
            & ~csv_pd["Designator"].str.contains(remove_rows[1])
        ]
        # Print it so that we can check it at a glance on the terminal
        print(swapped_csv)
        # If it's a position file "CPL" output that, otherwise it's a BOM
        if "cpl" in path_to_spreadsheet:
            print("Updated_JLCPCB_CPL.csv")
            swapped_csv.to_csv("Updated_JLCPCB_CPL.csv")
        else:
            print("Updated_JLCPCB_BOM.csv")
            swapped_csv.to_csv("Updated_JLCPCB_BOM.csv")


if __name__ == "__main__":
    path_to_spreadsheet = sys.argv[1]
    arg = sys.argv[2]
    bom_assembly_update(path_to_spreadsheet, arg)
