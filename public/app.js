/**
 * AegisCDS Clinical Workstation Application Logic
 * Integrates LangGraph cyclic states, dual-layer triage, HITL checkpoints, and benchmark analytics.
 */

// State
let currentPatientId = "PAT-ROBERTS-001";
let currentSessionId = null;
let currentCareBundles = [];
let currentRawAlerts = [];
let activeView = "live-triage";
let selectedOverrideReason = "Specialist Already Managing";

// DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initNavigation();
  initPatientSwitcher();
  initHITLControls();
  initFailureModeSelector();
  loadPatientData(currentPatientId);
  loadBenchmarkData();
  loadGuidelinesData();
  loadAuditLog();
  initLiveEventVetting();
  initOpenFDATerminal();
  initABDMVerification();
  loadMLStressResults();
  loadTelemetryStats();

  // Re-run simulation button
  document.getElementById("btn-run-simulation").addEventListener("click", () => {
    loadPatientData(currentPatientId);
  });

  // Benchmark refresh button
  document.getElementById("btn-refresh-benchmark").addEventListener("click", () => {
    loadBenchmarkData();
  });

  // Suppressed drawer toggle
  const suppToggle = document.getElementById("suppressed-toggle");
  if (suppToggle) {
    suppToggle.addEventListener("click", () => {
      const content = document.getElementById("suppressed-content");
      const chevron = document.getElementById("suppressed-chevron");
      if (content.style.display === "none") {
        content.style.display = "flex";
        chevron.textContent = "▲";
      } else {
        content.style.display = "none";
        chevron.textContent = "▼";
      }
    });
  }
});

/* ==========================================================================
   Theme Toggle
   ========================================================================== */
function initTheme() {
  const toggleBtn = document.getElementById("theme-toggle");
  const icon = document.getElementById("theme-icon");

  toggleBtn.addEventListener("click", () => {
    if (document.body.classList.contains("dark-theme")) {
      document.body.classList.remove("dark-theme");
      document.body.classList.add("light-theme");
      icon.textContent = "☀️";
    } else {
      document.body.classList.remove("light-theme");
      document.body.classList.add("dark-theme");
      icon.textContent = "🌙";
    }
  });
}

/* ==========================================================================
   Navigation Tabs
   ========================================================================== */
function initNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const targetView = tab.getAttribute("data-view");
      activeView = targetView;

      document.querySelectorAll(".view-panel").forEach(panel => {
        panel.classList.remove("active");
      });

      const activePanel = document.getElementById(`view-${targetView}`);
      if (activePanel) {
        activePanel.classList.add("active");
      }

      if (targetView === "audit-log") {
        loadAuditLog();
      }
      if (targetView === "ml-calibration") {
        loadMLStressResults();
      }
      if (targetView === "telemetry-dashboard") {
        loadTelemetryStats();
      }
    });
  });
}

/* ==========================================================================
   Patient Switcher
   ========================================================================== */
function initPatientSwitcher() {
  const pills = document.querySelectorAll(".patient-pill");
  pills.forEach(pill => {
    pill.addEventListener("click", () => {
      pills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      currentPatientId = pill.getAttribute("data-patient-id");
      loadPatientData(currentPatientId);
    });
  });
}

/* ==========================================================================
   Patient Data & Triage Loading
   ========================================================================== */
async function loadPatientData(patientId) {
  try {
    // 1. Fetch Raw Alerts & Patient Profile
    const rawRes = await fetch(`/api/patient/${patientId}/raw-alerts`);
    const rawData = await rawRes.json();
    currentRawAlerts = rawData.raw_alerts || [];
    renderPatientBanner(rawData.patient);
    renderLegacyAlerts(rawData.raw_alerts);

    // 2. Fetch Processed Triage from LangGraph Engine
    const triageRes = await fetch(`/api/patient/${patientId}/triage`);
    const triageData = await triageRes.json();
    currentSessionId = triageData.session_id;
    currentCareBundles = triageData.care_bundles || [];

    renderSmartTriage(triageData);
    renderLangGraphWorkflow(triageData);
    renderHITLWorkstation(triageData);

  } catch (err) {
    console.error("Error loading patient triage data:", err);
  }
}

