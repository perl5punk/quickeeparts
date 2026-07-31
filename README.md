# quickeeparts

quickeeparts is an AI-powered parts management application that helps repair shops, warehouses, and dealerships turn unused and extra inventory into revenue. Simply photograph a part you have laying around, and the application uses artificial intelligence to identify the part, estimate its market demand and resale value, queue it for approval, and automatically create professional listings on eBay and other selling platforms — all from a single, unified workflow.

---

## Features

- **Photo capture and upload for parts** — Snap or upload photos of any part to kick off the process.
- **AI-powered part identification** — Advanced image recognition identifies the part and returns its make, model, and details.
- **Demand and value estimation** — The system estimates market demand and suggests a competitive price.
- **Approval workflow with queue management** — Items are queued for review and approval before any listings are created.
- **Multi-platform listing creation** — Once approved, quickeeparts automatically generates listings on eBay and other selling platforms.

---

## How It Works

quickeeparts streamlines the entire process of turning unused parts into sold inventory:

1. **Capture** — Take a photo of the part using your phone, camera, or upload an existing image.
2. **Identify** — The AI engine analyzes the photo and identifies the part, returning its name, manufacturer, and specifications.
3. **Estimate value** — The system researches market data to estimate demand and suggest a competitive resale price.
4. **Queue** — The identified part is placed in the approval queue, awaiting review by an authorized user.
5. **Approve** — A manager or administrator reviews the queue and approves the item for listing.
6. **List** — Upon approval, quickeeparts automatically creates a listing on eBay and any other configured selling platforms, pushing the part into the marketplace.

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Photo   │────▶│  Identify│────▶│  Estimate│────▶│   Queue  │
│ Capture  │     │    AI    │     │  Demand  │     │  Review  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                               │
                                          ┌────▼────┐     ┌──────────┐
                                          │  Approve│────▶│   List   │
                                          └─────────┘     │ Create  │
                                                          │ Platform │
                                                          └──────────┘
```

---

## Project Structure

```
quickeeparts/
├── README.md          # This file
├── .gitignore         # Git ignore rules
├── .env.example       # Example environment variables
├── requirements.txt   # Python dependencies
├── Dockerfile.built-sandbox # Docker sandbox configuration
│
├── src/
│   ├── __init__.py
│   ├── app.py         # Main application entry point
│   ├── config.py      # Configuration and environment loading
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── ebay.py    # eBay API integration
│   │   └── platforms.py # Multi-platform listing logic
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── capture.py # Photo capture and upload handling
│   │   ├── identify.py # AI part identification
│   │   ├── estimate.py # Demand and value estimation
│   │   └── queue.py    # Approval queue management
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── part.py    # Part data model
│   │   └── listing.py # Listing data model
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py # Utility functions
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_capture.py
    ├── test_estimate.py
    ├── test_identify.py
    ├── test_queue.py
    ├── test_readme_accuracy.py
    └── test_readme_criteria.py
```

---

## Prerequisites

Before installing and running quickeeparts, ensure you have the following:

- **Python 3.10 or later** — The application is built with modern Python features.
- **pip** — The Python package installer (usually bundled with Python).
- **Virtual environment** — Recommended for isolating project dependencies.
- **eBay API credentials** — An active eBay developer account with API keys for listing management.
- **Image recognition / AI service** — An active API key for an external AI service (e.g., Google Cloud Vision, AWS Rekognition, or Azure Computer Vision) for part identification.
- **A PostgreSQL or SQLite database** — For storing part records, queues, and listing data.

---

## Installation

Follow these step-by-step instructions to set up the development environment:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/quickeeparts.git
   cd quickeeparts
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # On macOS / Linux
   # venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   # SQLite (default, no additional setup needed)
   # or
   # PostgreSQL — create the database
   createdb quickeeparts
   python src/app.py migrate
   ```

5. **Initialize the application**
   ```bash
   python src/app.py init
   ```

Your development environment is now ready.

---

## Configuration

quickeeparts is configured through environment variables. Copy the example file and fill in your values:

```bash
cp .env.example .env
```

