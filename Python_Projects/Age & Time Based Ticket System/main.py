age = int(input("Enter your age: "))
time =(input("Enter time of day (Morning / Afternoon / Evening) :")).capitalize()
if age <= 12:
    if time == "Morning":
        price = 100
    elif time == "Afternoon":
        price = 120
    else:
        price = 150
elif age <=18:
    if time == "Morning":
        price = 150
    elif time == "Afternoon":
        price = 170
    else:
        price = 200
else:
    if time == "Morning":
        price = 200
    elif time == "Afternoon":
        price = 250
    else:
        price = 300     
print("Your Ticket Price Is $", price)        