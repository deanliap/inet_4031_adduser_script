#!/usr/bin/python3

# INET4031
# Deanna Liapis
# 11/6/25
# 11/8/25

#Import statements:
#os: imports functions that interact with the operating system
#re: imports regular expression tools for pattern matching and string manipulation
#sys: imports the sys module used to access system specific parameters and functions 
import os
import re
import sys


def main():
    for line in sys.stdin:

        #Check if the line starts with '#' (aka a comment line)
        match = re.match("^#",line)

        #Remove extra spaces and split the line by using ':'-- the split parts get turned into fields
	#This cleans up the data and splits to get the important parts, like the username, password, ids, and description 
        fields = line.strip().split(':')

        #If the line is a comment or the data doesn't have 5 fields (required of users), skip it since it's invalid
        if match or len(fields) != 5:
            continue

        #Username and password are extracted from the 0th and 1st field, they correspond to entries in the passwd file
	#The GECOS field is being formatted using the name and ID fields from the passwd data.
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3],fields[2])

        #Split the final field into into group names-- which are separated in the passwd file by commas
        groups = fields[4].split(',')

        #Display a status message showing which user account is about to be created.
        print("==> Creating account for %s..." % (username))
        #Build the shell command that will create the user account.
    	#The cmd stores the full adduser command. GECOS field is set for the username.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)

        #These lines are commented out for testing purposes. The script will actually create the user accounts if uncommented.
	#This time, cmd execute the adduser command to create the account.
	#Only uncomment when you are ready to run. 
        print cmd
        os.system(cmd)

        #Display a status message showing which user account the password is being set for.
        print("==> Setting the password for %s..." % (username))
        #Build a command to set the user's password by piping it twice into the passwd command-- this is because Linux needs to confirm the password after it's typed in.
        #This command will automatically set the specified password for the new user account.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)

        #These lines are commented out for testing purposes. The script will actually create the user accoutns if uncommented.
        #This time, cmd executes the passwd command to set the user's password
        #Only uncomment when you are ready to run. 
        print cmd
        os.system(cmd)

        for group in groups:
            #Check that the group field is not just a placeholder ('-').
       	    #If group != '-', it means the user actually belongs to a valid group, so the script will assign the user to that group using the adduser command.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                print cmd
                os.system(cmd)

if __name__ == '__main__':
    main()
