# Banker's Algorithm
# Main program

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


def read_matrix(title, processes, resources):
    matrix = []

    print(f"\nEnter the {title} Matrix.")
    print("Resource order:", ", ".join(resources))

    for process in processes:
        row = read_resource_vector(
            f"{process}: ",
            len(resources)
        )
        matrix.append(row)

    return matrix


def calculate_need(maximum, allocation):
    need = []

    for i in range(len(maximum)):
        row = []

        for j in range(len(maximum[i])):
            row.append(maximum[i][j] - allocation[i][j])

        need.append(row)

    return need


def display_matrix(title, matrix, processes, resources):
    print(f"\n{title}")
    print(f"{'Process':<10}", end="")

    for resource in resources:
        print(f"{resource:>8}", end="")

    print()

    for process, row in zip(processes, matrix):
        print(f"{process:<10}", end="")

        for value in row:
            print(f"{value:>8}", end="")

        print()


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

    total_resources = read_resource_vector(
        f"Total vector ({', '.join(resources)}): ",
        resource_count
    )

    allocation = read_matrix("Allocation", processes, resources)
    maximum = read_matrix("Maximum Claim (Max)", processes, resources)

    # Validate that allocation does not exceed maximum claim.
    for i in range(process_count):
        for j in range(resource_count):
            if allocation[i][j] > maximum[i][j]:
                print(
                    f"Error: Allocation for {processes[i]} "
                    f"exceeds its maximum claim for {resources[j]}."
                )
                return

    need = calculate_need(maximum, allocation)

    print("\nTotal Resources:", total_resources)

    display_matrix("ALLOCATION MATRIX", allocation, processes, resources)
    display_matrix("MAXIMUM CLAIM MATRIX", maximum, processes, resources)
    display_matrix("NEED MATRIX (Max - Allocation)", need, processes, resources)


if _name_ == "_main_":
    main()
