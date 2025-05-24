import re
import os

# Extract element symbols from a chemical formula
def extract_elements(chemical_formula):
    """Regular expression to match element symbols
        :param chemical_formula : Chemical expressions
        :return: A list of extracted chemical element symbols
    """
    # Regular expression pattern to match chemical element symbols
    # [A-Z] matches any uppercase letter (first character of an element symbol)
    # [a-z]? matches zero or one lowercase letter (second character of an element symbol, if present)
    pattern = r"[A-Z][a-z]?"
    elements = re.findall(pattern, chemical_formula)
    return elements

# Read chemical expressions from an input file, extract element symbols, and write to an output file
def process_file(input_file_path, output_folder_path, log_file):
    """Reads chemical formulas from an input file, extracts element symbols, and writes the results to an output file.
        :param input_file_path: Path to the input file containing chemical formulas.
        :param output_folder_path: Path to the folder where the output file will be saved.
        :param log_file: A file object for logging messages.
        :return: A tuple containing the list of results and the path to the output file.
        """
    # Check if the input file exists
    if not os.path.exists(input_file_path):
        log_file.write(f"Error: The input file '{input_file_path}' does not exist.\n")
        return None, None

    # Ensure the output folder exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        log_file.write(f"Output folder '{output_folder_path}' has been created.\n")

    # Generate the output file name based on the input file name
    input_file_name = os.path.basename(input_file_path)
    output_file_name = f"{os.path.splitext(input_file_name)[0]}_elements.txt"
    output_file_path = os.path.join(output_folder_path, output_file_name)

    # Read chemical expressions from the input file and extract element symbols
    results = []
    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            # Strip leading and trailing whitespace
            line = line.strip()
            if line:  # Ensure non-empty lines are processed
                elements = extract_elements(line)
                results.append(elements)

    # Write the results to the output file
    with open(output_file_path, 'w') as output_file:
        for i, elements in enumerate(results):
            output_file.write(f"{elements}\n")

    log_file.write(f"Results have been written to '{output_file_path}'.\n")
    return results, output_file_path

# Extract specified suffix POTCAR files from the source folder and copy them to the input subfolder of the target folder
def extract_files(source_folder, target_folder_name, suffixes, log_file):
    """
    Extract specified suffix POTCAR files from the source folder and copy them to the input subfolder of the target folder
    :param source_folder: Path to the source folder
    :param target_folder_name: Name of the target folder (dynamically generated)
    :param suffixes: List of suffixes for the POTCAR files to be extracted
    """
    # Dynamically generate the target folder name
    target_folder = os.path.join(os.path.dirname(source_folder), target_folder_name)
    input_subfolder = os.path.join("Tot_Band", target_folder, "input")  # Create an input subfolder
    if not os.path.exists(input_subfolder):
        os.makedirs(input_subfolder)
        log_file.write(f"Target folder '{input_subfolder}' has been created.\n")

    # Dictionary to store the found file paths in the order of input
    found_files = {suffix: None for suffix in suffixes}

    # Traverse the source folder and its subfolders
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Check if the file name matches the POTCAR_XXX format
            if file.startswith("POTCAR_"):
                for suffix in suffixes:
                    if file.endswith(suffix):
                        # Construct the full file path
                        file_path = os.path.join(root, file)
                        # Store the found file path in the dictionary
                        found_files[suffix] = file_path
                        log_file.write(f"Found file '{file}' at path '{file_path}'.\n")
                        break  # Exit the loop after a match is found

    # Check if all required files have been found
    if all(found_files.values()):
        # Merge file contents in the order of input
        target_file_path = os.path.join(input_subfolder, "POTCAR")  # Save to the input subfolder
        with open(target_file_path, "w") as target_file:
            for suffix in suffixes:
                file_path = found_files[suffix]
                with open(file_path, "r") as source_file:
                    content = source_file.read()
                    target_file.write(content)
                    # target_file.write("\n")  # Add a newline character to separate contents of different files
        log_file.write(f"All file contents have been merged in order to '{target_file_path}'.\n")
        return True  # Indicate success
    else:
        missing_files = [f"POTCAR_{suffix}" for suffix, path in found_files.items() if path is None]
        log_file.write(f"The following required files were not found, and the target folder '{target_folder_name}' was not successfully created: {missing_files}\n")
        return False  # Indicate failure

# Main program
if __name__ == "__main__":
    # Input file path
    input_file_path = input("Please enter the path to the input file containing chemical expressions: ")
    # Output folder path
    output_folder_path = "output"  # Fixed output folder path
    # Source folder path
    source_folder = input("Please enter the path to the source folder (containing POTCAR files): ")

    # Open the log file
    log_file_path = os.path.join(output_folder_path, "output.log")
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    with open(log_file_path, 'w') as log_file:
        log_file.write("Program execution log:\n")

        # Process the input file, extract element symbols, and write to the output file
        results, output_file_path = process_file(input_file_path, output_folder_path, log_file)

        if results is None:
            log_file.write("The program terminated due to the non-existent input file.\n")
            print("The program terminated due to the non-existent input file.")
            exit()

        # Read the target folder names and corresponding POTCAR suffixes from the output file
        with open(output_file_path, 'r') as output_file:
            lines = output_file.readlines()

        # Lists to record successful and unsuccessful folders
        success_folders = []
        failed_folders = []

        # Iterate through each line, extract element symbols, and generate target folder names
        for line in lines:
            # Strip leading and trailing whitespace and remove brackets
            line = line.strip().strip('[]')
            # Split element symbols
            elements = [element.strip("'") for element in line.split(', ')]
            # Generate the target folder name
            target_folder_name = '_'.join(elements)
            # Generate the suffixes for the POTCAR files
            suffixes = elements

            # Call the function to extract files and merge
            if extract_files(source_folder, target_folder_name, suffixes, log_file):
                success_folders.append(target_folder_name)
            else:
                failed_folders.append(target_folder_name)

        # Final message
        if success_folders:
            log_file.write("\nThe following folders successfully created and merged POTCAR files:\n")
            for folder in success_folders:
                log_file.write(f"{folder}\n")
        if failed_folders:
            log_file.write("\nThe following folders were not successfully created due to missing POTCAR files:\n")
            for folder in failed_folders:
                log_file.write(f"{folder}\n")
        log_file.write("\nFile extraction and merging completed.\n")

    print(f"The program execution results have been recorded in '{log_file_path}'.")