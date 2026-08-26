(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);

  const MOBILE_PAGE_SIZE = 10;
  const MOBILE_BREAKPOINT = 760;

  const state = {
    data: null,
    quick: "",
    mobilePage: 0
  };

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, c => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[c]);
  }

  function displayDate(value) {
    if (!value) return "";

    return new Date(value + "T00:00:00").toLocaleDateString("en-AU", {
      day: "numeric",
      month: "short",
      year: "numeric"
    });
  }

  function humaniseSlug(value) {
    return String(value || "")
      .split(/[-_]/)
      .filter(Boolean)
      .map(x => x.charAt(0).toUpperCase() + x.slice(1))
      .join(" ");
  }

  function isMobile() {
    return window.innerWidth <= MOBILE_BREAKPOINT;
  }

  function navigateParent(url) {
    if (!url) return;

    if (window.parent !== window) {
      window.parent.location.href = url;
    } else {
      window.location.href = url;
    }
  }

  function scrollToResults() {
    const target = $("libraryResultsTop") || $("librarySearch");
    if (!target) return;

    target.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  }

  function typeLabel(record) {
    if (record.item_type === "tip") {
      return record.code || "Tip";
    }

    if (record.item_type === "event") {
      return record.event_status
        ? `Event · ${humaniseSlug(record.event_status)}`
        : "Event";
    }

    if (record.item_type === "resource") {
      return "Download";
    }

    return (
      state.data.labels.categories[record.category] ||
      humaniseSlug(record.category) ||
      "Article"
    );
  }

  function secondaryLabel(record) {
    if (record.series) {
      const name =
        state.data.labels.series[record.series] ||
        humaniseSlug(record.series);

      return name + (record.part ? ` · Part ${record.part}` : "");
    }

    if (record.item_type === "tip" && record.level) {
      return `${humaniseSlug(record.level)} level`;
    }

    if (record.event_date) {
      return displayDate(record.event_date);
    }

    return "";
  }

  function card(record) {
    const cls = ["tip", "event", "resource"].includes(record.item_type)
      ? record.item_type
      : "";

    const category =
      state.data.labels.categories[record.category] ||
      humaniseSlug(record.category);

    const tags = (record.tags || [])
      .slice(0, 6)
      .map(t => `<span class="tag">${escapeHtml(t)}</span>`)
      .join("");

    const actions =
      `${record.download_url ? `<a class="action download-link" href="${escapeHtml(record.download_url)}" target="_blank" rel="noopener">Download File</a>` : ""}` +
      `<button class="action open-link" type="button" data-open-url="${escapeHtml(record.open_url)}">Open in Issue ${escapeHtml(record.issue)}</button>`;

    return `
      <article class="card">
        <div class="card-top">
          <div class="badges">
            <span class="badge ${cls}">${escapeHtml(typeLabel(record))}</span>
            ${
              record.item_type !== "article" && category
                ? `<span class="badge">${escapeHtml(category)}</span>`
                : ""
            }
          </div>

          <span class="issue">
            Issue ${escapeHtml(record.issue)} · ${escapeHtml(displayDate(record.published))}
          </span>
        </div>

        <div class="series-line">${escapeHtml(secondaryLabel(record))}</div>

        <h3>${escapeHtml(record.title)}</h3>

        ${record.excerpt ? `<p>${escapeHtml(record.excerpt)}</p>` : ""}

        <div class="tags">${tags}</div>

        <div class="card-foot">
          <span class="anchor">
            #${escapeHtml(record.open_anchor_id || record.anchor_id)}
          </span>

          <div class="card-actions">${actions}</div>
        </div>
      </article>
    `;
  }

  function matchesQuick(record) {
    const q = state.quick;

    if (!q) return true;

    if (q === "learning") {
      return [
        "education",
        "editing",
        "photography-tips",
        "challenge"
      ].includes(record.category);
    }

    if (q === "club") {
      return (
        [
          "club-news",
          "community",
          "competition",
          "feature"
        ].includes(record.category) &&
        record.item_type !== "event"
      );
    }

    if (q === "events") {
      return record.item_type === "event" || record.category === "events";
    }

    if (q === "travel") {
      return record.category === "members-on-the-move";
    }

    if (q === "downloads") {
      return record.item_type === "resource";
    }

    return true;
  }

  function getFilteredRows() {
    const q = $("searchBox").value.trim().toLowerCase();
    const category = $("categoryFilter").value;
    const series = $("seriesFilter").value;
    const level = $("levelFilter").value;
    const issue = $("issueFilter").value;
    const type = $("typeFilter").value;

    return state.data.records
      .filter(record => {
        const haystack = [
          record.title,
          record.excerpt,
          record.category,
          record.series,
          record.code,
          record.level,
          record.event_status,
          record.event_date,
          ...(record.tags || []),
          ...(record.people || []),
          ...(record.locations || [])
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        return (
          (!q || haystack.includes(q)) &&
          (!category || record.category === category) &&
          (!series || record.series === series) &&
          (!level || record.level === level) &&
          (!issue || record.issue === issue) &&
          (!type || record.item_type === type) &&
          matchesQuick(record)
        );
      })
      .sort(
        (a, b) =>
          (b.published || "").localeCompare(a.published || "") ||
          (a.title || "").localeCompare(b.title || "")
      );
  }

  function setPagerVisibility(show) {
    document.querySelectorAll(".mobile-pager").forEach(pager => {
      pager.style.display = show ? "flex" : "none";
    });
  }

  function updatePager(totalRows) {
    const pageLabels = document.querySelectorAll("[data-mobile-page]");
    const rangeLabels = document.querySelectorAll("[data-mobile-range]");
    const previousButtons = document.querySelectorAll("[data-mobile-prev]");
    const nextButtons = document.querySelectorAll("[data-mobile-next]");

    if (!isMobile() || totalRows <= MOBILE_PAGE_SIZE) {
      setPagerVisibility(false);
      return;
    }

    const totalPages = Math.ceil(totalRows / MOBILE_PAGE_SIZE);

    if (state.mobilePage >= totalPages) {
      state.mobilePage = Math.max(0, totalPages - 1);
    }

    const firstResult = state.mobilePage * MOBILE_PAGE_SIZE + 1;
    const lastResult = Math.min(
      firstResult + MOBILE_PAGE_SIZE - 1,
      totalRows
    );

    pageLabels.forEach(label => {
      label.textContent = `Page ${state.mobilePage + 1} of ${totalPages}`;
    });

    rangeLabels.forEach(label => {
      label.textContent = `${firstResult}–${lastResult} of ${totalRows}`;
    });

    previousButtons.forEach(button => {
      button.disabled = state.mobilePage === 0;
    });

    nextButtons.forEach(button => {
      button.disabled = state.mobilePage >= totalPages - 1;
    });

    setPagerVisibility(true);
  }

  function applyFilters(resetMobile = false) {
    if (resetMobile) state.mobilePage = 0;

    const rows = getFilteredRows();

    let displayedRows = rows;

    if (isMobile()) {
      const start = state.mobilePage * MOBILE_PAGE_SIZE;
      displayedRows = rows.slice(start, start + MOBILE_PAGE_SIZE);
    }

    $("cards").innerHTML = displayedRows.map(card).join("");

    if (isMobile() && rows.length) {
      const firstResult = state.mobilePage * MOBILE_PAGE_SIZE + 1;
      const lastResult = Math.min(
        firstResult + displayedRows.length - 1,
        rows.length
      );

      $("resultCount").textContent =
        `${firstResult}–${lastResult} of ${rows.length} indexed items`;
    } else {
      $("resultCount").textContent =
        `${rows.length} of ${state.data.records.length} indexed items`;
    }

    $("emptyState").style.display = rows.length ? "none" : "block";

    updatePager(rows.length);
  }

  function fillSelect(select, values, labels, prefix = "") {
    values.forEach(value => {
      select.insertAdjacentHTML(
        "beforeend",
        `<option value="${escapeHtml(value)}">${escapeHtml(
          prefix + (labels?.[value] || humaniseSlug(value))
        )}</option>`
      );
    });
  }

  function initialise(data) {
    state.data = data;

    $("statRecords").textContent = data.summary.records;
    $("statLearning").textContent = data.summary.learning_resources;
    $("statTips").textContent = data.summary.tips;
    $("statIssues").textContent = data.summary.issues;

    $("archiveNote").textContent =
      `all ${data.summary.issues} Weekly Updates are indexed and live-linked.`;

    $("footerCoverage").textContent =
      `${data.summary.issues} issues indexed`;

    const categories = [
      ...new Set(data.records.map(r => r.category).filter(Boolean))
    ].sort((a, b) =>
      (data.labels.categories[a] || a).localeCompare(
        data.labels.categories[b] || b
      )
    );

    const series = [
      ...new Set(data.records.map(r => r.series).filter(Boolean))
    ].sort((a, b) =>
      (data.labels.series[a] || a).localeCompare(
        data.labels.series[b] || b
      )
    );

    const issues = data.issues.map(i => i.issue);

    fillSelect(
      $("categoryFilter"),
      categories,
      data.labels.categories
    );

    fillSelect(
      $("seriesFilter"),
      series,
      data.labels.series
    );

    fillSelect(
      $("issueFilter"),
      issues,
      null,
      "Issue "
    );

    $("seriesStrip").innerHTML =
      data.series
        .map(
          s => `
            <button
              class="series-card"
              type="button"
              data-series-jump="${escapeHtml(s.id)}"
            >
              <span class="series-name">${escapeHtml(s.name)}</span>
              <span class="series-meta">
                ${s.article_count}
                indexed article${s.article_count === 1 ? "" : "s"}
              </span>
              <span class="series-link">View series →</span>
            </button>
          `
        )
        .join("");

    document
      .querySelectorAll("[data-series-jump]")
      .forEach(button => {
        button.addEventListener("click", () => {
          $("seriesFilter").value = button.dataset.seriesJump;
          state.quick = "";
          state.mobilePage = 0;

          document
            .querySelectorAll("#quickFilters button")
            .forEach((x, i) =>
              x.classList.toggle("active", i === 0)
            );

          applyFilters();
          scrollToResults();
        });
      });

    applyFilters();
  }

  [
    "searchBox",
    "categoryFilter",
    "seriesFilter",
    "levelFilter",
    "issueFilter",
    "typeFilter"
  ].forEach(id => {
    $(id).addEventListener(
      id === "searchBox" ? "input" : "change",
      () => applyFilters(true)
    );
  });

  document
    .querySelectorAll("#quickFilters button")
    .forEach(button => {
      button.addEventListener("click", () => {
        state.quick = button.dataset.quick;
        state.mobilePage = 0;

        document
          .querySelectorAll("#quickFilters button")
          .forEach(x =>
            x.classList.toggle("active", x === button)
          );

        applyFilters();
      });
    });

  $("clearBtn").addEventListener("click", () => {
    [
      "searchBox",
      "categoryFilter",
      "seriesFilter",
      "levelFilter",
      "issueFilter",
      "typeFilter"
    ].forEach(id => {
      $(id).value = "";
    });

    state.quick = "";
    state.mobilePage = 0;

    document
      .querySelectorAll("#quickFilters button")
      .forEach((x, i) =>
        x.classList.toggle("active", i === 0)
      );

    applyFilters();
  });

  $("cards").addEventListener("click", event => {
    const button = event.target.closest("[data-open-url]");
    if (!button) return;

    navigateParent(button.dataset.openUrl);
  });

  document.querySelectorAll("[data-mobile-prev]").forEach(button => {
    button.addEventListener("click", () => {
      if (state.mobilePage === 0) return;

      state.mobilePage -= 1;
      applyFilters(false);
      scrollToResults();
    });
  });

  document.querySelectorAll("[data-mobile-next]").forEach(button => {
    button.addEventListener("click", () => {
      const rows = getFilteredRows();
      const totalPages = Math.ceil(rows.length / MOBILE_PAGE_SIZE);

      if (state.mobilePage >= totalPages - 1) return;

      state.mobilePage += 1;
      applyFilters(false);
      scrollToResults();
    });
  });

  $("editionGoBtn").addEventListener("click", () => {
    navigateParent($("editionSelect").value);
  });

  $("editionSelect").addEventListener("keydown", event => {
    if (event.key === "Enter") {
      navigateParent($("editionSelect").value);
    }
  });

  function toggleReturn() {
    $("returnSearchBtn").classList.toggle(
      "show",
      $("librarySearch").getBoundingClientRect().bottom < 0
    );
  }

  $("returnSearchBtn").addEventListener("click", () => {
    $("librarySearch").scrollIntoView({
      behavior: "smooth",
      block: "start"
    });

    setTimeout(
      () =>
        $("searchBox").focus({
          preventScroll: true
        }),
      400
    );
  });

  addEventListener("scroll", toggleReturn, {
    passive: true
  });

  let lastMobileState = isMobile();

  addEventListener("resize", () => {
    toggleReturn();

    const currentMobileState = isMobile();

    if (currentMobileState !== lastMobileState) {
      lastMobileState = currentMobileState;
      state.mobilePage = 0;

      if (state.data) {
        applyFilters();
      }
    }
  });

  toggleReturn();

  fetch("library.json", {
    cache: "no-store"
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return response.json();
    })
    .then(initialise)
    .catch(error => {
      console.error("Resource Library load failed", error);

      $("cards").innerHTML = `
        <div class="load-error">
          The Resource Library data could not be loaded.
          Please refresh the page.
        </div>
      `;
    });
})();
