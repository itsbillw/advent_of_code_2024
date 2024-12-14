def read_disk_map(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def create_disk_layout(disk_map):
    """Converts the input disk map into a layout of files and free spaces."""
    layout = []
    file_id = 0
    for i, digit in enumerate(disk_map):
        length = int(digit)
        if i % 2 == 0:  # file
            layout.append(
                ("F", length, file_id),
            )  # ('F' for file, with its length and file ID)
            file_id += 1
        else:  # free space
            layout.append((".", length, None))  # ('.' for free space, with its length)
    return layout


def create_initial_disk(disk_layout):
    """Create an initial disk list where each block is either a file ID or free space ('.')."""
    disk = []
    for item in disk_layout:
        if item[0] == "F":
            disk.extend(
                [item[2]] * item[1],
            )  # Repeat file ID for the length of the file
        else:
            disk.extend(["."] * item[1])  # Free spaces as '.'
    return disk


def compact_disk(disk):
    """Move the files one by one to the leftmost free space."""
    while True:
        free_index = next((i for i, block in enumerate(disk) if block == "."), None)
        if free_index is None:
            break  # No more free spaces

        # Move the rightmost file to the leftmost free space
        moved = False
        for i in range(len(disk) - 1, free_index, -1):
            if disk[i] != ".":
                disk[free_index] = disk[i]  # Move file to the free space
                disk[i] = "."  # Empty the original space
                moved = True
                break

        if not moved:
            break  # No more moves possible

    return disk


def calculate_checksum(disk):
    """Calculate the checksum by summing the positions of file blocks multiplied by their file IDs."""
    checksum = 0
    for i, block in enumerate(disk):
        if block != ".":
            checksum += i * block
    return checksum


def main():
    # Read the disk map input from the text file
    filename = "input/day_nine_input.txt"
    disk_map = read_disk_map(filename)

    # Create the initial disk layout based on the disk map
    disk_layout = create_disk_layout(disk_map)

    # Create the disk (list of file IDs and free spaces)
    disk = create_initial_disk(disk_layout)

    # Perform the compacting process
    final_disk_layout = compact_disk(disk)

    # Calculate and print the checksum
    checksum = calculate_checksum(final_disk_layout)
    print("Filesystem checksum:", checksum)


if __name__ == "__main__":
    main()
