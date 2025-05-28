import random
import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Union
dirnow = os.path.dirname(os.path.abspath(__file__))
os.chdir(dirnow)

exe_path = os.path.join(dirnow, "try.out")

def run_bash_command(
    command: Union[str, List[str]],
    directory: Optional[Union[str, Path]] = None,
    env: Optional[Dict[str, str]] = None,
    return_output: bool = False,
    raise_on_error: bool = True,
    shell: bool = False
) -> Optional[str]:
    """
    在指定目录中执行Bash命令
    
    Args:
        command: 要执行的命令，可以是字符串或列表
        directory: 执行命令的目录路径，默认为当前目录
        env: 环境变量字典，默认为None（使用当前环境）
        return_output: 是否返回命令输出，默认为False
        raise_on_error: 命令执行失败时是否抛出异常，默认为True
        shell: 是否通过shell执行命令，默认为False（直接执行）
    
    Returns:
        命令的标准输出（如果return_output为True），否则返回None
    
    Exceptions:
        subprocess.CalledProcessError: 命令执行失败且raise_on_error为True
    """
    # 保存当前工作目录，以便恢复
    original_dir = os.getcwd()
    
    try:
        # 如果指定了目录，则切换到该目录
        if directory:
            os.chdir(directory)
            print(f"已切换到目录: {directory}")
        
        # 执行命令
        result = subprocess.run(
            command,
            shell=shell,
            env=env or os.environ,
            capture_output=True,
            text=True,
            check=raise_on_error
        )
        
        # 打印命令输出
        if result.stdout:
            print(f"命令输出:\n{result.stdout}")
        if result.stderr and raise_on_error:
            print(f"命令错误输出:\n{result.stderr}")
        
        # 返回输出（如果需要）
        return result.stdout if return_output else None
    
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        if e.stdout:
            print(f"标准输出:\n{e.stdout}")
        if e.stderr:
            print(f"错误输出:\n{e.stderr}")
        raise  # 重新抛出异常，除非用户选择忽略错误
    finally:
        # 恢复到原始工作目录
        os.chdir(original_dir)
        if directory:
            print(f"已恢复到原始目录: {original_dir}")

data_file = os.path.join(dirnow, "data.txt")
temp_file = os.path.join(dirnow, "latex_template.tex")
games_folder = os.path.join(dirnow, "games")

run_bash_command(["bash", "compile.sh"], dirnow) # 保证 try.out 存在
assert os.path.isfile(exe_path)

if not os.path.isfile(data_file):
    print("generating data.txt ...")
    run_bash_command(["bash", "make_data.sh"], dirnow)

with open(data_file, "r") as fp:
    avai_inp = fp.read().split("==========\n")
    avai_inp = [x.strip() for x in avai_inp if x.strip() != ""]

def execute_and_capture(executable_path, input_string) -> str:
    """
    将指定字符串传递给可执行程序并捕获其标准输出
    
    Args:
        executable_path (str): 可执行程序的路径
        input_string (str): 要传递给程序的字符串
    
    Returns:
        str: 可执行程序的标准输出
    """
    try:
        # 使用subprocess.run执行程序，传递输入并捕获输出
        result = subprocess.run(
            executable_path,
            input=input_string.encode('utf-8'),  # 将字符串编码为字节
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True  # 如果程序返回非零退出状态码，抛出CalledProcessError
        )
        
        # 解码标准输出并返回
        return result.stdout.decode('utf-8')
    
    except subprocess.CalledProcessError as e:
        # 处理程序执行错误
        print(f"程序执行失败，返回代码: {e.returncode}")
        print(f"标准错误: {e.stderr.decode('utf-8')}")
        return ""
    except Exception as e:
        # 处理其他异常
        print(f"发生错误: {e}")
        return ""

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
with open(temp_file, "r") as fp:
    template = fp.read()

for i in range(5):
    for j in range(5):
        token = "A_{%d,%d}" % (i+1, j+1)
        assert template.find(token) != -1
        template = template.replace(token, str(game_val[i][j]))

template = template.replace("random\\_seed", str(random_seed))
template = template.replace("round\\_num", str(round_num))

with open("./games/%d.tex" % random_seed, "w") as fp:
    fp.write(template)

run_bash_command(["xelatex", str(random_seed)], games_folder)
run_bash_command(["bash", "clean.sh"], dirnow)
