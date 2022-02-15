from CMDRunner import command
from UI import interface
import json
from os.path import exists
import sys
import time

def show_diff(result, goal) -> None:
    lines = goal.strip().split("\n")
    new_lines = result.strip().split("\n")

    while len(new_lines) < len(lines):
        new_lines.append("")
    while len(lines) < len(new_lines):
        lines.append("")

    for line in range(len(new_lines)):
        if new_lines[line].strip() != lines[line].strip():
            print("❌ " + new_lines[line])
            print("   " + interface.format_text(lines[line] if lines[line] != "" else "\\n", "blue", True))
        else:
            print("✅ " + new_lines[line])

            
def input_equalls(result, goal) -> bool:
    lines = goal.strip().split("\n")
    new_lines = result.strip().split("\n")
    while len(new_lines) != len(lines):
        return False

    for line in range(len(new_lines)):
        if new_lines[line].strip() != lines[line].strip():
            return False

    return True

def run_tests():
    results = {}
    with open(".github/classroom/autograding.json", "r") as f:
        data = json.load(f)
    for test in data["tests"]:
        print("Running test: " + test["name"])
        results[test["name"]] = {}
        # just run the prep for the test
        command.script_interface(test["setup"].split(";")[0])
        compiler = command.script_interface(test["setup"].split(";")[1].strip().replace(";", ""))
        compiler.wait()

        # run the test (sometimes the executable has not finished being written to the filesystem by the subprocess)
        try:
            test_interface = command.script_interface(test["run"])
        except BrokenPipeError:
            time.sleep(0.1) #wait for the file to finish writing
            test_interface = command.script_interface(test["run"])
        test_interface.write(test["input"])
        # test_interface.write("\n") # might add this later
        results[test["name"]]["output"] = test_interface.read_all()
        results[test["name"]]["result"] = input_equalls(results[test["name"]]["output"], test["output"])
        test_interface.close()

        # run the cleanup for the test
        command.script_interface("make clean")
    
    for key in results:
        print("{}: {}".format(key, results[key]["result"]))


# check if the program is in the expected directory
if __name__ == "__main__":
    if not exists(".github/classroom/autograding.json") or not exists("Makefile"):
        print("Please run this program from the root directory of the project.")
        sys.exit(1)
    
    #show the user the available commands
    commands = ["Run Tests", "Modify .gitignore (Recommended)", "Quit"]
    main_menu = interface.prompt(commands)
    result = main_menu.get_input()
    if result is 0:
        run_tests()
    if result is 1:
        # add this folder to the .gitignore
        with open(".gitignore", "a") as f:
            f.write("GitHubTests/\n")
        pass
    if result is 2:
        exit()
            

