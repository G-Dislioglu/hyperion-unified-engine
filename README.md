# Hyperion Unified Engine

Ein einheitliches Framework für Datenanalyse, API-Integration und Dashboard-Visualisierung.

## Installation

Das Projekt kann einfach mit pip installiert werden:

```bash
# Repository klonen
git clone https://github.com/G-Dislioglu/hyperion-unified-engine.git
cd hyperion-unified-engine

# Editierbare Installation (für Entwicklung)
pip install -e .
```

## Konfiguration

Das System verwendet SQLite für die Datenspeicherung und API-Key-Validierung. Die Datenbank wird automatisch erstellt, wenn die Anwendung zum ersten Mal gestartet wird.

### API-Keys hinzufügen

Um API-Keys zur Authentifizierung hinzuzufügen, können Sie das folgende Python-Skript verwenden:

```python
from storage.db import conn, init_db

# Datenbank initialisieren
init_db()

# API-Key hinzufügen
api_key = "ihr-geheimer-api-key"
conn().execute("INSERT INTO users(api_key) VALUES (?)", (api_key,))
```

## Verwendung

### Dashboard starten

Das Dashboard kann direkt aus dem Projektverzeichnis gestartet werden:

```bash
streamlit run dashboard/app.py
```

Das Dashboard bietet folgende Funktionen:
- Login mit API-Key in der Sidebar
- Übersicht aller gespeicherten Tasks
- Visualisierung der Tasks pro Modul
- Formular zum Erstellen neuer Tasks

### Optimizer verwenden

Der Optimizer kann in eigenen Skripten verwendet werden:

```python
from hue.core import Optimizer

# Optimizer initialisieren
optimizer = Optimizer()

# Task speichern
optimizer.optimize(
    module="binance", 
    payload="{'symbol': 'BTCUSDT'}", 
    result="{'price': 50000}"
)
```

### API-Clients

Das Projekt enthält vorgefertigte API-Clients für:
- Binance
- CoinGecko
- Whale Alert
- OpenAI

Beispiel für die Verwendung des Binance-Clients:

```python
from apis.binance import BinanceClient

# Client initialisieren
client = BinanceClient()

# Preis abfragen
price = client.get_ticker_price("BTCUSDT")
print(price)
```

## Projektstruktur

```
hyperion-unified-engine/
├── adapters/            # Adapter-Module
│   └── __init__.py
├── apis/                # API-Client-Module
│   ├── __init__.py
│   ├── binance.py       # Binance API-Client
│   ├── coingecko.py     # CoinGecko API-Client
│   ├── openai.py        # OpenAI API-Client
│   └── whale_alert.py   # Whale Alert API-Client
├── dashboard/           # Streamlit-Dashboard
│   ├── __init__.py
│   └── app.py           # Hauptanwendung
├── hue/                 # Hyperion Unified Engine Core
│   ├── __init__.py
│   └── core.py          # Optimizer und Logging
├── storage/             # Datenspeicherung
│   ├── __init__.py
│   └── db.py            # Datenbankfunktionen und API-Key-Validierung
├── requirements.txt     # Abhängigkeiten
└── setup.py             # Installationskonfiguration
```

## Logging

Das System protokolliert alle Aktivitäten in der Datei `hyperion.log`. Die Logs enthalten Informationen über gestartete Sitzungen und gespeicherte Tasks.
