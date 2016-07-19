#!/usr/bin/env python

# Imports
import os
import sys
import argparse
import platform
from getpass import getpass

# Project Imports
import auth


def main():
    if platform.system() == 'Windows':
        os.system("title PoGoStick - Pokemon Go API")
        os.system("cls")
    elif platform.system() == 'Linux' or 'Darwin':
        sys.stdout.write("\x1b]2;PoGoStick - Pokemon Go API\x07")
        os.system("clear")
    else:
        os.system("clear")
        print("[!] Running on untested operating system.  Your mileage may vary.")

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="\"Google\" or \"PTC\" for authentication", required=True)
    parser.add_argument("-u", "--username", help="Username", default=None)
    parser.add_argument("-p", "--password", help="Password", default=None)
    args = parser.parse_args()
    if args.auth.lower() == "google":
        args.auth = "Google"
    elif args.auth.lower() == "ptc":
        args.auth = "PTC"
    else:
        print("[*] %s is not a valid authentication type.  Select Google or PTC." % args.auth)
        sys.exit(-1)

    if not args.username:
        args.username = raw_input("Username: ")
    if not args.password:
        args.password = getpass("Password: ")

    access_token = auth.authenticate(args.username, args.password, args.auth)


if __name__ == '__main__':
    main()
