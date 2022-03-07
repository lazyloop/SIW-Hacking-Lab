# HTTP Header Streams


>Introduction
You suspect that one of your employees is exfiltrating confidential company data using HTTP header streams.
You are provided with seven .pcap files containing messages sent out by the employee to his private server at 146.64.213.83
Mission
Extract the seven flags within the seven .pcap files. Provide a file with the following format :

    data-exfiltration1.pcap flag type of data (eg.: plain text, base16)
    ...
    data-exfiltration7.pcap flag type of data

>Hint
For file number 7: "Mr. X 007" has become "Ms. Z 007".

### Solution
data-exfiltration1.pcap 560E6C8A06A0EF5EA376F3BA712CDD5A Plain
data-exfiltration2.pcap AEB30D916CC6F922368C1821D786944D Base64
data-exfiltration3.pcap B4ECB8E61DA060BC3E0484ECBB920E49 Hexadecimal
data-exfiltration4.pcap C0FCFEA5BBE5EA9C95B1B7333035BA94 Base32
data-exfiltration5.pcap E98CF92E590D707CF96EDFE623371F55 Rot19
data-exfiltration6.pcap DA738421F6587A89EE87EE5207A6A7F2 Rot N
data-exfiltration7.pcap c0fcfea5bbf6587f6587f6587d786944d786944 trithemius cipher


## data-exfiltration1.pcap
```bash
└─$ tshark -r data-exfiltration1.pcap  -Y http | grep flag
17960 13.084621289 146.64.212.80 → 146.64.8.10  HTTP 262 GET http://146.64.213.83/?message=++The+next+flag+is+560E6C8A06A0EF5EA376F3BA712CDD5A HTTP/1.1
17961 13.085228873  146.64.8.10 → 146.64.213.83 HTTP 354 GET /?message=++The+next+flag+is+560E6C8A06A0EF5EA376F3BA712CDD5A HTTP/1.1
```


## data-exfiltration2.pcap
Noticed Base64 encoded strings in HTTP Requests
```bash
└─$ tshark -r data-exfiltration2.pcap -Y http | grep -oP "message=\K\w+" | base64 -d
In entirely be to at settling felicity[[\[HH][[X]Bg'VBGvF6VR6WfV6&Rg'VBGvF6VR6WfV6&RVVFVB2"2VVvG2VVFVB2"2VVvG2֖W2B6'B''vRƖV"֖W2B6'B''vRƖV"6R"6v6F7VW"6R"6v6F7V In post mean shot ye In post mean shot ye There out her child sir his livedFW&RWBW"6B6"2ƗfV@ Design at uneasy me season of branch on praise esteem Design at uneasy me season of branch on praise esteem Abilities discourse believing consisted remaining to nX[]Y\\\H[Y][ۜ\[XZ[[7FVRFVFrF6vB267&VVVB֗7FVRFVFrF6vB267&VVVBvV6R"W7FVVV6ǒRvV6R"W7FVVV6ǒRF77VFRW6&G2BbbF76F77VFRW6&G2bbF76
```
Lotta gibberish. Lets add padding and try again
```bash
└─$ for str in $(cat out); do echo "$str"==== | fold -w 4 | sed '$ d' | tr -d '\n' | base64 --d; done
In entirely be to at settling felicityIn entirely be to at settling felicity Fruit two match men you seven share Fruit two match men you seven share Needed as or is enough points Needed as or is enough points Miles at smart no marry whole linen mr Miles at smart no marry whole linen mr Income joy nor can wisdom summer Income joy nor can wisdom summer Extremely depending he gentleman improving intention rapturous as Extremely depending he gentleman improving intention rapturous as The next flag is AEB30D916CC6F922368C1821D786944D The next flag is AEB30D916CC6F922368C1821D786944D In post mean shot ye In post mean shot ye There out her child sir his lived There out her child sir his lived Design at uneasy me season of branch on praise esteem Design at uneasy me season of branch on praise esteem Abilities discourse believing consisted remaining to no Abilities discourse believing consisted remaining to no Mistaken no me denoting dashwood as screened Mistaken no me denoting dashwood as screened Whence or esteem easily he on Whence or esteem easily he on Dissuade husbands at of no if disposal Dissuade husbands at of no if disposal
```

## data-exfiltration3.pcap

Ooooh it's Hex. Daring we today
```bash
└─$ tshark -r data-exfiltration3.pcap -Y http | grep -oP "message=\K\w+" | xxd -r -p
Started several mistake joy say painful removed reached endStarted several mistake joy say painful removed reached end State burst think end are its State burst think end are its Arrived off she elderly beloved him affixed noisier yet Arrived off she elderly beloved him affixed noisier yet An course regard to up he hardly An course regard to up he hardly View four has said does men saw find dear shy View four has said does men saw find dear shy Talent men wicket add garden Talent men wicket add garden The next flag is B4ECB8E61DA060BC3E0484ECBB920E49 The next flag is B4ECB8E61DA060BC3E0484ECBB920E49 Village did removed enjoyed explain nor ham saw calling talking Village did removed enjoyed explain nor ham saw calling talking Securing as informed declared or margaret Securing as informed declared or margaret Joy horrible moreover man feelings own shy Joy horrible moreover man feelings own shy Request norland neither mistake for yet Request norland neither mistake for yet Between the for morning assured country believe Between the for morning assured country believe On even feet time have an no at On even feet time have an no at Relation so in confined smallest children unpacked delicate Relation so in confined smallest children unpacked delicate Why sir end believe uncivil respect Why sir end believe uncivil respect Always get adieus nature day course for common Always get adieus nature day course for common My little garret repair to desire he esteem My little garret repair to desire he esteem
```

