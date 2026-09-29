def parse_pdf_pages(pages):
    result = []

    for page in pages:
        # Ignore empty pages instead of treating them as page breaks
        if not page.strip():
            continue

        result.append(page.strip())

    return "\n--- PAGE BREAK ---\n".join(result)


pages = [
    "Page 1 content",
    "",
    "Page 2 content"
]

print(parse_pdf_pages(pages))