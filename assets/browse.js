(() => {
  "use strict";

  const $ = id => document.getElementById(id);
  const PAGE_SIZE = 10;

  const escapeHtml = value =>
    String(value ?? "").replace(/[&<>"']/g, c => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[c]);

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

  function navigate(url) {
    window.location.href = url;
  }

  function navigateParent(url) {
    if (!url) return;

    if (window.parent !== window) {
      window.parent.location.href = url;
    } else {
      window.location.href = url;
    }
  }

  function card(record, data) {
    const cls = ["tip", "event", "resource"].includes(record.item_type)
      ? record.item_type
      : "";

    const category =
      data.labels.categories[record.category] ||
      humaniseSlug(record.category);

    let label = category || "Article";

    if (record.item_type === "tip") label = record.code || "Tip";
    if (record.item_type === "event") {
      label = record.event_status
        ? `Event · ${humaniseSlug(record.event_status)}`
        : "Event";
    }
    if (record.item_type === "resource") label = "Download";

    let secondary = "";

    if (record.series) {
      const seriesName =
        data.labels.series[record.series] ||
        humaniseSlug(record.series);
      secondary =
        seriesName + (record.part ? ` · Part ${record.part}` : "");
    } else if (record.item_type === "tip" && record.level) {
      secondary = `${humaniseSlug(record.level)} level`;
    } else if (record.event_date) {
      secondary = displayDate(record.event_date);
    }

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
            <span class="badge ${cls}">${escapeHtml(label)}</span>
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

        <div class="series-line">${escapeHtml(secondary)}</div>
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

  function matchesQuick(record, quick) {
    if (!quick) return true;

    if (quick === "learning") {
      return [
        "education",
        "editing",
        "photography-tips",
        "challenge"
      ].includes(record.category);
    }

    if (quick === "club") {
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

    if (quick === "events") {
      return record.item_type === "event" || record.category === "events";
    }

    if (quick === "travel") return record.category === "members-on-the-move";
    if (quick === "downloads") return record.item_type === "resource";

    return true;
  }

  function filteredRows(data, params) {
    const q = (params.get("q") || "").trim().toLowerCase();
    const category = params.get("category") || "";
    const series = params.get("series") || "";
    const level = params.get("level") || "";
    const issue = params.get("issue") || "";
    const type = params.get("type") || "";
    const quick = params.get("quick") || "";

    return data.records
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
          matchesQuick(record, quick)
        );
      })
      .sort(
        (a, b) =>
          (b.published || "").localeCompare(a.published || "") ||
          (a.title || "").localeCompare(b.title || "")
      );
  }

  function urlFor(page, params) {
    const next = new URLSearchParams(params);
    next.set("page", String(page));
    return `browse.html?${next.toString()}`;
  }

  function indexUrl(params) {
    const next = new URLSearchParams(params);
    next.delete("page");
    const query = next.toString();
    return query ? `index.html?${query}` : "index.html";
  }

  function render(data) {
    const params = new URLSearchParams(window.location.search);
    const rows = filteredRows(data, params);

    const totalPages = Math.max(1, Math.ceil(rows.length / PAGE_SIZE));
    let page = Number.parseInt(params.get("page") || "2", 10);

    if (!Number.isFinite(page)) page = 2;
    page = Math.max(2, Math.min(page, totalPages));

    const start = (page - 1) * PAGE_SIZE;
    const displayedRows = rows.slice(start, start + PAGE_SIZE);

    const firstResult = rows.length ? start + 1 : 0;
    const lastResult = Math.min(start + displayedRows.length, rows.length);

    $("browsePageTitle").textContent = `Page ${page} of ${totalPages}`;
    $("browseRange").textContent =
      `${firstResult}–${lastResult} of ${rows.length} indexed items`;
    $("browseCards").innerHTML = displayedRows.map(r => card(r, data)).join("");

    if (!rows.length || !displayedRows.length) {
      $("browseEmpty").style.display = "block";
    }

    const backUrl = indexUrl(params);
    document.querySelectorAll("[data-back-index]").forEach(link => {
      link.href = backUrl;
    });

    document.querySelectorAll("[data-prev-page]").forEach(link => {
      link.href = page <= 2 ? backUrl : urlFor(page - 1, params);
      link.textContent = page <= 2 ? "← Back to Page 1" : "← Previous 10";
    });

    document.querySelectorAll("[data-next-page]").forEach(link => {
      if (page >= totalPages) {
        link.style.display = "none";
      } else {
        link.href = urlFor(page + 1, params);
      }
    });
  }

  $("browseCards").addEventListener("click", event => {
    const button = event.target.closest("[data-open-url]");
    if (!button) return;

    navigateParent(button.dataset.openUrl);
  });

  fetch("library.json", { cache: "no-store" })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch(error => {
      console.error("Resource Library browse page load failed", error);
      $("browseCards").innerHTML = `
        <div class="load-error">
          The Resource Library data could not be loaded.
          Please return to the Resource Library and try again.
        </div>
      `;
    });
})();
