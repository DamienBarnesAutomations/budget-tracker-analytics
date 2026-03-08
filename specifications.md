# specifications.md
## Render Deployment — Change Specification

---

## 1. Your Mission

You are an AI coding assistant. Your task is to read this entire project and make the specific, targeted changes described in this document so that the project deploys correctly on Render.com.

**Do not rewrite anything that is not listed here.** The application logic, Vue components, FastAPI endpoints, Pandas transformations, and Telegram bot are all correct and must not be changed.

---

## 2. Read These Files First

Before making any changes, read every file listed below in full. Follow all imports.

```
app.py
Dockerfile                     ← root (bot)
docker-compose.yml
requirements.txt
backend/main.py
backend/Dockerfile
backend/requirements.txt
frontend/Dockerfile
frontend/src/api.js
frontend/vite.config.js        ← read if it exists
handlers/file_handler.py
handlers/telegram_handler.py
services/google_sheet_services.py
services/dashboard_service.py
transformations/data_transformations.py
processors/file_processor.py
```

---

## 3. Background: How Render Works

Render does **not** use `docker-compose.yml`. It deploys each service independently from the same repository, using a different Dockerfile per service. The three services in this project map to three separate Render service types:

| Service | Render Type | Dockerfile |
|---|---|---|
| Telegram Bot | **Background Worker** | `./Dockerfile` (root) |
| FastAPI Backend | **Web Service** | `./backend/Dockerfile` |
| Vue Frontend | **Web Service** | `./frontend/Dockerfile` |

Each service is connected to the same GitHub repo. Render builds only the Dockerfile you specify per service.

Render injects a `$PORT` environment variable into Web Services at runtime. Your services must bind to this port, not a hardcoded one.

---

## 4. Required Changes

### 4.1 — Root `Dockerfile` (Bot)

**File:** `Dockerfile`

**Problem:** Verify the CMD runs `python app.py` and nothing else. The bot must not attempt to start a web server or bind any port. It is a background worker.

**Required state:**
```dockerfile
CMD ["python", "app.py"]
```

No `EXPOSE` directive is needed. Remove it if present.

---

### 4.2 — `backend/Dockerfile` (FastAPI)

**File:** `backend/Dockerfile`

**Problem:** The CMD likely hardcodes port `8000`. Render injects `$PORT` at runtime, so the app must bind to whatever port Render assigns.

**Change the CMD from:**
```dockerfile
CMD ["python", "backend/main.py"]
```
or any hardcoded uvicorn command, **to:**
```dockerfile
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

Also verify that `uvicorn` is present in `backend/requirements.txt`. If it is not, add it:
```
uvicorn[standard]
```

Also verify the `EXPOSE` line — change it to:
```dockerfile
EXPOSE 8000
```
(This is documentation only; Render uses `$PORT` regardless.)

---

### 4.3 — `backend/main.py` (FastAPI CORS)

**File:** `backend/main.py`

**Problem:** CORS is almost certainly configured for `localhost:3000`. On Render, the frontend will be served from a different domain (e.g. `https://budget-tracker-frontend.onrender.com`). Hardcoded localhost origins will block all API calls in production.

**Change the CORS configuration to allow all origins temporarily**, so the deployment can be verified. This is safe because the app has no authentication layer by design (per the README).

Find the CORS middleware configuration and change it to:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Note: `allow_credentials` must be `False` when `allow_origins=["*"]`. If the existing code has `allow_credentials=True` with a wildcard origin, it will throw an error — fix this.

---

### 4.4 — `frontend/src/api.js` (API Base URL)

**File:** `frontend/src/api.js`

**Problem:** The base URL for the Axios instance is almost certainly hardcoded to `http://localhost:8000`. This will not work in production.

**Change it to use a Vite environment variable:**
```javascript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

export default apiClient
```

This means in production, the Vue build will use `VITE_API_BASE_URL` (set at build time in Render), and locally it will fall back to `localhost:8000`.

---

### 4.5 — `frontend/Dockerfile` (Build Arg)

**File:** `frontend/Dockerfile`

**Problem:** The frontend Dockerfile does not pass `VITE_API_BASE_URL` through as a build argument. Because Vite bakes env vars into the bundle at build time, the variable must be declared as an `ARG` and set as an `ENV` before `npm run build` is called.

