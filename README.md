# RChive Sanitized Demo

This is a lightweight browser showroom demo for the IndieMaker IP-only listing. It mirrors the visible RChive V49 desktop modules while using only approved sample objects and mock responses.

## What Is Included

- Collection catalog and object detail pages
- V49-style desktop facade plus clearly labeled Breadmaker beta roadmap modules
- Archive, Search, Visual Search, Hallmarks, Smart Search, Makers & Brands, Sources, Commerce, Knowledge, Review, Mobile, Horology, and Numismatics
- Approved sample object images for the parrot brooch, Dante bust, and feather ring
- Tiny inspectable `app/sample_archive` folder with images, database JSON, mock APIs, and hosted-service routing notes
- Mock search, visual, hallmark, smart-search, source-pull, Knowledge-library, commerce, and review actions
- Local/hosted/hybrid capability routing disclosure for paid, concurrent, credit, or tier-based features
- Commerce Listing Maker preview for AI-assisted marketplace listing generation
- Hover explanations and a Demo Guide walkthrough panel
- Internal API stubs kept available as engine plumbing, not shown as a user tab

## What Is Not Included

- No production credentials
- No private research corpus
- No personal data
- No production database
- No live marketplace writes
- No real payment processing
- No real AI provider calls
- No sensitive infrastructure details
- No persistent public uploads
- No live writes of any kind

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Deploy on Render

Create a Render Web Service from this repository. Render can use `render.yaml`, or configure manually:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Suggested Buyer Walkthrough

1. Open the dashboard.
2. Review the synthetic-data notice.
3. Browse the Archive sample records.
4. Run Search, Visual Search, Hallmarks, and Smart Search.
5. Use Sources to simulate configured museum/reference pulls, local object intake, and import history.
6. Open Knowledge to see the private uploaded-reference-library concept.
7. Preview and validate a Commerce draft.
8. Open Listing Maker in Commerce to see the AI-assisted marketplace listing direction.
9. Attempt Publish and confirm live writes are blocked.
10. Review Mobile, Horology, and Numismatics roadmap tabs, then open Demo Guide.

## Acceptance Checklist

- Visible sidebar matches RChive V49 modules.
- API is not shown as a user tab.
- Archive shows approved sample records.
- Search returns mock archive results.
- Visual Search returns sample image matches.
- Hallmarks returns mark/material sample results.
- Smart Search returns a combined mock research path.
- Makers & Brands shows candidate identities.
- Sources shows configured pull/import sources, V49 local intake, and import history.
- Knowledge shows the private digital library concept for uploaded books, PDFs, scans, documents, and notes.
- Commerce validates drafts and blocks publishing.
- Commerce discloses Listing Maker as AI-assisted/service-ready marketplace listing generation.
- Review shows candidates and non-mutating promote/reject actions.
- Mobile, Horology, and Numismatics are clearly marked as active Breadmaker beta roadmap modules.
- Capability routing/tier disclosure is visible.
- Hover explanations and Demo Guide are available.
- `app/sample_archive` is inspectable and contains only sample files.
- Internal API stubs return mock JSON.
- No real secrets, private corpus, personal data, or production writes are present.
