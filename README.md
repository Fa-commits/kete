# RAG Agent mit Langchain und MySQL

Dieses Projekt implementiert einen Retrieval-Augmented Generation (RAG) Agenten unter Verwendung von Langchain und Langsmith. Der Agent ist in der Lage, Abfragen zu verarbeiten und dabei Informationen aus einer MySQL-Datenbank einzubeziehen.

## Funktionen

- Nutzung von Langchain für die Erstellung eines SQL-Agenten
- Integration mit einer MySQL-Datenbank für datengestützte Antworten
- Verwendung von Langsmith für Leistungsüberwachung und -optimierung
- Interaktive Benutzeroberfläche für Abfragen

## Voraussetzungen

- Python 3.8 oder höher
- MySQL-Datenbank
- OpenAI API-Schlüssel
- Langsmith API-Schlüssel

## Installation

1. Klonen Sie das Repository:
   ```bash
   git clone https://github.com/IhrBenutzername/IhrRepositoryName.git
   cd IhrRepositoryName
   ```

2. Erstellen Sie eine virtuelle Umgebung:
   ```bash
   python -m venv venv
   ```

3. Aktivieren Sie die virtuelle Umgebung:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Installieren Sie die erforderlichen Pakete:
   ```bash
   pip install -r requirements.txt
   ```

5. Erstellen Sie eine `.env` Datei im Hauptverzeichnis und fügen Sie folgende Umgebungsvariablen hinzu:
   ```
   OPENAI_API_KEY=Ihr_OpenAI_API_Schlüssel
   LANGCHAIN_API_KEY=Ihr_Langsmith_API_Schlüssel
   LANGCHAIN_ENDPOINT=https://api.eu.langsmith.com
   MYSQL_HOST=Ihr_MySQL_Host
   MYSQL_USER=Ihr_MySQL_Benutzer
   MYSQL_PASSWORD=Ihr_MySQL_Passwort
   MYSQL_DATABASE=Ihr_MySQL_Datenbankname
   ```

## Verwendung

1. Starten Sie das Programm:
   ```bash
   python src/main.py
   ```

2. Geben Sie Ihre Abfragen ein, wenn Sie dazu aufgefordert werden.

3. Geben Sie 'exit' ein, um das Programm zu beenden.

## Projektstruktur

```
IhrRepositoryName/
├── .env
├── .gitignore
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── database.py
│   └── main.py
└── README.md
```

## Beitrag

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder öffnen Sie ein Issue für Vorschläge und Fehlermeldungen.

## Lizenz

[MIT](https://choosealicense.com/licenses/mit/)
