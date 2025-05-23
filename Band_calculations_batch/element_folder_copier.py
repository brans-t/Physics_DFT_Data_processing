import os
import shutil

def copy_files(directory, elements):
    """
    Copy INCAR and KPOINTS files from a specified directory to a generated subfolder.

    :param directory: Directory containing INCAR and KPOINTS files.
    :param elements: List of element names used to generate the subfolder name.
    """
    if not os.path.isdir(directory):
        print(f"Error: The path '{directory}' is not a valid directory.")
        return

    # Strip leading and trailing whitespace from each element
    cleaned_elements = [element.strip() for element in elements]
    # Generate the target folder name based on the elements
    subfolder_name = '_'.join(cleaned_elements)
    # Generate the subfolder path (using the current working directory)
    subfolder_path = os.path.join(os.getcwd(), "Tot", subfolder_name, "input")

    # Ensure the subfolder exists
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"Created subfolder: {subfolder_path}")

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Check if the filename starts with any of the specified prefixes
        if filename.startswith(("INCAR", "KPOINTS", "vasp")):
            # Construct the input file path
            input_file = os.path.join(directory, filename)
            # Construct the output file path (save to the subfolder, keeping the same filename)
            output_file = os.path.join(subfolder_path, filename)
            # Copy the file
            shutil.copy(input_file, output_file)
            print(f"Copied {input_file} to {output_file}")


# Get the current working directory
current_directory = os.getcwd()
# Construct the path to the element file (assuming it is in the 'output' subdirectory of the current directory)
elements_file = os.path.join(current_directory, "output", "atom_elements.txt")
# Construct the path to the directory containing INCAR and KPOINTS files (assuming it is in the 'source_file' subdirectory of the current directory)
incar_directory = os.path.join(current_directory, "source_file")

# Open the element file and read it line by line
with open(elements_file, 'r') as file:
    for line in file:
        # Strip leading and trailing whitespace and remove brackets
        line = line.strip().strip('[]')
        # Split element symbols
        elements = [element.strip("'") for element in line.split(', ')]
        # Call the function to handle INCAR and KPOINTS files
        copy_files(incar_directory, elements)