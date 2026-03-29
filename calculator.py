while True:
    print("\n--- Calculator ---")
    print("Operations: +  -  *  /  //  %  **")
    print("Type 'exit' to quit")

    try:
        num1 = input("\nEnter first number: ")
        if num1.lower() == 'exit':
            break

        op = input("Enter operator: ").strip()
        if op.lower() == 'exit':
            break

        num2 = input("Enter second number: ")
        if num2.lower() == 'exit':
            break

        num1 = float(num1)
        num2 = float(num2)

        if op == '+':
            result = num1 + num2
        elif op == '-':
            result = num1 - num2
        elif op == '*':
            result = num1 * num2
        elif op == '/':
            if num2 == 0:
                print("Error: Cannot divide by zero!")
                continue
            result = num1 / num2
        elif op == '//':
            if num2 == 0:
                print("Error: Cannot divide by zero!")
                continue
            result = num1 // num2
        elif op == '%':
            if num2 == 0:
                print("Error: Cannot divide by zero!")
                continue
            result = num1 % num2
        elif op == '**':
            result = num1 ** num2
        else:
            print(f"Error: Unknown operator '{op}'")
            continue

        # Clean output: show int if no decimal needed
        if result == int(result):
            print(f"\nResult: {int(num1)} {op} {int(num2)} = {int(result)}")
        else:
            print(f"\nResult: {num1} {op} {num2} = {result}")

    except ValueError:
        print("Error: Please enter valid numbers!")

print("Goodbye!")