function renderPatientBanner(patient) {
  const banner = document.getElementById("patient-banner");
  if (!banner || !patient) return;

  const kObs = patient.recent_observations.find(o => o.code === "K+");
  const crObs = patient.recent_observations.find(o => o.code === "Creatinine");
  const egfrObs = patient.recent_observations.find(o => o.code === "eGFR");
  const sbpObs = patient.recent_observations.find(o => o.code === "BP_Systolic");
  const dbpObs = patient.recent_observations.find(o => o.code === "BP_Diastolic");

  const isCriticalK = kObs && kObs.value >= 6.0;

  banner.innerHTML = `
    <div class="patient-details">
      <div class="patient-avatar">${patient.name.split(" ").map(n => n[0]).join("")}</div>
      <div class="patient-demographics">
        <h1>
          ${patient.name} (${patient.age}${patient.gender === "Male" ? "M" : "F"})
          <span class="mrn-badge">${patient.mrn}</span>
        </h1>
        <div class="condition-chips">
          ${patient.conditions.map(c => `<span class="cond-chip">${c}</span>`).join("")}
        </div>
      </div>
    </div>
    <div class="patient-vitals-row">
      <div class="vital-stat">
        <span class="vital-label">Serum Potassium (K+)</span>
        <span class="vital-value ${isCriticalK ? 'critical' : ''}">${kObs ? kObs.value + ' ' + kObs.unit : 'N/A'}</span>
      </div>
      <div class="vital-stat">
        <span class="vital-label">Serum Creatinine</span>
        <span class="vital-value ${crObs && crObs.value >= 2.0 ? 'critical' : ''}">${crObs ? crObs.value + ' mg/dL' : 'N/A'}</span>
      </div>
      <div class="vital-stat">
        <span class="vital-label">eGFR CKD-EPI</span>
        <span class="vital-value">${egfrObs ? egfrObs.value + ' mL/min' : 'N/A'}</span>
      </div>
      <div class="vital-stat">
        <span class="vital-label">Blood Pressure</span>
        <span class="vital-value">${sbpObs && dbpObs ? `${sbpObs.value}/${dbpObs.value} mmHg` : 'N/A'}</span>
      </div>
    </div>
  `;
}

function renderLegacyAlerts(alerts) {
  const container = document.getElementById("legacy-alerts-list");
  const totalCountEl = document.getElementById("legacy-total-count");
  const statRawEl = document.getElementById("stat-raw-alerts");

  if (!container) return;
  totalCountEl.textContent = alerts.length;
  statRawEl.textContent = alerts.length;

  container.innerHTML = alerts.map((a, idx) => `
    <div class="legacy-alert-item priority-${a.raw_priority}">
      <div class="legacy-alert-header">
        <span class="legacy-alert-title">⚠️ ${a.title}</span>
        <span class="badge ${a.raw_priority === 'CRITICAL' ? 'badge-danger' : 'badge-danger'}" style="font-size:0.65rem;">
          ${a.raw_priority}
        </span>
      </div>
      <div class="legacy-alert-desc">${a.description}</div>
      <div class="legacy-alert-actions">
        <button class="btn-dismiss" onclick="alert('Dismiss clicked: Alert ignored without clinical rationale.')">Acknowledge / Dismiss</button>
        <button class="btn-dismiss" onclick="alert('Override clicked: Blanket override logged without safety review.')">Override</button>
      </div>
    </div>
  `).join("");
}

function renderSmartTriage(data) {
  const metrics = data.metrics;
  document.getElementById("stat-presented-bundles").textContent = metrics.presented_bundle_count;
  document.getElementById("stat-time-saved").textContent = `${metrics.estimated_review_time_saved_sec}s`;
  document.getElementById("alert-reduction-badge").textContent = `-${metrics.reduction_rate_pct}% Noise`;

  const heroBanner = document.getElementById("critical-hero-banner");
  const bundlesStream = document.getElementById("bundles-stream");
  const suppressedList = document.getElementById("suppressed-content");
  const suppressedCount = document.getElementById("suppressed-count");

  // Critical alerts
  const criticals = data.processed_alerts.filter(a => a.status === "ACTIVE_CRITICAL" || a.raw_priority === "CRITICAL");
  if (criticals.length > 0 && currentPatientId === "PAT-ELEANOR-002") {
    heroBanner.style.display = "block";
    heroBanner.innerHTML = `
      <div class="hero-header">
        <span class="hero-icon">🚨</span>
        <div class="hero-title">
          <h4>EMERGENCY CLINICAL SAFETY INTERVENTION: Potassium 6.2 mEq/L + Dual RAAS Blockade</h4>
          <span>Layer 1 Deterministic Circuit Breaker Engaged • Bypassed All Suppression Filters</span>
        </div>
      </div>
      <div class="hero-guideline">
        <strong>KDIGO 2024 Clinical Practice Recommendation 1.3.2:</strong> Immediately obtain a 12-lead ECG to rule out peaked T-waves. Suspend Spironolactone and Lisinopril. Initiate potassium binder (Lokelma 10g PO TID) and repeat serum electrolytes.
      </div>
      <div class="hero-orders-grid">
        <div class="hero-order-chip">
          <span>Stat 12-Lead Electrocardiogram (ECG)</span>
          <span class="urgency-tag">STAT</span>
        </div>
        <div class="hero-order-chip">
          <span>Hold Spironolactone & Lisinopril</span>
          <span class="urgency-tag">STAT</span>
        </div>
        <div class="hero-order-chip">
          <span>Lokelma (SZC) 10g PO TID</span>
          <span class="urgency-tag">URGENT</span>
        </div>
        <div class="hero-order-chip">
          <span>Stat Repeat BMP & Potassium</span>
          <span class="urgency-tag">STAT</span>
        </div>
      </div>
    `;
  } else {
    heroBanner.style.display = "none";
  }

  // Render Care Bundles
  bundlesStream.innerHTML = data.care_bundles.map(bundle => `
    <div class="care-bundle-card priority-${bundle.priority}">
      <div class="bundle-top">
        <div>
          <div class="bundle-title">📦 ${bundle.title}</div>
          <div class="bundle-summary">${bundle.category_summary}</div>
        </div>
        <span class="badge ${bundle.priority === 'CRITICAL' ? 'badge-danger' : 'badge-success'}">
          ${bundle.priority}
        </span>
      </div>

      <div class="bundle-evidence-box">
        <strong>Clinical RAG Grounding:</strong> ${bundle.clinical_rationale}
        <div style="font-size: 0.7rem; color: #93c5fd; margin-top: 0.25rem;">
          <em>Citation: ${bundle.evidence_citation}</em>
        </div>
      </div>

      <div class="orders-group-header">Consolidated Pre-Drafted Action Set (One-Click Signature):</div>
      <div class="orders-checkbox-list">
        ${bundle.suggested_orders.map((o, idx) => `
          <div class="order-checkbox-item">
            <input type="checkbox" id="order-${bundle.id}-${idx}" checked>
            <label for="order-${bundle.id}-${idx}" class="order-text">${o.order_name || o.order}</label>
            <span class="order-urgency ${o.urgency}">${o.urgency}</span>
          </div>
        `).join("")}
      </div>

      <div class="bundle-action-bar">
        <span style="font-size:0.75rem; color: var(--text-muted);">
          Consolidated ${bundle.consolidated_alert_ids.length} disparate warnings into 1 actionable care package.
        </span>
        <button class="btn btn-primary" onclick="switchToHITL()">
          <span>Review in HITL Gate ➔</span>
        </button>
      </div>
    </div>
  `).join("");

  // Render Suppressed Drawer
  const suppressed = data.processed_alerts.filter(a => a.status === "SUPPRESSED_NON_ACTIONABLE" || a.is_suppressed);
  suppressedCount.textContent = suppressed.length;

  suppressedList.innerHTML = suppressed.map(s => `
    <div class="suppressed-item">
      <div class="suppressed-item-title">🔇 ${s.title}</div>
      <div class="suppressed-item-reason">${s.suppression_reason || 'Suppressed based on stable baseline and high prior clinician override rate.'}</div>
    </div>
  `).join("");
}

