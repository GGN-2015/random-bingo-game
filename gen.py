import os
from run_bash_command import run_bash_command
from output_pdf import output_pdf
from get_game_with_random_seed import get_game_with_random_seed

# Get the current directory and set the project path
dirnow = os.path.dirname(os.path.abspath(__file__))
project_path = dirnow

def main():
    """Main function to generate a Bingo game, create a PDF, and clean up files."""
    # Path to the cleanup script
    clean_sh = os.path.join(dirnow, "scripts", "clean.sh")
    
    # Get random seed input from user
    random_seed_input = input("input_a_string >>> ").strip()
    random_seed = int(random_seed_input)  # Convert input to integer
    
    # Generate game configuration using the random seed
    game_val, round_num = get_game_with_random_seed(random_seed)
    
    # Generate PDF output from the game configuration
    output_pdf(game_val, random_seed, round_num)
    
    # Clean up auxiliary files after generation
    print("Cleaning up temporary files...")
    run_bash_command(
        ["bash", clean_sh],  # Execute the cleanup script
        dirnow,              # Run in the project's root directory
        env={"PROJECT_PATH": project_path}  # Pass project path to environment
    )

if __name__ == "__main__":
    main()