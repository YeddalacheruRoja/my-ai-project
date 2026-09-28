import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = FastAPI(title="RAG API")


class RAGRequest(BaseModel):
    query: str = Field(min_length=1)
    documents: list[str] = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class RAGResponse(BaseModel):
    answer: str
    sources: list[str]


def retrieve_documents(query: str, documents: list[str], top_k: int) -> list[str]:
    try:
        vectors = TfidfVectorizer().fit_transform([query, *documents])
    except ValueError:
        return []

    scores = cosine_similarity(vectors[0:1], vectors[1:]).ravel()
    ranked = sorted(range(len(documents)), key=lambda index: scores[index], reverse=True)
    return [documents[index] for index in ranked if scores[index] > 0][:top_k]


@app.post("/rag", response_model=RAGResponse)
def rag_endpoint(request: RAGRequest) -> RAGResponse:
    relevant_documents = retrieve_documents(request.query, request.documents, request.top_k)
    if not relevant_documents:
        raise HTTPException(status_code=422, detail="No relevant documents found for the query.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="RAG generation is not configured.")

    context = "\n\n".join(relevant_documents)
    try:
        completion = OpenAI(api_key=api_key).chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "Answer the question using only the supplied context. "
                    "If the context does not contain the answer, say so.",
                },
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.query}"},
            ],
        )
    except OpenAIError as error:
        raise HTTPException(status_code=502, detail="The generation provider request failed.") from error

    answer = completion.choices[0].message.content
    if not answer:
        raise HTTPException(status_code=502, detail="The generation provider returned an empty answer.")
    return RAGResponse(answer=answer, sources=relevant_documents)