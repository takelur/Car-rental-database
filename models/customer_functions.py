from controllers.user_input import string_input
from controllers.user_input import phone_input
from controllers.user_input import year_input
from controllers.user_input import integer_input


def add_customer(db_controller):
    first_name = string_input("Enter first name (leave blank to cancel): ")
    if first_name is None:
        return
    last_name = string_input("Enter last name (leave blank to cancel): ")
    if last_name is None:
        return
    # Not using regex for email, too many email conventions to consider
    email = string_input("Enter email (leave blank to cancel): ")
    if email is None:
        return
    phone = phone_input("Enter phone number (leave blank to cancel): ")
    if phone is None:
        return
    birth_year = year_input("Enter birth year (leave blank to cancel): ")
    if birth_year is None:
        return

    # Checks if customer already exists
    customer = db_controller.execute_single_read_query(
        f"SELECT first_name, last_name, phone_number FROM customer "
        f"WHERE first_name = ? AND last_name = ? AND phone_number = ?",
        (first_name, last_name, phone)
    )
    if customer:
        print("Customer already exists")
        return

    # Inserting the data into the customer table
    db_controller.execute_query(
        f"INSERT INTO customer (first_name, last_name, email, phone_number, birth_year) "
        f"VALUES (?, ?, ?, ?, ?)",
        (first_name, last_name, email, phone, birth_year)
    )


def edit_customer(db_controller):
    # Return if there are no customers
    if list_customers(db_controller) == -10:
        return

    # Loops until a valid input is given
    while True:
        customer_id = integer_input("Enter customer ID (leave blank to cancel): ")
        if customer_id is None:
            return
        # First check if customer exists
        customer = db_controller.execute_single_read_query(
            f"SELECT first_name, last_name FROM customer WHERE customer_id = ?",
            (customer_id,)
        )

        if customer is None:
            print("There is no customer with that ID")
            continue
        else:
            first_name = string_input("Enter new first name (leave blank to cancel): ")
            if first_name is None:
                return
            last_name = string_input("Enter new last name (leave blank to cancel): ")
            if last_name is None:
                return
            email = string_input("Enter new email (leave blank to cancel): ")
            if email is None:
                return
            phone = phone_input("Enter new phone number (leave blank to cancel): ")
            if phone is None:
                return
            birth_year = year_input("Enter new birth year (leave blank to cancel): ")
            if birth_year is None:
                return

            # Updates the customer table
            db_controller.execute_query(
                f"UPDATE customer SET first_name = ?, last_name = ?, email = ?, phone_number = ?, "
                f"birth_year = ? WHERE customer_id = ?",
                (first_name, last_name, email, phone, birth_year, customer_id)
            )
            # Updates the rental table with the new last name and phone number
            db_controller.execute_query(
                f"UPDATE rental SET customer_last_name = ?, customer_phone_number = ? WHERE customer_id = ?",
                (last_name, phone, customer_id)
            )
            return


def remove_customer(db_controller):
    # Return if there are no customers
    if list_customers(db_controller) == -10:
        return

    # Loops until a valid input is given
    while True:
        customer_id = integer_input("Enter customer ID (leave blank to cancel): ")
        if customer_id is None:
            return
        else:
            # First checks if customer exists
            customer = db_controller.execute_single_read_query(
                f"SELECT first_name, last_name FROM customer WHERE customer_id = ?",
                (customer_id,)
            )
            if customer is None:
                print("There is no customer with that ID")
                return
            # Checks if there are no rentals for this customer, returns if there are rentals
            elif db_controller.execute_single_read_query(
                f"SELECT customer_id FROM rental WHERE customer_id = ?", (customer_id,)
            ):
                print("This customer has rentals that need to be returned first!")
                return
            else:
                # Deletes customer from the customer table
                db_controller.execute_query(
                    f"DELETE FROM customer WHERE customer_id = ?", (customer_id,)
                )
                # The next command deletes the rental history for this customer, the idea is that when cars are
                # returned the customers will not be removed by default. This is to keep the rental history in the
                # database. If the customer asks to be removed then the rental history also needs to be removed to
                # delete everything identifying this customer to comply with the law.
                db_controller.execute_query(
                    f"DELETE FROM rental WHERE customer_id = ?", (customer_id,)
                )
                print(
                    f"Customer {customer[0]} {customer[1]} has been removed"
                )  # first_name and last_name
                return


def list_customers(db_controller):
    customers = db_controller.execute_read_query(
        "SELECT customer_id, first_name, last_name FROM customer", ()
    )
    if customers:
        print("Current customers:")
        print("---------------------------------------------------")
        print("ID | Name")
        for customer in customers:
            print(f"{customer[0]}: {customer[1]} {customer[2]}")
        print("---------------------------------------------------")
    else:
        print("There are no customers")
        return -10


# This is not a very efficient way to search (everything is partial search), but considering this program is for
# a small car rental company it is highly unlikely the database will get extremely large. Therefore the user is
# prioritized and the program will allow partial searches for more results.
def search_customer(db_controller, search_query):
    customers = db_controller.execute_read_query(
        "SELECT customer_id, first_name, last_name, email, phone_number, birth_year FROM customer "
        "WHERE first_name LIKE ('%' || ? || '%') OR last_name LIKE ('%' || ? || '%') OR email LIKE ('%' || ? || '%') "
        "OR phone_number LIKE ('%' || ? || '%') OR birth_year LIKE ('%' || ? || '%')",
        (search_query, search_query, search_query, search_query, search_query)
    )
    if len(customers) == 0:
        print("Match not found")
        return
    else:
        print("Match found: ")
        print("---------------------------------------------------")
        print("ID | Name | E-mail | Phone number | Birth year")
        for customer in customers:
            print(
                f"{customer[0]}: {customer[1]} {customer[2]} | {customer[3]} | {customer[4]} | {customer[5]}"
            )
        print("---------------------------------------------------")
        return
