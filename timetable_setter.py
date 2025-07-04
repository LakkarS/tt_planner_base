import sys
from itertools import pairwise
import random
from tabulate import tabulate

def use_preset(n):
    global slots, days, classes, n_classes_day, n_working_days, n_classes_week, subjects
    if n==0:        
        slots = {
            "1": "8:30-9:10",
            "2": "9:10-9:50",
            "Break": "9:50-10:30",
            "3": "10:30-11:10",
            "4": "11:10-11:50",
            "5": "11:50-12:30",
        }

        days = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
        }

        subjects = {
            "Maths": 5,
            "English": 3,
            "Science": 5,
            "Social Studies": 3,
            "Hindi": 5,
            "Comp Sc": 2,
            "Physical Education": 2,
        }

        classes = {key:value for key, value in slots.items() if key.isnumeric()}
        n_classes_day = len(classes)
        n_working_days = 5
        n_classes_week = n_classes_day * n_working_days
    
    elif n==1:
        slots = {
            "1": "8:15-8:55",
            "2": "8:55-9:35",
            "Break": "9:35-9:50",
            "3": "9:50-10:30",
            "4": "10:30-11:05",
            "5": "11:05-11:45",
            "6": "11:45-12:30",
            "Break": "12:30-12:55",
            "7": "12:55-1:35",
            "8": "1:35-2:10",
            "9": "2:10-2:50",
        }

        days = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
        }

        subjects = {
            "Maths": 7,
            "English": 5,
            "Physics": 4,
            "Chemistry": 4,
            "Biology": 4,
            "History & Civics": 3,
            "Geography": 3,
            "Hindi": 5,
            "Comp Sc": 3,
            "Physical Education": 2,
            "Art": 1,
            "Music": 1,
            "Dance": 1,
            "VE": 1,
            "GK": 1,
        }

        classes = {key:value for key, value in slots.items() if key.isnumeric()}
        n_classes_day = len(classes)
        n_working_days = 5
        n_classes_week = n_classes_day * n_working_days

    elif n==2:
        slots = {
            "1": "8:15-8:55",
            "2": "8:55-9:35",
            "Break": "9:35-9:50",
            "3": "9:50-10:30",
            "4": "10:30-11:05",
            "5": "11:05-11:45",
            "6": "11:45-12:30",
            "Break": "12:30-12:55",
            "7": "12:55-1:35",
            "8": "1:35-2:10",
            "9": "2:10-2:50",
        }

        days = {
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
        }

        subjects = {
            "Maths": 6,
            "English": 4,
            "Physics": 3,
            "Physics Lab": 2,
            "Chemistry": 3,
            "Chemistry Lab": 2,
            "Biology": 3,
            "Biology Lab": 2,
            "History & Civics": 3,
            "Geography": 3,
            "Hindi": 5,
            "Comp Sc": 1,
            "Comp Sc Lab": 2,
            "Physical Education": 2,
            "Art": 1,
            "Music": 1,
            "Dance": 1,
            "GK": 1,
        }

        classes = {key:value for key, value in slots.items() if key.isnumeric()}
        n_classes_day = len(classes)
        n_working_days = 5
        n_classes_week = n_classes_day * n_working_days

def print_tt():
    global slots
    heads = [" "] + [x for x in slots.keys() if "break" not in x.lower()]
    table = []
    for day, slots in tt.items():
        a = [day[0]] + [list(x.values())[0] for x in slots]
        table.append(a)
    print(tabulate(table, headers=heads, tablefmt="simple_grid"))

def reset_tt():
    for day, slots in tt.items():
        for slot in slots:
            slot[list(slot.keys())[0]] = None

def get_classes(day: str):
    d = tt[day]
    return [y[str(x+1)] for x, y in enumerate(d)]

