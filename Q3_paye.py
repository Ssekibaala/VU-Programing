"""
Question Three - URA PAYE Tax Assessment
A console programme that collects employee names and gross monthly
incomes, works out the PAYE due on each one using the URA monthly
tax bands, and prints a payroll summary for the tax officer.
"""

# URA monthly PAYE bands, in Uganda Shillings
BAND_1_TOP = 235000     # 0 per cent up to and including this figure
BAND_2_TOP = 335000     # 10 per cent up to and including this figure
BAND_3_TOP = 410000     # 20 per cent up to and including this figure
                        # anything above BAND_3_TOP is taxed at 30 per cent


# work out the PAYE rate that applies to one monthly income
def get_tax_rate(income: float) -> float:
    """
    Docstring: The function takes in one parameter, income, which is a
    gross monthly figure in Uganda Shillings
    It returns the tax rate as a decimal, for example 0.10 for 10 per cent
    It returns None if the income given is negative, since a negative
    income is not a figure the payroll can assess
    """
    # a negative income is invalid, so reject it rather than taxing it
    if income < 0:
        print("Income cannot be negative.")
        return None

    if income <= BAND_1_TOP:
        return 0.00        # tax free band
    elif income <= BAND_2_TOP:
        return 0.10        # low income band
    elif income <= BAND_3_TOP:
        return 0.20        # middle income band
    else:
        return 0.30        # high income band


# collect the name and gross income of every employee
def enter_employees() -> tuple:
    """
    Docstring: The function takes in no parameters
    It asks how many employees are on the payroll, then collects a name
    and a gross monthly income for each one, re-prompting whenever the
    income entered is negative or is not a number
    It returns two lists, names and incomes
    """
    names = []
    incomes = []

    # keep asking until a whole number greater than zero is given
    while True:
        try:
            count = int(input("How many employees? "))
            if count > 0:
                break
            print("Enter a number greater than zero.")
        except ValueError:
            print("Enter a whole number.")

    for position in range(1, count + 1):
        print(f"\nEmployee {position}")
        name = input("  Name: ").strip()

        # keep asking until the income is a number that is not negative
        while True:
            raw_income = input("  Gross monthly income (UGX): ").strip()
            try:
                income = float(raw_income)
                if income >= 0:
                    break
                print("  Income cannot be negative. Try again.")
            except ValueError:
                print("  Enter a number for the income. Try again.")

        names.append(name)
        incomes.append(income)

    return names, incomes


# print the payroll table and the summary figures beneath it
def display_payroll(names: list, incomes: list) -> None:
    """
    Docstring: The function takes in two parameters, names and incomes
    It prints each employee's gross income, tax rate and tax payable in
    a table, then the total tax collected, the highest and lowest
    incomes, and how many employees fall in the tax free band
    It returns nothing
    """
    if not names:
        print("\nNo employees were entered.")
        return

    header = f"{'Name':<20}{'Gross (UGX)':>15}{'Rate':>8}{'Tax (UGX)':>15}"
    print("\n" + header)
    print("-" * len(header))

    total_tax = 0.0
    tax_free_count = 0

    for name, income in zip(names, incomes):
        # get_tax_rate() is reused here so the band rule lives in one place
        rate = get_tax_rate(income)
        tax = income * rate
        total_tax += tax

        # anyone on a rate of zero is sitting in the tax free band
        if rate == 0.00:
            tax_free_count += 1

        print(
            f"{name:<20}{income:>15,.0f}"
            f"{rate * 100:>7.0f}%{tax:>15,.0f}"
        )

    print("-" * len(header))
    print(f"{'Total tax collected:':<30}{total_tax:>12,.0f} UGX")
    print(f"{'Highest income:':<30}{max(incomes):>12,.0f} UGX")
    print(f"{'Lowest income:':<30}{min(incomes):>12,.0f} UGX")
    print(f"{'Employees in tax free band:':<30}{tax_free_count:>12}")


# run the two stages of the programme in order
def main() -> None:
    """
    Docstring: The function takes in no parameters
    It collects the employee details, then displays the payroll
    It returns nothing
    """
    print("URA PAYE ASSESSMENT")
    names, incomes = enter_employees()
    display_payroll(names, incomes)


# guard so main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
