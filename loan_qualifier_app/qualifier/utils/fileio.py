# -*- coding: utf-8 -*-
"""Helper functions to load ("load_csv") and save ("save_qualifying_loans") CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
from pathlib import Path

def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.

# Set the output header
    header = ["Lender - Loan Level", "Max Loan Amount", "Max LTV", "Max DTI","Min Credit Score","Interest Rate"]

    output_path = Path("qualifying_loans.csv")


    with open(output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        for row in qualifying_loans:
            csvwriter.writerow(row)


# Above, we call upon the imported modules to create the set-up and then run the set-up to save the filtered list of dictionaries (inexpensive_loans)
# and save that list into a CSV file by separating out each value in the dictionary as a comma-delineated value and showing the Keys as a header in the 1st row    # YOUR CODE HERE!


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data
