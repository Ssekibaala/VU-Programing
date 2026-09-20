"""
Question Four - Kampala City Traders Stock Records
Reads product records from stock.txt, reports the products that have
fallen below a stock threshold, and writes the records back to file.

Each line of stock.txt holds one record:
    ProductCode,Name,Category,Quantity,UnitPrice
"""

import csv


# read every product record from the file into a list of dictionaries
def load_stock(filename: str) -> list:
    """
    Docstring: The function takes in one parameter, filename
    It reads each record from the file and stores it as a dictionary
    with the keys product_code, name, category, quantity and unit_price
    It returns a list of those dictionaries, or an empty list if the
    file is missing or cannot be read
    """
    products = []

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                # skip blank lines rather than treating them as records
                if not line:
                    continue

                parts = line.split(",")

                # a complete record has exactly five fields
                if len(parts) != 5:
                    print(f"Line {line_number} skipped, wrong number of fields.")
                    continue

                # ValueError is caught per record so that one damaged
                # line does not stop the rest of the file from loading
                try:
                    product = {
                        "product_code": parts[0].strip(),
                        "name": parts[1].strip(),
                        "category": parts[2].strip(),
                        "quantity": int(parts[3].strip()),
                        "unit_price": float(parts[4].strip()),
                    }
                except ValueError:
                    print(f"Line {line_number} skipped, quantity or price is not a number.")
                    continue

                products.append(product)

    except FileNotFoundError:
        print(f"The file {filename} was not found. No records loaded.")
    except ValueError as error:
        print(f"A value in {filename} could not be converted: {error}")
    except Exception as error:
        print(f"Unexpected error while reading {filename}: {error}")

    return products


# list every product that has dropped below the given quantity
def find_low_stock(products: list, threshold: int) -> None:
    """
    Docstring: The function takes in two parameters, products (a list of
    dictionaries) and threshold (a quantity)
    It prints the details of every product held in a quantity below the
    threshold, or a message if there are none
    It returns nothing
    """
    low_stock = [p for p in products if p["quantity"] < threshold]

    if not low_stock:
        print(f"\nNo product is below {threshold} units.")
        return

    header = (
        f"{'Code':<8}{'Name':<18}{'Category':<15}"
        f"{'Qty':>6}{'Unit Price':>14}"
    )

    print(f"\nProducts below {threshold} units")
    print(header)
    print("-" * len(header))

    for product in low_stock:
        print(
            f"{product['product_code']:<8}{product['name']:<18}"
            f"{product['category']:<15}{product['quantity']:>6}"
            f"{product['unit_price']:>14,.2f}"
        )

    print("-" * len(header))
    print(f"{len(low_stock)} product(s) need restocking.")


# write the list of products back to the file in CSV format
def save_records(filename: str, products: list) -> bool:
    """
    Docstring: The function takes in two parameters, filename and
    products (a list of dictionaries)
    It writes every product back to the file in comma separated format
    It returns True if the write succeeded and False if it did not
    """
    try:
        # the with statement closes the file automatically, even if an
        # error is raised part way through writing
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            for product in products:
                writer.writerow([
                    product["product_code"],
                    product["name"],
                    product["category"],
                    product["quantity"],
                    product["unit_price"],
                ])

        print(f"\n{len(products)} record(s) saved to {filename}.")
        return True

    except OSError as error:
        print(f"\nCould not write to {filename}: {error}")
        return False


# load the stock, report what is running low, then save it back
def main() -> None:
    """
    Docstring: The function takes in no parameters
    It loads stock.txt, lists the products below a threshold of 20
    units, then writes the records back to file
    It returns nothing
    """
    products = load_stock("stock.txt")

    if not products:
        print("There is nothing to process.")
        return

    print(f"{len(products)} product(s) loaded from stock.txt.")
    find_low_stock(products, 20)
    save_records("stock.txt", products)


# guard so main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