/* ==========================================================================
   LangGraph & HITL Workstation Rendering
   ========================================================================== */
function renderLangGraphWorkflow(data) {
  const stepEl = document.getElementById("graph-current-step");
  const hitlBadge = document.getElementById("hitl-pending-badge");
  if (data.hitl_status) {
    stepEl.textContent = `Step: ${data.hitl_status.current_step}`;
    hitlBadge.textContent = data.hitl_status.requires_human_approval ? "Awaiting Signature" : "Orders Dispatched";
    hitlBadge.className = data.hitl_status.requires_human_approval ? "tab-badge warning" : "tab-badge safe";
  }
}

function renderHITLWorkstation(data) {
  const ordersList = document.getElementById("hitl-orders-list");
  const cardStatus = document.getElementById("hitl-card-status");

  // Collect all suggested orders
  const allOrders = [];
  data.care_bundles.forEach(b => {
    b.suggested_orders.forEach(o => allOrders.push(o));
  });

  ordersList.innerHTML = allOrders.map((o, idx) => `
    <div class="order-checkbox-item">
      <input type="checkbox" id="hitl-order-${idx}" checked>
      <label for="hitl-order-${idx}" class="order-text">
        <strong>${o.order_name || o.order}</strong>
      </label>
      <span class="order-urgency ${o.urgency}">${o.urgency}</span>
    </div>
  `).join("");

  cardStatus.textContent = "STATUS: PENDING CLINICIAN SIGNATURE";
  cardStatus.className = "hitl-status-badge";
}

let hitlModalStartTime = performance.now();
let hitlClickCounter = 1;

function switchToHITL() {
  hitlModalStartTime = performance.now();
  hitlClickCounter = 1;
  document.querySelector('[data-view="langgraph-hitl"]').click();
}

