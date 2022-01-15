import requests
import sys
import argparse
from urllib.parse import urlparse
import random

parser = argparse.ArgumentParser(
    description="Simple reflected XSS Scanner"
)

parser.add_argument(
    "host",
    nargs="?",
    help="Host to test vulnerability"
)

parser.add_argument(
    "-d",
    "--data",
    help="Form data from POST request as key=value&key2=value"
)

parser.add_argument(
    "-s",
    "--session",
    help="Provide session headers as key=value&key2=value"
)

parser.add_argument(
    "-c",
    "--cookies",
    help="Provide cookies key=value&key2=value"
)
args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    print(
        f"Example: {sys.argv[0]} http://127.0.0.1:1337/form -d 'message=hello&csrf=nksnfksnfkj' -s 'session=abcdefg123456'")
    sys.exit(1)

if not args.host:
    print("No target provided")
    parser.print_help()
    sys.exit(1)

if not args.data:
    print("No form data provided")
    parser.print_help()
    sys.exit(1)


def to_dict(data):
    # Send help
    parsed = {}
    for fv in data.split("&"):
        fv = fv.split("=")
        parsed[fv[0]] = fv[1]
    return parsed


def get_payloads():
    return [
        payload for payload in
        requests.get(
            "https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/Intruder/xss-payload-list.txt").text.split(
            "\n")
        if "alert(1)" in payload
    ]


def alter_payload(payload, key, nonce):
    detection = f'"{nonce}:{key}:"+document.domain'
    return payload.replace("alert(1)", f"alert({detection})")


def create_session(domain, scheme, cookies, headers):
    sess = requests.Session()
    sess.get(f"{scheme}://{domain}")

    #cookies = to_dict(cookies)
    #headers = to_dict(headers)

    #sess.cookies = {**sess.cookies, **cookies}
    #sess.headers = {**sess.headers, **headers}

    return sess


def send_payload(sess, url, data, domain):
    nonce = random.getrandbits(100)
    payloads = get_payloads()

    for payload in payloads:
        for key in data:
            data[key] = alter_payload(payload, key, nonce)

    resp = sess.post(url=url, data=data).text
    for key in data:
        if data[key] in resp:
            print(f"Parameter {key} is vulnerable to payload: {payload}")
            exit(0)
    print(f"{domain} is not vulnerable to XSS")



def sanity_check(sess, url, data):
    resp = sess.post(url=url, data=data)
    if resp.status_code != 200:
        print(resp.text)
        print(f"Sanity check failed. Status code {resp.status_code}")
        return False
    return True


def main():
    target = urlparse(args.host)
    data = args.data
    domain = target.hostname

    sess = create_session(domain, target.scheme, args.cookies, args.session)
    data = to_dict(data)
    assert (sanity_check(sess=sess, url=args.host, data=data))

    send_payload(sess=sess, url=args.host, data=data, domain=domain)


if __name__ == "__main__":
    main()
