print("#Welcome to the calculator#\nCalculate how many time you lived and how many left till 90 years old.\n")
age = int(input("What is your current age? "))

if age >= 90:
    print("Sorry, Your time is over!☠️")
else:

    day = (90 * 365) - int(age) * 365
    week = (90 * 52) - int(age) * 52
    months = (90 * 12) - int(age) * 12
    # Days lived
    day_lived = int(age) * 365
    week_lived = int(age) * 52
    months_lived = int(age) * 12

    print(f"You have {day} days, {week} weeks, and {months} months left till 90 years old.\n")

    print(f"You already lived {day_lived} days, {week_lived} weeks, and {months_lived} months.")