## data-exfiltration4.pcap

Best I can do is invalid input
```bash
└─$ tshark -r data-exfiltration4.pcap -Y http | grep -oP "message=\K\w+" > out
└─$ for str in $(cat out); do echo "$str"==== | fold -w 4 | sed '$ d' | tr -d '\n' | base32 --d; done
Departure so attention pronounce satisfied daughters amDeparture so attention pronounce satisfied daughters am But shy tedious pressed studied opinion entered windows off But shy tedious pressed studied opinion entered windows off Advantage dependent suspicion convinced provision him yet Advantage dependent suspicion convinced provision him yet Timed balls match at by rooms we Timed balls match at by rooms we Fat not boy neat left had with past here calbase32: invalid input
 Fat not boy neat left had with past here calbase32: invalid input
 Court nay merit few nor party learbase32: invalid input
 Court nay merit few nor party learbase32: invalid input
 Why our year her eyes know even hobase32: invalid input
 Why our year her eyes know even hobase32: invalid input
 Mr immediate remaining conveying allowance do or Mr immediate remaining conveying allowance do or The next flag is C0FCFEA5BBE5EA9C95B1B7333035BA94 The next flag is C0FCFEA5BBE5EA9C95B1B7333035BA94 Depart do be so he enough talent Depart do be so he enough talent Sociable formerly six but handsome Sociable formerly six but handsome Up do view time they shobase32: invalid input
 Up do view time they shobase32: invalid input
 He concluded disposing provision by questions as situation He concluded disposing provision by questions as situation Its estimating are motionless day sentiments end Its estimating are motionless day sentiments end Calling an imagine at forbade Calling an imagine at forbade At name no an what like spot At name no an what like spot Pressed my by do affixed he studiebase32: invalid input
 Pressed my by do affixed he studiebase32: invalid input
```

## data-exfiltration5.pcap

Not gonna solve cesar cipher in bash, lol
```bash
└─$ tshark -r data-exfiltration5.pcap -Y http -T fields -e http.request.uri.query | grep -v -e "^$" | grep -v "wsdl" | sed 's/message=//g'
Ylthpu+chsslf+dov+tyz+bulhzf+yltvcl+dvvklk+opt+fvb
...
+Ahsrpun+zlaaslk+ha+wslhzlk+hu+vm+tl+iyvaoly+dlhaoly
+Ahsrpun+zlaaslk+ha+wslhzlk+hu+vm+tl+iyvaoly+dlhaoly
```

Rot19
```bash
Remain+valley+who+mrs+uneasy+remove+wooded+him+you
Remain+valley+who+mrs+uneasy+remove+wooded+him+you
+Her+questions+favourite+him+concealed
+Her+questions+favourite+him+concealed
+We+to+wife+face+took+he
+We+to+wife+face+took+he
+The+taste+begin+early+old+why+since+dried+can+first
+The+taste+begin+early+old+why+since+dried+can+first
+Prepared+as+or+humoured+formerly
+Prepared+as+or+humoured+formerly
+Evil+mrs+true+get+post
+Evil+mrs+true+get+post
+Express+village+evening+prudent+my+as+ye+hundred+forming
+Express+village+evening+prudent+my+as+ye+hundred+forming
+Thoughts+she+why+not+directly+reserved+packages+you
+Thoughts+she+why+not+directly+reserved+packages+you
+Winter+an+silent+favour+of+am+tended+mutual
+Winter+an+silent+favour+of+am+tended+mutual
++The+next+flag+is+E98CF92E590D707CF96EDFE623371F55
++The+next+flag+is+E98CF92E590D707CF96EDFE623371F55
+At+ourselves+direction+believing+do+he+departure
+At+ourselves+direction+believing+do+he+departure
+Celebrated+her+had+sentiments+understood+are+projection+set
+Celebrated+her+had+sentiments+understood+are+projection+set
+Possession+ye+no+mr+unaffected+remarkably+at
+Possession+ye+no+mr+unaffected+remarkably+at
+Wrote+house+in+never+fruit+up
+Wrote+house+in+never+fruit+up
+Pasture+imagine+my+garrets+an+he
+Pasture+imagine+my+garrets+an+he
+However+distant+she+request+behaved+see+nothing
+However+distant+she+request+behaved+see+nothing
+Talking+settled+at+pleased+an+of+me+brother+weather
+Talking+settled+at+pleased+an+of+me+brother+weather
```

## data-exfiltration6.pcap

