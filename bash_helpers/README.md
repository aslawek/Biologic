# bash scripts
Here I put some shell scripts for helping with the data.

I use it with git bash:
1) install git bash: next-next-next, tick "Windows Explorer integration -> Git Bash Here", next-next-next
2) go to folder .../Biologic/bash_helpers, use "Git Bash Here" and in terminal type "pwd"
3) type: "cd ~", then "touch .bashrc", and "export PATH=$PATH:/d/Python/Biologic/bash_helpers > .bashrc". Note, here put your path from pwd command!
4) restart terminal two times

Now you can use any script from "../Biologic/bash_helpers" by typing their names in Git Bash terminal.

**find_and_list_data.sh** - in data folder (default is /data) it will search for files according to type of Biologic data (CA/CV etc.) and given phrase.