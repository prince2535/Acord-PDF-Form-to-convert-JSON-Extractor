ACORD PDF -> JSON Extractor (Django)
===================================
A minimal Django (4.2 LTS) project providing a single POST endpoint `/api/extract/`
which accepts one PDF file (<= 5 MB), extracts text, sends it to OpenAI to parse
into a forced JSON schema (ACORD insurance extraction), validates the JSON against
a schema, and returns it in the response.

Requirements
------------
- Python 3.11 (recommended LTS)
- Install dependencies:
  pip install -r requirements.txt

Environment
-----------
Create a `.env` file in the project root with:
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini   # or another chat capable model
DJANGO_SECRET_KEY=change-me

Run
---
python manage.py migrate
python manage.py runserver

Test
----
curl -X POST -F "file=@/path/to/acord.pdf" http://127.0.0.1:8000/api/extract/

Notes
-----
- This project is a starting point. For production: HTTPS, authentication, rate-limits,
  stricter validation, async OpenAI calls and batching are recommended.
