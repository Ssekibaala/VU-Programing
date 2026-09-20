"""
Question Five (b) - SACCO Withdrawal Processing
Corrected and improved version of the junior developer's programme.

It charges a 2 per cent fee on withdrawals above 50,000 UGX, checks
the customer can cover the amount plus the fee, prints a neatly
aligned transaction slip and saves that slip to slip.txt.
"""

FEE_THRESHOLD = 50000    # a fee is only charged above this amount
FEE_RATE = 0.02          # 2 per cent
SLIP_FILE = "slip.txt"


# work out the fee and the resulting balance for one withdrawal
def process_withdrawal(balance: float, amount: float) -> tuple:
    """
    Docstring: The function takes in two parameters, balance and amount
    It charges 2 per cent on any withdrawal above 50,000 UGX and checks
    that the customer can cover the amount together with that fee
    It returns four values: whether the withdrawal went through, the
    amount, the fee charged and the resulting balance
    """
    # a withdrawal of zero or less is not a real transaction
    if amount <= 0:
        print("The withdrawal amount must be greater than zero.")
        return False, amount, 0.0, balance

    fee = 0.0
    if amount > FEE_THRESHOLD:
        fee = amount * FEE_RATE

    total_deduction = amount + fee
    new_balance = balance - total_deduction

    # the customer must cover the amount and the fee, not just the amount
    if new_balance < 0:
        print("Insufficient funds.")
        return False, amount, 0.0, balance

    return True, amount, fee, new_balance


# build the transaction slip as one block of text with aligned labels
def build_slip(balance: float, amount: float, fee: float, new_balance: float) -> str:
    """
    Docstring: The function takes in four parameters, the original
    balance, the amount withdrawn, the fee charged and the new balance
    It returns the whole slip as a single string, so that the same text
    can be both printed and written to file
    """
    width = 44

    lines = [
        "*" * width,
        "SACCO TRANSACTION SLIP".center(width),
        "*" * width,
        f"{'Original Balance:':<24}{balance:>20,.2f}",
        f"{'Amount Withdrawn:':<24}{amount:>20,.2f}",
        f"{'Fee Charged:':<24}{fee:>20,.2f}",
        "-" * width,
        f"{'New Balance:':<24}{new_balance:>20,.2f}",
        "*" * width,
    ]

    # join the lines with newlines to make one printable block
    return "\n".join(lines)


# write the slip to file using a with statement
def save_slip(slip_text: str, filename: str = SLIP_FILE) -> bool:
    """
    Docstring: The function takes in two parameters, slip_text and
    filename, which defaults to slip.txt
    It writes the slip to the file, and the with statement closes that
    file automatically even if an error is raised during writing
    It returns True if the slip was saved and False if it was not
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(slip_text + "\n")

        print(f"\nSlip saved to {filename}.")
        return True

    except OSError as error:
        print(f"\nCould not save the slip: {error}")
        return False


# run one withdrawal from start to finish
def main() -> None:
    """
    Docstring: The function takes in no parameters
    It asks for the balance and the withdrawal amount, processes the
    withdrawal, then prints and saves the slip
    It returns nothing
    """
    balance = 100000.0
    print(f"Current balance: {balance:,.2f} UGX")

    # keep asking until the amount entered is a number
    while True:
        raw_amount = input("Enter amount to withdraw (UGX): ").strip()
        try:
            amount = float(raw_amount)
            break
        except ValueError:
            print("Enter the amount as a number, for example 60000.")

    succeeded, amount, fee, new_balance = process_withdrawal(balance, amount)

    if not succeeded:
        print("No withdrawal was made. The balance is unchanged.")
        return

    slip = build_slip(balance, amount, fee, new_balance)
    print()
    print(slip)
    save_slip(slip)


# guard so main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
