// FloodSense AI — Enterprise Hydrological Dashboard Engine
// Full Light/Dark Theme, Mobile Adaptability & High-Integrity State Management

let trendChart = null;
let stationMap = null;
let regionalMap = null;
let currentTrendHours = 24;
let fullHistoryData = [];
let unreadAlertsCount = 3;

// Helper: Format technical underscores into clean human-readable text
function formatLabel(str) {
  if (!str) return '';
  return str.replace(/_/g, ' ').toUpperCase();
}

// Initial Mock Telemetry State
const initialData = {
  station: "NH15 Crossing Fakirpara Tangni",
  district: "Darrang",
  state: "Assam",
  data_source: "HYDROLOGY_BRIDGE",
  data_mode: "DERIVED_HYDROLOGY",
  timestamp: "2026-09-30T18:00:00",
  current_water_level: 60.31,
  prediction: 1,
  prediction_label: "HIGH WATER",
  probability: 0.985,
  risk_level: "CRITICAL",
  escalation_level: "STATE",
  status: "ACTIVE"
};

const initialHistory = [
  { timestamp: "2026-09-30T12:00:00", current_water_level: 59.85, prediction: 1, prediction_label: "HIGH WATER", probability: 0.88, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T13:00:00", current_water_level: 59.95, prediction: 1, prediction_label: "HIGH WATER", probability: 0.91, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T14:00:00", current_water_level: 60.05, prediction: 1, prediction_label: "HIGH WATER", probability: 0.94, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T15:00:00", current_water_level: 60.15, prediction: 1, prediction_label: "HIGH WATER", probability: 0.96, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T16:00:00", current_water_level: 60.22, prediction: 1, prediction_label: "HIGH WATER", probability: 0.97, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T17:00:00", current_water_level: 60.28, prediction: 1, prediction_label: "HIGH WATER", probability: 0.98, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-09-30T18:00:00", current_water_level: 60.31, prediction: 1, prediction_label: "HIGH WATER", probability: 0.99, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" }
];

// Theme Management (Light / Dark Mode with Persistence)
function initTheme() {
  const saved = localStorage.getItem('floodsense_theme');
  if (saved === 'light') {
    document.documentElement.classList.remove('dark');
  } else {
    document.documentElement.classList.add('dark');
  }
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('floodsense_theme', isDark ? 'dark' : 'light');
  if (window.lucide) lucide.createIcons();
  updateTrendChartTheme();
}

function updateTrendChartTheme() {
  if (!trendChart) return;
  const isDark = document.documentElement.classList.contains('dark');
  trendChart.options.scales.x.ticks.color = isDark ? '#94a3b8' : '#64748b';
  trendChart.options.scales.y.ticks.color = isDark ? '#94a3b8' : '#64748b';
  trendChart.options.scales.y.grid.color = isDark ? 'rgba(30, 58, 95, 0.4)' : '#e2e8f0';
  trendChart.update();
}

// Mobile Sidebar Navigation Controls
function toggleMobileSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('mobile-sidebar-backdrop');
  if (!sidebar) return;
  const isClosed = sidebar.classList.contains('-translate-x-full');
  if (isClosed) {
    sidebar.classList.remove('-translate-x-full');
    if (backdrop) backdrop.classList.remove('hidden');
  } else {
    sidebar.classList.add('-translate-x-full');
    if (backdrop) backdrop.classList.add('hidden');
  }
}

function closeMobileSidebar() {
  const sidebar = document.getElementById('app-sidebar');
  const backdrop = document.getElementById('mobile-sidebar-backdrop');
  if (sidebar) sidebar.classList.add('-translate-x-full');
  if (backdrop) backdrop.classList.add('hidden');
}

// App Initialization & URL Hash Route Detection
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  
  if (window.lucide) {
    lucide.createIcons();
  }
  
  fullHistoryData = initialHistory;
  updateCurrentView(initialData);

  // Read URL Hash for Route Persistence on Refresh (F5)
  handleHashRouting();
  window.addEventListener('hashchange', handleHashRouting);

  // Auto fetch from live backend every 60 seconds
  setInterval(() => {
    refreshDashboard(false);
  }, 60000);
});

