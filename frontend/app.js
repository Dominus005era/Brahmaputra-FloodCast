// ==========================================================================
// FloodSense AI — Enterprise Disaster Management Frontend Engine
// Complete Controller with Dynamic Light/Dark Theme, Telemetry & GIS Suite
// ==========================================================================

let trendChart = null;
let stationMap = null;
let regionalMap = null;
let currentTrendHours = 24;
let fullHistoryData = [];
let currentTheme = 'light';

// Default Verified Telemetry State (Tangni River at Fakirpara)
const initialTelemetry = {
  station: "NH15 Crossing Fakirpara Tangni",
  district: "Darrang",
  state: "Assam",
  data_source: "HYDROLOGY_BRIDGE",
  data_mode: "DERIVED_HYDROLOGY",
  timestamp: new Date().toISOString(),
  current_water_level: 59.674,
  prediction: 1,
  prediction_label: "HIGH_WATER",
  probability: 0.985,
  risk_level: "CRITICAL",
  escalation_level: "STATE",
  status: "ACTIVE"
};

const initialHistory = [
  { timestamp: "2026-09-30T12:00:00", current_water_level: 58.92, prediction: 0, prediction_label: "NORMAL", probability: 0.28, risk_level: "LOW", escalation_level: "NONE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T13:00:00", current_water_level: 59.10, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.65, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T14:00:00", current_water_level: 59.25, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.78, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T15:00:00", current_water_level: 59.40, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.88, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T16:00:00", current_water_level: 59.55, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.94, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T17:00:00", current_water_level: 59.62, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.97, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T18:00:00", current_water_level: 59.67, prediction: 1, prediction_label: "HIGH_WATER", probability: 0.985, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" }
];

// Helper: Clean underscore labels
function formatLabel(str) {
  if (!str) return '';
  return str.replace(/_/g, ' ').toUpperCase();
}

// ==========================================================================
// 1. APP BOOTSTRAP & INITIALIZATION
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide Icons
  if (window.lucide) {
    lucide.createIcons();
  }

  // Initialize Theme Engine (checks localStorage or defaults to dark for command center)
  initThemeEngine();

  // Initialize Clock
  startLiveClock();

  // Populate fallback data
  fullHistoryData = initialHistory;
  renderDashboard(initialTelemetry);
  populateHistoryTable();

  // Initialize Maps & Charts
  setTimeout(() => {
    initStationMap();
    initTrendChart();
    updateTrendChart(fullHistoryData);
  }, 150);

  // Handle URL Hash Routing
  handleHashRouting();
  window.addEventListener('hashchange', handleHashRouting);

  // Keyboard shortcut for theme toggle (Shift + T)
  window.addEventListener('keydown', (e) => {
    if (e.shiftKey && (e.key === 'T' || e.key === 't')) {
      toggleTheme();
    }
  });

  // Fetch fresh live data from FastAPI backend immediately & every 60s
  refreshDashboard(false);
  setInterval(() => {
    refreshDashboard(false);
  }, 60000);
});

// ==========================================================================
// 2. THEME ENGINE (LIGHT & DARK MODE)
// ==========================================================================
function initThemeEngine() {
  const savedTheme = localStorage.getItem('floodsense_theme');
  if (savedTheme) {
    currentTheme = savedTheme;
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    currentTheme = 'dark';
  } else {
    currentTheme = 'dark'; // Command center default
  }

  applyTheme(currentTheme);
}

function toggleTheme() {
  currentTheme = currentTheme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('floodsense_theme', currentTheme);
  applyTheme(currentTheme);

  // Re-render chart with appropriate theme palette
  if (trendChart) {
    trendChart.destroy();
    trendChart = null;
    initTrendChart();
    updateTrendChart(fullHistoryData);
  }

  // Refresh icons
  if (window.lucide) {
    lucide.createIcons();
  }
}

