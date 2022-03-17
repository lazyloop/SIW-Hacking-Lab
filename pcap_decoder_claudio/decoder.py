#!/usr/bin/env python3
# author: lazyloop
# datum : 2022/03/12

import sys
import argparse
import pyshark
import urllib.parse
import base64
from colorama import Fore

# Globale Variablen
pcap_filter = 'http.request.method == GET && tcp.dstport == 80'
search_string = 'The next flag is'

# Farbdefinitionen
red = Fore.LIGHTRED_EX
blu = Fore.LIGHTBLUE_EX
gre = Fore.LIGHTGREEN_EX
wht = Fore.LIGHTWHITE_EX
yel = Fore.YELLOW
rst = Fore.RESET

# Argument Parser

if len(sys.argv) != 3:
  print("[!] as source it needs a pcap file and as a second parameter the encoding type.")
  exit()

pcap_file = sys.argv[1]
encoding_type = sys.argv[2]

def pcap_wrapper():

    list = []

    # Beispiel Output von pcap mit den zusätzlichen Parametern display_filter und only_summaries 
    # 17961 13.085228873 146.64.8.10 146.64.213.83 HTTP 354 GET /?message=++The+next+flag+is+560E6C8A06A0EF5EA376F3BA712CDD5A HTTP/1.1
    pcap = pyshark.FileCapture(pcap_file, display_filter=pcap_filter, only_summaries=True)
    
    for packet in pcap:

        if 'message=' in str(packet):
            # Mit dem ersten split() wird pcap nach "message=" in zwei Teile getrennt
            # Mit dem zweiten split() trennen wir den "HTTP/1.1" String 
            list.append(str(packet).split('message=')[-1].split(' ')[0])
    
    return list


def pcap_resultset():

    pcap_list = pcap_wrapper()
    pcap_unique_items = set(pcap_list)

    for item in pcap_unique_items:
        if item != '':
            print(f'[+] {url_decoder(item)}')
    print('')


def url_decoder(item):

    output = urllib.parse.unquote_plus(item)
    return output


def get_the_flag(text_string):

    if search_string in text_string:
        flag = text_string
        print(f'{gre}{flag}')


def decoder(encoding):

    if encoding != 'plain':

        for item in pcap_wrapper():
            base_string = url_decoder(item)
            base_bytes = base_string.encode('ascii')
            
            if encoding == 'base64':
                text_bytes = base64.b64decode(base_bytes)
            elif encoding == 'base32':
                text_bytes = base64.b32decode(base_bytes)
            elif encoding == 'base16':
                text_bytes = base64.b16decode(base_bytes)
            
            text_string = text_bytes.decode('ascii')
            get_the_flag(text_string)
    else:
        for item in pcap_wrapper():
            text_string = url_decoder(item)
            get_the_flag(text_string)


def main():

    print(f'{blu}**************************************************************************************************************')
    print(f'{yel}[I] {rst}list pcap items filtered by {yel}[{pcap_filter}]{rst} and decoded from {yel}[{encoding_type}]')
    print(f'{blu}**************************************************************************************************************{rst}\n')

    pcap_resultset()

    try:
        decoder(encoding_type)
    except ValueError:
        print(f'{yel}[!] the given input is not {encoding_type}')
    

if __name__ == "__main__":
    main()