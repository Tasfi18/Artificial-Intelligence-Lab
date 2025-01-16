import random
import datetime


def VacuumSucker(location, status, count, cleaned):
    if status[location] == "dirty":
        status[location] = "clean"
        print(f"cleaning {location}")
        cleaned = cleaned + 1
        print(f"Status: {status}")
        count = count + 1
    if location == "A":
        location = "B"
        print(f"Moving to {location}")
        count = count + 1
    else:
        location = "A"
        print(f"Moving to {location}")
        count = count + 1
    return count, cleaned

loc = ["A", "B"]
stat = ["clean", "dirty"]
time = 5
count = 0
cleaned = 0

for i in range(1000):
    location = random.choice(loc)
    status = {"A": random.choice(stat), "B": random.choice(stat)}
    count, cleaned = VacuumSucker(location, status, count, cleaned)
print(f"Count : {count} Cleaned : {cleaned}")

print(f"Performance = {count/cleaned}")