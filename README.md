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

2. Erstellen Sie eine virtuelle Umgebung im Backend-Verzeichnis und aktivieren Sie diese:
   ```
   python -m venv venv
   source venv/bin/activate  # Für Windows: venv\Scripts\activate
   ```

3. Installieren Sie die erforderlichen Pakete im Backend-Verzeichnis:
   ```
   pip install -r requirements.txt
   ```

4. Erstellen Sie eine `.env`-Datei im Projektroot und fügen Sie folgende Umgebungsvariablen hinzu:
   ```
   LANGCHAIN_API_KEY=your_langsmith_api_key
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_ENDPOINT=https://eu.api.smith.langchain.com
   MYSQL_CONNECTION_STRING=your_mysql_connection_string
   LANGCHAIN_PROJECT=kete_langSmith
   MYSQL_HOST=mysql-kete-kete-database.c.aivencloud.com
   MYSQL_USER=your_user
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=your_database_name
   MYSQL_PORT=your_port
   MYSQL_SSL_CA=/location/of/ca.pem
   ```
5. Installieren Sie die erforderlichen Packete im Frontend-Verzeichnis
   ```
   npm install
   ```

## Verwendung

1. Stellen Sie sicher, dass Ihre virtuelle Umgebung aktiviert ist.

2. Führen Sie die Hauptskripte aus:
   
   Starten der Frontend App
   ```
   cd frontend/frontend/
   npm run dev
   ```
   Starten der Backend App
   ```
   cd backend/
   python backend/main.py
   ```

## Projektstruktur

```
project_root/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── main.py
│   ├── multi_agent_system.py
│   ├── rag_agent.py
│   └── venv/
│       ├── bin/
│       ├── include/
│       ├── lib/
│       └── pyvenv.cfg
│
├── frontend/
│   ├── frontend/
│   │   ├── .gitignore
│   │   ├── index.html
│   │   ├── jsconfig.json
│   │   ├── package.json
│   │   ├── public/
│   │   ├── README.md
│   │   ├── src/
│   │   └── vite.config.js
│
├── .env
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── package.json
```

- `backend/`: Enthält den Backend-Code und die virtuelle Umgebung.
  - `main.py`: Hauptskript zum Ausführen des Agenten.
  - `multi_agent_system.py`: Implementiert das Multi-Agenten-System.
  - `rag_agent.py`: Implementiert den RAG-Agenten mit LangChain.
  - `app.py`: Startet die Backend-Anwendung.

- `frontend/`: Enthält den Frontend-Code.
  - `src/`: Enthält den Quellcode für das Frontend.
  - `public/`: Enthält öffentliche Assets.
  - `index.html`: Haupt-HTML-Datei.
  - `package.json`: Enthält die Abhängigkeiten und Skripte für das Frontend.
  - `vite.config.js`: Konfigurationsdatei für Vite.

## Technologien
- Python: Programmiersprache für das Backend.
- LangChain: Framework für die Verarbeitung natürlicher Sprache.
- LangSmith: API für die Verarbeitung natürlicher Sprache.
- MySQL: Relationale Datenbank.
- Preact: JavaScript-Bibliothek für das Frontend.
- Vite: Build-Tool für das Frontend.

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
