# Marvis

Marvis is a personal AI assistant that acts on your behalf — so you can delegate tasks just by sending a message.

## What is Marvis?

Instead of switching between apps and manually performing tasks, you simply chat with Marvis through your preferred messaging platform and it handles everything for you.

## How it works

Send a message on any supported platform → Marvis understands your intent → Marvis takes action on your behalf.

## Supported Messaging Platforms

- WhatsApp
- Telegram
- Slack
- Facebook Messenger

## Integrations

### Google
| Integration | Capabilities |
|---|---|
| Google Calendar | Create, update, and delete events; check schedule |
| Google Drive | Upload, download, organize, and share files |
| Google Photos | Browse, search, and manage your photo library |
| Gmail | Read, compose, send, and organize emails |

### Social Media
| Integration | Capabilities |
|---|---|
| Twitter / X | Post tweets, reply, browse timeline |
| Facebook | Post updates, read feed |
| Instagram | Post photos/stories, browse feed, reply to DMs |

### Productivity & Communication
| Integration | Capabilities |
|---|---|
| Slack | Send messages, manage channels, set reminders |
| WhatsApp | Two-way communication interface |
| Telegram | Two-way communication interface |
| Facebook Messenger | Two-way communication interface |

### System
| Integration | Capabilities |
|---|---|
| PC / Local System | File management, app control, system tasks |

> More integrations coming soon.

## Architecture & Design

The user flow, system architecture, and database schema diagrams are available here:

**[View Diagrams →](https://app.diagrams.net/#G1T_mHKvWyPq3rXAd0ExpZkTVwEt9vhrED#%7B%22pageId%22%3A%22QfA07C8Jof4Y4qBS3fAS%22%7D)**

> Includes: User Flow · System Architecture · Database Schema

---

## Project Structure

```
Marvis/
├── marvis-server/   # FastAPI backend
└── marvis-client/   # React frontend
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+
- Docker & Docker Compose (for containerised setup)

---

## Running Without Docker

### Backend

```bash
cd marvis-server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

Server runs at **http://localhost:8000**
API docs available at **http://localhost:8000/docs**

---

### Frontend

```bash
cd marvis-client

# Install dependencies
npm install

# Copy and fill in environment variables
cp .env.example .env

# Start the dev server
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## Running With Docker

Make sure Docker Desktop is running, then from the root of the project:

```bash
# Copy backend environment file and fill in your values
cp marvis-server/.env.example marvis-server/.env

# Build and start all services (db, server, client)
docker compose up --build
```

| Service  | URL                        |
|----------|----------------------------|
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:4173      |
| Database | localhost:5432             |

### Useful Docker commands

```bash
# Run in background
docker compose up --build -d

# Stop all services
docker compose down

# Stop and delete the database volume
docker compose down -v

# View logs
docker compose logs -f server
```

### Run migrations inside Docker

```bash
docker compose exec server alembic upgrade head
```

---

## Linting

### Backend

```bash
cd marvis-server
ruff check .          # lint
ruff check . --fix    # lint and auto-fix
ruff format .         # format
```

### Frontend

```bash
cd marvis-client
npm run lint
```

### Pre-commit (runs automatically on every commit)

```bash
# Install hooks (first time only)
cd marvis-server && venv/bin/pre-commit install

# Run manually against all files
venv/bin/pre-commit run --all-files
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.
