# Hallo und willkommen zu meinem kleinen Kochbuch-Projekt. 

## Ziel der Anwendung
Das Ziel der Applikation ist es, Rezepte zu verwalten und anzuzeigen, sowie (als Kernaufgabe) einen Einkaufszettel auf Basis mehrerer Rezepte und einer Personenanzahl zu erstellen. 

*Beispiel*: 
Ich fahre mit 5 Freunden eine Woche in den Urlaub. Im Urlaub mache ich 1x Chili con carne, 1x Käse Fondue, 1x Gemüsecurry; 2x gehen wir Essen. Zusätzlich möchte ich an 4 Tagen morgens selber Brötchen backen. 

Die App kennt die Basis-Rezepte für Chili, Käse Fondue, Gemüsecurry und Brötchen (falls nicht, kann ich sie zufügen). Ich teile der App mit, dass ich für 5 Personen je 1x Chili, Käse Fondue und Gemüsecurry, sowie 3x Bröthchen benötige - die App spuckt mir einen Einkaufszettel (mit aggregierten Zutaten) aus. 

## Technische Details: 
- Datenbank: SQLite3
- API: Python/Flask
- Frontend: Angular

*Installation:* 
- git clone https://github.com/sir-toby/Kochbuch
- Python installieren (mind. 3.10; TBD)
- node.js und Angular installieren (siehe auch hier: https://angular.io/guide/setup-local)
- im Frontend-Ordner `npm i` ausführen um Abhängigkeiten zu installieren
- `python Backend/infrastructure/db_setup.py` ausführen, um die Datenbank zu erstellen
- (bei Bedarf: `python Backend/infrastructure/createTestData.py` ausführen um die Datenbank mit Testdaten zu füttern)

*Lokale Ausführung:*
- im Ordner "Backend" `flask run` ausführen --> die API sollte danach über localhost:5000 erreichbar sein (siehe auch Terminal)
- im ORdner "Frontend" `ng serve` ausführen --> das Frontend sollte über localhost:4200 erreichbar sein (siehe auch Terminal)

*Viel Spaß!*