***This project is for school holidays in Germany, so the documentation is in German.***

# Ferien-Bot

Stellt einen Countdown bis zu den Schulferien in den verschiedenen Bundesländern
von Deutschland zur Verfügung.

## Ausführen

1. Das Projekt mit Git klonen oder als ZIP herunterladen.
2. Die Datei `config-template.ini` nach `config.ini` kopieren und die Kopie
   bearbeiten, so dass die Daten darin stimmen.
3. Python 3.9 oder höher und die nötigen Bibliotheken müssen installiert sein
   oder werden (z.B. mit dem Befehl `pip3 install -r requirements.txt`).
   Empfehlung: Ein [venv](https://docs.python.org/3/library/venv.html) nutzen
   und die Bibliotheken darin installieren.
4. Entweder `bot_console.py`, `bot_mastodon.py` oder `bot_signal.py` periodisch
   ausführen, z.B. einmal täglich.

### Console

Gibt die Meldung einfach als Text aus. Praktisch zur Verwendung in Shell-Skripten.

### Mastodon

Postet die Meldung als Status in Mastodon. Der verwendete Mastodon-Account muss
mit den folgenden Einstellungen konfiguriert werden:

- `api_base_url`: die Adresse der Mastodon-Instanz
- `access_token`: das Zugriffstoken der Mastodon-"Anwendung" (s.u.)

In den Einstellungen von Mastodon gibt es den Bereich "Entwicklung" und dort den
Button "Neue Anwendung". Es muss eine Anwendung geben, die mindestens die Berechtigung
`write:statuses` besitzt - das Token davon muss dem Bot einkonfiguriert werden.

### Signal

Postet die Meldung als Signal-Nachricht in beliebig vielen Direktchats und/oder Gruppen.
Dies wird via [signal-cli](https://github.com/AsamK/signal-cli) realisiert, was vorher
separat eingerichtet werden muss (siehe 
[Installation](https://github.com/AsamK/signal-cli/wiki/DBus-service#system-bus)
und [Einrichtung](https://github.com/AsamK/signal-cli/wiki/Registration-with-captcha)).
Der Zugriff auf signal-cli erfolgt über DBus.

Benötigte Einstellungen für den Bot:

- `sender`: die Nummer, welche die Nachrichten versenden soll (muss in signal-cli konfiguriert sein)
  im Format 49123456789
- `recipients` (optional): `|`-getrennte Liste von Nummern im Format +49123456789,
  an welche die Nachrichten direkt versendet werden sollen
- `groups` (optional):  `|`-getrennte Liste von Gruppennamen, in denen `sender` Mitglied ist -
  in diesen Gruppen wird die Nachricht gepostet

## Globale Einstellungen

- `land_kuerzel`: zweibuchstabige Abkürzung des Bundeslandes, siehe 
  [hier](https://de.wikipedia.org/wiki/ISO_3166-2:DE) (hinterer Teil des Codes)
- `land_name`: Name des Bundeslandes
- `bar_width`: Breite der Fortschrittsanzeige in Zeichen
