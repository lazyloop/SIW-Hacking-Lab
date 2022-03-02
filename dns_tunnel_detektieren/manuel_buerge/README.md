Starte Wireshark und nutze den Browser um auf einige Seiten zuzugreifen. Nun sollten diverse DNS-Requests und Responses generiert werden.

### Beantworte nun die folgenden Fragen:

    Welche Protokolle im OSI-Stack werden für eine DNS-Abfrage verwendet?
    Mit welchem Display-Filter kannst du DNS-Requests und Responses filtern?
    Wo kannst du alle DNS-Display-Filter anzeigen?
    Es gibt mehrere Resource Records. Welche gibt es und welche findest du im Traffic?
    Welcher DNS-Server wird verwendet?

1. DNS?
2. ``dns``
3. Best option is to use the data panel and use the ``apply filter`` function for specific data that you want to filter out
4. ...
5. My Router


### Weitere Fragen

Beantworte die folgenden Fragen:

Tipp: UDP Port 5353 ist nicht der Standard-DNS-Ports. Mit einem Rechtsklick auf ein Paket können wir jedoch Decodieren selber bestimmen. Mach das und decodiere die Pakete auf UDP Port 5353 mit DNS. Klicke dazu auf "Decode As..."

Tipp: Zum decodieren kannst du z.B. CyberChef nehmen: https://gchq.github.io/CyberChef . Dieses Tool unterstützt sehr viele Codes.

    Wie sehen die DNS-Anfragen und die Responses auf dem Netz aus?
    Welche DNS-Records werden verwendet?
    Wie werden die Daten encodiert?
    Gibt es alternativen zur gewählten Encodierung?
    Wie kannst du die Daten wieder decodieren wenn du nur Zugriff auf das Netz hast?
    Neben dem Klartext werden auch andere, binäre Daten gesendet welche nicht von der Benutzerinteraktion stammt. Wozu könnten diese Dienen?
    Wie kann man diesen Angriff detektieren?
    Wie kann man den Angriff verhindern?
    Welche Techniken im Mittre&Attck-Framework nutzen wir hier?
    Zu Testzwecken haben wir alles auf dem lokalen Interface gemacht. Welche Infrastruktur benötigst du für diesen Angriff in der Praxis?

1. ``<encoded data>.<domain>`` or ``<tag>.<encoded data>``
2. MX Records
3. Hex
4. https://github.com/iagox86/dnscat2/blob/master/doc/protocol.md#datatypes (can be encrypted as well)
5. Cyberchef oder ``echo HEXDATA | xxd -r -p``
6. Public Key encryption
7. Long and/or excessive DNS requests
8. Blacklist comparison, IDS, Next Gen solutions
9. T1071.004
10. Public IP and compomised host

