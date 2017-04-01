1. Download the Latest version of virtual box.
2. Download and install Vagrant.
3. Clone or Download the VM configuration files from "https://github.com/dinker1462/fullstack-nanodegree-vm"
4. 'cd' to the vagrant directory in the downloaded folder
5. Run the command 'vagrant up' in your terminal, it may take several minutes for vagrant to set itself up
6. Run the command 'vagrant ssh'
7. Change the directory to '/vagrant/tournament'
8. Enter the PSQL command interface using the command 'psql'
9. Import the database config file with command '\i tournament.sql'
10. Go back to the terminal and run the python files 'tournament.py' and 'tournament_test.py'