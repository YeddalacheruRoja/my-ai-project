work_items = [
    "Add a new RAG endpoint to the API",
    "Fix a bug in the PDF parsing logic",
    "Add user authentication",
    "Fix incorrect date formatting in reports",
    "Add caching layer to search endpoint"
]

for item in work_items:
    if item.startswith("Add"):
        if "RAG endpoint" in item:
            branch_name = "feature/add-rag-endpoint"
        elif "user authentication" in item:
            branch_name = "feature/add-user-authentication"
        elif "caching layer" in item:
            branch_name = "feature/add-search-caching"

    elif item.startswith("Fix"):
        if "PDF parsing" in item:
            branch_name = "fix/pdf-parsing-bug"
        elif "date formatting" in item:
            branch_name = "fix/date-formatting-bug"

    print(f"{item} -> {branch_name}")