def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def main():
    print("Banker's Algorithm")
    print("Deadlock Avoidance System")
    print("-------------------------")

    process_count = read_positive_integer(
        "Enter the number of processes: "
    )

    resource_count = read_positive_integer(
        "Enter the number of resource types: "
    )

    print("\nProject Setup")
    print(f"Number of processes: {process_count}")
    print(f"Number of resource types: {resource_count}")


if _name_ == "_main_":
    main()