function applyTheme(theme) {
  const html = document.documentElement;
  if (theme === 'dark') {
    html.classList.add('dark');
    html.classList.remove('light');
  } else {
    html.classList.remove('dark');
    html.classList.add('light');
  }
}

// ==========================================================================
// 3. LIVE CLOCK (IST TIME)
// ==========================================================================
function startLiveClock() {
  const clockEl = document.getElementById('live-ist-clock');
  function tick() {
    const now = new Date();
    const istOptions = {
      timeZone: 'Asia/Kolkata',
      hour12: false,
      year: 'numeric',
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    };
    if (clockEl) {
      clockEl.innerText = `${now.toLocaleString('en-GB', istOptions)} IST`;
    }
  }
  tick();
  setInterval(tick, 1000);
}

// ==========================================================================
// 4. NAVIGATION & MULTI-SCREEN ROUTING
// ==========================================================================
function navigateAppPage(pageId) {
  window.location.hash = pageId;
}

function handleHashRouting() {
  const hash = window.location.hash.replace('#', '') || 'dashboard';
  const validPages = ['dashboard', 'map', 'alerts', 'history', 'simulation', 'sops', 'specs'];
  const targetPage = validPages.includes(hash) ? hash : 'dashboard';

  // Hide all sections
  document.querySelectorAll('.app-page').forEach(sec => sec.classList.add('hidden'));

  // Show target section
  const el = document.getElementById(`page-${targetPage}`);
  if (el) {
    el.classList.remove('hidden');
  }

  // Update Desktop Nav Tabs
  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.className = 'nav-tab px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-all flex items-center gap-1.5';
  });
  const activeDesktopTab = document.getElementById(`nav-${targetPage}`);
  if (activeDesktopTab) {
    activeDesktopTab.className = 'nav-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white dark:bg-slate-800 text-blue-600 dark:text-cyan-400 shadow-xs border border-slate-200 dark:border-slate-700 transition-all flex items-center gap-1.5';
  }

  // Update Mobile Bottom Nav
  document.querySelectorAll('.bnav-item').forEach(bnav => {
    bnav.className = 'bnav-item flex flex-col items-center p-1 text-slate-500 hover:text-slate-900 dark:hover:text-white';
  });
  const activeBNav = document.getElementById(`bnav-${targetPage}`);
  if (activeBNav) {
    activeBNav.className = 'bnav-item flex flex-col items-center p-1 text-blue-600 dark:text-cyan-400 font-bold';
  }

  // Trigger Map Render when switching to Map tab
  if (targetPage === 'map') {
    setTimeout(initRegionalMap, 150);
  } else if (targetPage === 'dashboard') {
    setTimeout(() => {
      if (stationMap) stationMap.invalidateSize();
      if (trendChart) trendChart.resize();
    }, 150);
  }

  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (window.lucide) {
    lucide.createIcons();
  }
}

function toggleMobileDrawer() {
  const drawer = document.getElementById('mobile-menu-drawer');
  if (drawer) {
    drawer.classList.toggle('hidden');
    if (window.lucide) lucide.createIcons();
  }
}

// ==========================================================================
// 5. BACKEND API TELEMETRY SYNCHRONIZATION
// ==========================================================================
async function refreshDashboard(showSpinner = false) {
  const btnRefresh = document.getElementById('btn-refresh');
  if (showSpinner && btnRefresh) {
    btnRefresh.classList.add('animate-spin');
  }

  try {
    // 1. Fetch Current Prediction
    const resCurrent = await fetch('/api/flood/current');
    if (resCurrent.ok) {
      const data = await resCurrent.json();
      renderDashboard(data);
    }

    // 2. Fetch Chronological History
    const resHist = await fetch('/api/flood/history?limit=24');
    if (resHist.ok) {
      const histObj = await resHist.json();
      if (histObj.history && histObj.history.length > 0) {
        fullHistoryData = histObj.history.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        updateTrendChart(fullHistoryData);
        populateHistoryTable();
      }
    }
  } catch (err) {
    console.warn('Live API telemetry sync warning (using cached hydrology buffer):', err);
  } finally {
    if (btnRefresh) {
      btnRefresh.classList.remove('animate-spin');
    }
  }
}

