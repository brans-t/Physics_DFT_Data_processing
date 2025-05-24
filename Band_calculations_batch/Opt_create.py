import os
import shutil

def create_opt(directory, elements):
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
    subfolder_path = os.path.join(os.getcwd(), "Tot Band", subfolder_name, "opt")

    # Ensure the subfolder exists
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"Created subfolder: {subfolder_path}")
    return subfolder_path



def move_input(con_directory, elements):

    if not os.path.isdir(con_directory):
        print(f"Error: The path '{con_directory}' is not a valid directory.")
        return

    # Strip leading and trailing whitespace from each element
    cleaned_elements = [element.strip() for element in elements]
    # Generate the target folder name based on the elements
    subfolder_name = '_'.join(cleaned_elements)
    input_path = os.path.join(os.getcwd(), "Tot Band", subfolder_name, 'input')

    # Iterate through all files in the directory
    for filename in os.listdir(input_path):
        if filename.startswith(("INCAR", "KPOINTS", "POTCAR", "POSCAR", "vasp.pbs")):
            # 构造输入文件路径
            input_file = os.path.join(input_path, filename)
            # 构造输出文件路径（保存到子文件夹，保持相同的文件名）
            output_path = create_opt(con_directory, elements)
            output_file = os.path.join(output_path, filename)
            # 复制文件
            shutil.copy(input_file, output_file)
            print(f"Copied {input_file} to {output_file}")



# Get the current working directory
current_directory = os.getcwd()
# Construct the path to the element file (assuming it is in the 'output' subdirectory of the current directory)
elements_file = os.path.join(current_directory, "output", "atom_elements.txt")
# Construct the path to the directory containing INCAR and KPOINTS files (assuming it is in the 'source_file' subdirectory of the current directory)
source_directory = os.path.join(current_directory, "source_file")

# Open the element file and read it line by line
with open(elements_file, 'r') as file:
    for line in file:
        # Strip leading and trailing whitespace and remove brackets
        line = line.strip().strip('[]')
        # Split element symbols
        elements = [element.strip("'") for element in line.split(', ')]
        # Call the function to handle INCAR and KPOINTS files
        create_opt(source_directory, elements)
        move_input(source_directory, elements)