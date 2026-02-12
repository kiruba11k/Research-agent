def normalize_sources(sources):
    citations = []
    for i, s in enumerate(sources, start=1):
        citations.append({
            "id": i,
            "title": s.get("title", "Source"),
            "url": s.get("url")
        })
    return citations
