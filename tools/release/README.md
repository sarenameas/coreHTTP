# Changelog preliminary update script.

## Prerequisites

- [Git](https://git-scm.com/downloads/)
- [Python 3](https://www.python.org/downloads/)

## Output

This scripts overwrites the existing CHANGELOG.md in the current library repo
to include all of the PRs since the last release. Not all of the PRs belong in
the CHANGELOG.md, but they are formatted in a compliant way for you to edit.

## Usage

1. Run this script with the current working directory as the library repo root.
The next release version, organization, and name of the library repo are optional.
If you don't add these parameters, then a placeholder will be written.

    ```console
    pythons update_changelog.py --version v1.0.1 --org aws --name coreHTTP
    ```

1. The CHANGELOG.md will be updated directly. Check your Git diff. See an example
output below.

    ![](example_output.jpg?raw=true)