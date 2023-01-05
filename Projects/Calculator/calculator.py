def add(num1 , num2):
    return (num1 + num2)

def subtract(num1 , num2):
    return (num1 - num2)

def multiply(num1 , num2):
    return (num1 * num2)

def divide(num1 , num2):
    return (num1 / num2)

num1 = float(input("Enter Number 1: "))
op = input("Enter operator: ")
num2 = float(input("Enter Number 2: "))

if (op == "+"):
    print(add(num1 , num2))
elif (op == "-"):
    print(subtract(num1 , num2))
elif (op == "*"):
    print(multiply(num1 , num2))
elif (op == "/"):
    print(divide(num1 , num2))
else: print("Invalid Operator")
