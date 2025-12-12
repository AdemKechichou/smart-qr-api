# Smart QR API

A production-ready REST API for generating customizable QR codes with built-in analytics tracking. Built with FastAPI and PostgreSQL.

**🔗 Live Demo:** https://smart-qr-api.up.railway.app/

**📚 Interactive API Docs:** https://smart-qr-api.up.railway.app//docs

---

## Features

- **Customizable QR Codes**
  - Custom colors (RGB)
  - Adjustable sizes
  - Logo embedding with automatic resizing
  - High error correction for reliable scanning

- **Analytics Dashboard**
  - Track total QR codes generated
  - Time-based analytics (today, last 30 days, last year)
  - Feature usage statistics
  - Average response time monitoring

- **Production-Ready**
  - Comprehensive error handling
  - PostgreSQL database integration
  - Secure environment variable management
  - Request validation with Pydantic

---

## Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **Image Processing:** Pillow, qrcode
- **Deployment:** Railway
- **Environment Management:** python-dotenv

---

## API Endpoints

### 1. Generate QR Code

**`POST /generate-qr/`**

Generate a customizable QR code with optional logo and colors.

**Request Body:**
```json
{
  "text": "https://example.com",
  "size": 15,
  "color": {
    "red": 255,
    "green": 0,
    "blue": 0
  },
  "logo_url": "https://example.com/logo.png"
}
```

**Parameters:**
- `text` (required): Content to encode in QR code
- `size` (optional): Box size for QR code pixels (default: 10)
- `color` (optional): RGB color values (0-255)
- `logo_url` (optional): URL to logo image to embed

**Response:** PNG image

---

### 2. Get Total Analytics

**`GET /analytics/total`**

Returns the total number of QR codes generated.

**Response:**
```json
{
  "total_qr_codes": 1523
}
```

---

### 3. Get Period Analytics

**`GET /analytics/period?timeframe={period}`**

Get QR code generation stats for a specific time period.

**Query Parameters:**
- `timeframe`: `today`, `month`, or `year`

**Response:**
```json
{
  "timeframe": "today",
  "count": 45,
  "period_start": "2025-12-12",
  "period_end": "2025-12-12"
}
```

---

### 4. Get Feature Statistics

**`GET /analytics/features`**

Returns detailed breakdown of feature usage.

**Response:**
```json
{
  "total": 1523,
  "with_color": 340,
  "with_logo": 892,
  "with_both": 156,
  "average_size": 12.3,
  "average_response_time_ms": 603.5
}
```

---

## Local Setup

### Prerequisites

- Python 3.10+
- PostgreSQL
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdemKechichou/smart-qr-api.git
   cd smart-qr-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE qr_api_db;
   ```

5. **Create database table**
   ```sql
   CREATE TABLE qr_requests (
       id SERIAL PRIMARY KEY,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       has_color BOOLEAN,
       has_logo BOOLEAN,
       size INTEGER,
       response_time_ms INTEGER
   );
   ```

6. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=qr_api_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

7. **Run the API**
   ```bash
   uvicorn main:app --reload
   ```

8. **Access the API**
   - API: http://127.0.0.1:8000
   - Interactive docs: http://127.0.0.1:8000/docs

---

## Usage Example

### Python

```python
import requests

# Generate a red QR code with logo
response = requests.post(
    "https://smart-qr-api.up.railway.app/generate-qr/",
    json={
        "text": "https://github.com/AdemKechichou",
        "size": 15,
        "color": {"red": 255, "green": 0, "blue": 0},
        "logo_url": "https://github.com/logo.png"
    }
)

# Save the QR code
with open("qr_code.png", "wb") as f:
    f.write(response.content)

# Get analytics
analytics = requests.get("https://smart-qr-api.up.railway.app/analytics/total")
print(analytics.json())
```

### cURL

```bash
# Generate QR code
curl -X POST "https://smart-qr-api.up.railway.app/generate-qr/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}' \
  --output qr.png

# Get analytics
curl "https://smart-qr-api.up.railway.app/analytics/total"
```

---

## Project Structure

```
smart-qr-api/
├── main.py              # FastAPI application and endpoints
├── database.py          # Database operations and queries
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

---

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request:** Invalid parameters or logo URL
- **500 Internal Server Error:** Database or server issues
- **Timeout Protection:** 5-second timeout on logo downloads
- **Database Resilience:** QR generation continues even if analytics fail

---

## Future Enhancements

- [ ] API key authentication
- [ ] Rate limiting (free vs paid tiers)
- [ ] Batch QR code generation
- [ ] SVG output format
- [ ] Custom QR code styles (dots, rounded corners)
- [ ] Background color customization
- [ ] QR code templates

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Contact

**Adem Kechichou**  
GitHub: [@AdemKechichou](https://github.com/AdemKechichou)  
Email: ademkechichou@gmail.com

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**
