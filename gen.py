import os
from run_bash_command import run_bash_command
from output_pdf import output_pdf
from get_game_with_random_seed import get_game_with_random_seed

def main():
    dirnow = os.path.dirname(os.path.abspath(__file__))
    project_path = dirnow
    clean_sh = os.path.join(dirnow, "scripts", "clean.sh")

    random_seed = input("input_a_string >>> ").strip()
    random_seed = int(random_seed)
    game_val, round_num = get_game_with_random_seed(random_seed)
    output_pdf(game_val, random_seed, round_num)

    # 最后删除辅助文件
    run_bash_command(["bash", clean_sh], dirnow, env={"PROJECT_PATH": project_path})

if __name__ == "__main__":
    main()