def assign_classes():
    one_per_day = False

    for subject, count in subjects.items():
        # print(f"{subject}: {count} classes per week")
        if "lab" in subject.lower():
            # print(f"  {subject} is a lab subject, assigning block slots.")
            one_per_day = False
            block_classes = count//2
        elif count > n_classes_week:
            raise ValueError(f"Subject {subject} has more classes than available slots in the week.")
        elif count > n_working_days:
            one_per_day = True
            block_classes = count - n_working_days
            # print(f"  {subject} requires at least one class per day.")
            pass
        elif count == n_working_days:
            one_per_day = True
            block_classes = 0
            # print(f"  {subject} can be scheduled once per day.")
            pass
        elif count < n_working_days:
            one_per_day = False
            block_classes = 0
            # print(f"  {subject} can be scheduled few times in a week.")
            pass
        
        if one_per_day:
            # print(f"  Assigning {subject} to one slot per day.")
            if block_classes:
                print(f"  {subject} requires {block_classes} block classes.")
                # print(list(pairwise(get_classes("Monday"))))
                selectable_days = [x for x in days.keys() if (None, None) in list(pairwise(get_classes(days[x])))]
                block_days = random.sample(selectable_days, block_classes)
                # print(selectable_days)
                for day in days:
                    while True:
                        if day in block_days:
                            that_day = get_classes(days[day])
                            avbl = [x for x in range(len(that_day)-1) if that_day[x:x+2] == [None, None]]
                            slot = random.choice(avbl)
                            tt[days[day]][int(slot)][str(slot+1)] = subject
                            count -= 1
                            tt[days[day]][int(slot)+1][str(slot+2)] = subject
                            count -= 1
                            break
                        else:
                            slot = random.choice(list(classes.keys()))
                            if tt[days[day]][int(slot)-1][slot] is None:
                                tt[days[day]][int(slot)-1][slot] = subject
                                count -= 1
                                break
            else:
                for day in days:
                    while True:
                        avbl_slots = [x for x in classes.keys() if tt[days[day]][int(x)-1][x] is None]
                        if not avbl_slots:
                            raise ValueError(f"No available slots for {subject} on {days[day]}.")
                        slot = random.choice(avbl_slots)
                        if tt[days[day]][int(slot)-1][slot] is None:
                            tt[days[day]][int(slot)-1][slot] = subject
                            count -= 1
                            break
                        else:
                            raise ValueError(f"Slot for {subject} not")
        else:
            if block_classes:
                selectable_days = [x for x in days.keys() if (None, None) in list(pairwise(get_classes(days[x])))]
                if len(selectable_days) < block_classes//2:
                    raise ValueError(f"Not enough days available for block classes of {subject}.")
                selected_days = random.sample(selectable_days, block_classes)
                for day in selected_days:
                    while True:
                            that_day = get_classes(days[day])
                            avbl = [x for x in range(len(that_day)-1) if that_day[x:x+2] == [None, None]]
                            slot = random.choice(avbl)
                            tt[days[day]][int(slot)][str(slot+1)] = subject
                            count -= 1
                            tt[days[day]][int(slot)+1][str(slot+2)] = subject
                            count -= 1
                            break
            else:
                try:
                    selected_days = random.sample([x for x in days.keys() if None in get_classes(days[x])], count)
                except ValueError:
                    raise ValueError(f"Not enough days available to assign {subject} classes.")
                for day in selected_days:
                    while True:
                        slot = random.choice([x for x in classes.keys() if None in get_classes(days[day])])
                        if tt[days[day]][int(slot)-1][slot] is None:
                            tt[days[day]][int(slot)-1][slot] = subject
                            break

use_preset(2)

if sum(subjects.values()) != n_classes_week:
    print(f"Total classes per week: {sum(subjects.values())}, Expected: {n_classes_week}")
    raise ValueError("Total classes per week does not match the expected number of classes.")

tt = {}
for day in range(n_working_days):
    tt[days[day+1]] = []
    for slot in classes:
        tt[days[day+1]].append({slot: None})
# {<day>:[{<slot>: None}]}

# sys.exit(0)

while True:
    try:
        assign_classes()
        break
    except ValueError as e:
        print(f"Error: {e}")
        reset_tt()
        print("Reassigning classes...")
    except KeyboardInterrupt as e:
        print("Exiting...")
        raise e

print_tt()
# print(tt)
