from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "mock_data"

app = FastAPI(
    title="RChive Sanitized Demo",
    description="Synthetic browser demo for an IndieMaker IP-only listing.",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def load_json(name: str) -> Any:
    with open(DATA_DIR / name, "r", encoding="utf-8") as handle:
        return json.load(handle)


def all_data() -> dict[str, Any]:
    return {
        "objects": load_json("objects.json"),
        "research": load_json("research_notes.json"),
        "knowledge": load_json("knowledge_articles.json"),
        "matches": load_json("visual_matches.json"),
        "commerce": load_json("commerce_listings.json"),
        "services": load_json("service_status.json"),
        "mobile": load_json("mobile_sessions.json"),
        "sources": load_json("sources.json"),
        "review": load_json("review_queue.json"),
        "hallmarks": load_json("hallmarks.json"),
        "makers": load_json("makers.json"),
    }


def object_by_id(object_id: str) -> dict[str, Any]:
    for item in load_json("objects.json"):
        if item["id"] == object_id:
            return item
    raise HTTPException(status_code=404, detail="Object not found in demo data")


def related(items: list[dict[str, Any]], ids: list[str]) -> list[dict[str, Any]]:
    wanted = set(ids)
    return [item for item in items if item["id"] in wanted]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    data = all_data()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "objects": data["objects"],
            "makers": data["makers"],
            "sources": data["sources"],
            "drafts": data["commerce"],
            "knowledge": data["knowledge"],
            "review": data["review"],
            "counts": {
                "objects": len(data["objects"]),
                "research": len(data["research"]),
                "knowledge": len(data["knowledge"]),
                "commerce": len(data["commerce"]),
                "services": len(data["services"]),
                "mobile": len(data["mobile"]),
                "sources": len(data["sources"]),
                "review": len(data["review"]),
                "hallmarks": len(data["hallmarks"]),
                "makers": len(data["makers"]),
            },
        },
    )


@app.get("/collection", response_class=HTMLResponse)
def collection(request: Request, category: str = "all", status: str = "all"):
    objects = load_json("objects.json")
    filtered = [
        item
        for item in objects
        if (category == "all" or item["category"] == category)
        and (status == "all" or item["status"] == status)
    ]
    return templates.TemplateResponse(
        "collection.html",
        {
            "request": request,
            "objects": filtered,
            "all_objects": objects,
            "category": category,
            "status": status,
            "categories": sorted({item["category"] for item in objects}),
            "statuses": sorted({item["status"] for item in objects}),
        },
    )


@app.get("/collection/{object_id}", response_class=HTMLResponse)
def object_detail(request: Request, object_id: str):
    item = object_by_id(object_id)
    research = related(load_json("research_notes.json"), item["research_note_ids"])
    knowledge = related(load_json("knowledge_articles.json"), item["knowledge_article_ids"])
    return templates.TemplateResponse(
        "object_detail.html",
        {
            "request": request,
            "item": item,
            "research": research,
            "knowledge": knowledge,
        },
    )


@app.get("/research", response_class=HTMLResponse)
def research(request: Request, object_id: str | None = None, compare: bool = False):
    objects = load_json("objects.json")
    notes = load_json("research_notes.json")
    if object_id:
        selected = object_by_id(object_id)
        notes = related(notes, selected["research_note_ids"])
    else:
        selected = None
    comparison = None
    if compare:
        comparison = (
            "The synthetic references agree on material family and approximate period, "
            "but differ on maker attribution. The demo would route this to deeper review."
        )
    return templates.TemplateResponse(
        "research.html",
        {
            "request": request,
            "objects": objects,
            "selected": selected,
            "notes": notes,
            "comparison": comparison,
        },
    )


@app.get("/sources", response_class=HTMLResponse)
def sources(request: Request):
    return templates.TemplateResponse(
        "sources.html",
        {
            "request": request,
            "sources": load_json("sources.json"),
            "objects": load_json("objects.json"),
        },
    )


@app.get("/review", response_class=HTMLResponse)
def review(request: Request):
    return templates.TemplateResponse(
        "review.html",
        {"request": request, "candidates": load_json("review_queue.json")},
    )


@app.get("/identify", response_class=HTMLResponse)
def identify(request: Request):
    return templates.TemplateResponse(
        "identify.html",
        {"request": request, "matches": load_json("visual_matches.json"), "uploaded": False},
    )


