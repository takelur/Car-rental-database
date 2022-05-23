from textwrap import dedent
from models.car_functions import add_car, edit_car, remove_car, search_car
from models.customer_functions import add_customer, edit_customer, remove_customer, search_customer
from models.rental_functions import add_rental, return_rental
from controllers.user_input import integer_input, string_input


# The main screen for the application
def main_menu(db_controller):
    print("Welcome to the Car-rental system!")
    exit_application = False

    while not exit_application:
        print(
            dedent(
                """
        Please select an option by entering the corresponding number:
        1. Customers
        2. Cars
        3. Rentals
        4. Search
        5. Import/export data
        6. Exit
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 7):
            if user_choice == 6:
                exit_application = True
                print("Thank you for using the Car-rental system!")
            elif user_choice == 1:
                customer_menu(db_controller)
            elif user_choice == 2:
                car_menu(db_controller)
            elif user_choice == 3:
                rental_menu(db_controller)
            elif user_choice == 4:
                search_menu(db_controller)
            elif user_choice == 5:
                import_export_menu()
        else:
            print("Your number is not in the menu range.")


# Submenu for doing changes to customers
def customer_menu(db_controller):
    exit_menu = False

    while not exit_menu:
        print(
            dedent(
                """
        What do you want to do with customers?
        1. Add new customer
        2. Edit existing customer
        3. Remove customer
        4. Return to main menu
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 5):
            if user_choice == 4:
                exit_menu = True
            elif user_choice == 1:
                add_customer(db_controller)
            elif user_choice == 2:
                edit_customer(db_controller)
            elif user_choice == 3:
                remove_customer(db_controller)
        else:
            print("Your number is not in the menu range.")


# Submenu for doing changes to cars
def car_menu(db_controller):
    exit_menu = False

    while not exit_menu:
        print(
            dedent(
                """
        What do you want to do with cars?
        1. Add new car
        2. Edit existing car
        3. Remove car
        4. Return to main menu
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 5):
            if user_choice == 4:
                exit_menu = True
            elif user_choice == 1:
                add_car(db_controller)
            elif user_choice == 2:
                edit_car(db_controller)
            elif user_choice == 3:
                remove_car(db_controller)
        else:
            print("Your number is not in the menu range.")


# Submenu for doing changes to rentals
def rental_menu(db_controller):
    exit_menu = False

    while not exit_menu:
        print(
            dedent(
                """
        What do you want to do with rentals?
        1. Assign a car to a customer
        2. Return a rented car
        3. Return to main menu
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 4):
            if user_choice == 3:
                exit_menu = True
            elif user_choice == 1:
                add_rental(db_controller)
            elif user_choice == 2:
                return_rental(db_controller)
        else:
            print("Your number is not in the menu range.")


# Submenu for importing and exporting data
def import_export_menu():
    exit_menu = False

    while not exit_menu:
        print(
            dedent(
                """
        Please select an option:
        1. Import data from CSV file
        2. Export data to CSV file
        3. Import data from JSON file
        4. Export data to JSON file
        5. Return to main menu
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 6):
            if user_choice == 5:
                exit_menu = True
            elif user_choice == 1:
                print("Importing from CSV file...")
            elif user_choice == 2:
                print("Exporting from CSV file...")
            elif user_choice == 3:
                print("Importing from JSON file...")
            elif user_choice == 4:
                print("Exporting from JSON file...")
        else:
            print("Your number is not in the menu range.")

def search_menu(db_controller):
    exit_menu = False

    while not exit_menu:
        print(
            dedent(
                """
        What do you want to search for?
        1. Customers
        2. Cars
        3. Go back.
        """
            )
        )

        # Makes sure that user inputs a number
        user_choice = integer_input("Enter your choice: ")

        # Makes sure the user enters a valid number
        if user_choice in range(1, 4):
            if user_choice == 3:
                exit_menu = True
            elif user_choice == 1:
                print("Searching for customers...")
                search_query = string_input("Please type your search query here: ")
                search_customer(db_controller, search_query)
            elif user_choice == 2:
                print("Searching for cars...")
                search_query = string_input("Please type your search query here: ")
                search_car(db_controller, search_query)
        else:
            print("Your number is not in the menu range.")