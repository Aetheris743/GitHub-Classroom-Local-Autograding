from CMDRunner import command
from UI import interface
import json
from os.path import exists
import sys

def run_tests():
    results = {}
    with open(".github/classroom/autograding.json", "r") as f:
        data = json.load(f)
    for test in data["tests"]:
        results[test["name"]] = {}
        # just run the prep for the test
        command.script_interface(test["setup"]).close()

        # run the test
        test_interface = command.script_interface(test["run"])
        test_interface.write(test["input"])
        # test_interface.write("\n") # might add this later
        results[test["name"]]["output"] = test_interface.read()
        results[test["name"]]["result"] = True if results[test["name"]]["output"] == test["output"] else False
        test_interface.close()

        # run the cleanup for the test
        command.script_interface("make clean").close()
    
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
            