**Find the build stage and add the ARG/ENV before the build step:**
```dockerfile
# Build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .

# Accept the API URL at build time
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

### 4.6 — `frontend/Dockerfile` (Nginx Port Binding)

**File:** `frontend/Dockerfile`

**Problem:** Render Web Services expect the app to bind to `$PORT`, but Nginx is configured to listen on port 80 by default. Render will timeout waiting for the service to open the correct port.

**Add a custom Nginx config that reads `$PORT`.**

After the `COPY --from=build-stage` line in the production stage, add:

```dockerfile
# Copy custom nginx config that binds to $PORT
COPY frontend/nginx.conf /etc/nginx/templates/default.conf.template
ENV PORT=80
CMD ["/bin/sh", "-c", "envsubst '$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
```

Then create the file `frontend/nginx.conf` with this content:
```nginx
server {
    listen ${PORT};
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

This is required for Vue Router to work correctly (SPA fallback to `index.html`) and for Render's port detection to succeed.

---

### 4.7 — `services/google_sheet_services.py` (Service Account Credentials)

**File:** `services/google_sheet_services.py`

**Problem:** The service account credentials are almost certainly loaded from a local `service_account.json` file path. On Render there is no filesystem to place this file — credentials must be injected as an environment variable.

**Read the current implementation carefully.** It will look something like:
```python
gc = gspread.service_account(filename='service_account.json')
```

**Change it to support both methods** — file (for local dev) and environment variable (for Render):

```python
import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

def get_gspread_client():
    creds_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
    if creds_json:
        # Production: credentials injected as environment variable
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        # Local development: credentials loaded from file
        creds = Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    return gspread.authorize(creds)
```

Replace all existing `gspread` client instantiation in the file with calls to `get_gspread_client()`.

This change applies to **both** `services/google_sheet_services.py` AND anywhere else in the project that directly instantiates a gspread or Google Auth client. Check `backend/main.py` and `services/dashboard_service.py` as well.

---

## 5. New File to Create

### `render.yaml` (Optional but recommended)

Create this file in the project root. It allows Render to auto-configure all three services from a single file ("Infrastructure as Code"), which is cleaner than clicking through the dashboard manually.

```yaml
services:
  - type: worker
    name: budget-tracker-bot
    runtime: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: TELEGRAM_TOKEN
        sync: false
      - key: GOOGLE_SHEET_ID
        sync: false
      - key: GOOGLE_SERVICE_ACCOUNT_JSON
        sync: false

  - type: web
    name: budget-tracker-api
    runtime: docker
    dockerfilePath: ./backend/Dockerfile
    envVars:
      - key: GOOGLE_SHEET_ID
        sync: false
      - key: GOOGLE_SERVICE_ACCOUNT_JSON
        sync: false

  - type: web
    name: budget-tracker-frontend
    runtime: docker
    dockerfilePath: ./frontend/Dockerfile
    dockerContext: .
    envVars:
      - key: VITE_API_BASE_URL
        sync: false
```

`sync: false` means Render will prompt for these values in the dashboard rather than storing them in the repo. This is correct for secrets.

---

## 6. Environment Variables Reference

This is the complete list of environment variables that must be set on each Render service. **Do not hardcode any of these values in the codebase.**

### Bot (Background Worker)
| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Bot token from BotFather |
| `GOOGLE_SHEET_ID` | The spreadsheet ID from the Google Sheets URL |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | The full contents of `service_account.json`, pasted as a single-line JSON string |

### API (Web Service)
| Variable | Description |
|---|---|
| `GOOGLE_SHEET_ID` | Same spreadsheet ID as above |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Same service account JSON as above |

### Frontend (Web Service)
| Variable | Description |
|---|---|
| `VITE_API_BASE_URL` | The full public URL of the API service, e.g. `https://budget-tracker-api.onrender.com` |

---

## 7. How to Get `GOOGLE_SERVICE_ACCOUNT_JSON` for Render

The `service_account.json` file cannot be uploaded to Render directly. Instead:

1. Open your `service_account.json` file in a text editor
2. Minify it to a single line (remove all newlines). You can use: `cat service_account.json | python3 -m json.tool --compact`
3. Copy the entire single-line JSON string
4. Paste it as the value of the `GOOGLE_SERVICE_ACCOUNT_JSON` environment variable in the Render dashboard for both the Bot and API services

---

## 8. What NOT to Change

Do not modify any of the following:
- `transformations/data_transformations.py`
- `processors/file_processor.py`
- `handlers/file_handler.py`
- `handlers/telegram_handler.py`
- Any Vue component files under `frontend/src/components/`
- `App.vue`
- `docker-compose.yml` — this is used for local development and should remain as-is
- `dashboard.py` — legacy Streamlit file, leave untouched

---

## 9. Verification Checklist

After making all changes, verify the following before committing:

- [ ] `backend/Dockerfile` CMD uses `${PORT:-8000}` and not a hardcoded port
- [ ] `backend/main.py` CORS allows `"*"` with `allow_credentials=False`
- [ ] `frontend/src/api.js` uses `import.meta.env.VITE_API_BASE_URL`
- [ ] `frontend/Dockerfile` declares `ARG VITE_API_BASE_URL` before `RUN npm run build`
- [ ] `frontend/nginx.conf` exists and uses `${PORT}` in the `listen` directive
- [ ] `frontend/Dockerfile` uses `envsubst` to render the nginx config at runtime
- [ ] `services/google_sheet_services.py` supports `GOOGLE_SERVICE_ACCOUNT_JSON` env var
- [ ] `render.yaml` exists in the project root
- [ ] Root `Dockerfile` has no `EXPOSE` and CMD is only `python app.py`