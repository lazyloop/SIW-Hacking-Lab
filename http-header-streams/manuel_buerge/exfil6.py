from urllib.parse import urlparse
from urllib.parse import parse_qs
from string import ascii_lowercase, digits

chars = ascii_lowercase+ digits
def rot_n(message, offset):
    rot_message = [x for x in message]
    for x in range(len(rot_message)):
        char = str(rot_message[x]).lower()
        if char != " ":
            index = chars.find(char)

            shift = (index + offset)%26
            rot_message[x] = chars[shift]
    return ''.join(rot_message)

f = open("out","r").readlines()
for line in f:
    request = urlparse(line)
    message = parse_qs(request.path)['message'][0]
    offset = 26 - int(parse_qs(request.path)['off-set'][0])

    x = rot_n(message, offset)
    print(x)
       