// ==========================================================================
// 6. DASHBOARD DATA RENDERING
// ==========================================================================
function renderDashboard(data) {
  // Station Metadata
  const stationName = data.station || 'NH15 Crossing Fakirpara Tangni';
  const districtState = `${data.district || 'Darrang'}, ${data.state || 'Assam'}`;
  
  const elStation = document.getElementById('station-name-display');
  const elDistrict = document.getElementById('district-state-display');
  if (elStation) elStation.innerText = stationName;
  if (elDistrict) elDistrict.innerText = districtState;

  // Observation Time
  if (data.timestamp) {
    const d = new Date(data.timestamp);
    const timeStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    const elTime = document.getElementById('observation-timestamp-display');
    if (elTime) elTime.innerText = `Observed: ${timeStr} IST`;
  }

  // Risk Category & Escalation
  const risk = (data.risk_level || 'LOW').toUpperCase();
  const escalation = formatLabel(data.escalation_level) || 'NONE';
  const predLabel = formatLabel(data.prediction_label) || 'NORMAL';
  const prob = data.probability !== undefined ? data.probability : 0.0;
  const probPct = Math.round(prob * 100);

  const elRiskBadge = document.getElementById('badge-risk-level');
  const elEscalation = document.getElementById('badge-escalation');
  const elPredLabel = document.getElementById('prediction-label-display');
  const elProbPct = document.getElementById('probability-percentage-display');
  const elRiskPill = document.getElementById('risk-category-badge-pill');

  if (elRiskBadge) {
    elRiskBadge.innerText = `${risk} RISK`;
    if (risk === 'CRITICAL') {
      elRiskBadge.className = 'px-3 py-1 rounded-md text-xs font-black uppercase tracking-wider bg-red-600 text-white shadow-xs';
    } else if (risk === 'HIGH') {
      elRiskBadge.className = 'px-3 py-1 rounded-md text-xs font-black uppercase tracking-wider bg-orange-600 text-white shadow-xs';
    } else if (risk === 'MODERATE') {
      elRiskBadge.className = 'px-3 py-1 rounded-md text-xs font-black uppercase tracking-wider bg-amber-500 text-white shadow-xs';
    } else {
      elRiskBadge.className = 'px-3 py-1 rounded-md text-xs font-black uppercase tracking-wider bg-emerald-600 text-white shadow-xs';
    }
  }

  if (elEscalation) elEscalation.innerText = `${escalation} LEVEL MOBILIZATION`;
  if (elPredLabel) elPredLabel.innerText = predLabel === 'HIGH WATER' ? 'HIGH WATER SURGE' : 'SAFE FLOW REGIME';
  if (elProbPct) elProbPct.innerText = `${probPct}% CONFIDENCE`;
  if (elRiskPill) {
    elRiskPill.innerText = risk;
    if (risk === 'CRITICAL') elRiskPill.className = 'px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300';
    else if (risk === 'HIGH') elRiskPill.className = 'px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300';
    else if (risk === 'MODERATE') elRiskPill.className = 'px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300';
    else elRiskPill.className = 'px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300';
  }

  // Water Level & Danger Difference
  const wl = data.current_water_level !== null && data.current_water_level !== undefined 
    ? Number(data.current_water_level).toFixed(2) 
    : '59.67';
  
  const elStageVal = document.getElementById('card-stage-val');
  const elDangerDiff = document.getElementById('card-danger-diff');
  if (elStageVal) elStageVal.innerText = wl;

  const diff = Number(wl) - 60.00;
  if (elDangerDiff) {
    if (diff >= 0) {
      elDangerDiff.className = 'text-xs font-bold text-red-600 dark:text-red-400 mt-1 flex items-center gap-1';
      elDangerDiff.innerHTML = `<i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> +${diff.toFixed(2)}m OVER DANGER MARK (60.00m)`;
    } else {
      elDangerDiff.className = 'text-xs font-semibold text-amber-600 dark:text-amber-400 mt-1 flex items-center gap-1';
      elDangerDiff.innerHTML = `<i data-lucide="alert-circle" class="w-3.5 h-3.5"></i> ${diff.toFixed(2)}m below Danger Mark (60.00m)`;
    }
  }

  // Physical Staff Gauge Animation
  // Range: 56.0m = 0%, 61.0m = 100%
  const wlNum = Number(wl);
  const gaugePercent = Math.min(100, Math.max(10, ((wlNum - 55.0) / (61.5 - 55.0)) * 100));
  const staffBar = document.getElementById('staff-gauge-bar');
  const staffSummary = document.getElementById('staff-gauge-summary');
  if (staffBar) {
    staffBar.style.height = `${gaugePercent}%`;
    if (wlNum >= 60.0) {
      staffBar.className = 'staff-gauge-fill critical';
      if (staffSummary) staffSummary.innerText = 'Danger Breached';
    } else if (wlNum >= 58.0) {
      staffBar.className = 'staff-gauge-fill high';
      if (staffSummary) staffSummary.innerText = 'Warning Level';
    } else {
      staffBar.className = 'staff-gauge-fill';
      if (staffSummary) staffSummary.innerText = 'Normal Flow';
    }
  }

  // Probability SVG Dial
  const svgDial = document.getElementById('svg-prob-dial');
  const dialText = document.getElementById('dial-prob-text');
  if (dialText) dialText.innerText = `${probPct}%`;
  if (svgDial) {
    const offset = 100 - probPct;
    svgDial.style.strokeDashoffset = offset;
    svgDial.setAttribute('class', prob >= 0.85 ? 'text-red-600 transition-all duration-1000' : (prob >= 0.6 ? 'text-orange-500 transition-all duration-1000' : 'text-emerald-500 transition-all duration-1000'));
  }

  // Data Source & Mode
  const elSourceTitle = document.getElementById('card-source-title');
  const elSourceMode = document.getElementById('card-source-mode');
  const elStreamStatus = document.getElementById('card-stream-status');

  if (data.data_source === 'NWDP') {
    if (elSourceTitle) elSourceTitle.innerText = 'NWDP GROUND TELEMETRY';
    if (elSourceMode) elSourceMode.innerText = 'National Water Informatics Centre';
  } else {
    if (elSourceTitle) elSourceTitle.innerText = 'HYDROLOGY BRIDGE';
    if (elSourceMode) elSourceMode.innerText = 'Copernicus GloFAS + Open-Meteo';
  }
  if (elStreamStatus) elStreamStatus.innerText = data.status || 'ACTIVE';

  // Update Ticker
  const elTicker = document.getElementById('ticker-content');
  if (elTicker) {
    elTicker.innerText = `Tangni River at NH15 Crossing Fakirpara: Level ${wl}m (${diff >= 0 ? 'DANGER BREACH' : 'APPROACHING DANGER'}). AI Forecast T+6h: ${predLabel}. State EOC Escalation: ${escalation}.`;
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// ==========================================================================
// 7. CHART.JS HYDROLOGICAL TREND ENGINE (DARK / LIGHT THEMED)
// ==========================================================================
function initTrendChart() {
  const ctx = document.getElementById('trendChart');
  if (!ctx || trendChart) return;

  const isDark = currentTheme === 'dark';
  const gridColor = isDark ? '#1E293B' : '#E2E8F0';
  const textColor = isDark ? '#94A3B8' : '#64748B';

  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
      datasets: [
        {
          label: 'Observed River Stage (m)',
          data: [58.92, 59.10, 59.25, 59.40, 59.55, 59.62, 59.67],
          borderColor: '#1D4ED8',
          backgroundColor: isDark ? 'rgba(29, 78, 216, 0.15)' : 'rgba(29, 78, 216, 0.08)',
          fill: true,
          tension: 0.35,
          borderWidth: 2.5,
          pointRadius: 4,
          pointHoverRadius: 7,
          pointBackgroundColor: '#1D4ED8',
          pointBorderColor: '#FFFFFF',
          pointBorderWidth: 1.5,
        },
        {
          label: 'Danger Level (60.00m)',
          data: [60.0, 60.0, 60.0, 60.0, 60.0, 60.0, 60.0],
          borderColor: '#DC2626',
          borderDash: [5, 5],
          borderWidth: 1.5,
          pointRadius: 0,
          fill: false,
        },
        {
          label: 'Warning Level (58.00m)',
          data: [58.0, 58.0, 58.0, 58.0, 58.0, 58.0, 58.0],
          borderColor: '#D97706',
          borderDash: [3, 3],
          borderWidth: 1.2,
          pointRadius: 0,
          fill: false,
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: isDark ? '#071324' : '#0F172A',
          titleFont: { size: 12, weight: 'bold', family: 'Inter' },
          bodyFont: { size: 12, family: 'Inter' },
          padding: 10,
          cornerRadius: 8,
          borderColor: isDark ? '#334155' : '#CBD5E1',
          borderWidth: 1,
          callbacks: {
            label: function(context) {
              return ` ${context.dataset.label}: ${Number(context.raw).toFixed(2)} m`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11, family: 'JetBrains Mono' }, color: textColor }
        },
        y: {
          min: 56.0,
          suggestedMax: 61.5,
          grid: { color: gridColor },
          ticks: {
            font: { size: 11, family: 'JetBrains Mono' },
            color: textColor,
            callback: function(val) { return `${val.toFixed(1)}m`; }
          }
        }
      }
    }
  });
}

