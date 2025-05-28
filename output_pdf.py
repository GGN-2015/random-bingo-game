import os
from run_bash_command import run_bash_command

dirnow = os.path.dirname(os.path.abspath(__file__))
project_path = dirnow
temp_file_zh = os.path.join(dirnow, "templates", "latex_template_zh.tex")
temp_file_en = os.path.join(dirnow, "templates", "latex_template_en.tex")
games_folder = os.path.join(dirnow, "games")

def output_pdf(game_val:list, random_seed:int, round_num:int):
    for temp_file_now in [temp_file_en, temp_file_zh]:
        print("processing %s" % temp_file_now)
        with open(temp_file_now, "r") as fp:
            template = fp.read()

        for i in range(5):
            for j in range(5):
                token = "A_{%d,%d}" % (i+1, j+1)
                assert template.find(token) != -1
                template = template.replace(token, "\\textbf{" + str(game_val[i][j]) + "}")

        template = template.replace("random\\_seed", str(random_seed))
        template = template.replace("round\\_num", str(round_num))
        lang = temp_file_now.split("_")[-1].split(".")[0] # 识别语言类型

        with open(os.path.join(games_folder, lang, "%d.tex" % random_seed), "w") as fp:
            fp.write(template)
        run_bash_command(["xelatex", str(random_seed)], os.path.join(games_folder, lang), env={"PROJECT_PATH": project_path})
