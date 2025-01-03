import subprocess
import time
import sys


def start_process(script_name, args=None):
    command = [sys.executable, script_name]
    if args:
        command.extend(args)
    return subprocess.Popen(command)


if __name__ == "__main__":
    server_process = start_process('./cs_fhe/simulation/server.py')
    
    time.sleep(2)

    client1_process = start_process('./cs_fhe/simulation/client.py', args=['7', 'bank'])
    client2_process = start_process('./cs_fhe/simulation/client.py', args=['5', 'telco'])
    
    # # DEBUG
    # time.sleep(4)
    # server_process.terminate()
    
    client1_process.wait()
    client2_process.wait()

    server_process.terminate()
