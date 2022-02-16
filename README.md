# GitHub Classroom Local Autograding
A python program to run Github Classroom auto-grading tests locally. 
This program will try to extract the .json test descriptions, run them against the code, 
and show the user the results in a much more readable format than the GitHub Classroom default
diffs. 

### A Few Notes on Security
This program reads commands from a file and executes them. It is important
to know and trust the source of any repository that this program is run against to prevent
arbitrary code execution. If you are unsure if a repository is trustworthy you
can inspect the tests at ```./github/classroom/autograding.json```.

## Usage
### Installation
First clone this repository and submodules
```
git clone --recursive https://github.com/Aetheris743/GitHub-Classroom-Local-Autograding/ {WHERE_YOU_WANT_TO_PUT_THIS}
```
then use python to run the main file (Note: python does need to be 
installed and can be installed using a package manager such as apt ```sudo apt install python3```
or from [Python.org](https://www.python.org/))
```
python3 ./GitHubTests/GitHubTestRunner.py
```
it will prompt you to enter the absolute path to the GitHub Classroom repository.
It will also prompt the user if it should automatically add the file it creates to the 
.gitignore file so that it is not accidentally added to git.
Then it will write a shell script to that repository to allow the tests to be run
at a future time by running:
```
./test
```
in the GitHub Classroom repository.

### What it Does
After running
```
./test
```
this program will run all of the GitHub tests locally, and print the results. Indicating whether
each test passed or failed with a ✅ or ❌ respectively.
```
EXAMPLE:

[0] - ❌ <test_1_name>
[1] - ✅ <test_2_name>
[2] - ✅ <test_3_name>
...
>
```
The user can then input the number of the test they would like to examine and it will show the test
input as well as the diffs between the files using ✅ to indicate that a line is correct and ❌ 
with incorrect lines with the correct line [underlined in blue]() right below it.
```
EXAMPLE INPUTS

OUTPUT                            GOAL
enter a number:                   Enter a number:
You entered: 2                    You entered: 2
2 squared is 4                    2 squared is 4
                                    
And... 4 Squared is 16            And... 4 squared is 16
```
```
EXAMPLE OUTPUT
Test 'test 1' used input '2\n'

❌ enter a number:
    Enter a number:
✅ You entered: 2
✅ 2 squared is 4
✅
❌ And... 4 Squared is 16
    And... 4 squared is 16
```
Then you can choose another test to inspect or exit the test inspector.

## How to Contribute

If you find any bugs feel free to [open issues on this repository](https://github.com/Aetheris743/GitHub-Classroom-Local-Autograding/issues/new/choose).
Or if you would like to contribute or change anything, you can fork the repository and open a pull request.
