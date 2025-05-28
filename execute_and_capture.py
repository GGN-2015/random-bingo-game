import subprocess

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
