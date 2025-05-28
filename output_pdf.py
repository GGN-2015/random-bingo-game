import os
from run_bash_command import run_bash_command

# Get the current directory and set up project paths
dirnow = os.path.dirname(os.path.abspath(__file__))
project_path = dirnow
template_folder = os.path.join(dirnow, "templates")  # Directory containing LaTeX templates
games_folder = os.path.join(dirnow, "games")         # Output directory for generated games

def output_pdf(game_val: list, random_seed: int, round_num: int):
    """
    Generate a PDF game file from a LaTeX template using the provided game values,
    random seed, and iteration count.
    
    Args:
        game_val (list): 2D list containing game values to populate the template
        random_seed (int): Seed value used for game generation
        round_num (int): Number of iterations taken to find the solution
    """
    # Process each template file in the templates directory
    for temp_file_now in os.listdir(template_folder):
        temp_file_now = os.path.join(template_folder, temp_file_now)

        print(f"Processing template: {temp_file_now}")
        with open(temp_file_now, "r") as fp:
            template = fp.read()  # Read the entire template content

        # Replace template placeholders with actual game values
        for i in range(5):
            for j in range(5):
                token = f"A_{{{i+1},{j+1}}}"  # Create token like "A_{1,1}"
                assert template.find(token) != -1, f"Token {token} not found in template"
                # Replace token with bolded game value in LaTeX format
                template = template.replace(token, f"\\textbf{{{str(game_val[i][j])}}}")

        # Replace seed and round number placeholders
        template = template.replace("random\\_seed", str(random_seed))
        template = template.replace("round\\_num", str(round_num))
        
        # Determine language from template filename (e.g., "en.tex" -> "en")
        lang = os.path.basename(temp_file_now).split(".")[0] 
        
        # Write updated template to a new TeX file
        output_tex_path = os.path.join(games_folder, lang, f"{random_seed}.tex")
        with open(output_tex_path, "w") as fp:
            fp.write(template)
        
        # Compile TeX to PDF using xelatex
        run_bash_command(
            ["xelatex", str(random_seed)],  # Command arguments
            os.path.join(games_folder, lang),  # Working directory for compilation
            env={"PROJECT_PATH": project_path}  # Environment variables
        )