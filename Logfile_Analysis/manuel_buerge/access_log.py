import re


def parse_line(line):
    # Nobody has a good time doing regex like this, right?
    pattern = r'(?P<src_ip>.*?)\s-\s-\s\[' \
              r'(?P<timestamp>.*?)\]\s\"' \
              r'(?P<method>.*?)\s' \
              r'(?P<url>.*?)\s' \
              r'(?P<proto>.*?)\"\s' \
              r'(?P<status_code>.*?)\s' \
              r'(?P<resp_size>.*?)\s\"' \
              r'(?P<http_referer>.*?)\"\s\"' \
              r'(?P<user_agent>.*?)\"(.*)'
    return re.match(pattern, line).groupdict()


def unparse_line(line):
    return f'{line["src_ip"]} - - [{line["timestamp"]}] "{line["method"]} {line["url"]} {line["proto"]}" ' \
           f'{line["status_code"]} {line["resp_size"]} "{line["http_referer"]}" "{line["user_agent"]}" "-"'



def get_unique(map_layout, logs):
    map_unique = map_layout.copy()
    for log in logs:
        for u_key in map_unique.keys():
            if log[u_key] not in map_unique[u_key]:
                map_unique[u_key][log[u_key]] = 1
            else:
                map_unique[u_key][log[u_key]] += 1
            map_unique[u_key] = dict(sorted(map_unique[u_key].items(), key=lambda item: item[1]))
    return map_unique


def get_sus(entries, logs):
    result = []
    for log in logs:
        for entry in entries:
            if entry["value"] in log[entry["type"]]:
                x = log[entry["type"]]
                match = unparse_line(log)
                match = match.replace(x, f"\033[91m{x}\033[0m")
                if match not in result:
                    result.append(match)
    return result


def get_connection_count(logs):
    count = {}
    for log in logs:
        src = log["src_ip"]
        if src in count.keys():
            count[src] += 1
        else:
            count[src] = 1
    return dict(sorted(count.items(), key=lambda item: item[1]))


def get_bytes_received(logs):
    count = {}

    def conv(x):
        try: return int(x)
        except: return 0

    for log in logs:
        src = log["src_ip"]
        if src in count.keys():
            count[src] += conv(log["resp_size"])
        else:
            count[src] = conv(log["resp_size"])
    return dict(sorted(count.items(), key=lambda item: item[1]))


if __name__ == "__main__":
    logs = [parse_line(line) for line in open("access.log", "r").readlines()]
    print(f"### {len(logs)} REQUESTS HAVE BEEN DETECTED")

    map_layout = {"src_ip": {}, "url": {}, "http_referer": {}, "user_agent": {}, "status_code": {}}

    unique_entries = get_unique(map_layout=map_layout, logs=logs)
    TAB = '\n    - '

    str_ip_addresses = TAB + TAB.join(
        [f"({unique_entries['src_ip'][entry]}x) {entry}" for entry in unique_entries['src_ip']]
    )
    print(f"\n### {len(unique_entries['src_ip'])} Unique IP addresses: \n{str_ip_addresses}\n")

    url = TAB + TAB.join(
        [f"({unique_entries['url'][entry]}x) {entry}" for entry in unique_entries['url']]
    )
    print(f"\n### {len(unique_entries['url'])} Unique URLs: \n{url}\n")

    http_referer = TAB + TAB.join(
        [f"({unique_entries['http_referer'][entry]}x) {entry}" for entry in unique_entries['http_referer']]
    )
    print(f"\n### {len(unique_entries['http_referer'])} Unique HTTP referers: \n{http_referer}\n")

    user_agent = TAB + TAB.join(
        [f"({unique_entries['user_agent'][entry]}x) {entry}" for entry in unique_entries['user_agent']]
    )
    print(f"\n### {len(unique_entries['user_agent'])} Unique User-Agents: \n{user_agent}\n")

    status_code = TAB + TAB.join(
        [f"({unique_entries['status_code'][entry]}x) {entry}" for entry in unique_entries['status_code']]
    )
    print(f"\n### {len(unique_entries['status_code'])} Unique status codes: \n{status_code}\n")


    connection_count = get_connection_count(logs)
    str_connection_count = TAB + TAB.join([f"{connection_count[n]} connections for {n}" for n in connection_count])
    print(f"\n### {len(connection_count)} Amount of requests submitted by source IP: \n{str_connection_count}\n")

    bytes_received = get_bytes_received(logs)
    str_bytes_received = TAB + TAB.join([f"{bytes_received[n]} bytes received by {n}" for n in bytes_received])
    print(f"\n### {len(connection_count)} Amount of bytes received by source IP: \n{str_bytes_received}\n")

    map_sus_entries = [
        {"type": "url", "value": "/robots.txt"},
        {"type": "url", "value": "/apache-log/access.log"},
        {"type": "url", "value": "/robots.txt"},
        {"type": "user_agent", "value": ".NET CLR"},
        {"type": "user_agent", "value": "T-Online Browser"},
        {"type": "user_agent", "value": "Bot"},
        {"type": "user_agent", "value": "zgrab"},
        {"type": "user_agent", "value": "curl"},
        {"type": "status_code", "value": "404"},
        {"type": "status_code", "value": "400"},
        {"type": "status_code", "value": "500"},
    ]
    sus = get_sus(entries=map_sus_entries, logs=logs)
    sus_entries = TAB + TAB.join(sus)
    print(f"\n### {len(sus)} Suspicious entries: \n{sus_entries}\n")
