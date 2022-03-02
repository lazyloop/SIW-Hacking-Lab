# Extracting C&C commands from HTTP traffic



## Introduction

>This challenge is about decrypting SSL traffic using Wireshark.
You have found some suspicious traffic in your network. One host connects every 15 seconds to a machine with the domain name cnc.hacking-lab.com. You have already found out that the host in your network is infected with some sort of trojan horse. After some discussion with the owner of cnc.hacking-lab.com you have found out that his system got compromised and is being misused as a command and control server for the trojan horse found in your network. You have managed to convince him to give you the pem file containing the private key and certificate used by the cnc.hacking-lab.com. Your task is now to find out what the trojan horse has sent and received.
Instructions

    Get the network capture from the Resources section (.pcap file)
    Get the private key
    Decrypt traffic between the trojan and server
    Find the flag hidden in an encrypted request sent to the server.

> The flag is the base64 decoded url data that has been sent to the server (find here a handy base64 decoder) or use the linux CLI, as in this example : echo "SGVsbG8gYjY0IHdvcmxkICE=" | base64 --decode


## Writeup

When filtering out where HTTP request have been sent to one stands out
```bash
└─$ tshark -r 3014-recording.200.pcap -o "tls.keys_list:127.0.0.1,443,http,apache.pem"  -Y http -T fields -e http.host -e ip.dst | grep -v -e "^$" | sort -u
36ohk6dgmcd1n.yom.mail.yahoo.net
a323.yahoofs.com
ad.doubleclick.net
ads.bluelithium.com
ads.yimg.com
ad.yieldmanager.com
amch.questionmarket.com
avatars.zenfs.com
cnc.hacking-lab.com
content.yieldmanager.edgesuite.net
crl.geotrust.com
crl.thawte.com
dps.msg.yahoo.com
d.yimg.com
ftp2.freebsd.org:21
gateway05.hack.er:3128
l1.yimg.com
login.yahoo.com
login.yahoo.net
l.yimg.com
mail.yahoo.com
mail.yimg.com
mi.adinterax.com
notepad-plus.sourceforge.net
ocsp.digicert.com
presence.msg.yahoo.com
prod.rest-core.msg.yahoo.com
s0.2mdn.net
sports.yahoo.com
s.yimg.com
us.bc.yahoo.com
us.lrd.yahoo.com
us.mg5.mail.yahoo.com
webplayer.yahooapis.com
www.google.ch
www.yahoo.com
```
```gateway05.hack.er:3128 | 192.168.200.204```
Looking weird there....


This totally as well
```bash
└─$ tshark -r 3014-recording.200.pcap -o "tls.keys_list:127.0.0.1,443,http,apache.pem" -Y "http.host == cnc.hacking-lab.com" -T fields -e http.host -e http.request.uri
cnc.hacking-lab.com     /gc.php?r=Z2V0Q29tbWFuZD10cnVlJnVzZXI9V3hUckZrJnBhc3M9c2VjdXJlJnNlcmlhbD13eHBVSUQzMzEyNTUyMw==
...
cnc.hacking-lab.com     /gc.php?r=Z2V0Q29tbWFuZD10cnVlJnVzZXI9V3hUckZrJnBhc3M9c2VjdXJlJnNlcmlhbD13eHBVSUQzMzEyNTUyMw==
cnc.hacking-lab.com     /gc.php?r=Z2V0Q29tbWFuZD10cnVlJnVzZXI9V3hUckZrJnBhc3M9c2VjdXJlJnNlcmlhbD13eHBVSUQzMzEyNTUyMw==
cnc.hacking-lab.com     /gc.php?r=Z2V0Q29tbWFuZD10cnVlJnVzZXI9V3hUckZrJnBhc3M9c2VjdXJlJnNlcmlhbD13eHBVSUQzMzEyNTUyMw==
```

```bash
└─$ tshark -r 3014-recording.200.pcap -o "tls.keys_list:127.0.0.1,443,http,apache.pem" -Y "http.host == cnc.hacking-lab.com" -T fields -e http.request.uri | sed 's/\/gc.php?r=//g' > out && for x in $(cat out); do echo $x | base64 -d && echo; done
getCommand=true&user=WxTrFk&pass=secure&serial=wxpUID33125523
...
getCommand=true&user=WxTrFk&pass=secure&serial=wxpUID33125523
getCommand=true&user=WxTrFk&pass=secure&serial=wxpUID33125523
```
Perfection a username and a password. The flag is `getCommand=true&user=WxTrFk&pass=secure&serial=wxpUID33125523`