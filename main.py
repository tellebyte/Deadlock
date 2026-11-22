
# Banker's Algorithm
# Deadlock Avoidance System

def read_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Enter a whole number.")


def read_vector(prompt, count):
    while True:
        try:
            values = [
                int(value)
                for value in input(prompt).replace(",", " ").split()
            ]

            if len(values) != count:
                print(f"Enter exactly {count} values.")
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
        matrix.append(read_vector(f"{process}: ", len(resources)))

    return matrix


def calculate_need(maximum, allocation):
    return [
        [
            maximum[i][j] - allocation[i][j]
            for j in range(len(maximum[i]))
        ]
        for i in range(len(maximum))
    ]


def calculate_available(total, allocation):
    allocated_totals = [
        sum(row[j] for row in allocation)
        for j in range(len(total))
    ]

    available = [
        total[j] - allocated_totals[j]
        for j in range(len(total))
    ]

    return allocated_totals, available


def display_vector(title, values, resources):
    print(f"\n{title}")
    for resource, value in zip(resources, values):
        print(f"  {resource}: {value}")


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


def safety_check(allocation, need, available, processes, resources):
    work = available.copy()
    finish = [False] * len(processes)
    safe_sequence = []

    print("\n========== SAFETY CHECK ==========")
    display_vector("Initial Work", work, resources)

    while len(safe_sequence) < len(processes):
        found = False

        for i, process in enumerate(processes):
            if finish[i]:
                continue

            if all(
                need[i][j] <= work[j]
                for j in range(len(resources))
            ):
                print(f"\n{process} can finish.")

                # Release the resources held by the completed process.
                work = [
                    work[j] + allocation[i][j]
                    for j in range(len(resources))
                ]

                finish[i] = True
                safe_sequence.append(process)
                found = True

                display_vector("Updated Work", work, resources)
                break

        if not found:
            break

    if all(finish):
        print("\nRESULT: SAFE STATE")
        print("Safe sequence:", " -> ".join(safe_sequence))
        return True

    unfinished = [
        processes[i]
        for i, done in enumerate(finish)
        if not done
    ]

    print("\nRESULT: UNSAFE STATE")
    print("Processes unable to finish:", ", ".join(unfinished))
    return False


def check_resource_request(
    process_index, request, allocation, need,
    available, processes, resources
):
    process = processes[process_index]

    print(f"\n========== REQUEST CHECK FOR {process} ==========")

    # Rule 1: Request must not exceed the process's remaining Need.
    if any(
        request[j] > need[process_index][j]
        for j in range(len(resources))
    ):
        print("Request denied: it exceeds the process's remaining Need.")
        return

    print("Check 1 passed: Request does not exceed Need.")

    # Rule 2: Request must not exceed currently Available resources.
    if any(
        request[j] > available[j]
        for j in range(len(resources))
    ):
        print("Request cannot be granted now: insufficient resources.")
        return

    print("Check 2 passed: Requested resources are Available.")

    # Save the current state in case the request must be rejected.
    old_available = available.copy()
    old_allocation = [row.copy() for row in allocation]
    old_need = [row.copy() for row in need]

    # Temporarily grant the request.
    for j in range(len(resources)):
        available[j] -= request[j]
        allocation[process_index][j] += request[j]
        need[process_index][j] -= request[j]

    print("\nChecking safety after temporary allocation...")

    is_safe = safety_check(
        allocation, need, available, processes, resources
    )

    if is_safe:
        print(f"\nREQUEST APPROVED for {process}.")
        print("The tentative allocation is retained.")
    else:
        # Roll back the temporary allocation.
        available[:] = old_available

        for i in range(len(processes)):
            allocation[i][:] = old_allocation[i]
            need[i][:] = old_need[i]

        print(f"\nREQUEST DENIED for {process}.")
        print("The resulting state would be unsafe.")
        print("Original resource values have been restored.")


def main():
    print("=" * 40)
    print("       BANKER'S ALGORITHM")
    print("      DEADLOCK AVOIDANCE SYSTEM")
    print("=" * 40)

    process_count = read_positive_integer("Number of processes: ")
    resource_count = read_positive_integer("Number of resource types: ")

    processes = [f"P{i}" for i in range(process_count)]
    resources = []

    for i in range(resource_count):
        default_name = chr(65 + i) if i < 26 else f"R{i + 1}"
        name = input(
            f"Resource {i + 1} name [{default_name}]: "
        ).strip()
        resources.append(name or default_name)

    total = read_vector(
        f"Total resources ({', '.join(resources)}): ",
        resource_count
    )

    allocation = read_matrix("Allocation", processes, resources)
    maximum = read_matrix("Maximum Claim (Max)", processes, resources)

    # Check that Allocation does not exceed Max.
    for i in range(process_count):
        for j in range(resource_count):
            if allocation[i][j] > maximum[i][j]:
                print(
                    f"Input error: {processes[i]}'s allocation of "
                    f"{resources[j]} exceeds its maximum claim."
                )
                return

    allocated_totals, available = calculate_available(total, allocation)

    if any(value < 0 for value in available):
        print("Input error: Allocated resources exceed total resources.")
        return

    need = calculate_need(maximum, allocation)

    display_vector("Total Resources", total, resources)
    display_vector("Allocated Totals", allocated_totals, resources)
    display_vector("Available Resources", available, resources)

    display_matrix("ALLOCATION MATRIX", allocation, processes, resources)
    display_matrix("MAXIMUM CLAIM MATRIX", maximum, processes, resources)
    display_matrix("NEED MATRIX", need, processes, resources)

    initial_safe = safety_check(
        allocation, need, available, processes, resources
    )

    if not initial_safe:
        print("\nRequest checking requires an initially safe state.")
        return

    answer = input(
        "\nCheck an additional resource request? (yes/no): "
    ).strip().lower()

    if answer not in ("yes", "y"):
        print("Program finished.")
        return

    process_index = read_positive_integer(
        f"Enter process number (1 to {process_count}) for the request: ",
        minimum=1
    ) - 1

    if process_index >= process_count:
        print("Invalid process number.")
        return

    request = read_vector(
        f"Request vector for {processes[process_index]} "
        f"({', '.join(resources)}): ",
        resource_count
    )

    check_resource_request(
        process_index, request, allocation, need,
        available, processes, resources
    )

    print("\nProgram finished.")


if __name__ == "__main__":
    main()
