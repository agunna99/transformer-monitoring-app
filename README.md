# GoKoye Keke 🛺

> Campus keke ride-hailing app for Godfrey Okoye University, Enugu, Nigeria.
> Built with FastAPI · PostgreSQL · WebSockets · Celery · React Native

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile App (Expo)                    │
│  Student App          │          Driver App             │
│  - Book rides         │          - Go online            │
│  - Live tracking      │          - Accept rides         │
│  - Ride history       │          - Stream GPS           │
└───────────┬───────────┴──────────────┬──────────────────┘
            │ HTTP + WebSocket         │ HTTP + WebSocket
┌───────────▼──────────────────────────▼──────────────────┐
│                  FastAPI Backend                         │
│  /auth  /rides  /drivers  /zones  /admin  /ws           │
└───────┬───────────────┬────────────────┬────────────────┘
        │               │                │
   PostgreSQL        Redis           Celery Worker
   (all data)    (broker/cache)   (background jobs)
                                   - notify drivers
                                   - auto-cancel rides
                                   - rating updates
```

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | FastAPI (Python 3.12)               |
| Database     | PostgreSQL 16 (async SQLAlchemy)    |
| Migrations   | Alembic                             |
| Auth         | JWT (access + refresh tokens)       |
| Real-time    | WebSockets (live GPS tracking)      |
| Background   | Celery + Redis                      |
| Matching     | Haversine formula (pure Python)     |
| Notifications| Firebase Cloud Messaging            |
| Mobile       | React Native (Expo)                 |

---

## Running the project (complete guide)

### Step 1 — Start all backend services

```bash
# Clone the project and enter the folder
cd gokoye-keke

# Copy environment file
cp .env.example .env

# Start everything with Docker (API + PostgreSQL + Redis + Celery)
make docker-up
```

### Step 2 — Set up the database

```bash
# In a second terminal (while Docker is running):
make migrate    # creates all tables
make seed       # loads campus zones, fares, and admin account
```

### Step 3 — Verify the backend

Open your browser:
- **API docs:** `http://localhost:8000/docs`
- **Health check:** `http://localhost:8000/health`

Admin credentials (created by seed):
- Email: `admin@gokoye.app`
- Password: `Admin1234!`

### Step 4 — Run the mobile app

```bash
cd mobile
npm install

# Edit src/api/client.ts — set API_BASE_URL to your machine's local IP
# e.g. http://192.168.1.100:8000/api/v1

npx expo start
```

Install **Expo Go** on your phone → scan the QR code.

---

## API endpoints

### Auth
| Method | Endpoint | Who |
|--------|----------|-----|
| POST | `/api/v1/auth/register/student` | Register with school email |
| POST | `/api/v1/auth/register/driver` | Register as driver |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh access token |

### Rides
| Method | Endpoint | Who |
|--------|----------|-----|
| POST | `/api/v1/rides/request` | Student books a ride |
| POST | `/api/v1/rides/{id}/accept` | Driver accepts |
| POST | `/api/v1/rides/{id}/start` | Driver starts trip |
| POST | `/api/v1/rides/{id}/complete` | Driver completes |
| POST | `/api/v1/rides/{id}/cancel` | Student or driver cancels |
| POST | `/api/v1/rides/{id}/rate` | Student rates driver |
| GET  | `/api/v1/rides/my-rides` | Student's ride history |

### Drivers
| Method | Endpoint | Who |
|--------|----------|-----|
| GET  | `/api/v1/drivers/nearby?lat=&lng=` | Student sees nearby keke |
| PATCH| `/api/v1/drivers/location` | Driver updates GPS position |
| GET  | `/api/v1/drivers/me` | Driver's own profile |

### Zones & Fares
| Method | Endpoint | Who |
|--------|----------|-----|
| GET  | `/api/v1/zones/` | List all campus zones |
| POST | `/api/v1/zones/fare-estimate` | Get fare between two zones |

### Admin
| Method | Endpoint | Who |
|--------|----------|-----|
| GET  | `/api/v1/admin/dashboard` | Platform stats |
| GET  | `/api/v1/admin/drivers/pending` | Drivers awaiting approval |
| PATCH| `/api/v1/admin/drivers/{id}/status` | Approve / ban driver |
| GET  | `/api/v1/admin/rides/live` | All active rides |

### WebSockets
| URL | Who | Purpose |
|-----|-----|---------|
| `ws://host/ws/driver/{ride_id}?token=` | Driver | Stream GPS to student |
| `ws://host/ws/ride/{ride_id}?token=` | Student | Receive live location + events |

---

## Phases completed

- ✅ Phase 1 — Auth, database models, ride lifecycle, WebSocket
- ✅ Phase 2 — Migrations, admin panel, campus zones & fares, push notifications
- ✅ Phase 3 — Driver matching (Haversine), Celery background jobs, auto-cancel, ride broadcasting
- ✅ Phase 4 — React Native mobile app (student + driver)

---

## Campus zones seeded

| Zone | Description |
|------|-------------|
| Main Gate | University main entrance |
| Faculty of Engineering | Engineering & Applied Sciences |
| Faculty of Management | Business & Management Sciences |
| Student Hostel | Main residential area |
| Chapel / Admin Block | Chapel and administration |
| Nike Market | Off-campus market junction |
| Ugwuomu Nike Junction | Main road junction |
| GRA / Presidential Road | Government Reserved Area |

---

Built by a Python developer for the Godfrey Okoye University community 🇳🇬
