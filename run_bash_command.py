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
    disp = False
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
        disp: 是否打印命令输出到终端
    
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
            if disp:
                print(f"已切换到目录: {directory}")
        
        # 执行命令
        if env is None:
            env = dict()

        result = subprocess.run(
            command,
            shell=shell,
            env={**env, **os.environ},
            capture_output=True,
            text=True,
            check=raise_on_error
        )
        
        # 打印命令输出
        if disp:
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

        if directory and disp:
            print(f"已恢复到原始目录: {original_dir}")