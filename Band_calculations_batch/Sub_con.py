import os
import subprocess  # Import the subprocess module

def submit_vasp_job(directory, script_name="vasp.pbs"):
    """
    Enter the specified directory and submit the vasp.pbs job script.

    Parameters:
        directory (str): The directory path containing the vasp.pbs script.
        script_name (str): The name of the job script file, default is "vasp.pbs".
    """
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Error: The directory {directory} does not exist.")
        return

    # Check if the script file exists
    script_path = os.path.join(directory, script_name)
    if not os.path.exists(script_path):
        print(f"Error: The script file {script_path} does not exist.")
        return

    # Change to the target directory
    os.chdir(directory)
    print(f"Changed to directory: {directory}")

    # Submit the job script
    try:
        # Use the qsub command to submit the job
        submit_command = f"qsub {script_name}"
        result = subprocess.run(
            submit_command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"Job submission successful! Output information:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Job submission failed! Error information:\n{e.stderr}")


# Main program
if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    # Get the directory where the current script is located
    script_dir = os.path.dirname(script_path)

    # Get the current working directory
    current_directory = os.getcwd()
    # Construct the path to the element file (assuming it is in the 'output' subdirectory of the current directory)
    elements_file = os.path.join(current_directory, "output", "atom_elements.txt")

    # Open the element file and read it line by line
    with open(elements_file, 'r') as file:
        for line in file:
            # Strip leading and trailing whitespace and remove brackets
            line = line.strip().strip('[]')
            # Split element symbols
            elements = [element.strip("'") for element in line.split(', ')]

            # Strip leading and trailing whitespace from each element
            cleaned_elements = [element.strip() for element in elements]
            # Generate the target folder name based on the elements
            subfolder_name = '_'.join(cleaned_elements)

            # Construct the target directory path (now pointing to the 'con' folder instead of 'opt')
            target_directory = os.path.join(script_dir, "Tot_Band", subfolder_name, "con")

            # Call the function to submit the job
            submit_vasp_job(target_directory)