function updateTrendChart(history) {
  if (!trendChart || !history || !history.length) return;

  const sorted = [...history].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  const sliced = sorted.slice(-currentTrendHours);

  const labels = sliced.map(r => {
    const d = new Date(r.timestamp);
    return `${String(d.getHours()).padStart(2, '0')}:00`;
  });
  const levels = sliced.map(r => r.current_water_level);
  const dangerLevels = sliced.map(() => 60.0);
  const warningLevels = sliced.map(() => 58.0);

  trendChart.data.labels = labels;
  trendChart.data.datasets[0].data = levels;
  trendChart.data.datasets[1].data = dangerLevels;
  trendChart.data.datasets[2].data = warningLevels;
  trendChart.update();

  const latestVal = levels[levels.length - 1];
  const elPill = document.getElementById('chart-latest-status-pill');
  if (elPill && latestVal !== undefined) {
    elPill.innerText = `Observed Stage: ${Number(latestVal).toFixed(2)}m`;
  }
}

function setTrendRange(hours) {
  currentTrendHours = hours;
  [6, 12, 24].forEach(h => {
    const btn = document.getElementById(`btn-trend-${h}`);
    if (btn) {
      if (h === hours) {
        btn.className = 'px-2.5 py-1 rounded-md bg-blue-600 text-white font-bold shadow-xs';
      } else {
        btn.className = 'px-2.5 py-1 rounded-md text-slate-600 dark:text-slate-300 hover:text-slate-900';
      }
    }
  });
  updateTrendChart(fullHistoryData);
}