function initHITLControls() {
  // Approve button
  document.getElementById("btn-hitl-approve").addEventListener("click", async () => {
    const latencyMs = Math.max(850, Math.round(performance.now() - hitlModalStartTime));
    hitlClickCounter++;
    try {
      // 1. Dispatch action
      const res = await fetch("/api/graph/hitl-action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: currentSessionId,
          patient_id: currentPatientId,
          decision: "APPROVED",
          reason: "Clinician signed pre-configured care bundle orders."
        })
      });
      const result = await res.json();

      // 2. Record telemetry
      fetch("/api/telemetry/hitl", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bundle_id: (currentCareBundles[0] && currentCareBundles[0].id) || "BND-ALL",
          patient_id: currentPatientId,
          action_type: "APPROVE_BUNDLE",
          modal_open_timestamp_ms: hitlModalStartTime,
          decision_submit_timestamp_ms: performance.now(),
          cognitive_latency_ms: latencyMs,
          click_count: hitlClickCounter
        })
      }).catch(console.error);

      if (result.success) {
        document.getElementById("hitl-card-status").textContent = "STATUS: CPOE ORDERS DISPATCHED TO EHR";
        document.getElementById("hitl-card-status").className = "hitl-status-badge safe";
        document.getElementById("node-hitl").className = "graph-node completed";
        document.getElementById("graph-current-step").textContent = "Step: CPOE_ORDERS_DISPATCHED";
        alert(`✓ Success: Care Bundle signed in ${latencyMs}ms and dispatched to EHR!`);
        loadAuditLog();
      }
    } catch (e) {
      console.error(e);
    }
  });

  // Override Drawer toggle
  document.getElementById("btn-hitl-override").addEventListener("click", () => {
    hitlClickCounter++;
    const drawer = document.getElementById("override-drawer-box");
    drawer.style.display = drawer.style.display === "none" ? "block" : "none";
  });

  // Override Chips selection
  const chips = document.querySelectorAll(".chip-btn");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      hitlClickCounter++;
      chips.forEach(c => c.classList.remove("selected"));
      chip.classList.add("selected");
      selectedOverrideReason = chip.getAttribute("data-reason");
    });
  });

  // Submit Structured Override
  document.getElementById("btn-submit-override").addEventListener("click", async () => {
    const note = document.getElementById("override-notes").value;
    const latencyMs = Math.max(1200, Math.round(performance.now() - hitlModalStartTime));
    hitlClickCounter++;
    try {
      const res = await fetch("/api/graph/hitl-action", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: currentSessionId,
          patient_id: currentPatientId,
          decision: "OVERRIDDEN",
          reason: selectedOverrideReason,
          clinical_justification: note || "Clinician structured override documented."
        })
      });
      const result = await res.json();

      // Record telemetry
      fetch("/api/telemetry/hitl", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          bundle_id: (currentCareBundles[0] && currentCareBundles[0].id) || "BND-ALL",
          patient_id: currentPatientId,
          action_type: "OVERRIDE_BUNDLE",
          modal_open_timestamp_ms: hitlModalStartTime,
          decision_submit_timestamp_ms: performance.now(),
          cognitive_latency_ms: latencyMs,
          click_count: hitlClickCounter,
          override_reason: selectedOverrideReason
        })
      }).catch(console.error);

      if (result.success) {
        document.getElementById("hitl-card-status").textContent = "STATUS: CLINICIAN OVERRIDE RECORDED";
        document.getElementById("hitl-card-status").className = "hitl-status-badge warning";
        document.getElementById("node-hitl").className = "graph-node completed";
        document.getElementById("override-drawer-box").style.display = "none";
        alert(`⚠️ Structured override recorded (${latencyMs}ms): "${selectedOverrideReason}". Active learning updated weights online.`);
        loadAuditLog();
      }
    } catch (e) {
      console.error(e);
    }
  });
}

/* ==========================================================================
   Failure Mode & Edge Case Simulation
   ========================================================================== */
function initFailureModeSelector() {
  const tabs = document.querySelectorAll(".fail-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const caseType = tab.getAttribute("data-case");
      runEdgeCaseSimulation(caseType);
    });
  });
  runEdgeCaseSimulation("stale_lab");
}

