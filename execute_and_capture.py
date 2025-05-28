import subprocess

def execute_and_capture(executable_path, input_string) -> str:
    """
    Passes a specified string to an executable program and captures its standard output.
    
    Args:
        executable_path (str): Path to the executable program.
        input_string (str): String to be passed as input to the program.
        
    Returns:
        str: Standard output of the executable program.
    """
    try:
        # Run the program using subprocess.run, pass input, and capture output
        result = subprocess.run(
            executable_path,
            input=input_string.encode('utf-8'),  # Encode string to bytes
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True  # Raise CalledProcessError for non-zero exit codes
        )
        
        # Decode and return the standard output
        return result.stdout.decode('utf-8')
    
    except subprocess.CalledProcessError as e:
        # Handle program execution errors
        print(f"Program execution failed, exit code: {e.returncode}")
        print(f"Standard error: {e.stderr.decode('utf-8')}")
        return ""
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return ""