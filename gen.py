import random
import os
from run_bash_command import run_bash_command
from execute_and_capture import execute_and_capture

dirnow = os.path.dirname(os.path.abspath(__file__))
project_path = dirnow
env = {
    "PROJECT_PATH": project_path
}
os.chdir(dirnow)

exe_path = os.path.join(dirnow, "try.out")
data_file = os.path.join(dirnow, "data.txt")
temp_file_zh = os.path.join(dirnow, "templates", "latex_template_zh.tex")
temp_file_en = os.path.join(dirnow, "templates", "latex_template_en.tex")
games_folder = os.path.join(dirnow, "games")

clean_sh = os.path.join(dirnow, "scripts", "clean.sh")
compile_sh = os.path.join(dirnow, "scripts", "compile.sh")
make_data_sh = os.path.join(dirnow, "scripts", "make_data.sh")

if not os.path.isfile(exe_path): # 保证 try.out 存在
    run_bash_command(["bash", compile_sh], dirnow, env=env)

if not os.path.isfile(data_file):
    print("generating data.txt ...")
    run_bash_command(["bash", make_data_sh], dirnow, env=env)

with open(data_file, "r") as fp:
    avai_inp = fp.read().split("==========\n")
    avai_inp = [x.strip() for x in avai_inp if x.strip() != ""]

max_siz = [
    [4, 6, 6, 6, 4],
    [6, 9, 9, 9, 6],
    [6, 9, 9, 9, 6],
    [6, 9, 9, 9, 6],
    [4, 6, 6, 6, 4]]

def get_number_list(sol):
    return [[int(x) for x in line.split() if x.strip() != ""] for line in sol.split("\n") if line.strip() != ""]

random_seed = input("input_a_string >>> ").strip()
random_seed = int(random_seed)
print("random_seed: %d" % random_seed)
random.seed(random_seed)

solution = random.choice(avai_inp)
num_sol  = get_number_list(solution)

aim_cnt = [[0 for _ in range(5)] for _ in range(5)]
for i in range(5):
    for j in range(5):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx = i + dx
                ny = j + dy
                if 0 <= nx < 5 and 0 <= ny < 5:
                    aim_cnt[i][j] += int(num_sol[nx][ny] == 1)

sol_cnt = 0
round_num = 0
game_val = [[0 for _ in range(5)] for _ in range(5)]

while sol_cnt != 1:
    round_num += 1
    print("finding solutions round %d ..." % round_num)
    game_val = [[0 for _ in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            game_val[i][j] = aim_cnt[i][j]
            if num_sol[i][j] != 1:
                while game_val[i][j] == aim_cnt[i][j]:
                    game_val[i][j] = random.randint(1, max_siz[i][j])

    inp = "\n".join([" ".join([str(x) for x in line]) for line in game_val]) + "\n"
    sol_cnt = int(execute_and_capture(exe_path, inp))
    print("- sol_cnt: %d" % sol_cnt)

print(game_val)

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
    run_bash_command(["xelatex", str(random_seed)], os.path.join(games_folder, lang), env=env)


# 最后删除辅助文件
run_bash_command(["bash", clean_sh], dirnow, env=env)
