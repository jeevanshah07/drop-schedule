import sqlite3


def save_schedule(schedule_list: list, cur, db) -> None:
    for classname in schedule_list:
        sqlInsert = "INSERT INTO schedule (classname) VALUES (?)"
        cur.execute(sqlInsert, (classname, ))
        db.commit()


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


db = sqlite3.connect('data/schedule.db')
cur = db.cursor()

schedule = fetch_schedule(cur)

if not schedule:
    p1 = input("What is your first period class? ")
    p2 = input("What is your second period class? ")
    p3 = input("What is your third period class? ")
    p4 = input("What is your fourth period class? ")
    p5 = input("What is your fifth period class? ")
    p6 = input("What is your sixth period class? ")
    p7 = input("What is your seventh period class? ")
    p8 = input("What is your eighth period class? ")

    schedule = [p1, p2, p3, p4, p5, p6, p7, p8]

    save_schedule(schedule, cur, db)

schedule = fetch_schedule(cur)

day = int(input("What day is today?: "))
if day == 1:
    schedule = [
        schedule[0], schedule[1], schedule[2], schedule[4], schedule[5],
        schedule[6]
    ]
    print_schedule(schedule)
elif day == 2:
    schedule = [
        schedule[1], schedule[2], schedule[3], schedule[5], schedule[6],
        schedule[7]
    ]
    print_schedule(schedule)

elif day == 3:
    schedule = [
        schedule[2], schedule[3], schedule[0], schedule[6], schedule[7],
        schedule[4]
    ]
    print_schedule(schedule)

elif day == 4:
    schedule = [
        schedule[3], schedule[0], schedule[1], schedule[7], schedule[4],
        schedule[5]
    ]
    print_schedule(schedule)
