import os

def replace_elements_in_poscar(input_file, output_file, elements, atom_counts):
    """
    Replace element names and atom counts in a POSCAR file.

    :param input_file: Path to the input POSCAR file.
    :param output_file: Path to the output POSCAR file.
    :param elements: List of element names to replace.
    :param atom_counts: List of atom counts to replace.
    """
    try:
        # Open the input file and read all lines
        with open(input_file, 'r') as infile:
            lines = infile.readlines()

        # Replace element names in line 6 (index 5)
        elements_line = lines[5].strip().split()
        lines[5] = "    " + "   ".join(elements) + "\n"

        # Replace atom counts in line 7 (index 6)
        counts_line = lines[6].strip().split()
        lines[6] = "    " + "    ".join(map(str, atom_counts)) + "\n"

        # Write the modified content to the output file
        with open(output_file, 'w') as outfile:
            outfile.writelines(lines)

        print(f"Processed {input_file} -> {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")


def batch_replace_poscar_files(directory, elements, atom_counts):
    """
    Batch process all POSCAR files in a directory and save the modified files to a specified subfolder.

    :param directory: Directory containing POSCAR files.
    :param elements: List of element names to replace.
    :param atom_counts: List of atom counts to replace.
    """
    # Check if the directory exists and is a directory
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        return

    # Strip leading and trailing whitespace from each element
    cleaned_elements = [element.strip() for element in elements]
    # Generate the target folder name
    subfolder_name = '_'.join(cleaned_elements)
    # Generate the subfolder path (using the current working directory)
    subfolder_path = os.path.join(os.getcwd(),  "Tot", subfolder_name, "input")

    # Ensure the subfolder exists
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"Created subfolder: {subfolder_path}")

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("POSCAR"):
            # Construct the input file path
            input_file = os.path.join(directory, filename)
            # Construct the output file path (save to the subfolder, keeping the same filename)
            output_file = os.path.join(subfolder_path, filename)
            # Call the function to replace element names and atom counts in the POSCAR file
            replace_elements_in_poscar(input_file, output_file, cleaned_elements, atom_counts)


# Read element combinations from a file
# Get the current working directory
current_directory = os.getcwd()
# Construct the path to the element file (assuming it is in the 'output' subdirectory of the current directory)
elements_file = os.path.join(current_directory, "output", "atom_elements.txt")
# Construct the path to the POSCAR file directory (assuming it is in the 'source_file' subdirectory of the current directory)
poscar_directory = os.path.join(current_directory, "source_file")

# Open the element file and read it line by line
with open(elements_file, 'r') as file:
    for line in file:
        # Strip leading and trailing whitespace and remove brackets
        line = line.strip().strip('[]')
        # Split element symbols
        elements = [element.strip("'") for element in line.split(', ')]
        # Assume fixed atom counts
        atom_counts = [2, 1, 1, 1]
        # Call the function to process POSCAR files
        batch_replace_poscar_files(poscar_directory, elements, atom_counts)