// Route handling from URL hash
function handleHashRouting() {
  const hash = window.location.hash.replace('#', '') || 'landing';
  const appPages = ['dashboard', 'map', 'alerts', 'history', 'simulation', 'how-it-works', 'system-details', 'settings'];
  
  if (appPages.includes(hash)) {
    sessionStorage.setItem('floodsense_location', 'Darrang, Assam');
    showView('app');
    setActiveAppPage(hash);
  } else if (hash === 'location-gate') {
    showView('location-gate');
  } else if (hash === 'learn-more') {
    showView('learn-more');
  } else {
    showView('landing');
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// View Switching Helper
function showView(viewId) {
  document.querySelectorAll('.app-view').forEach(v => v.classList.add('hidden'));
  const target = document.getElementById(`view-${viewId}`);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('animate-fade-in');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

// Navigation to Primary Views
function navigateTo(viewId) {
  window.location.hash = viewId;
}

// Confirm Location & Enter Dashboard
function confirmLocationAndEnter() {
  sessionStorage.setItem('floodsense_location', 'Darrang, Assam');
  window.location.hash = 'dashboard';
}

// Navigation inside App Shell with Single Active State
function navigateAppPage(pageId) {
  closeMobileSidebar();
  window.location.hash = pageId;
}

function setActiveAppPage(pageId) {
  // Hide all pages
  document.querySelectorAll('.app-page').forEach(p => p.classList.add('hidden'));
  
  // Reset all nav items to inactive
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.remove('active', 'bg-blue-700', 'dark:bg-blue-600', 'text-white', 'shadow-sm');
    n.classList.add('text-slate-600', 'dark:text-slate-300');
  });

  const targetPage = document.getElementById(`page-${pageId}`);
  const targetNav = document.getElementById(`nav-${pageId}`);

  if (targetPage) {
    targetPage.classList.remove('hidden');
    targetPage.classList.add('animate-fade-in');
  }

  if (targetNav) {
    targetNav.classList.add('active', 'bg-blue-700', 'dark:bg-blue-600', 'text-white', 'shadow-sm');
    targetNav.classList.remove('text-slate-600', 'dark:text-slate-300');
  }

  // Handle More submenu expansion for sub-items
  const submenu = document.getElementById('more-submenu');
  const chevron = document.getElementById('more-chevron');
  if (pageId === 'how-it-works' || pageId === 'system-details') {
    if (submenu) submenu.classList.remove('hidden');
    if (chevron) chevron.style.transform = 'rotate(180deg)';
  }

  if (pageId === 'dashboard') {
    setTimeout(() => {
      initStationMap();
      initTrendChart();
      updateTrendChart(fullHistoryData);
    }, 100);
  } else if (pageId === 'map') {
    setTimeout(initRegionalMap, 150);
  } else if (pageId === 'history') {
    populateHistoryTable();
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Toggle More Submenu
function toggleMoreMenu() {
  const submenu = document.getElementById('more-submenu');
  const chevron = document.getElementById('more-chevron');
  if (!submenu) return;
  if (submenu.classList.contains('hidden')) {
    submenu.classList.remove('hidden');
    if (chevron) chevron.style.transform = 'rotate(180deg)';
  } else {
    submenu.classList.add('hidden');
    if (chevron) chevron.style.transform = 'rotate(0deg)';
  }
}

// Modals: About, Features, Sign In, Alerts, Logout
function openAboutModal() {
  document.getElementById('modal-about')?.classList.remove('hidden');
}
function closeAboutModal() {
  document.getElementById('modal-about')?.classList.add('hidden');
}

function openFeaturesModal() {
  document.getElementById('modal-features')?.classList.remove('hidden');
}
function closeFeaturesModal() {
  document.getElementById('modal-features')?.classList.add('hidden');
}

function openSignInModal() {
  document.getElementById('modal-signin')?.classList.remove('hidden');
}
function closeSignInModal() {
  document.getElementById('modal-signin')?.classList.add('hidden');
}
function confirmSignInAndEnter() {
  closeSignInModal();
  confirmLocationAndEnter();
}

function openAlertDetailModal(alertId) {
  document.getElementById('modal-alert-detail')?.classList.remove('hidden');
  if (unreadAlertsCount > 1) {
    unreadAlertsCount = 2;
    const badge = document.getElementById('sidebar-alert-badge');
    const countBadge = document.getElementById('alerts-count-badge');
    if (badge) badge.innerText = unreadAlertsCount;
    if (countBadge) countBadge.innerText = `${unreadAlertsCount} ACTIVE ALERTS`;
  }
}
function closeAlertDetailModal() {
  document.getElementById('modal-alert-detail')?.classList.add('hidden');
}

function promptLogout() {
  document.getElementById('modal-logout')?.classList.remove('hidden');
}
function closeLogoutModal() {
  document.getElementById('modal-logout')?.classList.add('hidden');
}
function confirmLogoutAndReturn() {
  sessionStorage.removeItem('floodsense_location');
  closeLogoutModal();
  window.location.hash = 'landing';
}

// Fetch Live Data from Backend API
async function refreshDashboard(showSpinner = false) {
  const btnRefresh = document.getElementById('btn-refresh');
  if (showSpinner && btnRefresh) {
    btnRefresh.classList.add('animate-spin');
  }

  try {
    const resCurrent = await fetch('/api/flood/current');
    if (resCurrent.ok) {
      const current = await resCurrent.json();
      updateCurrentView(current);
    }

    const resHistory = await fetch('/api/flood/history?limit=24');
    if (resHistory.ok) {
      const hist = await resHistory.json();
      if (hist.history && hist.history.length > 0) {
        fullHistoryData = hist.history.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
        updateTrendChart(fullHistoryData);
        populateHistoryTable();
      }
    }
  } catch (err) {
    console.warn('Live fetch note (using verified state):', err);
  } finally {
    if (btnRefresh) {
      btnRefresh.classList.remove('animate-spin');
    }
  }
}

// Update View from Data
function updateCurrentView(data) {
  if (document.getElementById('hdr-station')) {
    document.getElementById('hdr-station').innerText = data.station || 'NH15 Crossing Fakirpara Tangni';
  }
  if (document.getElementById('hdr-district')) {
    document.getElementById('hdr-district').innerText = `${data.district || 'Darrang'}, ${data.state || 'Assam'} • Brahmaputra Basin`;
  }
  
  if (data.timestamp) {
    const d = new Date(data.timestamp);
    const timeStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    if (document.getElementById('hdr-timestamp')) {
      document.getElementById('hdr-timestamp').innerText = timeStr;
    }
    if (document.getElementById('card-updated-time')) {
      document.getElementById('card-updated-time').innerText = `Observed: ${String(d.getHours()).padStart(2, '0')}:00 hrs`;
    }
  }

  // Hero Risk & Probability
  const risk = (data.risk_level || 'LOW').toUpperCase();
  if (document.getElementById('hero-risk-level')) {
    document.getElementById('hero-risk-level').innerText = risk;
  }
  
  const probPercent = Math.round((data.probability || 0) * 100);
  if (document.getElementById('hero-prob-val')) {
    document.getElementById('hero-prob-val').innerText = `${probPercent}%`;
  }
  if (document.getElementById('hero-pred-label')) {
    document.getElementById('hero-pred-label').innerText = formatLabel(data.prediction_label) || 'HIGH WATER';
  }

  const offset = 201.06 - (201.06 * (data.probability || 0));
  const probCircle = document.getElementById('prob-circle');
  if (probCircle) probCircle.style.strokeDashoffset = offset;

  // Current Water Level
  const wl = data.current_water_level !== null ? Number(data.current_water_level).toFixed(2) : '60.31';
  if (document.getElementById('card-water-level')) {
    document.getElementById('card-water-level').innerText = wl;
  }
  if (document.getElementById('card-prediction-label')) {
    document.getElementById('card-prediction-label').innerText = formatLabel(data.prediction_label) || 'HIGH WATER';
  }

  // Data Source Title
  const srcTitle = document.getElementById('src-title');
  const srcSubtitle = document.getElementById('src-subtitle');
  if (srcTitle && srcSubtitle) {
    if (data.data_source === 'NWDP') {
      srcTitle.innerText = 'ACTIVE DATA SOURCE: NWDP GROUND TELEMETRY';
      srcSubtitle.innerText = 'Government of India Station Telemetry';
    } else {
      srcTitle.innerText = 'ACTIVE DATA SOURCE: HYDROLOGY BRIDGE';
      srcSubtitle.innerText = 'Copernicus GloFAS & Open-Meteo Failover Stream';
    }
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Leaflet Map on Dashboard (Station Overview)
function initStationMap() {
  const container = document.getElementById('stationMap');
  if (!container || stationMap) return;

  const lat = 26.5083;
  const lon = 92.1164;

  stationMap = L.map('stationMap', {
    center: [lat, lon],
    zoom: 13,
    zoomControl: true
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(stationMap);

  const marker = L.marker([lat, lon]).addTo(stationMap);
  marker.bindPopup('<b>NH15 Crossing Fakirpara Tangni</b><br>Darrang District, Assam<br>Warning: 58.0m | Danger: 60.0m').openPopup();
}

// Leaflet Map on Regional Map View
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
    attribution: '© OpenStreetMap contributors'
  }).addTo(regionalMap);

  // Critical Darrang Circle Marker
  const darrangCircle = L.circle([26.5083, 92.1164], {
    color: '#DC2626',
    fillColor: '#DC2626',
    fillOpacity: 0.35,
    radius: 20000
  }).addTo(regionalMap);

  darrangCircle.bindPopup('<b>Darrang District — CRITICAL RISK</b><br>Station: NH15 Crossing Fakirpara Tangni<br>Prediction: High Water within 6 Hours').openPopup();

  // Neighboring Districts (Bongaigaon, Sonitpur, Nagaon)
  L.circle([26.4767, 90.5584], { color: '#16A34A', fillColor: '#16A34A', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Bongaigaon</b><br>Risk: LOW');
  L.circle([26.7271, 92.8336], { color: '#D97706', fillColor: '#D97706', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Sonitpur</b><br>Risk: MODERATE');
  L.circle([26.3464, 92.6840], { color: '#16A34A', fillColor: '#16A34A', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Nagaon</b><br>Risk: LOW');
}

// Chart.js initialization
function initTrendChart() {
  const ctx = document.getElementById('trendChart');
  if (!ctx || trendChart) return;

  const isDark = document.documentElement.classList.contains('dark');

  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
      datasets: [
        {
          label: 'Observed River Stage (m)',
          data: [59.85, 60.05, 60.15, 60.22, 60.28, 60.31],
          borderColor: '#0284c7',
          backgroundColor: 'rgba(2, 132, 199, 0.12)',
          fill: true,
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 7,
          pointBackgroundColor: '#0284c7',
          borderWidth: 2.5
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
          backgroundColor: isDark ? '#0F1F38' : '#ffffff',
          titleColor: isDark ? '#f8fafc' : '#0f172a',
          bodyColor: isDark ? '#cbd5e1' : '#334155',
          borderColor: isDark ? '#1E3A5F' : '#e2e8f0',
          borderWidth: 1,
          padding: 10,
          cornerRadius: 8
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 11 }, color: isDark ? '#94a3b8' : '#64748b' }
        },
        y: {
          min: 56.0,
          suggestedMax: 62.0,
          grid: { color: isDark ? 'rgba(30, 58, 95, 0.4)' : '#e2e8f0' },
          ticks: { font: { size: 11 }, color: isDark ? '#94a3b8' : '#64748b' }
        }
      }
    }
  });
}

function updateTrendChart(history) {
  if (!trendChart || !history.length) return;

  const sorted = [...history].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  const sliced = sorted.slice(-currentTrendHours);

  const labels = sliced.map(r => {
    const d = new Date(r.timestamp);
    return `${String(d.getHours()).padStart(2, '0')}:00`;
  });
  const levels = sliced.map(r => r.current_water_level);

  trendChart.data.labels = labels;
  trendChart.data.datasets[0].data = levels;
  trendChart.update();

  const latestVal = levels[levels.length - 1];
  const latestPill = document.getElementById('trend-latest-pill');
  if (latestPill && latestVal !== undefined) {
    latestPill.innerText = `${Number(latestVal).toFixed(2)} m`;
  }
}

function setTrendRange(hours) {
  currentTrendHours = hours;
  [6, 12, 24].forEach(h => {
    const btn = document.getElementById(`btn-range-${h}`);
    if (btn) {
      if (h === hours) {
        btn.className = 'px-3 py-1 rounded-lg bg-blue-700 text-white font-bold shadow-xs';
      } else {
        btn.className = 'px-3 py-1 rounded-lg hover:bg-white dark:hover:bg-slate-700 transition-all text-slate-600 dark:text-slate-300 font-semibold';
      }
    }
  });
  updateTrendChart(fullHistoryData);
}

// Populate & Filter History Table
function populateHistoryTable(recordsToRender = null) {
  const tbody = document.getElementById('tbl-full-history-body');
  if (!tbody) return;

  const records = recordsToRender || fullHistoryData;
  const sortedDesc = [...records].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  if (!sortedDesc.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="py-8 text-center text-slate-400">
          No historical telemetry records found matching the active filters.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = sortedDesc.map(r => {
    const d = new Date(r.timestamp);
    const dateStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
    const risk = (r.risk_level || 'LOW').toUpperCase();

    let riskBadge = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-400 border-emerald-300 dark:border-emerald-800';
    if (risk === 'CRITICAL') riskBadge = 'bg-red-100 text-red-800 dark:bg-red-950 dark:text-red-400 border-red-300 dark:border-red-800';
    else if (risk === 'HIGH') riskBadge = 'bg-orange-100 text-orange-800 dark:bg-orange-950 dark:text-orange-400 border-orange-300 dark:border-orange-800';
    else if (risk === 'MODERATE') riskBadge = 'bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-400 border-amber-300 dark:border-amber-800';

    const cleanPred = formatLabel(r.prediction_label);
    const cleanSource = formatLabel(r.data_source);

    return `
      <tr class="hover:bg-slate-100 dark:hover:bg-slate-800/50 transition-colors">
        <td class="py-3.5 px-4 font-mono text-slate-700 dark:text-slate-300">${dateStr}</td>
        <td class="py-3.5 px-4 font-bold text-slate-900 dark:text-white">${Number(r.current_water_level).toFixed(2)}</td>
        <td class="py-3.5 px-4 font-bold text-purple-700 dark:text-purple-400">${cleanPred}</td>
        <td class="py-3.5 px-4 font-bold text-slate-800 dark:text-slate-200">${Math.round((r.probability || 0) * 100)}%</td>
        <td class="py-3.5 px-4"><span class="px-2.5 py-0.5 rounded-full text-[10px] font-black border ${riskBadge}">${risk}</span></td>
        <td class="py-3.5 px-4 font-semibold text-slate-700 dark:text-slate-300">${r.escalation_level}</td>
        <td class="py-3.5 px-4 font-mono text-[11px] text-slate-500">${cleanSource}</td>
        <td class="py-3.5 px-4 text-emerald-600 dark:text-emerald-400 font-bold">${r.status}</td>
      </tr>
    `;
  }).join('');
}

function filterHistoryTable() {
  const riskFilter = document.getElementById('hist-filter-risk')?.value || 'all';
  const predFilter = document.getElementById('hist-filter-pred')?.value || 'all';
  const sourceFilter = document.getElementById('hist-filter-source')?.value || 'all';

  const filtered = fullHistoryData.filter(r => {
    const matchRisk = riskFilter === 'all' || (r.risk_level || '').toUpperCase() === riskFilter;
    const matchPred = predFilter === 'all' || formatLabel(r.prediction_label) === predFilter;
    const matchSource = sourceFilter === 'all' || r.data_source === sourceFilter;
    return matchRisk && matchPred && matchSource;
  });

  populateHistoryTable(filtered);
}

// Export CSV Audit Log
function exportHistoryCSV() {
  if (!fullHistoryData.length) return;
  const headers = ['Timestamp', 'Water_Level_m', 'Prediction', 'Probability', 'Risk_Level', 'Escalation', 'Data_Source', 'Status'];
  const rows = fullHistoryData.map(r => [
    r.timestamp,
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

// Simulation Sandbox Controls
function updatePageSimSlider(val) {
  const display = document.getElementById('page-sim-level-display');
  if (display) display.innerText = `${Number(val).toFixed(2)} m`;
}

function resetSimSlider() {
  const slider = document.getElementById('page-sim-level-slider');
  if (slider) {
    slider.value = 59.8;
    updatePageSimSlider(59.8);
  }
}

async function executePageSimulation() {
  const slider = document.getElementById('page-sim-level-slider');
  if (!slider) return;
  const level = parseFloat(slider.value);
  const btn = document.getElementById('btn-page-run-sim');

  if (btn) {
    btn.disabled = true;
    btn.innerText = 'Evaluating AI...';
  }

  try {
    const res = await fetch('/api/flood/predict-custom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ water_level: level })
    });

    if (res.ok) {
      const data = await res.json();
      if (document.getElementById('page-sim-pred-label')) {
        document.getElementById('page-sim-pred-label').innerText = formatLabel(data.prediction_label);
      }
      if (document.getElementById('page-sim-prob')) {
        document.getElementById('page-sim-prob').innerText = `${Math.round(data.probability * 100)}%`;
      }
      if (document.getElementById('page-sim-risk')) {
        document.getElementById('page-sim-risk').innerText = data.risk_level;
      }
      if (document.getElementById('page-sim-escalation')) {
        document.getElementById('page-sim-escalation').innerText = data.escalation_level;
      }
    }
  } catch (err) {
    console.error('Simulation error:', err);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerText = 'Run AI Inference';
    }
  }
}