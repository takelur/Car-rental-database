from controllers.user_input import string_input
from controllers.user_input import integer_input
from controllers.user_input import plate_input

import sys


def add_car(db_controller):
    make = string_input("Enter the make of the car (leave blank to cancel): ")
    if make is None:
        return
    model = string_input("Enter the model of the car (leave blank to cancel): ")
    if model is None:
        return
    plate = plate_input("Enter the plate of the car (leave blank to cancel): ")
    if plate is None:
        return
    year = integer_input("Enter the year of the car (leave blank to cancel): ")
    if year is None:
        return
    color = string_input("Enter the color of the car (leave blank to cancel): ")
    if color is None:
        return
    mileage = integer_input("Enter the mileage of the car (leave blank to cancel): ")
    if mileage is None:
        return

    # Inserting data this way to ensure fields are inserted as data and not commands
    db_controller.execute_query(
        f"INSERT INTO car (make, model, plate, year, color, mileage) VALUES (?, ?, ?, ?, ?, ?)",
        (make, model, plate, year, color, mileage),
    )


def edit_car(db_controller):
    list_cars(db_controller)
    while True:
        car_id = integer_input("Enter the ID of the car you want to edit (leave blank to cancel): ")
        if car_id is None:
            return
        else:
            # First check if it exists
            car = db_controller.execute_single_read_query(
                f"SELECT make, model, plate FROM car WHERE car_id = ?", (car_id,)
            )
            if car is None:
                print("There is no car with that ID.")
            else:
                make = string_input("Enter the new make of the car (leave blank to cancel): ")
                if make is None:
                    return
                model = string_input("Enter the new model of the car (leave blank to cancel): ")
                if model is None:
                    return
                plate = plate_input("Enter the new plate of the car (leave blank to cancel): ")
                if plate is None:
                    return
                year = integer_input("Enter the new year of the car (leave blank to cancel): ")
                if year is None:
                    return
                color = string_input("Enter the new color of the car (leave blank to cancel): ")
                if color is None:
                    return
                mileage = integer_input("Enter the new mileage of the car (leave blank to cancel): ")
                if mileage is None:
                    return

                db_controller.execute_query(
                    f"UPDATE car SET make = ?, model = ?, plate = ?, "
                    f"year = ?, color = ?, mileage = ? WHERE car_id = ?",
                    (make, model, plate, year, color, mileage, car_id),
                )
                return


def remove_car(db_controller):
    list_cars(db_controller)
    while True:
        car_id = integer_input("Enter the ID of the car you want to remove (leave blank to cancel): ")
        if car_id is None:
            return
        else:
            # First check if it exists
            car = db_controller.execute_single_read_query(
                f"SELECT make, model, plate, year FROM car WHERE car_id = ?", (car_id,)
            )
            if car is None:
                print("There is no car with that ID.")
            else:
                db_controller.execute_query(f"DELETE FROM car WHERE car_id = ?", (car_id,))
                print(
                    f"Deleted {car[3]} model {car[0]} {car[1]}, {car[2]}."
                )  # year, make, model, plate


def list_cars(db_controller):
    cars = db_controller.execute_read_query(
        f"SELECT car_id, make, model, plate FROM car", ()
    )

    print("ID\t| Make | Model | Plate")
    for car in cars:
        print(f"{car[0]}\t{car[1]} {car[2]} {car[3]}")


def list_available_cars(db_controller):
    cars = db_controller.execute_read_query(
        f"SELECT car_id, make, model, plate FROM car WHERE available = 1", ()
    )
    if cars:
        print("Available cars: ")
        print("ID\t| Make | Model | Plate")
        for car in cars:
            print(f"{car[0]}\t{car[1]} {car[2]} {car[3]}")
    else:
        print("There are no available cars.")
        return -10
