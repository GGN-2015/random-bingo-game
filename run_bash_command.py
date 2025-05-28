from pathlib import Path
from typing import Optional, List, Dict, Union
import os
import subprocess

def run_bash_command(
    command: Union[str, List[str]],
    directory: Optional[Union[str, Path]] = None,
    env: Optional[Dict[str, str]] = None,
    return_output: bool = False,
    raise_on_error: bool = True,
    shell: bool = False,
    disp: bool = False
) -> Optional[str]:
    """
    Executes a Bash command in a specified directory with configurable options.
    This function provides robust handling of command execution, directory management, 
    environment variables, and error handling.
    
    Args:
        command (Union[str, List[str]]): 
            The command to execute. Use a list for arguments (recommended for safety) or 
            a string when `shell=True` (e.g., "command arg1 arg2").
            
        directory (Optional[Union[str, Path]]): 
            The working directory where the command should run. Defaults to the current 
            directory. Path can be a string or `Path` object.
            
        env (Optional[Dict[str, str]]): 
            A dictionary of environment variables to set for the command. Merges with 
            the current environment variables. Use `None` to inherit the parent environment.
            
        return_output (bool): 
            If `True`, returns the command's standard output as a string. Otherwise, 
            returns `None`.
            
        raise_on_error (bool): 
            If `True`, raises a `subprocess.CalledProcessError` when the command exits 
            with a non-zero status. If `False`, errors are logged but not raised.
            
        shell (bool): 
            If `True`, executes the command through the shell (useful for pipes, globs, 
            or shell-specific syntax). Use `False` (default) for direct execution 
            (safer for untrusted input).
            
        disp (bool): 
            If `True`, prints the command's output and errors to the terminal in real-time.
            
    Returns:
        Optional[str]: The command's standard output if `return_output=True`, otherwise `None`.
        
    Raises:
        subprocess.CalledProcessError: When the command fails and `raise_on_error=True`.
        OSError: For invalid directory paths or permission issues.
        
    Example Usage:
        # Run "ls -l" in a specific directory and print output
        run_bash_command(["ls", "-l"], directory="/usr/bin", disp=True)
        
        # Execute a shell script with custom environment variables
        run_bash_command("./script.sh", env={"API_KEY": "secret"}, shell=True)
    """
    # Save the original working directory to ensure we revert back after execution
    original_dir = os.getcwd()
    
    try:
        # Handle directory switching with error checking
        if directory:
            # Convert Path objects to string for compatibility
            directory_str = str(directory)
            os.chdir(directory_str)  # May raise OSError for invalid paths
            if disp:
                print(f"Switched to directory: {directory_str}")
        
        # Prepare environment variables: merge user-provided env with system environment
        merged_env = {**os.environ, **(env or {})}
        
        # Execute the command using subprocess.run for robust process management
        result = subprocess.run(
            command,
            shell=shell,              # Use shell for complex commands (risks injection)
            env=merged_env,           # Inherit and override environment variables
            stdout=subprocess.PIPE,   # Capture stdout for later processing
            stderr=subprocess.PIPE,   # Capture stderr for error reporting
            text=True,                # Return output as string (not bytes)
            check=raise_on_error      # Raise exception on non-zero exit codes
        )
        
        # Print live output if requested
        if disp:
            if result.stdout:
                print(f"Command Output:\n{result.stdout}")
            if result.stderr:
                print(f"Command Error:\n{result.stderr}")
        
        # Return the captured output if the caller requested it
        return result.stdout if return_output else None
    
    except subprocess.CalledProcessError as e:
        # Comprehensive error logging for failed commands
        error_msg = (
            f"Command failed with exit code {e.returncode}:\n"
            f"Command: {' '.join(command) if isinstance(command, list) else command}\n"
            f"Directory: {directory or original_dir}"
        )
        print(error_msg)
        if e.stdout:
            print(f"Standard Output:\n{e.stdout}")
        if e.stderr:
            print(f"Standard Error:\n{e.stderr}")
        # Re-raise the exception to allow upstream handling
        if raise_on_error:
            raise
    
    except OSError as e:
        # Handle directory-related errors (e.g., permission denied)
        print(f"Error accessing directory {directory}: {e}")
        raise
    
    finally:
        # Ensure we always return to the original working directory
        os.chdir(original_dir)
        if disp:
            print(f"Reverted to original directory: {original_dir}")