@app.post("/identify", response_class=HTMLResponse)
async def identify_post(request: Request, image: UploadFile | None = File(default=None)):
    filename = image.filename if image else "sample-object"
    return templates.TemplateResponse(
        "identify.html",
        {
            "request": request,
            "matches": load_json("visual_matches.json"),
            "uploaded": True,
            "filename": filename,
        },
    )


@app.get("/hallmarks", response_class=HTMLResponse)
def hallmarks(request: Request):
    return templates.TemplateResponse(
        "hallmarks.html",
        {"request": request, "hallmarks": load_json("hallmarks.json")},
    )


@app.get("/makers", response_class=HTMLResponse)
def makers(request: Request):
    return templates.TemplateResponse(
        "makers.html",
        {"request": request, "makers": load_json("makers.json")},
    )


@app.get("/knowledge", response_class=HTMLResponse)
def knowledge(request: Request, q: str = ""):
    articles = load_json("knowledge_articles.json")
    query = q.strip().lower()
    if query:
        articles = [
            article
            for article in articles
            if query in article["title"].lower()
            or query in article["category"].lower()
            or query in article["summary"].lower()
            or any(query in tag.lower() for tag in article["tags"])
        ]
    return templates.TemplateResponse(
        "knowledge.html",
        {"request": request, "articles": articles, "q": q},
    )


@app.get("/commerce", response_class=HTMLResponse)
def commerce(request: Request, validated: bool = False, publish_attempt: bool = False):
    return templates.TemplateResponse(
        "commerce.html",
        {
            "request": request,
            "drafts": load_json("commerce_listings.json"),
            "validated": validated,
            "publish_attempt": publish_attempt,
        },
    )


@app.post("/commerce/validate")
def commerce_validate():
    return JSONResponse(
        {
            "status": "valid",
            "message": "Synthetic draft passed demo validation.",
            "checks": ["title", "description", "condition", "price", "disclosures"],
            "demo_only": True,
        }
    )


@app.post("/commerce/publish")
def commerce_publish():
    return JSONResponse(
        {
            "status": "blocked",
            "message": "Live marketplace writes are disabled in this sanitized demo.",
            "demo_only": True,
        },
        status_code=403,
    )


@app.get("/services", response_class=HTMLResponse)
def services(request: Request):
    return templates.TemplateResponse(
        "services.html",
        {"request": request, "services": load_json("service_status.json")},
    )


@app.get("/mobile", response_class=HTMLResponse)
def mobile(request: Request):
    return templates.TemplateResponse(
        "mobile.html",
        {"request": request, "sessions": load_json("mobile_sessions.json")},
    )


@app.get("/api", response_class=HTMLResponse)
def api_docs(request: Request):
    endpoints = [
        "GET /api/v1/health",
        "GET /api/v1/sources",
        "POST /api/v1/sources/{source_id}/pull",
        "GET /api/v1/statistics",
        "GET /api/v1/review/candidates",
        "POST /api/v1/review/candidates/{candidate_id}/promote",
        "GET /api/v1/commerce/readiness",
        "GET /api/v1/hallmarks/search",
        "GET /api/v1/makers",
        "GET /api/objects",
        "GET /api/objects/{object_id}",
        "GET /api/research/{object_id}",
        "GET /api/knowledge/search?q=",
        "GET /api/identify/sample",
        "POST /api/identify/mock",
        "GET /api/commerce/drafts",
        "POST /api/commerce/validate",
        "POST /api/commerce/publish",
        "GET /api/services/status",
        "GET /api/mobile/sessions",
    ]
    return templates.TemplateResponse(
        "api_docs.html",
        {"request": request, "endpoints": endpoints},
    )


@app.get("/api/v1/health")
def api_v1_health():
    return {
        "status": "ok",
        "application": "RChive sanitized demo",
        "database_exists": True,
        "demo_only": True,
    }


@app.get("/api/v1/sources")
def api_v1_sources():
    sources = load_json("sources.json")
    return {"count": len(sources), "sources": sources, "demo_only": True}


@app.post("/api/v1/sources/{source_id}/pull")
def api_v1_source_pull(source_id: str):
    source = next((item for item in load_json("sources.json") if item["id"] == source_id), None)
    if source is None:
        raise HTTPException(status_code=404, detail="Synthetic source not found")
    return {
        "source_id": source_id,
        "source_name": source["name"],
        "requested_limit": 10,
        "records_added": 0,
        "message": "Demo import is simulated. No remote content was fetched.",
        "demo_only": True,
    }


