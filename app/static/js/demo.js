const sampleCards = [
  { title: "Rhinestone Parrot Brooch", body: "Matched as jewellery / brooch with clear stones, bird silhouette, and commerce-ready photo set.", meta: "Sample archive record obj-parrot-brooch" },
  { title: "Feather Motif Silver Ring", body: "Matched as jewellery / ring with maker candidate and metal-review workflow.", meta: "Sample archive record obj-feather-ring" },
  { title: "Dante Bronze-Tone Bust", body: "Matched as decorative art with subject inscription and material uncertainty.", meta: "Sample archive record obj-dante-bust" }
];

const visualCards = [
  { image: "/static/images/parrot-brooch.jpg", title: "88% - Rhinestone parrot brooch", body: "Mock match: bird silhouette, clear stone rows, black eye accent, long tail feathers.", meta: "Next: inspect clasp, back marks, and missing stones." },
  { image: "/static/images/nelson-feather-ring.jpg", title: "76% - Feather motif silver ring", body: "Mock match: feather form, patina, open band shape, and stamped detail.", meta: "Next: capture interior marks for hallmark review." },
  { image: "/static/images/dante-bust.jpg", title: "71% - Dante bust", body: "Mock match: bust form, helmet profile, inscription, and patinated surface.", meta: "Next: compare material notes and inspect base." }
];

const hallmarkCards = [
  { title: "No visible front mark - brooch back required", body: "Routes the parrot brooch to back-side inspection before maker or metal claims are made.", meta: "front_image_only / clasp_check_needed" },
  { title: "Possible silver or maker stamp inside band", body: "Links the feather ring to maker review and metal verification.", meta: "maker_candidate / human_review_required" },
  { title: "DANTE inscription visible on bust", body: "Treated as subject evidence, not a maker hallmark.", meta: "subject_inscription / not_maker_mark" }
];

const smartCards = [
  { title: "Smart Search mock reasoning", body: "The query combines object description, visible materials, sample image evidence, and Knowledge tags, then returns candidate workflows.", meta: "Reveals workflow only; production ranking and private indexes are not exposed." },
  { title: "Suggested path", body: "Archive record -> Visual Search -> Hallmark Search -> Knowledge -> Candidate Review -> Commerce readiness.", meta: "All actions are sample responses." }
];

function activatePage(page) {
  const target = document.querySelector(`#page-${page}`);
  if (!target) return;
  document.querySelectorAll(".showroom-page").forEach((item) => item.classList.remove("is-visible"));
  target.classList.add("is-visible");
  document.querySelectorAll("[data-page-nav]").forEach((item) => item.classList.toggle("is-active", item.dataset.pageNav === page));
  const title = document.querySelector("#page-title");
  if (title) title.textContent = target.dataset.title || page;
  if (location.hash !== `#${page}`) history.replaceState(null, "", page === "archive" ? location.pathname : `#${page}`);
}

function renderResultCards(targetId, cards) {
  const target = document.querySelector(`#${targetId}`);
  if (!target) return;
  target.innerHTML = cards.map((card) => `
    <article class="result-card" data-tip="Mock response generated from sample data only.">
      <h2>${card.title}</h2>
      <p>${card.body}</p>
      <small>${card.meta}</small>
    </article>
  `).join("");
}

function renderVisualCards(targetId) {
  const target = document.querySelector(`#${targetId}`);
  if (!target) return;
  target.innerHTML = visualCards.map((card) => `
    <article class="match-card" data-tip="This is a prepared sample result, not a live image-index call.">
      <img src="${card.image}" alt="">
      <div>
        <span>${card.title}</span>
        <h2>${card.body}</h2>
        <p>${card.meta}</p>
      </div>
    </article>
  `).join("");
}

async function postDemo(url) {
  const result = document.querySelector("#commerce-result");
  if (!result) return;
  result.classList.remove("hidden");
  result.textContent = "Checking demo endpoint...";
  try {
    const response = await fetch(url, { method: "POST" });
    const body = await response.json();
    result.textContent = `${body.status}: ${body.message}`;
  } catch (error) {
    result.textContent = "Demo endpoint unavailable.";
  }
}

document.querySelectorAll("[data-page-nav]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    activatePage(link.dataset.pageNav);
  });
});

document.querySelectorAll("[data-fill-results]").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.fillResults;
    if (id === "visual-results") renderVisualCards(id);
    if (id === "search-results") renderResultCards(id, sampleCards);
    if (id === "hallmark-results") renderResultCards(id, hallmarkCards);
    if (id === "smart-results") renderResultCards(id, smartCards);
  });
});

document.querySelectorAll("[data-clear-results]").forEach((button) => {
  button.addEventListener("click", () => {
    const target = document.querySelector(`#${button.dataset.clearResults}`);
    if (target) target.innerHTML = "";
  });
});

document.querySelectorAll("[data-demo-post]").forEach((button) => {
  button.addEventListener("click", () => postDemo(button.dataset.demoPost));
});

document.querySelectorAll("[data-demo-search]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    activatePage("search");
    renderResultCards("search-results", sampleCards);
  });
});

document.querySelectorAll("[data-mock-action]").forEach((button) => {
  button.addEventListener("click", () => {
    const messages = {
      "open-folder": "Sample archive folder is represented inside app/sample_archive.",
      refresh: "Archive refresh simulated. Sample records are already current.",
      "stage-object": "Object intake staged as a preview only. No database write occurred.",
      "pull-source": "Source pull simulated. No museum API, specialist source, live website, or scraper was contacted.",
      "listing-maker": "Listing Maker preview simulated. Production support may be AI-assisted, automated as a service, and tier or credit aware.",
      reject: "Candidate rejection simulated. Canonical data was not changed."
    };
    window.alert(messages[button.dataset.mockAction] || "Demo action simulated.");
  });
});

const guide = document.querySelector("#demo-guide");
document.querySelectorAll("[data-guide]").forEach((button) => {
  button.addEventListener("click", () => {
    guide?.classList.add("is-open");
    guide?.setAttribute("aria-hidden", "false");
  });
});
document.querySelectorAll("[data-guide-close]").forEach((button) => {
  button.addEventListener("click", () => {
    guide?.classList.remove("is-open");
    guide?.setAttribute("aria-hidden", "true");
  });
});

activatePage((location.hash || "#archive").replace("#", ""));
