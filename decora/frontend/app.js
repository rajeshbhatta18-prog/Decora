(function(){
  "use strict";

  const COLOR_HEX = {
    "Neutral White": "#F5F3EF", "Sage Green": "#9CAF88",
    "Deep Charcoal": "#2B2B2B", "Brushed Gold": "#C6A15B",
    "Off White": "#F2EFE9", "Slate Blue": "#5B7C99",
    "Light Grey": "#C9CBCD", "Teal": "#2A9D8F",
    "Neutral White ": "#F5F3EF"
  };

  const STAGE_LABELS = {
    input: "Input Capture", layout: "Layout Engine", feedback: "Feedback Core",
    visualization: "2D Visualization", verified: "Verified", render3d: "3D Upscaling", complete: "Final Output"
  };
  // Maps a backend `stage` value to which stepper node should be marked active.
  const STAGE_TO_STEP = {
    layout: "layout", feedback: "feedback", visualization: "visualization",
    verified: "visualization", complete: "complete"
  };

  // Mirrors backend furniture_codes.py / database.py FURNITURE_SIZES --
  // each category the user can require, with the specific full-name
  // variants ("size/type") available for it. A category with a single
  // entry (e.g. dresser) still gets a select for consistency.
  const FURNITURE_CATALOG = [
    { category: "bed", label: "Bed", checked: true, options: [
      ["double_bed", "Double bed"], ["single_bed", "Single bed"], ["kingsize_bed", "King-size bed"],
    ]},
    { category: "wardrobe", label: "Wardrobe", checked: true, options: [
      ["wooden_wardrobe", "Wooden wardrobe"], ["fabric_wardrobe", "Fabric wardrobe"], ["hanger_wardrobe", "Hanger wardrobe"],
    ]},
    { category: "table", label: "Table", checked: true, options: [
      ["medium_table", "Medium table"], ["large_table", "Large table"],
    ]},
    { category: "chair", label: "Chair", checked: false, options: [
      ["plastic_chair", "Plastic chair"], ["metal_chair", "Metal chair"], ["adjustable_chair", "Adjustable chair"],
    ]},
    { category: "bookshelf", label: "Bookshelf", checked: false, options: [
      ["wooden_bookshelf", "Wooden bookshelf"], ["bamboo_bookshelf", "Bamboo bookshelf"],
    ]},
    { category: "bedside_table", label: "Bedside table", checked: false, options: [
      ["bedside_table", "Bedside table"],
    ]},
    { category: "dresser", label: "Dresser", checked: false, options: [
      ["dresser", "Dresser"],
    ]},
    { category: "mirror", label: "Mirror", checked: false, options: [
      ["mirror", "Mirror"],
    ]},
    { category: "dustbin", label: "Dustbin", checked: false, options: [
      ["dustbin", "Dustbin"],
    ]},
  ];

  function buildFurnitureGroup(){
    const wrap = $("furnitureGroup");
    wrap.innerHTML = FURNITURE_CATALOG.map(({ category, label, checked, options }) => {
      const cbId = "furn-" + category;
      const selId = "furn-size-" + category;
      const opts = options.map(([value, text], i) =>
        '<option value="' + value + '"' + (i === 0 ? " selected" : "") + '>' + text + '</option>'
      ).join("");
      return (
        '<div class="furnrow">' +
          '<input type="checkbox" id="' + cbId + '" ' + (checked ? "checked" : "") + ' />' +
          '<label class="furnname" for="' + cbId + '">' + label + '</label>' +
          '<select id="' + selId + '" ' + (checked ? "" : "disabled") + '>' + opts + '</select>' +
        '</div>'
      );
    }).join("");

    // Toggling the checkbox enables/disables its size dropdown.
    wrap.querySelectorAll(".furnrow").forEach((row) => {
      const cb = row.querySelector('input[type=checkbox]');
      const sel = row.querySelector('select');
      cb.addEventListener("change", () => { sel.disabled = !cb.checked; });
    });
  }

  let session = null;   // last known SessionState from the backend
  let revCount = 0;

  const $ = (id) => document.getElementById(id);

  function preventFormSubmission(event){
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
  }

  function apiBase(){
    return $("apiBase").value.trim().replace(/\/+$/, "");
  }

  function logRevision(method, path, status, ok){
    revCount += 1;
    $("revCount").textContent = String(revCount);
    const tr = document.createElement("tr");
    const time = new Date().toLocaleTimeString();
    tr.innerHTML =
      '<td class="mono">' + String(revCount).padStart(2, "0") + '</td>' +
      '<td class="mono">' + method + " " + path + '</td>' +
      '<td class="mono ' + (ok ? "status-ok" : "status-err") + '">' + status + '</td>' +
      '<td class="mono">' + time + '</td>';
    $("revBody").prepend(tr);
  }

  async function api(method, path, body){
    const url = apiBase() + path;
    let res, data;
    try {
      res = await fetch(url, {
        method,
        headers: body !== undefined ? { "Content-Type": "application/json" } : undefined,
        body: body !== undefined ? JSON.stringify(body) : undefined,
      });
    } catch (netErr) {
      logRevision(method, path, "network error", false);
      throw new Error("Could not reach " + url + ". Is the backend running and is the Server URL correct?");
    }
    try { data = await res.json(); } catch (_) { data = null; }
    logRevision(method, path, res.status, res.ok);
    if (!res.ok) {
      const detail = (data && data.detail) ? data.detail : ("HTTP " + res.status);
      throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    return data;
  }

  function showError(msg){
    $("errorBanner").innerHTML = msg ? ('<div class="banner">⚠ ' + escapeHtml(msg) + '</div>') : "";
  }

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, (c) => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;" }[c]));
  }

  function setStage(stage){
    $("stampStage").textContent = STAGE_LABELS[stage] || stage;
    const activeStep = STAGE_TO_STEP[stage] || "input";
    const order = ["input","layout","feedback","visualization","render3d","complete"];
    const activeIdx = order.indexOf(activeStep);
    document.querySelectorAll(".step").forEach((el) => {
      const idx = order.indexOf(el.dataset.stage);
      el.classList.remove("active","done");
      if (idx < activeIdx) el.classList.add("done");
      else if (idx === activeIdx) el.classList.add("active");
    });
  }

  function swatch(name){
    const hex = COLOR_HEX[name] || "#CCCCCC";
    return '<span class="swatch"><i style="background:' + hex + '"></i>' + escapeHtml(name) + '</span>';
  }

  function renderResults(layout){
    const rows = layout.furniture.map((f) =>
      '<tr><td>' + escapeHtml(f.name.replace(/_/g," ")) + '</td>' +
      '<td class="num">' + f.w + '\u2032 × ' + f.h + '\u2032</td>' +
      '<td class="num">(' + f.x + ', ' + f.y + ')</td></tr>'
    ).join("");

    const warnings = layout.warnings && layout.warnings.length
      ? '<div class="warnings"><p> Warnings </p><ul>' +
        layout.warnings.map((w) => '<li>' + escapeHtml(w) + '</li>').join("") + '</ul></div>'
      : "";

    const cost = (layout.estimated_cost != null)
      ? '<p class="cost">Estimated cost: <b>' + layout.estimated_cost.toLocaleString() + ' NPR</b></p>'
      : "";

    $("results").innerHTML =
      '<div class="scorebar">' +
        '<div class="score">' + layout.match_score.toFixed(3) + '<small>match score</small></div>' +
        '<div class="swatches">' + swatch(layout.wall_color) + swatch(layout.accent_color) + '</div>' +
      '</div>' +
      '<p class="note"><b>' + escapeHtml(layout.name) + '</b> — ' + escapeHtml(layout.style) + ' style</p>' +
      '<table class="schedule"><caption>Furniture schedule</caption>' +
      '<thead><tr><th>Mark</th><th>Size</th><th>Location (x, y)</th></tr></thead>' +
      '<tbody>' + rows + '</tbody></table>' +
      warnings + cost;
  }

  // A "north"/"south" wall runs along the room's length; an "east"/"west"
  // wall runs along the room's width. Openings are positioned along that run.
  function wallRunLength(wall, length, width){
    return (wall === "north" || wall === "south") ? length : width;
  }

  function round2(n){ return Math.round(n * 100) / 100; }

  // Door sits flush into whichever corner was picked.
  function cornerPosition(wall, corner, openingWidth, length, width){
    const run = wallRunLength(wall, length, width);
    if (corner === "right") return Math.max(0, round2(run - openingWidth));
    return 0;
  }

  // Windows are centered on their wall.
  function centeredPosition(wall, openingWidth, length, width){
    const run = wallRunLength(wall, length, width);
    return Math.max(0, round2((run - openingWidth) / 2));
  }

  // No width fields in the UI anymore — use sensible fixed openings.
  const DOOR_WIDTH = 3;
  const WINDOW_WIDTH = 4;

  function buildRoomInput(){
    const length = parseFloat($("length").value);
    const width = parseFloat($("width").value);

    const doors = [];
    if ($("doorOn").checked) {
      const wall = $("doorWall").value;
      doors.push({
        wall,
        position: cornerPosition(wall, $("doorCorner").value, DOOR_WIDTH, length, width),
        width: DOOR_WIDTH,
      });
    }

    const windows = [];
    if ($("windowOn").checked) {
      const count = parseInt($("windowCount").value, 10);
      const w1Wall = $("windowWall1").value;
      windows.push({ wall: w1Wall, position: centeredPosition(w1Wall, WINDOW_WIDTH, length, width), width: WINDOW_WIDTH });

      if (count === 2) {
        const w2Wall = $("windowWall2").value;
        windows.push({ wall: w2Wall, position: centeredPosition(w2Wall, WINDOW_WIDTH, length, width), width: WINDOW_WIDTH });
      }
    }

    // Each furniture row's checkbox gates its size/type <select>. If a
    // category is checked, send the SPECIFIC variant the user picked
    // (e.g. "double_bed") so the backend fixes that exact item per
    // pipeline instructions #2 ("if the user selects furniture then the
    // furniture needs should be fixed"). Categories left unchecked are
    // omitted entirely and filled in by the recommendation model.
    const required_furniture = Array.from(
      document.querySelectorAll('#furnitureGroup .furnrow')
    ).filter((row) => row.querySelector('input[type=checkbox]').checked)
     .map((row) => row.querySelector('select').value);

    return {
      length, width, doors, windows,
      style: $("style").value,
      budget: parseInt($("budget").value, 10),
      required_furniture,
      room_type: $("roomType").value,
    };
  }

  // Window 1 and Window 2 walls can't match — disable whichever option
  // the other select currently holds, and nudge off a value if it
  // becomes invalid. Only relevant once the second window row is shown.
  function syncWindowWallOptions(){
    const w1 = $("windowWall1"), w2 = $("windowWall2");
    if ($("windowRow2").hidden) {
      Array.from(w1.options).forEach((opt) => { opt.disabled = false; });
      return;
    }
    Array.from(w2.options).forEach((opt) => { opt.disabled = (opt.value === w1.value); });
    Array.from(w1.options).forEach((opt) => { opt.disabled = (opt.value === w2.value); });
    if (w2.value === w1.value) {
      const alt = Array.from(w2.options).find((o) => !o.disabled);
      if (alt) w2.value = alt.value;
    }
    if (w1.value === w2.value) {
      const alt = Array.from(w1.options).find((o) => !o.disabled);
      if (alt) w1.value = alt.value;
    }
  }

  $("windowCount").addEventListener("change", () => {
    const twoWindows = $("windowCount").value === "2";
    $("windowRow2").hidden = !twoWindows;
    $("windowWall1Label").textContent = twoWindows ? "Window 1 wall" : "Wall";
    syncWindowWallOptions();
  });
  $("windowWall1").addEventListener("change", syncWindowWallOptions);
  $("windowWall2").addEventListener("change", syncWindowWallOptions);
  syncWindowWallOptions();

  function resetDownstreamUI(){
    ["visBox","render3dBox","finalBox"].forEach((id) => $(id).hidden = true);
    $("floorplanWrap").hidden = true;
    $("verifyRow").hidden = true;
    $("verifyNote").textContent = "";
    $("render3dNote").textContent = "";
  }

  $("roomForm").addEventListener("submit", (e) => {
    preventFormSubmission(e);
  });

  // ---- Section 01 + 02: Input Capture -> Layout Engine ----
  $("getSuggestionBtn").addEventListener("click", async (e) => {
    e.preventDefault();
    e.stopPropagation();
    preventFormSubmission(e);
    showError("");
    const btn = e.currentTarget;
    btn.disabled = true;
    try {
      const room = buildRoomInput();
      if (room.width > room.length) {
        showError("Width (" + room.width + "ft) can't be greater than length (" + room.length + "ft). Width may equal length.");
        return;
      }
      session = await api("POST", "/api/design", room);
      renderResults(session.current_layout);
      setStage(session.stage);
      resetDownstreamUI();
      $("feedbackBox").hidden = false;
      $("fbStyle").value = room.style;
      $("fbBudget").value = room.budget;
      $("visBox").hidden = false;
      // Change Layout only does anything with two window walls.
      $("changeLayoutBtn").hidden = room.windows.length !== 2;
      $("changeLayoutNote").textContent = "";
    } catch (err) {
      showError(err.message);
    } finally {
      btn.disabled = false;
    }
  });

  // ---- Section 03: Feedback Core ----
  $("modifyBtn").addEventListener("click", async (e) => {
    preventFormSubmission(e);
    if (!session) return;
    showError("");
    try {
      session = await api("POST", "/api/design/" + session.session_id + "/modify", {
        style: $("fbStyle").value,
        budget: parseInt($("fbBudget").value, 10),
      });
      renderResults(session.current_layout);
      setStage(session.stage);
      resetDownstreamUI();
      $("visBox").hidden = false;
    } catch (err) {
      showError(err.message);
    }
  });

  // ---- Section 04: alternate layout (swap window-wall order) ----
  $("changeLayoutBtn").addEventListener("click", async (e) => {
    preventFormSubmission(e);
    if (!session) return;
    showError("");
    const btn = e.currentTarget;
    btn.disabled = true;
    try {
      session = await api("POST", "/api/design/" + session.session_id + "/change-layout", undefined);
      renderResults(session.current_layout);
      setStage(session.stage);
      $("changeLayoutNote").textContent = "Showing an alternate layout (mirrored window-wall order). Not happy yet? Try again or accept.";
      resetDownstreamUI();
      $("visBox").hidden = false;
      $("changeLayoutBtn").hidden = false;
    } catch (err) {
      showError(err.message);
    } finally {
      btn.disabled = false;
    }
  });

  // ---- Section 04: 2D Visualization & Verification ----
  $("acceptBtn").addEventListener("click", async (e) => {
    preventFormSubmission(e);
    if (!session) return;
    showError("");
    try {
      session = await api("POST", "/api/design/" + session.session_id + "/accept", undefined);
      setStage(session.stage);
      // floorplan_path is a server-side filesystem path, not a browser URL —
      // always fetch the image through the dedicated endpoint below.
      $("floorplanImg").src = apiBase() + "/api/design/" + session.session_id + "/floorplan?t=" + Date.now();
      $("floorplanWrap").hidden = false;
      $("verifyRow").hidden = false;
      $("verifyNote").textContent = "";
    } catch (err) {
      showError(err.message);
    }
  });

  async function verify(approved){
    if (!session) return;
    showError("");
    try {
      session = await api("POST", "/api/design/" + session.session_id + "/verify?approved=" + approved, undefined);
      setStage(session.stage);
      if (approved) {
        $("verifyNote").textContent = "Approved — proceed to 3D Upscaling below.";
        $("verifyNote").className = "note ok";
        $("render3dBox").hidden = false;
      } else {
        $("verifyNote").textContent = "Sent back to Feedback Core — adjust the form on the left and select Modify & Re-run.";
        $("verifyNote").className = "note";
        $("render3dBox").hidden = true;
      }
    } catch (err) {
      showError(err.message);
    }
  }
  $("approveBtn").addEventListener("click", () => verify(true));
  $("rejectBtn").addEventListener("click", () => verify(false));

  // ---- Section 05: 3D Upscaling ----
  $("render3dBtn").addEventListener("click", async (e) => {
    preventFormSubmission(e);
    console.log("3D upscaling will be available soon.");
    }
  );

  // ---- Dataset sanity check (Section 02 helper) ----
  async function checkSeed(){
    try {
      const info = await api("GET", "/api/layouts/seed-info", undefined);
      $("stampDataset").textContent = info.count.toLocaleString() + " layouts";
    } catch (err) {
      $("stampDataset").textContent = "unreachable";
    }
  }
  // Pipeline instructions: room breadth (width) may equal length, but
  // must not exceed it. Keep the width field's max in sync with length
  // and surface a note so the user sees the constraint before submitting.
  function syncWidthLimit(){
    const lengthVal = parseFloat($("length").value);
    const widthEl = $("width");
    if (!isNaN(lengthVal) && lengthVal > 0) {
      widthEl.max = String(lengthVal);
    }
    const widthVal = parseFloat(widthEl.value);
    if (!isNaN(lengthVal) && !isNaN(widthVal) && widthVal > lengthVal) {
      $("dimNote").textContent = "Width can't be greater than length (" + lengthVal + "ft).";
      $("dimNote").style.color = "var(--rust)";
    } else {
      $("dimNote").textContent = "";
    }
  }
  $("length").addEventListener("input", syncWidthLimit);
  $("width").addEventListener("input", syncWidthLimit);
  syncWidthLimit();

  buildFurnitureGroup();
  checkSeed();
  setStage("input");
})();