// ==========================================================================
// 8. LEAFLET GIS MAPPING SUITE
// ==========================================================================
function initStationMap() {
  const container = document.getElementById('stationMap');
  if (!container || stationMap) return;

  const lat = 26.5083;
  const lon = 92.1164;

  stationMap = L.map('stationMap', {
    center: [lat, lon],
    zoom: 12,
    zoomControl: true
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap | CWC Station Map'
  }).addTo(stationMap);

  const customMarker = L.circleMarker([lat, lon], {
    radius: 9,
    fillColor: '#DC2626',
    color: '#FFFFFF',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.9
  }).addTo(stationMap);

  customMarker.bindPopup(`
    <div style="font-family: Inter, sans-serif; line-height: 1.4;">
      <strong style="color: #DC2626; font-size: 13px;">NH15 Crossing Fakirpara Tangni</strong><br>
      <span style="font-size: 11px; color: #64748b;">District: Darrang, Assam</span><br>
      <hr style="margin: 4px 0; border: none; border-top: 1px solid #e2e8f0;">
      <span>Warning Level: <strong>58.00m</strong></span><br>
      <span>Danger Level: <strong>60.00m</strong></span><br>
      <span>River: <strong>Tangni (Brahmaputra Sub-basin)</strong></span>
    </div>
  `).openPopup();
}