@app.get("/api/v1/statistics")
def api_v1_statistics():
    data = all_data()
    return {
        "objects": len(data["objects"]),
        "knowledge_entries": len(data["knowledge"]),
        "research_notes": len(data["research"]),
        "review_candidates": len(data["review"]),
        "marketplace_drafts": len(data["commerce"]),
        "demo_only": True,
    }


@app.get("/api/v1/review/candidates")
def api_v1_review_candidates():
    return {"candidates": load_json("review_queue.json"), "demo_only": True}


@app.get("/api/v1/hallmarks/search")
def api_v1_hallmarks_search(q: str = ""):
    hallmarks = load_json("hallmarks.json")
    query = q.strip().lower()
    if query:
        hallmarks = [
            item
            for item in hallmarks
            if query in item["mark"].lower()
            or query in item["material"].lower()
            or query in item["interpretation"].lower()
        ]
    return {"results": hallmarks, "demo_only": True}


@app.get("/api/v1/makers")
def api_v1_makers():
    return {"makers": load_json("makers.json"), "demo_only": True}


@app.post("/api/v1/review/candidates/{candidate_id}/promote")
def api_v1_review_promote(candidate_id: str):
    candidate = next((item for item in load_json("review_queue.json") if item["id"] == candidate_id), None)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Synthetic candidate not found")
    return {
        "status": "simulated",
        "candidate_id": candidate_id,
        "message": "Promotion is simulated and does not alter canonical data.",
        "demo_only": True,
    }


@app.get("/api/v1/commerce/readiness")
def api_v1_commerce_readiness():
    drafts = load_json("commerce_listings.json")
    providers = ["mock", "ebay_sandbox", "woocommerce_demo", "chrono24_feed", "rubylane_prep", "manual_export"]
    return {
        "products": [
            {
                "draft_id": draft["id"],
                "title": draft["title"],
                "channels": [
                    {
                        "provider": provider,
                        "status": "READY" if provider in {"mock", "manual_export"} else "SIMULATED",
                        "mechanism": "mock" if provider == "mock" else "export-or-sandbox",
                    }
                    for provider in providers
                ],
            }
            for draft in drafts
        ],
        "demo_only": True,
    }


@app.get("/api/objects")
def api_objects():
    return load_json("objects.json")


@app.get("/api/objects/{object_id}")
def api_object(object_id: str):
    return object_by_id(object_id)


@app.get("/api/research/{object_id}")
def api_research(object_id: str):
    item = object_by_id(object_id)
    return related(load_json("research_notes.json"), item["research_note_ids"])


@app.get("/api/knowledge/search")
def api_knowledge_search(q: str = ""):
    articles = load_json("knowledge_articles.json")
    query = q.strip().lower()
    if not query:
        return articles
    return [
        article
        for article in articles
        if query in article["title"].lower()
        or query in article["category"].lower()
        or query in article["summary"].lower()
        or any(query in tag.lower() for tag in article["tags"])
    ]


@app.get("/api/identify/sample")
def api_identify_sample():
    return load_json("visual_matches.json")


@app.post("/api/identify/mock")
async def api_identify_mock(image: UploadFile | None = File(default=None)):
    return {
        "status": "mocked",
        "uploaded_filename": image.filename if image else None,
        "matches": load_json("visual_matches.json"),
        "demo_only": True,
    }


@app.get("/api/commerce/drafts")
def api_commerce_drafts():
    return load_json("commerce_listings.json")


@app.post("/api/commerce/validate")
def api_commerce_validate(draft_id: str = Form(default="draft-001")):
    return {
        "status": "valid",
        "draft_id": draft_id,
        "message": "Synthetic draft passed demo validation.",
        "demo_only": True,
    }


@app.post("/api/commerce/publish")
def api_commerce_publish():
    return JSONResponse(
        {
            "status": "blocked",
            "message": "Live marketplace writes are disabled in this sanitized demo.",
            "demo_only": True,
        },
        status_code=403,
    )


@app.get("/api/services/status")
def api_services_status():
    return load_json("service_status.json")


@app.get("/api/mobile/sessions")
def api_mobile_sessions():
    return load_json("mobile_sessions.json")