### Required Environment Variables

| Variable                        | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `EBAY_CLIENT_ID`                | Your eBay API client (application) ID                                       |
| `EBAY_CLIENT_SECRET`            | Your eBay API client secret                                                 |
| `EBAY_AUTH_TOKEN`               | eBay API authentication token (or refresh token)                            |
| `AI_SERVICE_API_KEY`            | API key for your image recognition / AI service (e.g., Google Vision, AWS)  |
| `AI_SERVICE_ENDPOINT`           | The endpoint URL for the AI image recognition service                       |
| `DATABASE_URL`                  | Database connection string (e.g., `sqlite:///parts.db` or `postgresql://...`)|
| `SECRET_KEY`                    | Secret key for application session security                                 |
| `APPROVAL_REQUIRED`             | Set to `true` to enable the approval workflow (default: `true`)             |
| `ALLOWED_PLATFORMS`             | Comma-separated list of platforms to list on (e.g., `ebay,mecum,barrett`)   |

### External Service Configuration

- **eBay API** — Register at [eBay Developer Portal](https://developer.ebay.com/) to obtain your API credentials.
- **AI / Image Recognition** — Any service that supports image classification and object detection (Google Cloud Vision, AWS Rekognition, Azure Computer Vision).
- **Database** — PostgreSQL is recommended for production; SQLite is supported for development.

---

## Usage Examples

### Upload a Part Photo

Upload a photo of a part for identification and processing:

```bash
python src/app.py upload-photo \
    --image "photos/exhaust_manifold.jpg" \
    --description "Aluminum exhaust manifold, used"
```

Response:
```json
{
  "id": "part-4f8a2c1e",
  "status": "identified",
  "part_name": "Aluminum Exhaust Manifold",
  "manufacturer": "BorgWarner",
  "confidence": 0.94
}
```

### Check Part Identification

Query the identification result for a specific part:

```bash
python src/app.py check-identification --id part-4f8a2c1e
```

Response:
```json
{
  "id": "part-4f8a2c1e",
  "status": "identified",
  "part_name": "Aluminum Exhaust Manifold",
  "manufacturer": "BorgWarner",
  "estimated_value": 85.00,
  "demand_score": 0.78,
  "confidence": 0.94
}
```

### View the Approval Queue

See all parts currently waiting for approval:

```bash
python src/app.py view-queue
```

Output:
```
Approval Queue
─────────────────────────────────────────────────
ID             Part                    Value    Submitted
─────────────────────────────────────────────────
part-4f8a2c1e  Exhaust Manifold        $85.00   2025-01-15
part-9b3d7e2a  Brake Caliper           $120.00  2025-01-14
part-1c5f8d3b  Alternator              $65.00   2025-01-13
─────────────────────────────────────────────────
3 items in queue
```

### Approve a Part

Approve a specific part for listing:

```bash
python src/app.py approve --id part-4f8a2c1e
```

Response:
```json
{
  "id": "part-4f8a2c1e",
  "status": "listed",
  "listing_url": "https://www.ebay.com/itm/1234567890",
  "platforms": ["ebay"]
}
```

### List an Approved Part

Manually trigger listing creation for an already-approved part:

```bash
python src/app.py list-part --id part-9b3d7e2a --platforms ebay,mecum
```

Response:
```json
{
  "id": "part-9b3d7e2a",
  "status": "listed",
  "listings": [
    { "platform": "ebay", "url": "https://www.ebay.com/itm/1234567890" },
    { "platform": "mecum", "url": "https://www.mecum.com/listings/abc123" }
  ]
}
```

---

## Testing

Run the full test suite to verify everything is working correctly:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Run a specific test file
pytest tests/test_identify.py
```

### Test Environment

Before running tests, make sure your `.env` file is set up or create a test-specific environment:

```bash
cp .env.example .env.test
# Update .env.test with test values
export $(cat .env.test | xargs)
pytest
```

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file in the repository root for the full license text.

```
MIT License

Copyright (c) 2025 quickeeparts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

*Built for shops with too many extra parts — quickeeparts helps you sell them fast.*
