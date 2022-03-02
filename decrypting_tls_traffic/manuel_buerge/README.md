# Decrypting SSL/TLS Traffic

## Explanation

> When you have the SSL/TLS private key, it is possible to decrypt the SSL traffic. This can be extremely useful, if you have to debug HTTPS traffic and cannot use HTTP instead or put a MITM front. SSL decryption only works with RSA key exchange if the RSA keys can be provided.
Instruction
In this case you have a network capture between a web client and server, you have the key and should:

    Get the network capture from the Resources section (.pcap file)
    Get the private key
    Decrypt traffic between client and server
    Find the flag hidden in a "sensitive web page"

> The flag is the content of the first line (and first line only) after the ``<body>`` tag

To decrypt the TLS traffic we can open the pcap in Wireshark and go to
`Edit -> Preferences -> Protocols -> TLS -> RSA key list`
Then add
```127.0.0.1 443 http c:/temp/lab.temp```

Or in tshark
```bash
└─$ tshark -r lab.pcap -q -o "tls.keys_list:127.0.0.1,443,http,lab.pem" -z "follow,tls,ascii,3"
```

```html
<html>
<head>
<title>Protected</title>
</head>
<body>
This is the SSL/TLS protected web page.
<br>
You have completed this lab successfully.
</body>
</html>
```