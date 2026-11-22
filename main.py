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
        matrix.append(
            read_vector(f"{process}: ", len(resources))
        )

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

    safety_check(allocation, need, available, processes, resources)


if _name_ == "_main_":
    main()
