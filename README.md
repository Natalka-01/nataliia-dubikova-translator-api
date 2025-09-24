# Simple Translator API

A small demo project built with **FastAPI** to show how to design, test, and document an API.  
The API translates one English word (`apple`) into Spanish (`manzana`) and includes authentication.

---

## Features
- FastAPI app with two endpoints:
  - `/` → welcome message
  - `/translate` → word translation
- Case-insensitive translation
- Requires a fake bearer token (`Bearer test-fake-jwt-token`)
- Automated tests with `pytest` and `requests`
- Fixtures in `conftest.py` for reusability
- HTML test reports with `pytest-html`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Natalka-01/nataliia-dubikova-translator-api.git
   cd nataliia-dubikova-translator-api

2. Create a virtual environment

    python -m venv .venv
    source .venv/bin/activate   # on Linux/Mac
    .venv\Scripts\activate      # on Windows

3. Install dependencies:

    pip install -r requirements.txt

**Running the API**

Start the FastAPI server with Uvicorn:
uvicorn main:app --reload

By default, the server runs at: http://127.0.0.1:8000

Interactive docs:

Swagger UI: http://127.0.0.1:8000/docs


**Running Tests**
pytest -v

Generate an HTML test report:
pytest -v --html=report.html --self-contained-html


Open report.html in your browser.

Example Usage: 

Welcome endpoint:
curl http://127.0.0.1:8000/

Response:
{"message": "👋 Welcome to the Translator API! Go to /docs for usage."}


Correct request:
curl -H "Authorization: Bearer test-fake-jwt-token" \
"http://127.0.0.1:8000/translate?query=apple&locale=es-ES"

Response:

{
  "translation": "manzana"
}
