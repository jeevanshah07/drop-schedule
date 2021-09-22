import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-e',
                    '--edit',
                    help='edit your schedule',
                    action="store_true")
parser.add_argument('-d',
                    '--day',
                    type=int,
                    choices=[1, 2, 3, 4],
                    help='day',
                    required=False)
args = parser.parse_args()


def save_schedule(cur, db) -> list:
    cur.execute("DELETE FROM schedule")
    db.commit()

    p1 = input("What is your first period class? ")
    p2 = input("What is your second period class? ")
    p3 = input("What is your third period class? ")
    p4 = input("What is your fourth period class? ")
    p5 = input("What is your fifth period class? ")
    p6 = input("What is your sixth period class? ")
    p7 = input("What is your seventh period class? ")
    p8 = input("What is your eighth period class? ")

    schedule = [p1, p2, p3, p4, p5, p6, p7, p8]

    for classname in schedule:
        sqlInsert = "INSERT INTO schedule (classname) VALUES (?)"
        cur.execute(sqlInsert, (classname, ))
        db.commit()

    return schedule


def fetch_schedule(cur) -> list:
    schedule = []
    sqlInsert = "SELECT * FROM schedule"
    cur.execute(sqlInsert)
    c = list(cur.fetchall())
    for i in c:
        schedule.append(i[0])

    return schedule


def print_schedule(schedule_list: list) -> None:
    for idx, class_name in enumerate(schedule_list):
        print("Block #{}: {} ".format(idx, class_name))


def order_schedule(schedule: list, order: list) -> None:
    schedule = [
        schedule[order[0]], schedule[order[1]], schedule[order[2]],
        schedule[order[3]], schedule[order[4]], schedule[order[5]]
    ]

    print_schedule(schedule)

def main():
    db = sqlite3.connect('data/schedule.db')
    cur = db.cursor()

    schedule = fetch_schedule(cur)

    if not schedule or args.edit:
        schedule = save_schedule(cur, db)

    if args.day:
        day = int(args.day)
    else:
        day = int(input("What day is today?: "))

    if day == 1:
        order_schedule(schedule, order=[0, 1, 2, 4, 5, 6])
    elif day == 2:
        order_schedule(schedule, order=[1, 2, 3, 5, 6, 7])

    elif day == 3:
        order_schedule(schedule, order=[2, 3, 0, 6, 7, 4])

    elif day == 4:
        order_schedule(schedule, order=[3, 0, 1, 7, 4, 5])

if __name__ == '__main__':
    main()
