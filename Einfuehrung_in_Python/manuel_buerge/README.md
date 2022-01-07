# Slowloris

> Ohne zu wissen was Slowloris ist hätte ich nach der Analyse des Scripts behauptet, dass dies ein DoS ist welcher so viele Verbindungen öffnet bis der Webserver nicht mehr antworten kann.

### Wo wird der eigentliche Programmcode gestartet?

Wenn das file nicht importiert wird sondern von der Shell aus gestartet wird, wird ```main()``` ausgeführt
![](https://i.imgur.com/ZdhAI71.png)


### Was ist der Hauptteil des Programms? & Was wird in diesem Hauptteil genau gemacht?

Der Hauptteil des Exploits besteht aus 3 `for loops`


#### Loop 1
Iterierender function call zu `init_socket` mit der Server IP als parameter

##### `init_socket(ip)`
- Socketverbindung zum Server wird eröffnet und ein HTTP GET Request mit einem random User-Agent wird gesendet. 
- Die Socketverbindung wird returned und in einer list gespeichert

```python
def init_socket(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ...
    s.connect((ip, args.port))
    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")
    ...    
    return s
```

#### Loop 2
- Loop 2 lauf ininite
- Im Loop 2 wird ein `keep-alive` header für alle offenen Verbindungen gesendet
- Falls der Header nicht gesendet werden kann, wird die Socketverbindung entfernt.

#### Loop 3
- Loop 3 lauf ininite
- Loop 3 funktioniert genau gleich wie Loop 1
- Es werden nur so viele Socketverbindungen bis es die Anzahl des angegebenen Parameters `args.sockets` erreicht hat


#### Wann terminiert das Programm?
Sobald zwischen zwischen Zeile `187` und `209` eine Exception geworfen wird oder der Interpreter ein Exit requested



#### Falls du den Server nicht erfolgreich angreifen kannst: Woran könne das liegen?

![](https://i.imgur.com/8xIFSiY.png)

Needs more brrrrr
![](https://i.imgur.com/feZT6Zy.png)
