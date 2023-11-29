import os
import sys

import importlib


def run_script(command):
    try:
        script_name = ""
        if command == "train":
            script_name = "train_entrance"
            # subprocess.run(["python", "train_entrance.py"], check=True)
        elif command == "predict":
            script_name = "sever"
            # subprocess.run(["python", "sever.py"], check=True)
        if script_name != "":
            module = importlib.import_module(script_name)
            module.main()
        else:
            print("do nothing")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        run_script(command)
    else:
        command = os.environ.get('cmd', '')
        run_script(command)
