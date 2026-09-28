# RAG API

A small FastAPI endpoint that ranks supplied documents with TF-IDF and generates an answer from the retrieved context using OpenAI.

## Run

```powershell
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY = "your-api-key"
uvicorn main:app --reload
```

Set `OPENAI_MODEL` to override the default `gpt-4o-mini` model. The API key is read from the environment and is never included in the request.

## Request

Send `POST /rag` with a question, candidate documents, and an optional result limit (`top_k`, from 1 to 10):

```json
{
  "query": "What is Python?",
  "documents": [
    "Python is a programming language designed for readable code.",
    "Oranges are a citrus fruit."
  ],
  "top_k": 2
}
```

The response contains the generated `answer` and the retrieved `sources`. A request with no matching documents returns `422`; missing OpenAI configuration returns `503`.

Interactive API documentation is available at `/docs` while the server is running.