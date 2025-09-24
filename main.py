from fastapi import FastAPI, Query, Header
from fastapi.responses import JSONResponse


app = FastAPI(
    title="Simple Translator API",
    description="A tiny demo API that translates a few English words into other languages.",
    version="1.0.0",
)


translations = {
    ("apple", "es-ES"): "manzana"
}

@app.get("/", summary="Welcome")
def root():
    """Root endpoint to show welcome message."""
    return {"message": "Welcome to the Translator API! Go to /docs for usage. (=^-^=)"}

@app.get(
    "/translate",
    summary="Translate a word",
    description="Provide an English word and a locale (like `es-ES`) to get its translation.",
)
def translate(
    query: str = Query(..., min_length=1, description="The English word to translate e.g. `apple`"),
    locale: str = Query(..., min_length=1, description="The target locale, e.g. `es-ES`, `fr-FR`, `de-DE`"),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    # Simple auth check
    if authorization != "Bearer test-fake-jwt-token":
        return JSONResponse(content={"error": "Unauthorized"}, status_code=401)

    # Look up the translation
    translation = translations.get((query.strip().lower(), locale))

    if translation:
        return JSONResponse(content={"translation": translation}, status_code=200)
    else:
        return JSONResponse(content={"error": "Translation not found"}, status_code=404)











