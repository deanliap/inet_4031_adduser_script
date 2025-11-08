#!/usr/bin/python3

# INET4031
# Deanna Liapis
# 11/8/25

import os
import re

def main():
    # Ask for dry-run
    dry_run_input = input("Run in dry-run mode? (Y/N): ").strip().upper()
    dry_run = True if dry_run_input == 'Y' else False

    # Open the input file explicitly
    with open("create-users.input") as f:
        for line in f:
            # Skip commented lines
            match = re.match("^#", line)

            # Split fields by colon
            fields = line.strip().split(':')

            # Skip invalid lines (not 5 fields or comment)
            if match or len(fields) != 5:
                if dry_run:
                    if match:
                        print("Dry run, skipping commented line:", line.strip())
                    else:
                        print("Dry run, skipping invalid line (wrong number of fields):", line.strip())
                continue

            # Extract user info
            username = fields[0]
            password = fields[1]
            gecos = "%s %s,,," % (fields[3], fields[2])

            # Split groups
            groups = fields[4].split(',')

            # Create user
            print("==> Creating account for %s..." % username)
            cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
            if dry_run:
                print("Dry run, would execute:", cmd)
            else:
                os.system(cmd)

            # Set password
            print("==> Setting the password for %s..." % username)
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
            if dry_run:
                print("Dry run, would execute:", cmd)
            else:
                os.system(cmd)

            # Assign groups
            for group in groups:
                if group != '-':
                    print("==> Assigning %s to the %s group..." % (username, group))
                    cmd = "/usr/sbin/adduser %s %s" % (username, group)
                    if dry_run:
                        print("Dry run, would execute:", cmd)
                    else:
                        os.system(cmd)

if __name__ == '__main__':
    main()
