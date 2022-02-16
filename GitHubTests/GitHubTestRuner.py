from CMDRunner import command
from UI import interface
import json
from os.path import exists, join
import sys
import os
import stat
import time

# Show the diff between two strings
def show_diff(result, goal) -> None:
    print("")
    lines = goal.split("\n")
    new_lines = result[:-1].split("\n")

    while len(new_lines) < len(lines):
        new_lines.append("")
    while len(lines) < len(new_lines):
        lines.append("")

    for line in range(len(new_lines)):
        if new_lines[line].strip() != lines[line].strip():
            print("❌ " + new_lines[line])
            print("   " + interface.format_text(lines[line] if lines[line].strip() != "" else "\\n", "blue", True))
        else:
            print("✅ " + new_lines[line])
    print("")

# a modified string compare that fits the input/output format          
def input_equalls(result, goal, line_ending="\r\n") -> bool:
    lines = goal.split("\n")
    new_lines = result[:-1].split("\n")

    while len(new_lines) != len(lines):
        new_lines.append("")
    # while len(lines) < len(new_lines):
    #     lines.append("")

    for line in range(len(new_lines)):
        if new_lines[line].strip() != lines[line].strip():
            return False
    return True

def run_tests(timout=0.1):
    results = {}
    with open(".github/classroom/autograding.json", "r") as f:
        data = json.load(f)

    number_passed = 0
    number_total = len(data["tests"])
    for test in data["tests"]:
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
            try:
                test_interface = command.script_interface(test["run"])
            except BrokenPipeError:
                print("Unnable to run tests: Program may not be compiling succussfully. If it is, please re-run this script after running 'make clean'.")
        test_interface.write(test["input"])
        test_interface.proc.stdin.flush()
        test_interface.proc.stdin.close()
        test_interface.wait(timout) #wait for the test to finish running
        # test_interface.write("\n") # might add this later
        results[test["name"]]["output"] = test_interface.read_all()
        results[test["name"]]["result"] = input_equalls(results[test["name"]]["output"], test["output"])
        if results[test["name"]]["result"]:
            number_passed += 1
        test_interface.close()

        # run the cleanup for the test
        command.script_interface("make clean")
    
    options = []
    for key in results:
        symbol = "✅" if results[key]["result"] else "❌"
        options.append(f"{symbol} {key}")
    options_prompt = interface.prompt(options)
    if number_passed != number_total:
        print(f"\n\nPassed {number_passed} out of {number_total}\n\nExamine test results (-1 to quit):")
        option = options_prompt.get_input()
        while option > -1 and option < len(options):
            test_input = data['tests'][option]['input'].replace('\r', '\\r').replace('\n', '\\n')
            print(f"Test '{ data['tests'][option]['name'] }' used stdin input '{ test_input }'")
            show_diff(results[data["tests"][option]["name"]]["output"], data["tests"][option]["output"])
            print("Examine test results (-1 to quit):")
            option = options_prompt.get_input()        

    if number_passed == number_total:
        print(f"\nPassed all tests! 🎊🥳🚀\n")
        return

# check if the program is in the expected directory
if __name__ == "__main__":
    if not exists(".github/classroom/autograding.json"):
        directory = input("To configure test runner, please enter project root folder: ")
        while not exists(join(directory, ".github/classroom/autograding.json")):
            print("That folder does not appear to be the root folder of a repository.")
            directory = input("To configure test runner, please enter project root folder: ")
        
        with open(join(directory, "test"), "w") as f:
            f.write(f"#!/bin/sh\npython3 {__file__}")
        
        os.chmod(join(directory, "test"), stat.S_IEXEC)

        should_change_git = input("Update .gitignore (Recommended) (y/n):")
        if should_change_git == "y":
            with open(join(directory,".gitignore"), "a") as f:
                f.write("test\n")
        print("Finished")
        sys.exit(0)
    run_tests()