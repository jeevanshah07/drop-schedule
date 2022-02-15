"""
Set, create, edit, and view, the schedule
"""
# Imports
import sqlite3
import argparse

# Get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--edit", help="edit your schedule", action="store_true")
parser.add_argument(
    "-d", "--day", type=int, choices=[1, 2, 3, 4], help="day", required=False
)

# Save the passed in arguments
args = parser.parse_args()


def save_schedule(cur: sqlite3.Cursor, db: sqlite3.Connection) -> list[str]:
    """
    Saves an inputted schedule

    Args:
        cur: A sqlite3.Cursor instance used to edit the database
        db: A sqlite3.Connection instance that is used to hold data

    Returns:
        A list of strings that contains the new schedule
    """

    # Remove anything that's already saved
    cur.execute("DELETE FROM schedule")
    db.commit()  # Commit changes to the data base

    # Take input to store as the schedule
    p1 = input("What is your first period class? ")
    p2 = input("What is your second period class? ")
    p3 = input("What is your third period class? ")
    p4 = input("What is your fourth period class? ")
    p5 = input("What is your fifth period class? ")
    p6 = input("What is your sixth period class? ")
    p7 = input("What is your seventh period class? ")
    p8 = input("What is your eighth period class? ")

    # Save input as a list
    schedule = [p1, p2, p3, p4, p5, p6, p7, p8]

    # Iterate through the schedule list and save each class in the sqlite3 database
    for classname in schedule:
        sql_insert = "INSERT INTO schedule (classname) VALUES (?)"
        cur.execute(sql_insert, (classname,))
        db.commit()

    # Return the schedule list
    return schedule


def fetch_schedule(cur: sqlite3.Cursor) -> list:
    """
    Retrieves a set schedule from an sqlite3 database

    Args:
        cur: A sqlite3.Cursor instance used to retrieve data from the sqlite3 database

    Returns:
        A list containing the saved schedule
    """
    schedule = []  # Initalize a new empty list
    sql_insert = "SELECT * FROM schedule"  # Store the sql code to run, good practice to prevent sql injection

    # Execute, save, and return the results of the sql code
    cur.execute(sql_insert)
    c = list(cur.fetchall())
    for i in c:
        schedule.append(i[0])

    return schedule


def print_schedule(schedule_list: list[str]) -> None:
    """
    Outputs the schedule in a nice and formatted way

    Args:
        schedule_list: A list of strings containing the schedule
    """
    # Iterate through the list and output the block number and class name
    for idx, class_name in enumerate(schedule_list):
        idx += 1
        print(f"Block #{idx}: {class_name}")


def order_schedule(schedule: list[str], order: list[int]) -> None:
    """
    Orders the schedule based on input

    Args:
        schedule: A list of strings that holds the schedule
        order: A list of integers that has what order the schedule should be ordered in
    """
    # Reorder schedule based on the numbers in the order param
    schedule = [
        schedule[order[0]],
        schedule[order[1]],
        schedule[order[2]],
        schedule[order[3]],
        schedule[order[4]],
        schedule[order[5]],
    ]

    print_schedule(schedule)  # Print out the newly ordered schedule


def main():
    """The main function, executes all the needed code and functions"""

    # Initalize a database connection and database cursor
    db = sqlite3.connect("data/schedule.db")
    cur = db.cursor()

    # Try to get the saved schedule
    schedule = fetch_schedule(cur)

    # If there is no saved schedule or the edit arg is passed in...
    if not schedule or args.edit:
        schedule = save_schedule(cur, db)  # ...Save a new schedule

    # If the day is explicitly passed in save it, else ask for the day number
    if args.day:
        day = int(args.day)
    else:
        day = int(input("What day is today?: "))

    # Based on the day number order the schedule (which also prints it out)
    if day == 1:
        order_schedule(schedule, order=[0, 1, 2, 4, 5, 6])
    elif day == 2:
        order_schedule(schedule, order=[1, 2, 3, 5, 6, 7])

    elif day == 3:
        order_schedule(schedule, order=[2, 3, 0, 6, 7, 4])

    elif day == 4:
        order_schedule(schedule, order=[3, 0, 1, 7, 4, 5])


if __name__ == "__main__":
    main()
