"""
Question Five (c) - process_withdrawal() with exception handling
This version accepts the amount in whatever form the user typed it and
converts it inside the function, so text such as 'fifty thousand' is
rejected politely instead of crashing the programme.
"""

FEE_THRESHOLD = 50000    # a fee is only charged above this amount
FEE_RATE = 0.02          # 2 per cent


# work out the fee and the resulting balance, validating the amount first
def process_withdrawal(balance: float, amount) -> tuple:
    """
    Docstring: The function takes in two parameters, balance and amount
    The amount may arrive as text, so it is converted inside a try block
    It charges 2 per cent on any withdrawal above 50,000 UGX and checks
    the customer can cover the amount together with that fee
    It returns four values: whether the withdrawal went through, the
    amount as a number, the fee charged and the resulting balance
    """
    # float() raises ValueError on text such as 'fifty thousand' and
    # TypeError on a value such as None, so both are caught here
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        print("Invalid amount. Enter the withdrawal as a number, for example 50000.")
        return False, 0.0, 0.0, balance

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
