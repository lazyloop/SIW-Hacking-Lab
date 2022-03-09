import sys
import pyshark
from codecs import decode
from urllib.parse import urlparse, unquote_plus


def _decode(data, encoding):
    if encoding == "plain":
        return data
    try:
        return decode(data, encoding)
    except:
        try:
            return decode(data.encode(), encoding).decode()
        except:
            return f"Unable to decode {data} with {encoding}"
def format_params(query):
    q = query.split("&")
    res = []
    for x in q:
        x = x.split("=")
        if len(x) == 1 or x[1] == "": return None
        res.append({"key": x[0], "value": unquote_plus(x[1])})
    return res


def get_query(packet):
    requests = []
    if "request" in dir(packet.http):
        request = urlparse(packet.http.request_full_uri)
        if request.query: requests.append(request.query)
    return requests


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"USAGE: {sys.argv[0]} file encoding")
        print(f"python3 {sys.argv[0]} file.pcap base64")
        exit(0)

    print(f"[+] FILE: {sys.argv[1]}")
    cap = pyshark.FileCapture(sys.argv[1], display_filter='http')
    encoding = sys.argv[2]

    for packet in cap:
        queries = get_query(packet)
        for query in queries:
            params = format_params(query)
            if params is not None:
                for param in params:
                    param["value"] = _decode(param["value"], encoding)
                    print(f"KEY:{param['key']} Value:{param['value']}")
