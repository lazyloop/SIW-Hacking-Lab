import re


def get_executed_commands(logs):
    commands = []
    for line in logs:
        if "COMMAND" in line:
            pattern = r".*PWD=(?P<directory>.*)\S.*USER=(?P<user>.*)\S.*COMMAND=(?P<command>.*)$"
            commands.append(re.match(pattern, line).groupdict())
    return commands


def get_successful_ssh(logs):
    logins = []
    for line in logs:
        if "Accepted password" in line and "sshd" in line:
            pattern = r".*Accepted password for (?P<user>.*) from (?P<src_ip>.*) .*$"
            logins.append(re.match(pattern, line).groupdict())
    return logins


def get_failed_ssh(logs):
    logins = []
    for line in logs:
        if "Failed password" in line and "sshd" in line:
            pattern = r".*Failed password for (?P<user>.*) from (?P<src_ip>.*) .*$"
            logins.append(re.match(pattern, line).groupdict())
    return logins


if __name__ == "__main__":
    logs = [line for line in open("auth.log", "r").readlines()]

    TAB = '\n    - '

    commands = get_executed_commands(logs)
    str_commands = TAB + TAB.join(
        [f"User {command['user']} executed {command['directory']} {command['command']}" for command in commands]
    )
    print(f"\n### {len(commands)} Commands executed: \n{str_commands}\n")

    logins = get_successful_ssh(logs)
    str_logins = TAB + TAB.join(
        [f"User {login['user']} logged in from {login['src_ip']}" for login in logins]
    )
    print(f"\n### {len(logins)} successful logins: \n{str_logins}\n")

    failed_logins = get_failed_ssh(logs)
    str_logins = TAB + TAB.join(
        [f"User \"{login['user']}\" failed from {login['src_ip']}" for login in failed_logins]
    )
    print(f"\n### {len(failed_logins)} unsuccessful logins: \n{str_logins}\n")
