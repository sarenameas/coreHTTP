#!/usr/bin/env python3
import subprocess
import re
import argparse
import os
from datetime import datetime

# Month number to string map.
month_map = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

def run_cmd(cmd):
    """
    Execute the input command on the shell.
    """
    print(f"Executing command: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            encoding="utf-8",
            check=True,
            timeout=180,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        result = e.stdout
        return result


def main():
    """
    Update the CHANGELOG.md in this repo.
    """
    parser = argparse.ArgumentParser(description="Create a preliminary change.")
    parser.add_argument(
        "--root", "-r",
        action="store",
        dest="root",
        default=".",
        required=False,
        help="The root path to the the library repo.",
    )
    parser.add_argument(
        "--version", "-v",
        action="store",
        dest="version",
        default="<next_version>",
        required=False,
        help="The next version of this library."
    )
    parser.add_argument(
        "--org", "-o",
        action="store",
        dest="org",
        default="<org>",
        required=False,
        help="The Github organization this library belongs to.")
    parser.add_argument(
        "--repo", "-n",
        action="store",
        dest="repo",
        default="<repo>",
        required=False,
        help="The Github repo name of this library.")

    args = parser.parse_args()
    root = args.root
    version = args.version
    repo = args.repo
    org = args.org

    # Ensure the cwd is the the root specified.
    os.chdir(root)

    # Get the current tag.
    current_tag = run_cmd("git describe --tags --abbrev=0").split("\n")[0]

    # Get the all of the commits since the last tag.
    commits = run_cmd(f'git log --pretty="%s" {current_tag}..HEAD').split("\n")[:-1]
    commits.reverse()

    # Format the PR and commit.
    updates = []
    for commit in commits:
        search = re.search("(.*)(\(\#.*\))", commit)
        msg = search.group(1)
        pr = search.group(2)
        commit = " - " + pr.replace("(", "[").replace(")", "]")
        commit += f"(https://github.com/{org}/{repo}/pull/{pr[2:-1]}) "
        commit += msg[:-1] + "\n"
        updates.append(commit)

    # Format each of these PRs into bullet points.

    # Update the CHANGELOG.md
    with open("CHANGELOG.md", "r+") as f:
        changelog = f.readlines()
        f.seek(0)
        f.write(changelog[0])
        f.write("\n")
        f.write(f"## {version} {month_map[datetime.now().month]} {datetime.now().year}\n")
        f.write("\n")
        for update in updates:
            f.write(update)
        f.writelines(changelog[1:])


if __name__ == "__main__":
    main()
