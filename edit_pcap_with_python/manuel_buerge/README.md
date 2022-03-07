# PCAP-Datei mit Python bearbeiten
## Pyshark

In der letzten Lektion haben wir verschiedenen Wireshakr-Dumps nach Daten durchsucht.

Diese Aufgabe war zwar manuell lösbar, aber mühsam. Mittels dem Kommandozeilen-Tool haben wir die Aufgabe automatisiert. Heute wollen wir eine weitere Möglichkeit Anschauen: pyshark.

Diese Python-Bibliothek kann dazu verwendet werden PCAP-Daten einzulesen oder Live-Interfaces zu überwachen. Danach können die Pakete in Pyhton verarbeitet werden. Genau was wir brauchen.

Lese dazu zunächst die Zusammenfassung der wichtigsten Funktionen: https://github.com/KimiNewt/pyshark
Aufgabenstellung

Schreibe nun ein Programm welches:

    Die verschiedenen Dateien einlest
    Die relevanten HTTP-Parameter ausliest
    Die Parameter decodiert falls notwendig

Da die Dateien verschiedene Encodings verwenden muss Dateiname und Code natürlich übereinstimmten. Du kannst entweder alles statisch lösen oder das Programm flexibel gestalten.

Ein Vorschlag:

    Parameter: Dateiname
    Parameter: Codec

Ein Beispiel: ``python3 http_message_filter.py data-exfiltration4.pcap base32``