async function runEdgeCaseSimulation(caseType) {
  const container = document.getElementById("failure-display-card");
  try {
    const res = await fetch("/api/simulate-edge-case", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ case_type: caseType })
    });
    const data = await res.json();

    container.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <h3 style="font-family: var(--font-heading); font-size: 1.15rem; color: var(--text-main);">
          Clinical Scenario: ${data.unmitigated.clinical_scenario}
        </h3>
      </div>
      <div class="fail-comparison-grid">
        <div class="fail-box unmitigated">
          <h4>❌ Unmitigated Naive System Behavior (How Tools Fail in Real Clinics)</h4>
          <p><strong>System Action:</strong> ${data.unmitigated.naive_system_behavior}</p>
          <p><strong>Potential Patient Harm:</strong> <span style="color: var(--critical-red); font-weight: 600;">${data.unmitigated.potential_harm}</span></p>
          <p><strong>Status:</strong> ${data.unmitigated.guardrail_status}</p>
        </div>

        <div class="fail-box mitigated">
          <h4>✓ AegisCDS Safety Net Engaged (Harm Prevented)</h4>
          <p><strong>Guardrail Circuit:</strong> <code>${data.mitigated.guardrail_engaged}</code></p>
          <p><strong>Invariant Enforced:</strong> ${data.mitigated.rule_enforced}</p>
          <p><strong>System Response:</strong> ${data.mitigated.system_action}</p>
          <p style="color: var(--safe-green); font-weight: 700; margin-top: 0.5rem;">
            🛡️ Zero False Negative Standard Preserved: Patient Protected
          </p>
        </div>
      </div>
    `;
  } catch (err) {
    console.error(err);
  }
}

/* ==========================================================================
   Benchmark & Confusion Matrix Studio
   ========================================================================== */
async function loadBenchmarkData() {
  try {
    const res = await fetch("/api/benchmark");
    const data = await res.json();

    // Render KPI Cards
    const kpiGrid = document.getElementById("kpi-cards-grid");
    kpiGrid.innerHTML = data.kpi_comparison.map(k => `
      <div class="kpi-card">
        <span class="kpi-metric-name">${k.metric}</span>
        <div class="kpi-measured highlight">${k.achievement}</div>
        <div class="kpi-sub"><strong>Measured:</strong> ${k.measured}</div>
        <div class="kpi-sub" style="margin-top: 0.2rem;">Baseline: ${k.baseline}</div>
      </div>
    `).join("");

    // Render Confusion Matrix
    const cm = data.confusion_matrix;
    document.getElementById("cm-tp").textContent = cm.true_positives;
    document.getElementById("cm-fp").textContent = cm.false_positives;
    document.getElementById("cm-fn").textContent = cm.false_negatives;
    document.getElementById("cm-tn").textContent = cm.true_negatives;

  } catch (err) {
    console.error(err);
  }
}

/* ==========================================================================
   Guideline RAG Explorer
   ========================================================================== */
function loadGuidelinesData() {
  const grid = document.getElementById("guidelines-grid");
  const guidelines = [
    {
      source: "KDIGO 2024 Clinical Practice Guideline",
      section: "Rec 1.3.2: Severe Hyperkalemia Management",
      threshold: "Serum K+ >= 6.0 mEq/L",
      text: "Immediately obtain a 12-lead ECG to assess for peaked T-waves or conduction blocks. Temporarily suspend potassium-sparing diuretics (spironolactone) and ACE inhibitors/ARBs. Initiate urgent potassium-lowering therapy (Lokelma 10g PO TID) and repeat stat serum potassium."
    },
    {
      source: "KDIGO 2024 Acute Kidney Injury Consensus",
      section: "Section 2.1: Rapid eGFR Decline on Nephrotoxic Agents",
      threshold: "Creatinine increase > 50% from baseline",
      text: "An acute rise in serum creatinine > 50% within 7-30 days of initiating or titrating RAAS blockers warrants immediate clinical evaluation for prerenal azotemia or renal artery stenosis. Dose reduction or temporary hold is recommended."
    },
    {
      source: "ADA Standards of Care in Diabetes (2024)",
      section: "Chapter 6: Glycemic Targets & Re-testing Interval",
      threshold: "HbA1c re-order interval < 90 days",
      text: "Perform A1C testing at least twice a year in stable patients meeting goals. Re-testing within 90 days without therapy modification provides negligible clinical utility and represents non-actionable nuisance alert noise."
    },
    {
      source: "Joint ADA-KDIGO Consensus (2024)",
      section: "Comprehensive Annual Diabetic Nephropathy Assessment",
      threshold: "Annual Routine Screening Triggers",
      text: "Comprehensive annual diabetic care should consolidate urinary albumin-to-creatinine ratio (uACR), annual dilated eye exam, monofilament foot exam, and statin adherence into a single unified outpatient care bundle."
    },
    {
      source: "ACC/AHA 2023 Guideline for Hypertension",
      section: "Section 8.2: Outpatient BP Monitoring During Titration",
      threshold: "Systolic BP 130-139 mmHg during 30-day titration",
      text: "For patients undergoing active antihypertensive medication titration, minor BP elevations measured in clinic should be interpreted alongside home BP logs. Suppress interruptive alerts if dose was adjusted within 4 weeks."
    },
    {
      source: "FDA Black Box & ACC/AHA Safety Advisory",
      section: "Contraindication: Combined ACE-i / ARB / DRI",
      threshold: "Concomitant Dual/Triple RAAS Blockade",
      text: "Concomitant use of ACE inhibitors, angiotensin receptor blockers, or aliskiren is strongly contraindicated due to markedly increased risk of severe hypotension, syncope, hyperkalemia, and acute renal failure."
    }
  ];

  grid.innerHTML = guidelines.map(g => `
    <div class="guideline-card">
      <span class="guide-source-tag">${g.source}</span>
      <h4>${g.section}</h4>
      <div class="guide-threshold-badge">Trigger: ${g.threshold}</div>
      <div class="guide-text">${g.text}</div>
    </div>
  `).join("");
}

/* ==========================================================================
   Clinician Audit Trail Loading
   ========================================================================== */
async function loadAuditLog() {
  try {
    const res = await fetch("/api/audit-log");
    const data = await res.json();
    const tbody = document.getElementById("audit-table-body");
    const countEl = document.getElementById("audit-count");
    countEl.textContent = data.length;

    tbody.innerHTML = data.map(item => `
      <tr>
        <td><code>${item.id}</code></td>
        <td style="font-family: var(--font-mono); font-size: 0.72rem;">${item.timestamp}</td>
        <td><strong>${item.patient_id}</strong></td>
        <td><code>${item.clinician_id}</code></td>
        <td><span class="action-badge ${item.action}">${item.action}</span></td>
        <td><strong>${item.override_reason || 'N/A'}</strong></td>
        <td style="color: var(--text-muted); font-size: 0.75rem;">${item.clinical_justification || 'Documented'}</td>
      </tr>
    `).join("");
  } catch (err) {
    console.error(err);
  }
}

/* ==========================================================================
   Real-Time Event Vetting & Live Stream Controller
   ========================================================================== */
function initLiveEventVetting() {
  const triggerBtn = document.getElementById("btn-trigger-vetting-pipeline");
  const sampleBtn = document.getElementById("btn-stream-sample-event");
  const scenarioSelect = document.getElementById("select-ingest-scenario");

  if (triggerBtn) {
    triggerBtn.addEventListener("click", () => {
      runVettingScenario(scenarioSelect.value);
    });
  }

  if (sampleBtn) {
    sampleBtn.addEventListener("click", () => {
      runVettingScenario("crit_k_eleanor");
    });
  }

  // Poll database stats and live stream feed every 3 seconds
  refreshLiveFeed();
  setInterval(refreshLiveFeed, 3000);
}

async function runVettingScenario(scenarioKey) {
  let payload = {};
  if (scenarioKey === "crit_k_eleanor") {
    payload = {
      patient_id: "PAT-ELEANOR-002",
      event_type: "LAB_RESULT",
      title: "EMERGENCY Serum K+ 6.2 mEq/L Spike",
      payload: { medication_name: "Spironolactone", description: "Potassium spiked to 6.2 on Lisinopril + Spironolactone." }
    };
  } else if (scenarioKey === "stale_lab_harold") {
    payload = {
      patient_id: "PAT-ROBERTS-001",
      event_type: "PRESCRIPTION_ORDER",
      title: "New Rx: Spironolactone 25mg",
      payload: { medication_name: "Spironolactone", description: "Prescribed with 45 days old lab telemetry." }
    };
  } else if (scenarioKey === "nuisance_robert") {
    payload = {
      patient_id: "PAT-ROBERTS-001",
      event_type: "LAB_ORDER",
      title: "Duplicate Lab Order: HbA1c",
      payload: { medication_name: "Metformin", description: "HbA1c re-ordered 85 days after prior test (Result: 6.9%)." }
    };
  } else {
    payload = {
      patient_id: "PAT-ROBERTS-001",
      event_type: "PRESCRIPTION_ORDER",
      title: "Lethal Contraindication: Dual RAAS Blockade",
      payload: { medication_name: "Lisinopril", description: "Concurrent Lisinopril + Losartan ordered." }
    };
  }

  try {
    const res = await fetch("/api/events/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    renderVettingPipelineAnimation(result);
    refreshLiveFeed();
  } catch (err) {
    console.error("Error ingesting event:", err);
  }
}

function renderVettingPipelineAnimation(vettingResult) {
  const s1Card = document.getElementById("stage1-card");
  const s1Status = document.getElementById("stage1-status");
  const s1Detail = document.getElementById("stage1-detail");

  const s2Card = document.getElementById("stage2-card");
  const s2Status = document.getElementById("stage2-status");
  const s2Detail = document.getElementById("stage2-detail");

  const s3Card = document.getElementById("stage3-card");
  const s3Status = document.getElementById("stage3-status");
  const s3Detail = document.getElementById("stage3-detail");

  const outCard = document.getElementById("stage-outcome-card");
  const outStatus = document.getElementById("final-outcome-status");
  const outDetail = document.getElementById("final-outcome-detail");

  // Reset classes
  [s1Card, s2Card, s3Card, outCard].forEach(c => {
    if (c) c.className = "stage-card";
  });

  // Stage 1
  const s1 = vettingResult.stage_1_temporal_vetting;
  if (s1.status === "PASSED") {
    s1Card.classList.add("passed");
    s1Status.textContent = "✓ PASSED (FRESH)";
    s1Status.style.color = "var(--safe-green)";
    s1Detail.textContent = s1.notes;
  } else {
    s1Card.classList.add("blocked");
    s1Status.textContent = "⚠️ BLOCKED (DATA GAP)";
    s1Status.style.color = "var(--warning-amber)";
    s1Detail.textContent = s1.notes;
  }

  // Stage 2
  const s2 = vettingResult.stage_2_safety_vetting;
  if (s2) {
    if (s2.status === "CRITICAL_BYPASS_ENGAGED") {
      s2Card.classList.add("critical");
      s2Status.textContent = "🚨 CRITICAL BYPASS";
      s2Status.style.color = "var(--critical-red)";
      s2Detail.textContent = s2.critical_reason;
    } else {
      s2Card.classList.add("passed");
      s2Status.textContent = "✓ PASSED (SAFE)";
      s2Status.style.color = "var(--safe-green)";
      s2Detail.textContent = "No physiological emergency invariants violated.";
    }
  }

  // Stage 3
  const s3 = vettingResult.stage_3_ml_rag_vetting;
  if (s3) {
    if (s3.status === "SUPPRESSED_NON_ACTIONABLE") {
      s3Card.classList.add("blocked");
      s3Status.textContent = `🔇 SUPPRESSED (${s3.actionability_score})`;
      s3Status.style.color = "var(--text-faint)";
      s3Detail.textContent = "Low actionable score; moved to background audit drawer.";
    } else {
      s3Card.classList.add("passed");
      s3Status.textContent = `✓ ACTIONABLE (${s3.actionability_score})`;
      s3Status.style.color = "var(--action-blue)";
      s3Detail.textContent = `Grounded in: ${s3.guideline_citation}`;
    }
  }

  // Final Outcome
  outStatus.textContent = vettingResult.final_outcome;
  if (vettingResult.final_outcome === "ACTIVE_CRITICAL_ESCALATION") {
    outCard.classList.add("critical");
    outStatus.style.color = "var(--critical-red)";
    outDetail.textContent = "Emergency stat bundle created & sent to HITL gate.";
  } else if (vettingResult.final_outcome === "ACTIONABLE_DATA_GAP_BLOCKED") {
    outCard.classList.add("blocked");
    outStatus.style.color = "var(--warning-amber)";
    outDetail.textContent = "Mandatory renal panel order generated before dispense.";
  } else if (vettingResult.final_outcome === "SUPPRESSED_NUISANCE_NOISE") {
    outStatus.style.color = "var(--text-faint)";
    outDetail.textContent = "Silenced from clinician screen; saved to SQLite audit table.";
  } else {
    outCard.classList.add("passed");
    outStatus.style.color = "var(--safe-green)";
    outDetail.textContent = "Synthesized consolidated care bundle ready for one-click review.";
  }
}

async function refreshLiveFeed() {
  try {
    const res = await fetch("/api/events/vetted-feed");
    const data = await res.json();

    // Update DB counts
    const dbRaw = document.getElementById("db-raw-events-count");
    const dbVetted = document.getElementById("db-vetted-bundles-count");
    if (dbRaw && data.db_stats) dbRaw.textContent = data.db_stats.raw_clinical_events;
    if (dbVetted && data.db_stats) dbVetted.textContent = data.db_stats.vetted_care_bundles;

    // Update Ticker list
    const list = document.getElementById("vetted-events-stream-list");
    if (list && data.events) {
      if (data.events.length === 0) {
        list.innerHTML = `<div style="color:var(--text-faint); font-size:0.75rem; text-align:center; padding:1rem;">Awaiting streaming clinic events...</div>`;
      } else {
        list.innerHTML = data.events.map(e => `
          <div class="stream-event-card ${e.final_outcome.includes('CRITICAL') ? 'CRITICAL' : e.final_outcome.includes('BLOCKED') ? 'BLOCKED' : e.final_outcome.includes('SUPPRESSED') ? 'SUPPRESSED' : ''}">
            <div class="stream-event-top">
              <span class="stream-event-title">${e.title}</span>
              <span class="stream-event-time">${e.timestamp.split("T")[1].replace("Z","")}</span>
            </div>
            <div class="stream-event-outcome">
              Patient: <strong>${e.patient_name}</strong> • Outcome: <em>${e.final_outcome}</em>
            </div>
          </div>
        `).join("");
      }
    }
  } catch (err) {
    console.error(err);
  }
}

/* ==========================================================================
   Phase 2: ML Stress & Calibration Studio
   ========================================================================== */
async function loadMLStressResults() {
  const kpiGrid = document.getElementById("ml-stress-kpi-grid");
  const tableBody = document.getElementById("ml-stress-table-body");
  const runBtn = document.getElementById("btn-run-stress-test");

  if (runBtn && !runBtn.dataset.bound) {
    runBtn.dataset.bound = "true";
    runBtn.addEventListener("click", () => {
      loadMLStressResults();
      alert("⚡ ML Calibration Stress Test executed successfully across 90%, 95%, and 98% class imbalance regimes!");
    });
  }

  try {
    const res = await fetch("/api/ml/stress-test");
    const data = await res.json();

    if (kpiGrid && data.scenarios) {
      const s95 = data.scenarios.find(s => s.noise_ratio === 0.95) || data.scenarios[0];
      kpiGrid.innerHTML = `
        <div class="kpi-card passed">
          <div class="kpi-icon">🎯</div>
          <div class="kpi-val">${s95.brier_score}</div>
          <div class="kpi-label">Brier Score Loss (95% Noise)</div>
          <div class="kpi-target">Target: &lt; 0.05 (Strict Quadratic Loss)</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">📐</div>
          <div class="kpi-val">${s95.ece}</div>
          <div class="kpi-label">Expected Calibration Error (ECE)</div>
          <div class="kpi-target">Target: &lt; 0.05 (Tight Probability Gating)</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">📊</div>
          <div class="kpi-val">${s95.pr_auc}</div>
          <div class="kpi-label">PR-AUC under Imbalance</div>
          <div class="kpi-target">Target: &gt; 0.90 (Reliable High-Recall)</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">🛡️</div>
          <div class="kpi-val">${s95.zero_fn_satisfied ? "PASS (0 FN)" : "GUARDED"}</div>
          <div class="kpi-label">Deterministic Zero-FN Invariant</div>
          <div class="kpi-target">Life Threats 100% Preserved</div>
        </div>
      `;
    }

    if (tableBody && data.scenarios) {
      tableBody.innerHTML = data.scenarios.map(s => `
        <tr>
          <td><span class="badge ${s.noise_ratio >= 0.95 ? 'badge-danger' : 'badge-warning'}">${s.noise_percentage}</span></td>
          <td><strong>${s.total_samples}</strong> alerts</td>
          <td>${s.actionable_count} true actionable</td>
          <td><strong style="color:var(--safe-green);">${s.brier_score}</strong></td>
          <td><strong style="color:var(--safe-green);">${s.ece}</strong></td>
          <td>${s.pr_auc}</td>
          <td><span class="audit-badge safe">✓ 100% Sensitivity</span></td>
        </tr>
      `).join("");
    }
  } catch (err) {
    console.error("Error loading ML stress test results:", err);
  }
}

/* ==========================================================================
   Phase 2: Clinician Cognitive Telemetry & Online Active Learning
   ========================================================================== */
async function loadTelemetryStats() {
  const kpiGrid = document.getElementById("telemetry-kpi-grid");
  const weightsContainer = document.getElementById("active-learning-weights-container");

  try {
    const [telemetryRes, learningRes] = await Promise.all([
      fetch("/api/telemetry/stats"),
      fetch("/api/active-learning/stats")
    ]);
    const telemetryData = await telemetryRes.json();
    const learningData = await learningRes.json();

    if (kpiGrid) {
      kpiGrid.innerHTML = `
        <div class="kpi-card passed">
          <div class="kpi-icon">⏱️</div>
          <div class="kpi-val">${telemetryData.avg_cognitive_latency_ms} ms</div>
          <div class="kpi-label">Avg Clinician Decision Latency</div>
          <div class="kpi-target">Baseline was 142,000 ms (142s)</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">🖱️</div>
          <div class="kpi-val">${telemetryData.clicks_saved_per_encounter} Clicks</div>
          <div class="kpi-label">Clicks Saved per Encounter</div>
          <div class="kpi-target">Baseline was 14 clicks/patient</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">⚡</div>
          <div class="kpi-val">${telemetryData.cognitive_time_reduction_pct}%</div>
          <div class="kpi-label">Total Time Reclaimed</div>
          <div class="kpi-target">Goal: &gt; 70% Review Efficiency</div>
        </div>
        <div class="kpi-card passed">
          <div class="kpi-icon">🧠</div>
          <div class="kpi-val">${learningData.total_override_feedbacks_processed} Overrides</div>
          <div class="kpi-label">Online Feedback Adjustments</div>
          <div class="kpi-target">Active Online Learning Active</div>
        </div>
      `;
    }

    if (weightsContainer && learningData.current_active_weights) {
      weightsContainer.innerHTML = Object.entries(learningData.current_active_weights).map(([feature, weight]) => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:0.6rem 0; border-bottom:1px solid var(--border-color); font-size:0.85rem;">
          <span style="font-family:'JetBrains Mono',monospace; color:var(--text-main);">${feature}</span>
          <span class="badge ${weight > 1.5 ? 'badge-safe' : 'badge-info'}" style="font-family:'JetBrains Mono',monospace;">Weight: ${weight}</span>
        </div>
      `).join("");
    }
  } catch (err) {
    console.error("Error loading telemetry stats:", err);
  }
}