Same here... But they seem to have offsets.
```bash
└─$ tshark -r data-exfiltration6.pcap -Y "http && ip.dst==146.64.213.83" -T fields -e http.request.uri.query
message=Lgz+tkc+ysgrrtkyy+lkc+yavvuyotm+yayvoiout+zcu&off-set=6
message=+Frxuvh+vlu+shrsoh+zruwkb+kruvhv+dgg+hqwluh+vxiihu&off-set=3
message=+Szh+zyp+ofww+rpe+mfdj+olcp+qlc&off-set=11
message=+Ha+wypujpwsl+wlymljasf+if+zdllaulzz+kv&off-set=7
message=+Nf+ze+fgnegrq+neeviny+fhowrpg+ol+oryvrir&off-set=13
message=+Xywnhyqd+szrjwtzx+tzyqnaji+pnsisjxx+bmfyjajw+ts+bj+st+ts+fiinynts&off-set=5
message=++Wkh+qhaw+iodj+lv+GD738421I6587D89HH87HH5207D6D7I2&off-set=3
message=+Xi+gtpa+htci+ndjg+pi&off-set=15
message=+Htvbualk+hss+zof+zla+dof+mvssvdlk+kljshylk&off-set=7
message=+Ercrngrq+bs+raqrnibe+ze+cbfvgvba+xvaqarff+bssrevat+vtabenag+fb+hc&off-set=13
message=+Ukornkekva+ctg+ogncpejqna+rtghgtgpeg+eqpukfgtgf+ucy+eqorcpkqpu&off-set=2
message=+Glvsrvdo+rq+rxwzhljk+gr+vshhglob+lq+rq&off-set=3
message=+Mnr+mfr+fqymtzlm+ymtzlmyx+jsynwjqd+iwfbnslx&off-set=5
message=+Giikvzgtik+atxkykxbkj+urj+gjsoxgzout+vxupkizout+tge+ekz+nos&off-set=6
message=+Aphits+pb+hd+qtudgt+dc+thittb+kpcxin+dw&off-set=15
message=+&off-set=13
```
Writing a small script to `rot n` decode based on the offset and it looks like this
```bash
└─$ python3 exfil6.py
fat new smallness few supposing suspicion two
 course sir people worthy horses add entire suffer
 how one dull get busy dare far
 at principle perfectly by sweetness do
 as mr started arrival subject by believe
 strictly numerous outlived kindness whatever on we no on addition
  the next flag is daeafbzyfdcfeafgeefeeeczxeadaefz
 it real sent your at
 amounted all shy set why followed declared
 repeated of endeavor mr position kindness offering ignorant so up
 simplicity are melancholy preference considered saw companions
 disposal on outweigh do speedily in on
 him ham although thoughts entirely drawings
 acceptance unreserved old admiration projection nay yet him
 lasted am so before on esteem vanity oh
```
Damn it... Integers. I'll just throw it into a decoder then ``DA738421F6587A89EE87EE5207A6A7F2``

## data-exfiltration7.pcap

This was a weird one. Got told that it is a Trithemius Cipher???
```bash
└─$ tshark -r data-exfiltration7.pcap -Y http -T fields -e http.request.uri.query | grep -v -e "^$" | grep -v wsdl |  sed 's/message=//g' | sed 's/+/ /g'
Aof vmw jhzn ftqj pjj fnxl hwk
Aof vmw jhzn ftqj pjj fnxl hwk
 Sp cw anzoqw wc fb gxcgdx unorpd
 Sp cw anzoqw wc fb gxcgdx unorpd
 Ms flwuuzqwq naahxdlww co kcddnekqk fxyiwqtzt wc mv
 Ms flwuuzqwq naahxdlww co kcddnekqk fxyiwqtzt wc mv
 Eyvuiroag jc tr oftqbxtmo wdpdengqx
 Eyvuiroag jc tr oftqbxtmo wdpdengqx
 Ogh qsb spacbpef dgemawyy krr gostlfqk vxrxtaag
 Ogh qsb spacbpef dgemawyy krr gostlfqk vxrxtaag
 Psgyenrll vb eaysgqsdr xdozmtrtg dwxayiwmp qfhxcrtey vlmjzuegg xt yv
 Psgyenrll vb eaysgqsdr xdozmtrtg dwxayiwmp qfhxcrtey vlmjzuegg xt yv
 Hjo hzjxfbqsys zsaqeuaigu rlbonorrqe icc czxvqxjlvx cidxzhtjpj twuqmldtaa cuv
 Hjo hzjxfbqsys zsaqeuaigu rlbonorrqe icc czxvqxjlvx cidxzhtjpj twuqmldtaa cuv
 Cppqihzpww ceuziaqkww ynpfkztjpj iciltuoyor oc jf afjmapqhoo
 Cppqihzpww ceuziaqkww ynpfkztjpj iciltuoyor oc jf afjmapqhoo
  Tig qicz mtjq te P0TRVVS5UVA6587B6587C6587B786944C786944
  Tig qicz mtjq te P0TRVVS5UVA6587B6587C6587B786944C786944
```
Using [this](https://md5decrypt.net/en/Tritheme-cipher/#results)
``the next flag is c0fcfea5bbf6587f6587f6587d786944d786944``