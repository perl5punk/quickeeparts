# quickeeparts

> Turn your shop's surplus parts into profitable listings — automatically.

---

## Description

Small automotive and industrial shops are constantly sitting on untracked surplus inventory: leftover parts scattered in corners, bins, and shelves. They know those parts have value, but the hassle of photographing each piece, researching what it's worth, and listing it across marketplaces is a drag nobody has time for.

**quickeeparts** solves that pain. It's a utility that lets you **take a photo of a surplus part**, have an AI model automatically identify it, **assess its demand and estimated resale value**, queue the listing for approval, and — once approved — **push it live on eBay and other marketplaces** with a single workflow.

Think of it as the ultimate spare-parts utility: scan, identify, value, approve, and sell.

---

## Features

- **Photo-based part identification** — Upload a picture of any part; an AI/vision model identifies the part and extracts key attributes (make, model, compatibility).
- **Demand and value assessment** — The system analyses market data to estimate demand and suggests a competitive listing price.
- **Approval queue workflow** — Parts don't go live automatically. Every identified part enters an approval queue so a human can review, adjust, and confirm before anything is published.
- **Multi-platform listing** — Once approved, listings are created on eBay and are extensible to other marketplaces (Mercari, Facebook Marketplace, etc.).
- **Dashboard interface** — A web-based dashboard for managing parts, reviewing approvals, tracking listing performance, and seeing your surplus inventory at a glance.

---

## Install / Setup

### Prerequisites

- **Python 3.10** or later
- **Redis** — used as the message broker for Celery background tasks
- **PostgreSQL** (or another supported relational database) — for persistence

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/quickeeparts.git
cd quickeeparts
```

### 2. Create a virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

Required configuration includes:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (e.g. `postgres://user:pass@localhost:5432/quickeeparts`) |
| `REDIS_URL` | Redis connection string (default `redis://localhost:6379/0`) |
| `VISION_API_KEY` | API key for your AI vision / image-recognition service (e.g. Google Vision, AWS Rekognition) |
| `EBAY_CLIENT_ID` | eBay API client ID |
| `EBAY_CLIENT_SECRET` | eBay API client secret |
| `EBAY_RUNTIME_ID` | eBay application runtime ID |
| `SECRET_KEY` | Django/Flask secret key for session signing |

### 5. Database setup

```bash
# Create the database (if using PostgreSQL)
createdb quickeeparts

# Apply migrations
python manage.py migrate
```

### 6. Start the application

```bash
# Start the web server
python manage.py runserver

# Start the Celery worker (in a separate terminal)
celery -A quickeeparts worker --loglevel=info

# Start Redis in the background
redis-server
```

---

## Usage

### Upload a part photo

Use the CLI to take or upload a photo of a surplus part. The system will identify it and queue it for review.

```bash
# Upload a photo and start identification
quickeeparts upload --photo /path/to/engine_part.jpg

# Or from the web dashboard, click "Add Part" and upload directly
```

### Review and approve parts

Browse the approval queue and either approve or reject identified parts.

```bash
# List parts awaiting approval
quickeeparts approve --list

# Approve a specific part by ID and publish to eBay
quickeeparts approve --part-id 42 --publish

# View all listing performance
quickeeparts listings --status all
```

### Example: end-to-end workflow

```bash
# 1. Photograph a surplus alternator
quickeeparts upload --photo alternator_2019_f150.jpg

# 2. The system identifies it, assesses demand, and queues it
#    → Part identified: Bosch Alternator — 2019 Ford F-150
#    → Estimated value: $85–$120
#    → Status: pending_approval

# 3. Review and approve
quickeeparts approve --part-id 107 --publish

# 4. Listing goes live on eBay (and configured marketplaces)
#    → Listing ID: EB-98372615
#    → Status: active
```

### Dashboard

Visit `http://localhost:8000` (or whatever port you configured) to use the web interface. The dashboard shows:

- Current surplus inventory with photo thumbnails
- Parts waiting for approval
- Active listings across marketplaces
- Sales and value analytics

---

## Project Structure

```
quickeeparts/
│
├── src/                      # Main application source code
│   ├── __init__.py
│   ├── core/                 # Core business logic
│   │   ├── identification/   # AI-based part identification
│   │   ├── valuation/        # Demand and price estimation
│   │   └── approval/         # Approval queue workflow
│   ├── marketplaces/         # Marketplace integrations
│   │   ├── ebay/             # eBay API client
│   │   └── mercari/          # Mercari integration (extensible)
│   ├── api/                  # REST API endpoints
│   └── dashboard/            # Web dashboard (templates & views)
│
├── tests/                    # Unit and integration tests
│   ├── test_identification/
│   ├── test_valuation/
│   └── test_marketplaces/
│
├── config/                   # Configuration files
│   ├── settings.py           # Application settings
│   └── urls.py               # URL routing
│
├── migrations/               # Database migrations
├── media/                    # Uploaded part photos
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables
└── README.md                 # This file
```

> **Note:** This layout is the intended architecture. As development progresses, directories and modules may evolve accordingly.

---

## Contributing

Contributions are welcome! Whether you want to improve the part identification model, add a new marketplace integration, or polish the dashboard UI — every contribution makes the tool better for shops everywhere.

### How to contribute

1. **Fork** the repository on GitHub.
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes** — write code, add tests, and update documentation as needed.
4. **Run the tests** to make sure everything still works:
   ```bash
   pytest
   ```
5. **Commit** your changes with a clear message:
   ```bash
   git commit -m "Add Mercari marketplace integration"
   ```
6. **Push** to your fork and **open a pull request** against the `main` branch.

### Coding standards

- Follow **PEP 8** for Python code style.
- Write **docstrings** for functions and classes.
- Include **tests** for new features and bug fixes.
- Keep pull requests focused — one feature or fix per PR.

### Need help?

Open an issue on GitHub or reach out to the maintainers if you have questions about the architecture or how best to approach a contribution.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
