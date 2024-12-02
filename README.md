# RAG Agent mit MySQL-Integration

Dieses Projekt implementiert einen Retrieval-Augmented Generation (RAG) Agenten, der Daten aus einer MySQL-Datenbank in den Abfrageprozess einbindet. Es nutzt LangChain und LangSmith (EU) für die Verarbeitung.

## Voraussetzungen

- Python 3.8+
- Git
- Visual Studio Code (empfohlen)
- MySQL-Datenbank

## Installation

1. Klonen Sie das Repository:
   ```
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:
   ```
   python -m venv venv
   source venv/bin/activate  # Für Windows: venv\Scripts\activate
   ```

3. Installieren Sie die erforderlichen Pakete:
   ```
   pip install -r requirements.txt
   ```

4. Erstellen Sie eine `.env`-Datei im Projektroot und fügen Sie folgende Umgebungsvariablen hinzu:
   ```
   LANGCHAIN_API_KEY=your_langsmith_api_key
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_ENDPOINT=https://api.eu.langchain.com
   MYSQL_CONNECTION_STRING=your_mysql_connection_string
   ```

## Verwendung

1. Stellen Sie sicher, dass Ihre virtuelle Umgebung aktiviert ist.

2. Führen Sie das Hauptskript aus:
   ```
   python src/main.py
   ```

## Projektstruktur

```
project_root/
│
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── rag_agent.py
│   └── main.py
│
├── .env
├── .gitignore
└── requirements.txt
```

- `database.py`: Enthält Funktionen für die Datenbankverbindung und -abfragen.
- `rag_agent.py`: Implementiert den RAG-Agenten mit LangChain.
- `main.py`: Hauptskript zum Ausführen des Agenten.

## Neueste Änderungen

### Implementierung des RAG-Agents mit MySQL-Integration
Pull Request: [#1](https://github.com/Fa-commits/kete/pull/1)

#### Änderungen:
- Hinzufügen der Datei `.DS_Store`.
- Modifikation der `.gitignore`:
  - Hinzufügen von `.pyc` zur Ignorierliste.
- Aktualisierung der `requirements.txt`:
  - Hinzufügen der folgenden Abhängigkeiten:
    - `langchain`
    - `langchain-openai`
    - `langchain-community`
    - `langchain-experimental`
    - `langgraph`
    - `langsmith`
    - `openai`
    - `mysql-connector-python`
    - `python-dotenv`
    - `pymysql`
    - `sqlalchemy`

Für weitere Details siehe den [Pull Request](https://github.com/Fa-commits/kete/pull/1).

## Entwicklung

1. Erstellen Sie einen neuen Branch für Ihre Änderungen:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Machen Sie Ihre Änderungen und committen Sie sie:
   ```
   git add .
   git commit -m "Beschreibung Ihrer Änderungen"
   ```

3. Pushen Sie den Branch zu GitHub:
   ```
   git push origin feature/your-feature-name
   ```

4. Erstellen Sie einen Pull Request auf GitHub.

## Beitrag

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request für alle Änderungen.

## Lizenz

[MIT License](https://opensource.org/licenses/MIT)