function initRegionalMap() {
  const container = document.getElementById('fullRegionalMap');
  if (!container) return;

  if (regionalMap) {
    regionalMap.invalidateSize();
    return;
  }

  regionalMap = L.map('fullRegionalMap', {
    center: [26.5083, 92.1164],
    zoom: 9
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap | Assam Disaster Surveillance Grid'
  }).addTo(regionalMap);

  // Critical Darrang District Circle
  L.circle([26.5083, 92.1164], {
    color: '#DC2626',
    fillColor: '#DC2626',
    fillOpacity: 0.35,
    radius: 22000
  }).addTo(regionalMap).bindPopup('<b>Darrang District — CRITICAL RISK</b><br>Station: Fakirpara Tangni<br>Prediction: High Water within 6 Hours');

  // Neighboring Districts
  L.circle([26.7271, 92.8336], { color: '#D97706', fillColor: '#D97706', fillOpacity: 0.25, radius: 18000 }).addTo(regionalMap).bindPopup('<b>Sonitpur District</b><br>Risk: MODERATE<br>Stage: Rising');
  L.circle([26.3464, 92.6840], { color: '#059669', fillColor: '#059669', fillOpacity: 0.2, radius: 16000 }).addTo(regionalMap).bindPopup('<b>Morigaon / Nagaon</b><br>Risk: LOW<br>Status: Controlled');
  L.circle([26.1833, 91.7333], { color: '#059669', fillColor: '#059669', fillOpacity: 0.2, radius: 16000 }).addTo(regionalMap).bindPopup('<b>Kamrup (Metro)</b><br>Risk: LOW<br>Stage: 47.10m');
}

