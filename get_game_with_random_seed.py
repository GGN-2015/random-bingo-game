import random
import os
from run_bash_command import run_bash_command
from execute_and_capture import execute_and_capture

# Get the current directory and set up project paths
dirnow = os.path.dirname(os.path.abspath(__file__))
project_path = dirnow
data_file = os.path.join(dirnow, "data.txt")  # Data file containing possible solutions
make_data_sh = os.path.join(dirnow, "scripts", "make_data.sh")  # Script to generate data
exe_path = os.path.join(dirnow, "try.out")  # Executable for solving the game
compile_sh = os.path.join(dirnow, "scripts", "compile.sh")  # Script to compile the solver

# Maximum possible adjacent cells for each grid position
# Used to limit the random values generated during game creation
max_siz = [
    [4, 6, 6, 6, 4],
    [6, 9, 9, 9, 6],
    [6, 9, 9, 9, 6],
    [6, 9, 9, 9, 6],
    [4, 6, 6, 6, 4]
]

# Ensure the solver executable exists, compile if necessary
if not os.path.isfile(exe_path):
    print("Compiling solver executable...")
    run_bash_command(["bash", compile_sh], dirnow, env={"PROJECT_PATH": project_path})

# Ensure data file exists, generate if necessary
if not os.path.isfile(data_file):
    print("Generating data.txt ...")
    run_bash_command(["bash", make_data_sh], dirnow, env={"PROJECT_PATH": project_path})

def get_number_list(sol):
    """
    Convert solution string into a 2D list of integers
    Args:
        sol: String containing solution data
    Returns:
        2D list representing the solution grid
    """
    return [[int(x) for x in line.split() if x.strip() != ""] for line in sol.split("\n") if line.strip() != ""]

def get_game_with_random_seed(random_seed: int):
    """
    Generate a game configuration with a unique solution using a specified random seed
    Args:
        random_seed: Integer seed for the random number generator
    Returns:
        Tuple containing:
            - 2D list representing the game configuration
            - Number of rounds taken to find a valid configuration
    """
    # Initialize random number generator with the given seed
    random.seed(random_seed)

    # Read available solutions from data file
    with open(data_file, "r") as fp:
        avai_inp = fp.read().split("==========\n")
        avai_inp = [x.strip() for x in avai_inp if x.strip() != ""]

    # Randomly select a base solution
    solution = random.choice(avai_inp)
    num_sol  = get_number_list(solution)

    # Calculate the target counts (number of adjacent marked cells) for each grid
    aim_cnt = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx = i + dx
                    ny = j + dy
                    if 0 <= nx < 5 and 0 <= ny < 5:
                        aim_cnt[i][j] += int(num_sol[nx][ny] == 1)

    # Variables to track solution count and iteration rounds
    sol_cnt = 0
    round_num = 0
    game_val = [[0 for _ in range(5)] for _ in range(5)]

    # Keep generating game configurations until a unique solution is found
    while sol_cnt != 1:
        round_num += 1
        print(f"Finding solutions round {round_num} ...")
        game_val = [[0 for _ in range(5)] for _ in range(5)]

        # Generate game configuration based on the target counts
        for i in range(5):
            for j in range(5):
                # Start with the correct target count
                game_val[i][j] = aim_cnt[i][j]
                # For cells not marked in the solution, randomize the count
                if num_sol[i][j] != 1:
                    # Ensure the randomized count is different from the correct count
                    while game_val[i][j] == aim_cnt[i][j]:
                        game_val[i][j] = random.randint(1, max_siz[i][j])

        # Convert the game configuration to input format for the solver
        inp = "\n".join([" ".join([str(x) for x in line]) for line in game_val]) + "\n"
        # Execute the solver and get the number of solutions
        sol_cnt = int(execute_and_capture(exe_path, inp))
        print(f"- sol_cnt: {sol_cnt}")

    return game_val, round_num