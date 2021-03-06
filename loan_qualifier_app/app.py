# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
from tracemalloc import stop
import fire
import questionary
from pathlib import Path
# Above we import the dependencies of this script from Modules that come with Anaconda

from qualifier.utils.fileio import load_csv, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value
# Above we import the dependencies of this script from Modules that came in the starter file or in the case of
# save_csv, was added in manually


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """
    # This gives us the list of loans and their requirements that we check our application against

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")
    # In the case of the filepath being incorrectly entered, the script will exit

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """
    # This function utilizes questionary as essentially a nicer UI version of the Input() function to gather
    # the data on the applicant for the loan. Lastly, it ensures the saved responses are in the right data type 
    # to be able to run a comparison on it against the loan's requirements

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """
    # From the Calculator file in Utils, these functions are imported to perform some basic calculations on the 
    # applicants inputs to get the ratios needed to compare to the banks' loan requirements

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    # Small modification manually added to take care of edge cases:
    if len(bank_data_filtered) > 0:
        print(f"Found {len(bank_data_filtered)} qualifying loans")
    else:
        print("Sorry, there are no loans available to you at the moment.")

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans):
    yn_save = questionary.confirm("Would you like to save the results in a CSV file?").ask()
    if yn_save == False:
        print("Thanks for using our software")
        sys.exit()
    else:
        csvpath = questionary.path("Perfect. Just input your absolute file path here (.csv):").ask()
        csvpath = Path(csvpath)

    return save_csv(qualifying_loans, csvpath)
    # Saves qualifying loans based on the inputed file path after confirming if the user wants to save the list of
    # loans that they qualify for
      
            


def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )
    # Decide whether or not to save and save based on a desired filepasth
    save_qualifying_loans(qualifying_loans)
    
 

if __name__ == "__main__":
    fire.Fire(run)