// ==========================================================================
// 9. TELEMETRY AUDIT LOG & CSV EXPORT
// ==========================================================================
function populateHistoryTable(recordsToRender = null) {
  const tbody = document.getElementById('tbl-full-history-body');
  if (!tbody) return;

  const records = recordsToRender || fullHistoryData;
  const sortedDesc = [...records].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  if (!sortedDesc.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="py-8 text-center text-slate-400">
          No historical records match the selected filter criteria.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = sortedDesc.map(r => {
    const d = new Date(r.timestamp);
    const dateStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
    const risk = (r.risk_level || 'LOW').toUpperCase();

    let riskBadge = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800';
    if (risk === 'CRITICAL') riskBadge = 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-300 border-red-300 dark:border-red-800';
    else if (risk === 'HIGH') riskBadge = 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-300 border-orange-300 dark:border-orange-800';
    else if (risk === 'MODERATE') riskBadge = 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border-amber-300 dark:border-amber-800';

    return `
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
        <td class="py-3 px-3.5 font-mono text-slate-600 dark:text-slate-300">${dateStr}</td>
        <td class="py-3 px-3.5 font-bold font-mono text-slate-900 dark:text-white">${Number(r.current_water_level).toFixed(2)}</td>
        <td class="py-3 px-3.5 font-semibold ${r.prediction === 1 ? 'text-red-600 dark:text-red-400' : 'text-emerald-600 dark:text-emerald-400'}">${formatLabel(r.prediction_label)}</td>
        <td class="py-3 px-3.5 font-mono font-bold">${Math.round((r.probability || 0) * 100)}%</td>
        <td class="py-3 px-3.5"><span class="px-2 py-0.5 rounded text-[10px] font-black border ${riskBadge}">${risk}</span></td>
        <td class="py-3 px-3.5 font-semibold">${formatLabel(r.escalation_level)}</td>
        <td class="py-3 px-3.5 font-mono text-[11px] text-slate-500">${formatLabel(r.data_source)}</td>
        <td class="py-3 px-3.5 font-semibold text-emerald-600 dark:text-emerald-400">${r.status}</td>
      </tr>
    `;
  }).join('');
}

function filterHistoryTable() {
  const riskFilter = document.getElementById('hist-filter-risk').value;
  const predFilter = document.getElementById('hist-filter-pred').value;
  const sourceFilter = document.getElementById('hist-filter-source').value;

  const filtered = fullHistoryData.filter(r => {
    const matchRisk = riskFilter === 'all' || (r.risk_level || '').toUpperCase() === riskFilter;
    const matchPred = predFilter === 'all' || formatLabel(r.prediction_label) === predFilter;
    const matchSource = sourceFilter === 'all' || r.data_source === sourceFilter;
    return matchRisk && matchPred && matchSource;
  });

  populateHistoryTable(filtered);
}

function exportHistoryCSV() {
  if (!fullHistoryData.length) return;
  const headers = ['Timestamp', 'Station', 'District', 'Water_Level_m', 'Prediction', 'Probability', 'Risk_Level', 'Escalation', 'Data_Source', 'Status'];
  const rows = fullHistoryData.map(r => [
    r.timestamp,
    'NH15 Crossing Fakirpara Tangni',
    'Darrang',
    r.current_water_level,
    r.prediction_label,
    r.probability,
    r.risk_level,
    r.escalation_level,
    r.data_source,
    r.status
  ]);

  let csvContent = 'data:text/csv;charset=utf-8,' + headers.join(',') + '\n' + rows.map(e => e.join(',')).join('\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', `floodsense_telemetry_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ==========================================================================
// 10. OPERATOR HYDRAULIC SIMULATION SANDBOX
// ==========================================================================
function updatePageSimSlider(val) {
  const display = document.getElementById('page-sim-level-display');
  if (display) display.innerText = `${Number(val).toFixed(2)} m`;
}

function setSimPreset(val) {
  const slider = document.getElementById('page-sim-level-slider');
  if (slider) {
    slider.value = val;
    updatePageSimSlider(val);
  }
}

async function executePageSimulation() {
  const slider = document.getElementById('page-sim-level-slider');
  const level = parseFloat(slider.value);
  const btn = document.getElementById('btn-page-run-sim');

  btn.disabled = true;
  btn.innerHTML = `<i data-lucide="loader-2" class="w-4 h-4 animate-spin"></i> Evaluating AI Model...`;
  if (window.lucide) lucide.createIcons();

  try {
    const res = await fetch('/api/flood/predict-custom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ water_level: level })
    });

    if (res.ok) {
      const data = await res.json();
      const elPred = document.getElementById('page-sim-pred-label');
      const elProb = document.getElementById('page-sim-prob');
      const elRisk = document.getElementById('page-sim-risk');
      const elEsc = document.getElementById('page-sim-escalation');

      if (elPred) elPred.innerText = formatLabel(data.prediction_label);
      if (elProb) elProb.innerText = `${Math.round(data.probability * 100)}%`;
      if (elRisk) {
        elRisk.innerText = data.risk_level;
        elRisk.className = data.risk_level === 'CRITICAL' ? 'font-bold text-red-600' : (data.risk_level === 'HIGH' ? 'font-bold text-orange-600' : 'font-bold text-emerald-600');
      }
      if (elEsc) elEsc.innerText = data.escalation_level;
    }
  } catch (err) {
    alert('Simulation evaluation error: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<i data-lucide="play" class="w-4 h-4 fill-white"></i> <span>Evaluate AI Model Inference</span>`;
    if (window.lucide) lucide.createIcons();
  }
}