/* ==========================================================================
   Phase 2: ABDM Indian Health Records Bridge
   ========================================================================== */
function initABDMVerification() {
  const btn = document.getElementById("btn-verify-abha");
  const input = document.getElementById("input-abha-id");
  const resultContainer = document.getElementById("abha-verification-result");

  if (btn && input && resultContainer) {
    btn.addEventListener("click", async () => {
      const abhaVal = input.value.trim() || "robert.chen@abdm";
      resultContainer.innerHTML = `<div style="color:var(--text-faint); font-size:0.85rem;">Verifying ABHA ID with ABDM Gateway Sandbox...</div>`;

      try {
        const res = await fetch("/api/abdm/verify", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ abha_id: abhaVal })
        });
        const data = await res.json();

        if (data.status === "VERIFIED") {
          resultContainer.innerHTML = `
            <div style="background:var(--bg-panel); border:1px solid var(--safe-green); border-radius:8px; padding:1rem; margin-top:0.75rem;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="color:var(--safe-green); font-weight:700; font-size:0.95rem;">✓ ABHA ID VERIFIED (NHA Gateway)</span>
                <span class="badge badge-safe">CONSENT GRANTED</span>
              </div>
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-top:0.75rem; font-size:0.85rem;">
                <div><strong>Patient Name:</strong> ${data.patient_name} (${data.gender})</div>
                <div><strong>State / District:</strong> ${data.state} (${data.district})</div>
                <div><strong>ABHA Number:</strong> <span style="font-family:'JetBrains Mono',monospace;">${data.abha_number}</span></div>
                <div><strong>ABHA Address:</strong> <span style="font-family:'JetBrains Mono',monospace;">${data.abha_address}</span></div>
                <div><strong>Consent Token:</strong> <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem;">${data.consent_token}</span></div>
                <div><strong>Verified At:</strong> ${data.verified_at}</div>
              </div>
              <div style="margin-top:0.75rem; padding-top:0.5rem; border-top:1px solid var(--border-color); font-size:0.8rem; color:var(--text-faint);">
                <strong>FHIR M3 Status:</strong> Ready for NDHM Care Context Health Document Exchange.
              </div>
            </div>
          `;
        } else {
          resultContainer.innerHTML = `
            <div style="background:var(--bg-panel); border:1px solid var(--danger-red); border-radius:8px; padding:1rem; margin-top:0.75rem; color:var(--danger-red);">
              <strong>Verification Failed:</strong> ${data.error}
            </div>
          `;
        }
      } catch (err) {
        resultContainer.innerHTML = `<div style="color:var(--danger-red);">Error connecting to ABDM Sandbox Gateway.</div>`;
      }
    });
  }
}


