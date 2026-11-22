def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def read_resource_vector(prompt, count):
    while True:
        try:
            values = [
                int(value)
                for value in input(prompt).replace(",", " ").split()
            ]

            if len(values) != count:
                print(f"Please enter exactly {count} values.")
                continue

            if any(value < 0 for value in values):
                print("Resource amounts cannot be negative.")
                continue

            return values

        except ValueError:
            print("Enter whole numbers separated by spaces or commas.")


def read_allocation_matrix(processes, resources):
    allocation = []

    print("\nEnter the Allocation Matrix.")
    print("Enter resource amounts in this order:", ", ".join(resources))

    for process in processes:
        row = read_resource_vector(
            f"{process} allocation: ",
            len(resources)
        )
        allocation.append(row)

    return allocation


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

    processes = [f"P{i}" for i in range(process_count)]
    resources = []

    for i in range(resource_count):
        default_name = chr(65 + i) if i < 26 else f"R{i + 1}"
        name = input(
            f"Enter name for resource {i + 1} [{default_name}]: "
        ).strip()
        resources.append(name or default_name)

    print("\nEnter the total amount of each resource.")
    print("Resource order:", ", ".join(resources))

    total_resources = read_resource_vector(
        "Total resource vector: ",
        resource_count
    )

    allocation = read_allocation_matrix(processes, resources)

    print("\nProject Setup")
    print("Processes:", ", ".join(processes))
    print("Resources:", ", ".join(resources))
    print("Total resource vector:", total_resources)

    print("\nAllocation Matrix")
    print(f"{'Process':<10}", end="")
    for resource in resources:
        print(f"{resource:>8}", end="")
    print()

    for process, row in zip(processes, allocation):
        print(f"{process:<10}", end="")
        for amount in row:
            print(f"{amount:>8}", end="")
        print()


if __name__ == "__main__":
    main()
