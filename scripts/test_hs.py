import os
from pathlib import Path

Path('frontend').mkdir(parents=True, exist_ok=True)

# 1. frontend/index.html
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FloodSense AI — Know the risk. Act before the flood.</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Google Fonts: Inter -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Custom Styles -->
  <link rel="stylesheet" href="styles.css" />
  
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif'],
          },
          colors: {
            brandBlue: '#126BFF',
            brightBlue: '#2D7CFF',
            darkShell: '#031226',
            darkSidebar: '#06172B',
            darkCard: '#071A31',
            darkBorder: '#183452',
            lightBg: '#F4F7FB',
            riskLow: '#22C55E',
            riskModerate: '#F59E0B',
            riskHigh: '#F97316',
            riskCritical: '#EF233C',
          },
          animation: {
            'glow-critical': 'glowCritical 2.5s ease-in-out infinite',
            'glow-green': 'glowGreen 3s ease-in-out infinite',
            'fade-in': 'fadeIn 0.25s ease-out forwards',
            'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
          },
          keyframes: {
            glowCritical: {
              '0%, 100%': { boxShadow: '0 0 15px rgba(239, 35, 60, 0.4), inset 0 0 15px rgba(239, 35, 60, 0.2)' },
              '50%': { boxShadow: '0 0 30px rgba(239, 35, 60, 0.75), inset 0 0 25px rgba(239, 35, 60, 0.35)' }
            },
            glowGreen: {
              '0%, 100%': { boxShadow: '0 0 6px rgba(34, 197, 94, 0.4)' },
              '50%': { boxShadow: '0 0 14px rgba(34, 197, 94, 0.7)' }
            },
            fadeIn: {
              '0%': { opacity: '0', transform: 'translateY(5px)' },
              '100%': { opacity: '1', transform: 'translateY(0)' }
            }
          }
        }
      }
    }
  </script>
</head>
<body class="bg-[#031226] text-slate-100 font-sans antialiased min-h-screen flex flex-col overflow-x-hidden selection:bg-blue-600 selection:text-white">

  <!-- ========================================================================= -->
  <!-- 1. LANDING PAGE VIEW -->
  <!-- ========================================================================= -->
  <section id="view-landing" class="app-view min-h-screen flex flex-col justify-between bg-gradient-to-b from-[#020b18] via-[#051833] to-[#020b18] relative overflow-hidden">
    
    <!-- Background River Landscape & Atmospheric Glow -->
    <div class="absolute inset-0 pointer-events-none opacity-20">
      <svg viewBox="0 0 1440 800" class="w-full h-full object-cover">
        <defs>
          <linearGradient id="landingRiverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#126BFF" />
            <stop offset="50%" stop-color="#00D2FF" />
            <stop offset="100%" stop-color="#051833" />
          </linearGradient>
        </defs>
        <path d="M-100,500 C300,350 500,650 900,450 C1200,300 1350,600 1600,480 L1600,900 L-100,900 Z" fill="url(#landingRiverGrad)" opacity="0.6" />
      </svg>
    </div>

    <!-- Top Landing Navigation -->
    <header class="w-full max-w-7xl mx-auto px-6 py-5 flex items-center justify-between z-20">
      <div class="flex items-center gap-3 cursor-pointer" onclick="navigateTo('landing')">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/30 flex-shrink-0">
          <i data-lucide="waves" class="w-6 h-6 text-white"></i>
        </div>
        <div>
          <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
            FloodSense <span class="text-cyan-400 text-xs px-1.5 py-0.5 rounded bg-cyan-950 border border-cyan-800">AI</span>
          </h1>
          <p class="text-[11px] text-slate-400">AI-Powered Flood Early Warning</p>
        </div>
      </div>

      <!-- Center Nav Links -->
      <nav class="hidden md:flex items-center gap-1 bg-[#06172B]/80 backdrop-blur-md px-4 py-1.5 rounded-full border border-slate-800 shadow-inner">
        <button onclick="navigateTo('landing')" class="px-4 py-1.5 rounded-full text-xs font-semibold text-white bg-blue-600 shadow-sm">Home</button>
        <button onclick="openAboutModal()" class="px-4 py-1.5 rounded-full text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-all">About</button>
        <button onclick="navigateTo('learn-more')" class="px-4 py-1.5 rounded-full text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-all">How It Works</button>
        <button onclick="openFeaturesModal()" class="px-4 py-1.5 rounded-full text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800/50 transition-all">Features</button>
      </nav>

      <!-- Right Sign In / Operator Button -->
      <div>
        <button onclick="openSignInModal()" class="px-5 py-2 rounded-full text-xs font-bold text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-600 transition-all shadow-sm flex items-center gap-2">
          <i data-lucide="user-check" class="w-3.5 h-3.5 text-cyan-400"></i>
          <span>Sign In</span>
        </button>
      </div>
    </header>

    <!-- Landing Hero Center -->
    <div class="w-full max-w-6xl mx-auto px-6 py-10 flex flex-col items-center text-center z-20 space-y-8 my-auto">
      
      <div class="space-y-3 max-w-3xl">
        <h2 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-none">
          Know the risk.<br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-blue-500">Act before the flood.</span>
        </h2>
        <p class="text-sm sm:text-base text-slate-300 font-normal max-w-2xl mx-auto pt-2 leading-relaxed">
          AI transforms river-level data into early insights so communities can stay safe.
        </p>
      </div>

      <!-- Dotted Pipeline Story Indicator -->
      <div class="text-[11px] font-semibold text-cyan-400/80 tracking-widest uppercase flex items-center gap-2">
        <span>────</span> How it works <span>────►</span>
      </div>

      <!-- 5-STAGE CIRCULAR PIPELINE NODES -->
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-4 w-full max-w-5xl">
        
        <!-- 01 Sense -->
        <div onclick="navigateTo('learn-more')" class="bg-[#071A31]/90 backdrop-blur-md border border-slate-800 hover:border-blue-500/50 rounded-2xl p-4 flex flex-col items-center text-center transition-all duration-300 group hover:-translate-y-1 shadow-lg cursor-pointer">
          <div class="w-12 h-12 rounded-full bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-cyan-400 mb-3 group-hover:scale-110 transition-transform">
            <i data-lucide="droplet" class="w-6 h-6"></i>
          </div>
          <span class="text-[10px] font-extrabold text-blue-400 tracking-wider">01</span>
          <h4 class="text-sm font-bold text-white mt-0.5">Sense</h4>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">Real-time water level monitoring</p>
        </div>

        <!-- 02 Understand -->
        <div onclick="navigateTo('learn-more')" class="bg-[#071A31]/90 backdrop-blur-md border border-slate-800 hover:border-cyan-500/50 rounded-2xl p-4 flex flex-col items-center text-center transition-all duration-300 group hover:-translate-y-1 shadow-lg cursor-pointer">
          <div class="w-12 h-12 rounded-full bg-cyan-600/20 border border-cyan-500/40 flex items-center justify-center text-cyan-300 mb-3 group-hover:scale-110 transition-transform">
            <i data-lucide="brain" class="w-6 h-6"></i>
          </div>
          <span class="text-[10px] font-extrabold text-cyan-400 tracking-wider">02</span>
          <h4 class="text-sm font-bold text-white mt-0.5">Understand</h4>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">AI analyzes patterns & trends</p>
        </div>

        <!-- 03 Predict -->
        <div onclick="navigateTo('learn-more')" class="bg-[#071A31]/90 backdrop-blur-md border border-slate-800 hover:border-purple-500/50 rounded-2xl p-4 flex flex-col items-center text-center transition-all duration-300 group hover:-translate-y-1 shadow-lg cursor-pointer">
          <div class="w-12 h-12 rounded-full bg-purple-600/20 border border-purple-500/40 flex items-center justify-center text-purple-300 mb-3 group-hover:scale-110 transition-transform">
            <i data-lucide="trending-up" class="w-6 h-6"></i>
          </div>
          <span class="text-[10px] font-extrabold text-purple-400 tracking-wider">03</span>
          <h4 class="text-sm font-bold text-white mt-0.5">Predict</h4>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">Forecast flood risk within 6 hours</p>
        </div>

        <!-- 04 Assess -->
        <div onclick="navigateTo('learn-more')" class="bg-[#071A31]/90 backdrop-blur-md border border-slate-800 hover:border-amber-500/50 rounded-2xl p-4 flex flex-col items-center text-center transition-all duration-300 group hover:-translate-y-1 shadow-lg cursor-pointer">
          <div class="w-12 h-12 rounded-full bg-amber-600/20 border border-amber-500/40 flex items-center justify-center text-amber-300 mb-3 group-hover:scale-110 transition-transform">
            <i data-lucide="shield-check" class="w-6 h-6"></i>
          </div>
          <span class="text-[10px] font-extrabold text-amber-400 tracking-wider">04</span>
          <h4 class="text-sm font-bold text-white mt-0.5">Assess</h4>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">Risk level & escalation evaluation</p>
        </div>

        <!-- 05 Act -->
        <div onclick="navigateTo('learn-more')" class="bg-[#071A31]/90 backdrop-blur-md border border-slate-800 hover:border-red-500/50 rounded-2xl p-4 flex flex-col items-center text-center transition-all duration-300 group hover:-translate-y-1 shadow-lg cursor-pointer">
          <div class="w-12 h-12 rounded-full bg-red-600/20 border border-red-500/40 flex items-center justify-center text-red-400 mb-3 group-hover:scale-110 transition-transform">
            <i data-lucide="bell" class="w-6 h-6"></i>
          </div>
          <span class="text-[10px] font-extrabold text-red-400 tracking-wider">05</span>
          <h4 class="text-sm font-bold text-white mt-0.5">Act</h4>
          <p class="text-[11px] text-slate-400 mt-1 leading-snug">Timely alerts for better decisions</p>
        </div>

      </div>

      <!-- CTA Action Buttons -->
      <div class="flex items-center gap-4 pt-2">
        <button onclick="navigateTo('location-gate')" class="px-8 py-3.5 rounded-full text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-600 shadow-xl shadow-blue-600/30 transition-all flex items-center gap-2 transform hover:scale-105">
          <span>Get Started</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>
        <button onclick="navigateTo('learn-more')" class="px-8 py-3.5 rounded-full text-sm font-semibold text-slate-300 bg-slate-900/80 hover:bg-slate-800 border border-slate-700 transition-all">
          Learn More
        </button>
      </div>

    </div>

    <!-- Bottom Feature Strip -->
    <footer class="w-full bg-[#020712]/90 border-t border-slate-800/80 py-4 px-6 z-20">
      <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
        <div class="flex items-center gap-2">
          <i data-lucide="radio" class="w-4 h-4 text-blue-400"></i>
          <span>Real-time Monitoring</span>
        </div>
        <div class="flex items-center gap-2">
          <i data-lucide="cpu" class="w-4 h-4 text-cyan-400"></i>
          <span>AI-Powered Predictions</span>
        </div>
        <div class="flex items-center gap-2">
          <i data-lucide="shield" class="w-4 h-4 text-emerald-400"></i>
          <span>Early Warnings Save Lives</span>
        </div>
        <div class="flex items-center gap-2">
          <i data-lucide="building" class="w-4 h-4 text-amber-400"></i>
          <span>Trusted by Local Authorities</span>
        </div>
      </div>
    </footer>

  </section>

  <!-- ========================================================================= -->
  <!-- 1.1 LEARN MORE VIEW (POLISHED 4-PILLAR INFORMATION VIEW) -->
  <!-- ========================================================================= -->
  <section id="view-learn-more" class="app-view min-h-screen flex flex-col justify-between bg-gradient-to-b from-[#020b18] via-[#051833] to-[#020b18] p-6 hidden">
    <div class="max-w-5xl w-full mx-auto my-auto space-y-6 animate-fade-in py-6">
      
      <!-- Top Navigation Header -->
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-blue-600/30 border border-blue-500/40 flex items-center justify-center text-cyan-300">
            <i data-lucide="info" class="w-5 h-5"></i>
          </div>
          <div>
            <h2 class="text-xl font-bold text-white">About FloodSense AI Platform</h2>
            <p class="text-xs text-slate-400">Understanding AI-Powered Flood Early Warning</p>
          </div>
        </div>
        <button onclick="navigateTo('landing')" class="px-4 py-2 rounded-xl text-xs font-bold text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 flex items-center gap-1.5 transition-all">
          <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
          <span>BACK TO HOME</span>
        </button>
      </div>

      <!-- 4 Core Pillars Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- Pillar 1 -->
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 space-y-2 shadow-lg">
          <div class="flex items-center gap-2.5 text-blue-400">
            <i data-lucide="compass" class="w-5 h-5"></i>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">1. WHAT IS FLOODSENSE AI?</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            FloodSense AI is an AI-powered flood early-warning platform that monitors water-level conditions and identifies the possibility of high-water conditions in advance.
          </p>
        </div>

        <!-- Pillar 2 -->
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 space-y-2 shadow-lg">
          <div class="flex items-center gap-2.5 text-cyan-400">
            <i data-lucide="target" class="w-5 h-5"></i>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">2. WHY DOES IT MATTER?</h3>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed">
            Instead of only showing the current water level, FloodSense helps identify rising risk early so authorities can monitor the situation and prepare a timely response before inundation occurs.
          </p>
        </div>

        <!-- Pillar 3 -->
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 space-y-3 shadow-lg">
          <div class="flex items-center gap-2.5 text-purple-400">
            <i data-lucide="git-merge" class="w-5 h-5"></i>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">3. HOW DOES IT WORK?</h3>
          </div>
          <div class="bg-[#031226] border border-slate-800 rounded-xl p-3 text-[11px] text-slate-300 flex flex-wrap items-center justify-between gap-1 font-mono">
            <span>Water-Level Data</span>
            <span>➔</span>
            <span>Data Validation</span>
            <span>➔</span>
            <span class="text-purple-400 font-bold">AI Prediction</span>
            <span>➔</span>
            <span>Risk Assessment</span>
            <span>➔</span>
            <span class="text-red-400 font-bold">Alert & Escalation</span>
          </div>
        </div>

        <!-- Pillar 4 -->
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 space-y-2 shadow-lg">
          <div class="flex items-center gap-2.5 text-emerald-400">
            <i data-lucide="check-square" class="w-5 h-5"></i>
            <h3 class="text-sm font-bold uppercase tracking-wider text-white">4. WHAT DOES THE USER GET?</h3>
          </div>
          <ul class="text-xs text-slate-300 space-y-1">
            <li class="flex items-center gap-2"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> Current water-level situation & trend</li>
            <li class="flex items-center gap-2"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> 6-hour high-water prediction & probability</li>
            <li class="flex items-center gap-2"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> Actionable explanation behind the alert</li>
            <li class="flex items-center gap-2"><i data-lucide="check" class="w-3.5 h-3.5 text-emerald-400"></i> Data-source transparency & historical verification</li>
          </ul>
        </div>

      </div>

      <!-- Action Button -->
      <div class="text-center pt-2">
        <button onclick="navigateTo('location-gate')" class="px-8 py-3.5 rounded-full text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-xl shadow-blue-600/30 transition-all">
          Proceed to Location Gate →
        </button>
      </div>

    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- 2. LOCATION / ACCESS GATE VIEW -->
  <!-- ========================================================================= -->
  <section id="view-location-gate" class="app-view min-h-screen flex flex-col items-center justify-center p-6 bg-gradient-to-b from-[#020b18] via-[#04142d] to-[#020b18] hidden relative z-30">
    
    <div class="max-w-md w-full bg-[#071A31] border border-[#183452] rounded-3xl p-8 shadow-2xl space-y-6 text-center animate-fade-in relative">
      
      <!-- Top Location Pin Visual -->
      <div class="w-16 h-16 rounded-full bg-blue-600/20 border border-blue-500/40 mx-auto flex items-center justify-center text-blue-400 shadow-inner">
        <i data-lucide="map-pin" class="w-8 h-8"></i>
      </div>

      <div class="space-y-1">
        <h3 class="text-xl font-bold text-white">Is your monitoring area</h3>
        <h2 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">Darrang, Assam?</h2>
      </div>

      <!-- Verified MVP Pilot Region Box -->
      <div class="bg-[#0a2344]/80 border border-blue-500/30 rounded-2xl p-4 text-left flex items-center justify-between gap-3 shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-blue-600/30 flex items-center justify-center text-cyan-300 flex-shrink-0">
            <i data-lucide="navigation" class="w-5 h-5"></i>
          </div>
          <div>
            <h4 class="text-sm font-bold text-white">Darrang, Assam</h4>
            <p class="text-[11px] text-slate-300">FloodSense AI is currently running its MVP pilot for this region.</p>
          </div>
        </div>
        <div class="w-6 h-6 rounded-full bg-emerald-500/20 border border-emerald-500 flex items-center justify-center text-emerald-400 flex-shrink-0">
          <i data-lucide="check" class="w-3.5 h-3.5 font-black"></i>
        </div>
      </div>

      <!-- Buttons -->
      <div class="space-y-3">
        <button onclick="confirmLocationAndEnter()" class="w-full py-3.5 rounded-xl text-sm font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-600/30 transition-all flex items-center justify-center gap-2">
          <span>Yes, Continue to Dashboard</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>

        <button onclick="showDifferentLocationNotice()" class="w-full py-3 rounded-xl text-xs font-semibold text-slate-300 bg-slate-900/60 hover:bg-slate-900 border border-slate-800 transition-all">
          No, My Location is Different
        </button>
      </div>

      <!-- Region Unsupported Notice (Hidden by default) -->
      <div id="diff-location-box" class="hidden pt-2 border-t border-slate-800 space-y-3 text-xs text-slate-400 animate-fade-in">
        <p class="text-amber-300 font-semibold">
          This platform is currently available only for <strong class="text-white">Darrang, Assam</strong>.
        </p>
        <p class="text-[11px]">
          The current MVP is deployed for the Darrang pilot region. More Brahmaputra basin regions will be supported in future.
        </p>
        <div class="flex gap-2">
          <button onclick="hideDifferentLocationNotice()" class="flex-1 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-semibold hover:bg-slate-700">
            Back to Gate
          </button>
          <button onclick="navigateTo('landing')" class="flex-1 py-2 rounded-lg bg-blue-600 text-white text-xs font-bold hover:bg-blue-500">
            Back to Home
          </button>
        </div>
      </div>

      <!-- Security Guarantee -->
      <div class="pt-2 text-[10px] text-slate-400 flex items-center justify-center gap-1.5">
        <i data-lucide="lock" class="w-3 h-3 text-emerald-400"></i>
        <span>Your data and location preferences are secure.</span>
      </div>

    </div>

  </section>

  <!-- ========================================================================= -->
  <!-- 3. MAIN APPLICATION SHELL (DASHBOARD & SECONDARY PAGES) -->
  <!-- ========================================================================= -->
  <div id="view-app" class="app-view min-h-screen flex flex-col md:flex-row flex-1 hidden bg-[#031226]">
    
    <!-- ========================================================================= -->
    <!-- LEFT SIDEBAR -->
    <!-- ========================================================================= -->
    <aside class="w-full md:w-60 bg-[#06172B] text-white flex flex-col flex-shrink-0 border-r border-[#183452] z-30 justify-between select-none">
      <div>
        <!-- Brand Logo Header -->
        <div class="p-4 border-b border-[#183452] flex items-center justify-between">
          <div class="flex items-center gap-2.5 cursor-pointer" onclick="navigateTo('landing')">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-md shadow-blue-500/20 flex-shrink-0">
              <i data-lucide="waves" class="w-5 h-5 text-white"></i>
            </div>
            <div>
              <h1 class="text-sm font-extrabold tracking-tight text-white leading-tight">
                FloodSense <span class="text-cyan-400">AI</span>
              </h1>
              <p class="text-[9px] text-slate-400">Flood Early Warning</p>
            </div>
          </div>
        </div>

        <!-- Navigation Links -->
        <nav class="p-3 space-y-1">
          <!-- Main Section -->
          <button onclick="navigateAppPage('dashboard')" id="nav-dashboard" class="nav-item w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-bold transition-all text-white bg-blue-600 shadow-md shadow-blue-600/30">
            <i data-lucide="layout-dashboard" class="w-4 h-4 text-cyan-200"></i>
            <span>Dashboard</span>
          </button>

          <button onclick="navigateAppPage('map')" id="nav-map" class="nav-item w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800/60">
            <i data-lucide="map" class="w-4 h-4 text-slate-400"></i>
            <span>Map View</span>
          </button>

          <button onclick="navigateAppPage('alerts')" id="nav-alerts" class="nav-item w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800/60">
            <div class="flex items-center gap-3">
              <i data-lucide="bell" class="w-4 h-4 text-slate-400"></i>
              <span>Alerts</span>
            </div>
            <span id="sidebar-alert-badge" class="w-5 h-5 rounded-full bg-red-600 text-white text-[10px] font-black flex items-center justify-center animate-pulse">3</span>
          </button>

          <!-- DATA & REPORTS -->
          <div class="pt-3 pb-1 px-3">
            <span class="text-[9px] font-extrabold uppercase tracking-widest text-slate-400">DATA & REPORTS</span>
          </div>

          <button onclick="navigateAppPage('history')" id="nav-history" class="nav-item w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800/60">
            <i data-lucide="history" class="w-4 h-4 text-slate-400"></i>
            <span>History</span>
          </button>

          <button onclick="navigateAppPage('simulation')" id="nav-simulation" class="nav-item w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800/60">
            <i data-lucide="sliders" class="w-4 h-4 text-slate-400"></i>
            <span>Simulation</span>
          </button>

          <!-- SYSTEM -->
          <div class="pt-3 pb-1 px-3">
            <span class="text-[9px] font-extrabold uppercase tracking-widest text-slate-400">SYSTEM</span>
          </div>

          <!-- MORE ACCORDION -->
          <div>
            <button onclick="toggleMoreMenu()" id="btn-more-toggle" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 transition-all">
              <div class="flex items-center gap-3">
                <i data-lucide="more-horizontal" class="w-4 h-4 text-slate-400"></i>
                <span>More</span>
              </div>
              <i data-lucide="chevron-down" id="more-chevron" class="w-3.5 h-3.5 text-slate-400 transition-transform"></i>
            </button>
            
            <div id="more-submenu" class="hidden pl-6 pr-2 py-1 space-y-1 text-xs">
              <button onclick="navigateAppPage('how-it-works')" id="nav-how-it-works" class="nav-item w-full text-left py-1.5 px-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2">
                <i data-lucide="book-open" class="w-3.5 h-3.5 text-slate-400"></i>
                <span>How It Works</span>
              </button>
              <button onclick="navigateAppPage('system-details')" id="nav-system-details" class="nav-item w-full text-left py-1.5 px-2 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800/50 flex items-center gap-2">
                <i data-lucide="cpu" class="w-3.5 h-3.5 text-slate-400"></i>
                <span>System Details</span>
              </button>
            </div>
          </div>

          <button onclick="navigateAppPage('settings')" id="nav-settings" class="nav-item w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all text-slate-300 hover:text-white hover:bg-slate-800/60">
            <i data-lucide="settings" class="w-4 h-4 text-slate-400"></i>
            <span>Settings</span>
          </button>

          <button onclick="promptLogout()" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-red-300 hover:bg-red-950/30 transition-all">
            <i data-lucide="log-out" class="w-4 h-4"></i>
            <span>Logout</span>
          </button>
        </nav>
      </div>

      <!-- Bottom Status -->
      <div class="p-3 border-t border-[#183452] space-y-2">
        <div class="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-emerald-950/60 border border-emerald-800/60 text-emerald-300 text-[10px]">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-glow-green"></span>
          <span class="font-bold">SYSTEM OPERATIONAL</span>
        </div>
        <div class="text-[9px] text-slate-400 text-center">
          © 2026 FloodSense AI
        </div>
      </div>
    </aside>

    <!-- ========================================================================= -->
    <!-- RIGHT MAIN CONTENT AREA -->
    <!-- ========================================================================= -->
    <div class="flex-1 flex flex-col min-w-0 bg-[#031226] overflow-y-auto">
      
      <!-- TOP COMMAND CENTER HEADER -->
      <header class="bg-[#071A31] border-b border-[#183452] px-6 py-3 flex flex-wrap items-center justify-between gap-4 sticky top-0 z-20 shadow-md">
        <!-- Left: Station Details -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-blue-600/20 border border-blue-500/40 flex items-center justify-center text-blue-400 flex-shrink-0">
            <i data-lucide="map-pin" class="w-4 h-4"></i>
          </div>
          <div>
            <h2 id="hdr-station" class="text-xs font-bold text-white tracking-tight">NH15 Crossing Fakirpara Tangni</h2>
            <p id="hdr-district" class="text-[11px] text-slate-400 font-medium">Darrang, Assam</p>
          </div>
        </div>

        <!-- Right: Status Indicators -->
        <div class="flex items-center gap-3 flex-wrap">
          <!-- Last Updated -->
          <div class="flex items-center gap-1.5 bg-[#031226] border border-[#183452] px-3 py-1.5 rounded-lg text-xs text-slate-300 font-medium">
            <i data-lucide="clock" class="w-3.5 h-3.5 text-slate-400"></i>
            <span>Last Updated:</span>
            <span id="hdr-timestamp" class="font-bold text-white">28 Aug 2026, 20:00</span>
          </div>

          <!-- Demo Mode Button -->
          <div onclick="navigateAppPage('simulation')" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-950/50 text-amber-300 border border-amber-800/80 cursor-pointer hover:bg-amber-900/60 transition-all shadow-xs">
            <i data-lucide="play-circle" class="w-3.5 h-3.5 text-amber-400 fill-amber-500/20"></i>
            <span>DEMO MODE</span>
            <span class="text-[10px] opacity-75 font-normal ml-1">Historical data replay</span>
          </div>

          <!-- Refresh Button -->
          <button onclick="refreshDashboard(true)" id="btn-refresh" title="Refresh Live State" class="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i>
          </button>
        </div>
      </header>

      <!-- ========================================================================= -->
      <!-- PAGE 1: MAIN DASHBOARD (CLEAN, FOCUSED COMMAND CENTER) -->
      <!-- ========================================================================= -->
      <div id="page-dashboard" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto">
        
        <!-- TOP ROW: HERO 6-HOUR RISK + CURRENT WATER LEVEL -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          
          <!-- 1. HERO CRITICAL RISK CARD (2 COLS) -->
          <div id="hero-card" class="lg:col-span-2 rounded-2xl p-6 text-white shadow-xl transition-all duration-500 flex flex-col justify-between bg-gradient-to-r from-[#4c0519] via-[#881337] to-[#9f1239] border border-red-500/40 animate-glow-critical relative overflow-hidden">
            <div class="relative z-10 flex flex-wrap items-center justify-between gap-6">
              <!-- Left Warning -->
              <div class="space-y-1.5 flex-1 min-w-[240px]">
                <div class="text-[10px] font-extrabold uppercase tracking-widest text-red-200/90">
                  6-HOUR FLOOD RISK
                </div>

                <div class="flex items-center gap-3.5 my-1">
                  <div class="w-12 h-12 rounded-2xl bg-red-600/60 border border-red-400/80 flex items-center justify-center shadow-lg flex-shrink-0">
                    <i data-lucide="alert-triangle" class="w-7 h-7 text-white fill-white/20 animate-pulse"></i>
                  </div>
                  <div>
                    <h3 id="hero-risk-level" class="text-3xl sm:text-4xl font-black tracking-tight uppercase leading-none">CRITICAL</h3>
                  </div>
                </div>

                <p id="hero-risk-desc" class="text-xs sm:text-sm text-red-100/95 font-medium max-w-md pt-1">
                  High-water conditions are likely within the next 6 hours.
                </p>
              </div>

              <!-- Right Ring Gauge -->
              <div class="bg-black/35 backdrop-blur-md rounded-2xl p-4 border border-white/10 flex items-center gap-4 flex-shrink-0 shadow-inner">
                <div class="relative w-18 h-18 flex items-center justify-center">
                  <svg class="w-18 h-18 transform -rotate-90" viewBox="0 0 80 80">
                    <circle cx="40" cy="40" r="32" stroke="currentColor" stroke-width="6" class="text-red-950/60" fill="transparent" />
                    <circle id="prob-circle" cx="40" cy="40" r="32" stroke="currentColor" stroke-width="6" class="text-amber-400 transition-all duration-1000" fill="transparent" stroke-dasharray="201.06" stroke-dashoffset="4.02" stroke-linecap="round" />
                  </svg>
                  <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                    <span id="hero-prob-val" class="text-base font-black leading-none text-white">99%</span>
                  </div>
                </div>
                <div class="text-left leading-tight pr-1">
                  <div class="text-[9px] text-amber-300 uppercase tracking-widest font-bold">MODEL PREDICTION</div>
                  <div id="hero-pred-label" class="text-xs font-black text-amber-400 mt-0.5 uppercase tracking-wide">HIGH WATER</div>
                  <div class="text-[10px] text-slate-300">Next 6 Hours</div>
                  <div class="text-[9px] text-slate-400 mt-0.5">Prediction Probability</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. CURRENT WATER LEVEL CARD (1 COL) -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between relative overflow-hidden">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <i data-lucide="droplet" class="w-4 h-4 text-blue-600 fill-blue-500/20"></i>
                CURRENT WATER LEVEL
              </span>
            </div>

            <div class="my-2 flex items-center justify-between">
              <div>
                <div class="flex items-baseline gap-1.5">
                  <span id="card-water-level" class="text-3xl sm:text-4xl font-black text-slate-900">60.31</span>
                  <span class="text-sm font-bold text-slate-500">m</span>
                </div>
                <div class="text-[11px] text-slate-500 font-medium">Current observation</div>
              </div>

              <!-- Sparkline -->
              <div class="w-20 h-10 flex items-center justify-center opacity-85">
                <svg viewBox="0 0 80 40" class="w-full h-full text-blue-500">
                  <path d="M0,35 Q20,30 40,20 Q60,10 80,5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" />
                  <circle cx="80" cy="5" r="3" fill="#2563eb" />
                </svg>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs pt-2 border-t border-slate-100 text-slate-500 font-medium">
              <div class="flex items-center gap-1 text-red-600 font-bold" id="card-trend-pill">
                <i data-lucide="arrow-up-right" class="w-3.5 h-3.5 text-red-600"></i>
                <span>Rising trend</span>
              </div>
              <span class="text-[11px]" id="card-updated-time">Observed: 20:00</span>
            </div>
          </div>

        </div>

        <!-- MIDDLE ROW: 3 KEY STATUS CARDS -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          <!-- NEXT 6 HOURS -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <i data-lucide="clock-9" class="w-4 h-4 text-purple-600"></i>
                NEXT 6 HOURS
              </span>
            </div>

            <div class="my-2 flex items-center justify-between">
              <div>
                <span id="card-prediction-label" class="text-2xl font-black text-purple-700 uppercase tracking-tight">HIGH WATER</span>
                <p class="text-xs text-slate-500 font-medium mt-0.5">High-water conditions are likely.</p>
              </div>
              <div class="text-purple-400 opacity-60">
                <i data-lucide="waves" class="w-7 h-7"></i>
              </div>
            </div>

            <div class="flex items-center justify-between text-xs pt-2 border-t border-slate-100 text-slate-500 font-medium">
              <span>Prediction Horizon: 6 Hours</span>
              <i data-lucide="activity" class="w-3.5 h-3.5 text-purple-600"></i>
            </div>
          </div>

          <!-- RECOMMENDED ACTION -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div class="flex items-center justify-between">
              <span class="text-xs font-extrabold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
                <i data-lucide="shield-alert" class="w-4 h-4 text-amber-600"></i>
                RECOMMENDED ACTION
              </span>
            </div>

            <div class="my-2">
              <span id="card-action-title" class="text-xl font-black text-amber-700 uppercase tracking-tight">STATE-LEVEL ATTENTION</span>
              <p id="card-action-desc" class="text-xs text-slate-500 font-medium mt-0.5">Authorities should increase monitoring and prepare for possible flood conditions.</p>
            </div>

            <div class="pt-2 border-t border-slate-100">
              <div class="p-1.5 rounded-lg bg-red-50 text-red-700 text-[10px] font-bold flex items-center justify-between">
                <span>Trigger: Critical risk detected</span>
                <span>ESCALATION LEVEL: STATE</span>
              </div>
            </div>
          </div>

          <!-- DATA SOURCE -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs font-extrabold uppercase tracking-wider text-blue-600 flex items-center gap-1.5">
                  <i data-lucide="radio" class="w-4 h-4"></i>
                  DATA SOURCE
                </span>
              </div>

              <div>
                <h4 id="src-title" class="text-sm font-extrabold text-blue-900 uppercase tracking-tight">HYDROLOGY BRIDGE</h4>
                <p id="src-subtitle" class="text-xs text-slate-500 font-medium">Derived Hydrology</p>
              </div>

              <div id="src-banner" class="p-2 rounded-xl bg-emerald-50 text-emerald-900 text-xs flex items-center gap-2">
                <i data-lucide="check-circle" class="w-4 h-4 text-emerald-600 flex-shrink-0"></i>
                <span class="text-[11px] font-medium leading-tight">Government gauge stream delayed. Using verified hydrology bridge.</span>
              </div>
            </div>

            <div class="pt-2 border-t border-slate-100 flex justify-between items-center text-xs">
              <button onclick="navigateAppPage('system-details')" class="text-blue-600 hover:underline font-bold text-[11px]">View Source Details</button>
            </div>
          </div>

        </div>

        <!-- LOWER ROW: 24H TREND + WHY RISK HIGH + STATION LOCATION -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          
          <!-- WATER LEVEL TREND -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-1.5">
                <i data-lucide="line-chart" class="w-4 h-4 text-blue-600"></i>
                <h4 class="text-xs font-extrabold text-slate-800 uppercase tracking-wider">WATER LEVEL TREND <span class="text-[10px] text-slate-400 font-normal">(LAST 24 HOURS)</span></h4>
              </div>
              
              <div class="flex items-center gap-1 bg-slate-100 p-0.5 rounded-lg text-[11px] font-bold text-slate-600">
                <button onclick="setTrendRange(6)" id="btn-range-6" class="px-2 py-0.5 rounded hover:bg-white transition-all">6H</button>
                <button onclick="setTrendRange(12)" id="btn-range-12" class="px-2 py-0.5 rounded hover:bg-white transition-all">12H</button>
                <button onclick="setTrendRange(24)" id="btn-range-24" class="px-2 py-0.5 rounded bg-blue-600 text-white shadow-xs">24H</button>
              </div>
            </div>

            <!-- Chart -->
            <div class="relative h-44 w-full my-1">
              <canvas id="trendChart"></canvas>
            </div>

            <div class="flex items-center justify-between text-[10px] text-slate-500 pt-2 border-t border-slate-100 font-medium">
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-blue-600"></span> Water Level (m)</span>
              <span class="flex items-center gap-1 font-bold text-blue-600" id="trend-latest-pill">● 60.31 m</span>
            </div>
          </div>

          <!-- WHY IS THE RISK HIGH? -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div>
              <div class="flex items-center gap-2 mb-3">
                <div class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-black text-xs">?</div>
                <h4 class="text-xs font-extrabold text-slate-800 uppercase tracking-wider">WHY IS THE RISK HIGH?</h4>
              </div>

              <div class="space-y-2.5 text-xs">
                <div class="flex items-start gap-2.5">
                  <div class="w-6 h-6 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-600 flex-shrink-0 mt-0.5">
                    <i data-lucide="droplet" class="w-3.5 h-3.5"></i>
                  </div>
                  <div>
                    <div class="font-bold text-slate-800 text-xs">Water level is already high</div>
                    <div class="text-slate-500 text-[11px] leading-tight">The river level is currently elevated.</div>
                  </div>
                </div>

                <div class="flex items-start gap-2.5">
                  <div class="w-6 h-6 rounded-full bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-600 flex-shrink-0 mt-0.5">
                    <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
                  </div>
                  <div>
                    <div class="font-bold text-slate-800 text-xs">Water level is increasing</div>
                    <div class="text-slate-500 text-[11px] leading-tight">Recent observation show an increasing pattern.</div>
                  </div>
                </div>

                <div class="flex items-start gap-2.5">
                  <div class="w-6 h-6 rounded-full bg-red-50 border border-red-200 flex items-center justify-center text-red-600 flex-shrink-0 mt-0.5">
                    <i data-lucide="bar-chart-2" class="w-3.5 h-3.5"></i>
                  </div>
                  <div>
                    <div class="font-bold text-slate-800 text-xs">AI predicts high water</div>
                    <div class="text-slate-500 text-[11px] leading-tight">The model detects patterns associated with high-water conditions.</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 p-2.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-[11px] font-semibold text-center">
              These signs indicate a high chance of high water within the next 6 hours.
            </div>
          </div>

          <!-- STATION LOCATION -->
          <div class="bg-white text-slate-800 rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-extrabold uppercase tracking-wider text-slate-500">STATION LOCATION</span>
              <button onclick="navigateAppPage('map')" class="text-xs text-blue-600 hover:underline font-bold">View Full Map →</button>
            </div>

            <!-- Leaflet Map Container -->
            <div id="stationMap" class="w-full h-40 rounded-xl border border-slate-200 z-10 overflow-hidden"></div>

            <div class="pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
              <div>
                <div class="font-bold text-slate-800 text-[11px] flex items-center gap-1">
                  <i data-lucide="map-pin" class="w-3.5 h-3.5 text-blue-600"></i>
                  <span>NH15 Crossing Fakirpara Tangni</span>
                </div>
                <div class="text-[10px] text-slate-500 pl-4.5">Darrang, Assam</div>
              </div>
              <div class="text-right text-[10px] font-mono text-slate-500">
                26.5083° N<br>92.1164° E
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 2: MAP VIEW -->
      <!-- ========================================================================= -->
      <div id="page-map" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 shadow-xl space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                <i data-lucide="map" class="w-5 h-5 text-blue-400"></i>
                <span>Regional Flood Risk Map — Assam Basin</span>
              </h3>
              <p class="text-xs text-slate-400">Geographic early warning overlays across monitored Brahmaputra river stations.</p>
            </div>

            <div class="flex items-center gap-2">
              <select class="bg-slate-900 border border-slate-700 text-xs rounded-xl px-3 py-2 text-slate-200">
                <option>All Stations</option>
                <option selected>NH15 Crossing Fakirpara (Tangni)</option>
              </select>
              <select class="bg-slate-900 border border-slate-700 text-xs rounded-xl px-3 py-2 text-slate-200">
                <option selected>Risk Overlay: Active</option>
                <option>Terrain Only</option>
              </select>
            </div>
          </div>

          <!-- Interactive Full Map with Region Highlighting -->
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
            <div class="lg:col-span-3 h-[520px] rounded-xl overflow-hidden border border-slate-800 relative">
              <div id="fullRegionalMap" class="w-full h-full"></div>
            </div>

            <!-- Risk Legend & Station Details -->
            <div class="bg-[#0a2344] border border-slate-800 rounded-xl p-4 flex flex-col justify-between space-y-4">
              <div class="space-y-3">
                <h4 class="text-xs font-bold text-slate-300 uppercase tracking-wider">RISK LEVEL LEGEND</h4>
                <div class="space-y-2 text-xs">
                  <div class="flex items-center justify-between p-2 rounded-lg bg-emerald-950/40 border border-emerald-800/60 text-emerald-300">
                    <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span> LOW</span>
                    <span class="text-[10px]">Safe stage</span>
                  </div>
                  <div class="flex items-center justify-between p-2 rounded-lg bg-amber-950/40 border border-amber-800/60 text-amber-300">
                    <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> MODERATE</span>
                    <span class="text-[10px]">Watch stage</span>
                  </div>
                  <div class="flex items-center justify-between p-2 rounded-lg bg-orange-950/40 border border-orange-800/60 text-orange-300">
                    <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-orange-400"></span> HIGH</span>
                    <span class="text-[10px]">Warning stage</span>
                  </div>
                  <div class="flex items-center justify-between p-2 rounded-lg bg-red-950/60 border border-red-800/80 text-red-300">
                    <span class="flex items-center gap-2"><span class="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></span> CRITICAL</span>
                    <span class="text-[10px] font-bold">DARRANG (Active)</span>
                  </div>
                </div>
              </div>

              <div class="p-3 rounded-xl bg-slate-900/90 border border-slate-800 space-y-1.5 text-xs">
                <div class="font-bold text-white">Selected Station:</div>
                <div class="text-cyan-300 font-semibold">NH15 Crossing Fakirpara Tangni</div>
                <div class="text-[11px] text-slate-400">District: Darrang, Assam</div>
                <div class="text-[11px] text-slate-400">Current Level: <strong class="text-white">60.31 m</strong></div>
                <div class="text-[11px] text-red-400 font-bold">Risk: CRITICAL (99%)</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 3: ALERTS CENTER -->
      <!-- ========================================================================= -->
      <div id="page-alerts" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 shadow-xl space-y-5">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                <i data-lucide="bell" class="w-5 h-5 text-red-400 animate-pulse"></i>
                <span>Active Risk Alerts & Broadcast Log</span>
              </h3>
              <p class="text-xs text-slate-400">Real-time critical escalation warnings dispatched to district and state emergency teams.</p>
            </div>
            <span id="alerts-count-badge" class="px-3 py-1 rounded-full text-xs font-extrabold bg-red-600/20 text-red-400 border border-red-500">
              3 ACTIVE ALERTS
            </span>
          </div>

          <!-- Alert Cards List -->
          <div class="space-y-3">
            <!-- Alert 1 (CRITICAL) -->
            <div onclick="openAlertDetailModal('alert-1')" class="p-4 rounded-xl bg-gradient-to-r from-red-950/80 to-slate-900 border border-red-700/80 hover:border-red-500 flex flex-wrap items-center justify-between gap-4 cursor-pointer transition-all shadow-md">
              <div class="flex items-start gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-red-600/30 border border-red-500 flex items-center justify-center text-red-400 flex-shrink-0 mt-0.5">
                  <i data-lucide="alert-octagon" class="w-6 h-6 animate-pulse"></i>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-black bg-red-600 text-white uppercase">CRITICAL</span>
                    <span class="text-xs font-bold text-white">High-water conditions likely within next 6 hours</span>
                  </div>
                  <p class="text-xs text-slate-300 mt-1">Station: <strong>NH15 Crossing Fakirpara Tangni</strong> • Darrang, Assam (Water Level: 60.31m, Probability: 99%)</p>
                  <div class="text-[11px] text-slate-400 mt-1">Recommended: <strong>STATE-LEVEL ATTENTION</strong> — Deploy emergency monitoring teams.</div>
                </div>
              </div>
              <div class="text-right text-xs">
                <span class="px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-300 font-bold border border-emerald-800 text-[10px]">● ACTIVE</span>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">28 Aug 2026, 20:00</div>
              </div>
            </div>

            <!-- Alert 2 (HIGH) -->
            <div onclick="openAlertDetailModal('alert-2')" class="p-4 rounded-xl bg-gradient-to-r from-orange-950/80 to-slate-900 border border-orange-700/80 hover:border-orange-500 flex flex-wrap items-center justify-between gap-4 cursor-pointer transition-all shadow-md">
              <div class="flex items-start gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-orange-600/30 border border-orange-500 flex items-center justify-center text-orange-400 flex-shrink-0 mt-0.5">
                  <i data-lucide="trending-up" class="w-6 h-6"></i>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-black bg-orange-600 text-white uppercase">HIGH</span>
                    <span class="text-xs font-bold text-white">Continuous water surge detected (+0.25m in 3h)</span>
                  </div>
                  <p class="text-xs text-slate-300 mt-1">Tangni River catchment flow acceleration exceeds warning threshold.</p>
                </div>
              </div>
              <div class="text-right text-xs">
                <span class="px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-300 font-bold border border-emerald-800 text-[10px]">● ACTIVE</span>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">28 Aug 2026, 19:00</div>
              </div>
            </div>

            <!-- Alert 3 (OPERATIONAL FAILOVER) -->
            <div onclick="openAlertDetailModal('alert-3')" class="p-4 rounded-xl bg-gradient-to-r from-blue-950/80 to-slate-900 border border-blue-700/80 hover:border-blue-500 flex flex-wrap items-center justify-between gap-4 cursor-pointer transition-all shadow-md">
              <div class="flex items-start gap-3.5">
                <div class="w-10 h-10 rounded-xl bg-blue-600/30 border border-blue-500 flex items-center justify-center text-blue-400 flex-shrink-0 mt-0.5">
                  <i data-lucide="radio" class="w-6 h-6"></i>
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-black bg-blue-600 text-white uppercase">TELEMETRY</span>
                    <span class="text-xs font-bold text-white">Government stream delay: Failover to GloFAS Hydrology Bridge</span>
                  </div>
                  <p class="text-xs text-slate-300 mt-1">Automatic source resilience active. Zero telemetry interruption.</p>
                </div>
              </div>
              <div class="text-right text-xs">
                <span class="px-2.5 py-1 rounded-full bg-blue-950 text-blue-300 font-bold border border-blue-800 text-[10px]">● OPERATIONAL</span>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">28 Aug 2026, 17:00</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 4: HISTORY VIEW -->
      <!-- ========================================================================= -->
      <div id="page-history" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-5 shadow-xl space-y-5">
          <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-3">
            <div>
              <h3 class="text-base font-extrabold text-white">Historical Water Level & Prediction Log</h3>
              <p class="text-xs text-slate-400">Chronological telemetry observations and model inferences stored in Microsoft SQL Server.</p>
            </div>
            
            <button onclick="exportHistoryCSV()" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold flex items-center gap-2 shadow-md transition-all">
              <i data-lucide="download" class="w-4 h-4"></i>
              <span>Export CSV</span>
            </button>
          </div>

          <!-- Filter Toolbar -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div>
              <label class="text-[10px] text-slate-400 uppercase font-bold">Date Range</label>
              <select id="hist-filter-range" onchange="filterHistoryTable()" class="w-full mt-1 bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-1.5 text-slate-200">
                <option value="24h">Last 24 Hours</option>
                <option value="7d" selected>Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-slate-400 uppercase font-bold">Risk Level</label>
              <select id="hist-filter-risk" onchange="filterHistoryTable()" class="w-full mt-1 bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-1.5 text-slate-200">
                <option value="all" selected>All Risk Levels</option>
                <option value="CRITICAL">Critical</option>
                <option value="HIGH">High</option>
                <option value="MODERATE">Moderate</option>
                <option value="LOW">Low</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-slate-400 uppercase font-bold">Prediction</label>
              <select id="hist-filter-pred" onchange="filterHistoryTable()" class="w-full mt-1 bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-1.5 text-slate-200">
                <option value="all" selected>All Predictions</option>
                <option value="HIGH WATER">High Water</option>
                <option value="NORMAL">Normal</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-slate-400 uppercase font-bold">Source</label>
              <select id="hist-filter-source" onchange="filterHistoryTable()" class="w-full mt-1 bg-slate-900 border border-slate-700 text-xs rounded-lg px-3 py-1.5 text-slate-200">
                <option value="all" selected>All Sources</option>
                <option value="NWDP">NWDP</option>
                <option value="HYDROLOGY_BRIDGE">Hydrology Bridge</option>
              </select>
            </div>
          </div>

          <!-- History Table -->
          <div class="overflow-x-auto rounded-xl border border-slate-800">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-900 text-slate-400 font-bold border-b border-slate-800 text-[11px]">
                <tr>
                  <th class="py-3 px-3">Timestamp</th>
                  <th class="py-3 px-3">Water Level (m)</th>
                  <th class="py-3 px-3">Prediction</th>
                  <th class="py-3 px-3">Probability</th>
                  <th class="py-3 px-3">Risk Level</th>
                  <th class="py-3 px-3">Escalation</th>
                  <th class="py-3 px-3">Source</th>
                  <th class="py-3 px-3">Status</th>
                </tr>
              </thead>
              <tbody id="tbl-full-history-body" class="divide-y divide-slate-800 font-medium text-slate-200">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 5: SIMULATION SANDBOX -->
      <!-- ========================================================================= -->
      <div id="page-simulation" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-6 shadow-xl space-y-6">
          <div class="border-b border-slate-800 pb-3 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400">
                <i data-lucide="sliders" class="w-6 h-6"></i>
              </div>
              <div>
                <h3 class="text-base font-extrabold text-white">Operator Simulation Sandbox</h3>
                <p class="text-xs text-slate-400">Test how FloodSense AI evaluates real-time flood risk under hypothetical river levels.</p>
              </div>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-950 text-amber-300 border border-amber-800">
              DEMO REPLAY / SANDBOX
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Left Slider Controls -->
            <div class="bg-[#04142d] border border-slate-800 rounded-2xl p-5 space-y-4">
              <div class="flex justify-between items-center">
                <span class="text-xs font-bold text-slate-300">Simulated Gauge Height:</span>
                <span id="page-sim-level-display" class="font-mono text-2xl font-black text-blue-400">59.80 m</span>
              </div>
              
              <input type="range" id="page-sim-level-slider" min="50.0" max="63.0" step="0.1" value="59.8" oninput="updatePageSimSlider(this.value)" class="w-full accent-blue-600 cursor-pointer h-2 bg-slate-700 rounded-lg" />
              
              <div class="flex justify-between text-[10px] text-slate-400">
                <span>50.0m (Safe)</span>
                <span>58.0m (Warning)</span>
                <span>60.0m (Danger)</span>
                <span>63.0m (Critical)</span>
              </div>

              <div class="pt-4 flex gap-3">
                <button onclick="resetSimSlider()" class="flex-1 py-2.5 rounded-xl text-xs font-semibold text-slate-300 bg-slate-800 hover:bg-slate-700 transition-all">Reset</button>
                <button onclick="executePageSimulation()" id="btn-page-run-sim" class="flex-1 py-2.5 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-md transition-all">Run AI Inference</button>
              </div>
            </div>

            <!-- Right Live AI Output -->
            <div class="bg-[#04142d] border border-slate-800 rounded-2xl p-5 space-y-3">
              <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-400">AI Evaluation Result:</h4>
              
              <div class="space-y-2 text-xs">
                <div class="flex justify-between items-center p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span class="text-slate-400">Prediction Label:</span>
                  <span id="page-sim-pred-label" class="font-bold text-red-400">HIGH WATER</span>
                </div>
                <div class="flex justify-between items-center p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span class="text-slate-400">Model Probability:</span>
                  <span id="page-sim-prob" class="font-mono font-bold text-white">98%</span>
                </div>
                <div class="flex justify-between items-center p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span class="text-slate-400">Risk Level:</span>
                  <span id="page-sim-risk" class="font-black text-red-400">CRITICAL</span>
                </div>
                <div class="flex justify-between items-center p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span class="text-slate-400">Escalation:</span>
                  <span id="page-sim-escalation" class="font-bold text-amber-300">STATE</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 6: HOW IT WORKS -->
      <!-- ========================================================================= -->
      <div id="page-how-it-works" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-6 shadow-xl space-y-6">
          <div>
            <h3 class="text-base font-extrabold text-white">5-Stage Early Warning Pipeline</h3>
            <p class="text-xs text-slate-400">How FloodSense AI monitors river-level telemetry and predicts flood danger 6 hours ahead.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-5 gap-4 text-center">
            <div class="p-4 rounded-xl bg-[#04142d] border border-slate-800 flex flex-col items-center">
              <div class="w-10 h-10 rounded-full bg-blue-600/20 text-cyan-400 flex items-center justify-center font-black text-sm mb-2">1</div>
              <h5 class="text-xs font-bold text-white">1. Ingest</h5>
              <p class="text-[11px] text-slate-400 mt-1">Water level telemetry is received from NWDP or Copernicus GloFAS bridge.</p>
            </div>

            <div class="p-4 rounded-xl bg-[#04142d] border border-slate-800 flex flex-col items-center">
              <div class="w-10 h-10 rounded-full bg-blue-600/20 text-cyan-400 flex items-center justify-center font-black text-sm mb-2">2</div>
              <h5 class="text-xs font-bold text-white">2. Engineer</h5>
              <p class="text-[11px] text-slate-400 mt-1">Calculates 19 temporal hydrological signals (lags, rolling stats & trends).</p>
            </div>

            <div class="p-4 rounded-xl bg-[#04142d] border border-slate-800 flex flex-col items-center">
              <div class="w-10 h-10 rounded-full bg-blue-600/20 text-cyan-400 flex items-center justify-center font-black text-sm mb-2">3</div>
              <h5 class="text-xs font-bold text-white">3. Predict</h5>
              <p class="text-[11px] text-slate-400 mt-1">Random Forest (200 Trees) evaluates 6h high-water probability.</p>
            </div>

            <div class="p-4 rounded-xl bg-[#04142d] border border-slate-800 flex flex-col items-center">
              <div class="w-10 h-10 rounded-full bg-blue-600/20 text-cyan-400 flex items-center justify-center font-black text-sm mb-2">4</div>
              <h5 class="text-xs font-bold text-white">4. Assess</h5>
              <p class="text-[11px] text-slate-400 mt-1">Prediction is converted into a clear risk level: Low / Moderate / High / Critical.</p>
            </div>

            <div class="p-4 rounded-xl bg-[#04142d] border border-slate-800 flex flex-col items-center">
              <div class="w-10 h-10 rounded-full bg-blue-600/20 text-cyan-400 flex items-center justify-center font-black text-sm mb-2">5</div>
              <h5 class="text-xs font-bold text-white">5. Act</h5>
              <p class="text-[11px] text-slate-400 mt-1">Actionable recommendations are escalated to local and state authorities.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 7: SYSTEM DETAILS -->
      <!-- ========================================================================= -->
      <div id="page-system-details" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-6 shadow-xl space-y-6">
          <div>
            <h3 class="text-base font-extrabold text-white">Technical Specification & Model Audits</h3>
            <p class="text-xs text-slate-400">Verified hyperparameters, feature engineering set, and SQL Server backend specifications.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="p-5 rounded-2xl bg-[#04142d] border border-slate-800 space-y-2">
              <h4 class="text-xs font-bold uppercase text-slate-400">AI MODEL BENCHMARK</h4>
              <div class="text-sm font-bold text-white">Random Forest Classifier (200 Trees)</div>
              <div class="text-xs text-slate-300 space-y-1.5 pt-2">
                <div class="flex justify-between"><span>Test Accuracy:</span><span class="font-bold text-emerald-400">98.56%</span></div>
                <div class="flex justify-between"><span>Test Precision:</span><span class="font-bold text-emerald-400">98.36%</span></div>
                <div class="flex justify-between"><span>Test Recall:</span><span class="font-bold text-emerald-400">99.92%</span></div>
                <div class="flex justify-between"><span>Test F1-Score:</span><span class="font-bold text-emerald-400">0.9913</span></div>
              </div>
            </div>

            <div class="p-5 rounded-2xl bg-[#04142d] border border-slate-800 space-y-2">
              <h4 class="text-xs font-bold uppercase text-slate-400">19 TEMPORAL HYDROLOGICAL FEATURES</h4>
              <div class="text-xs text-slate-300 space-y-1">
                <div>• Current Water Level (Stage)</div>
                <div>• Month, Hour, DayOfYear</div>
                <div>• 5 Time Lags (1h, 3h, 6h, 12h, 24h)</div>
                <div>• 5 Rolling Stats (6h, 12h, 24h Mean/Min/Max/Std)</div>
                <div>• 5 Trend Rates of Change (1h, 3h, 6h, 12h, 24h)</div>
              </div>
            </div>

            <div class="p-5 rounded-2xl bg-[#04142d] border border-slate-800 space-y-2">
              <h4 class="text-xs font-bold uppercase text-slate-400">BACKEND & DATABASE</h4>
              <div class="text-xs text-slate-300 space-y-1">
                <div>• <strong>Framework:</strong> FastAPI (Python 3.13)</div>
                <div>• <strong>Database:</strong> Microsoft SQL Server (SQL EXPRESS)</div>
                <div>• <strong>Database Name:</strong> FloodSenseDB</div>
                <div>• <strong>Deduplication:</strong> UNIQUE (station, timestamp, source)</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- PAGE 8: SETTINGS -->
      <!-- ========================================================================= -->
      <div id="page-settings" class="app-page p-5 space-y-4 max-w-[1600px] w-full mx-auto hidden">
        <div class="bg-[#071A31] border border-[#183452] rounded-2xl p-6 shadow-xl space-y-5">
          <h3 class="text-base font-extrabold text-white">Operator Configuration & Pilot Settings</h3>
          <div class="space-y-3 text-xs text-slate-300">
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
              <span>Active Pilot Region:</span>
              <span class="font-bold text-white">Darrang, Assam (Brahmaputra Basin)</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
              <span>Primary Station:</span>
              <span class="font-bold text-white">NH15 Crossing Fakirpara Tangni (26.5083° N, 92.1164° E)</span>
            </div>
            <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 flex justify-between items-center">
              <span>Operator Role:</span>
              <span class="font-bold text-emerald-400">DEOC Duty Officer (Authorized)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- BOTTOM GLOBAL FOOTER STRIP -->
      <footer class="mt-auto bg-[#020712] border-t border-[#183452] py-3 px-6 text-[11px] text-slate-400">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-1.5"><i data-lucide="clock" class="w-3.5 h-3.5 text-blue-400"></i><span>Predict floods within 6 hours</span></div>
          <div class="flex items-center gap-1.5"><i data-lucide="brain" class="w-3.5 h-3.5 text-purple-400"></i><span>Explain risk with clear reasons</span></div>
          <div class="flex items-center gap-1.5"><i data-lucide="activity" class="w-3.5 h-3.5 text-cyan-400"></i><span>Verify with real data & trends</span></div>
          <div class="flex items-center gap-1.5"><i data-lucide="bell" class="w-3.5 h-3.5 text-red-400"></i><span>Act with timely alerts</span></div>
          <div class="flex items-center gap-1.5"><i data-lucide="users" class="w-3.5 h-3.5 text-emerald-400"></i><span>Protect communities, save lives</span></div>
        </div>
      </footer>

    </div>

  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: ABOUT FLOODSENSE AI -->
  <!-- ========================================================================= -->
  <div id="modal-about" class="fixed inset-0 bg-black/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[#071A31] border border-[#183452] rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4 animate-fade-in text-slate-200">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-blue-600/30 flex items-center justify-center text-cyan-300">
            <i data-lucide="info" class="w-4 h-4"></i>
          </div>
          <h3 class="text-sm font-bold text-white">About FloodSense AI</h3>
        </div>
        <button onclick="closeAboutModal()" class="text-slate-400 hover:text-white">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs leading-relaxed text-slate-300">
        <p>
          <strong>FloodSense AI</strong> is an enterprise-grade hydrological intelligence system specifically architected for the flash-flood vulnerable river catchments of the Brahmaputra Basin.
        </p>
        <p>
          By combining live ground telemetry from the National Water Development Project (NWDP) with high-resolution temporal lag engineering and 200-Tree Random Forest classification, FloodSense forecasts high-water conditions <strong>6 hours in advance</strong> with a verified 98.56% test accuracy.
        </p>
        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="text-[10px] text-slate-400 font-bold uppercase">MVP Pilot Deployment</div>
          <div class="text-cyan-300 font-semibold">Darrang District, Assam</div>
          <div class="text-slate-400 text-[11px]">Primary Station: NH15 Crossing Fakirpara Tangni</div>
        </div>
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closeAboutModal()" class="px-5 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: FEATURES OVERVIEW -->
  <!-- ========================================================================= -->
  <div id="modal-features" class="fixed inset-0 bg-black/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[#071A31] border border-[#183452] rounded-3xl max-w-xl w-full p-6 shadow-2xl space-y-4 animate-fade-in text-slate-200">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-cyan-600/30 flex items-center justify-center text-cyan-300">
            <i data-lucide="layers" class="w-4 h-4"></i>
          </div>
          <h3 class="text-sm font-bold text-white">FloodSense Core Features</h3>
        </div>
        <button onclick="closeFeaturesModal()" class="text-slate-400 hover:text-white">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="flex items-center gap-1.5 text-blue-400 font-bold">
            <i data-lucide="radio" class="w-3.5 h-3.5"></i>
            <span>Real-Time Telemetry</span>
          </div>
          <p class="text-slate-400 text-[11px]">Continuous stage observation with dual failover resilience.</p>
        </div>

        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="flex items-center gap-1.5 text-cyan-400 font-bold">
            <i data-lucide="cpu" class="w-3.5 h-3.5"></i>
            <span>6-Hour ML Forecast</span>
          </div>
          <p class="text-slate-400 text-[11px]">200-Tree Random Forest trained on 19 temporal hydrological signals.</p>
        </div>

        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="flex items-center gap-1.5 text-amber-400 font-bold">
            <i data-lucide="shield-alert" class="w-3.5 h-3.5"></i>
            <span>XAI Explainability</span>
          </div>
          <p class="text-slate-400 text-[11px]">Clear, human-readable rationale behind every risk escalation.</p>
        </div>

        <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
          <div class="flex items-center gap-1.5 text-emerald-400 font-bold">
            <i data-lucide="database" class="w-3.5 h-3.5"></i>
            <span>Enterprise SQL Server</span>
          </div>
          <p class="text-slate-400 text-[11px]">Full history audit log with unique constraint deduplication.</p>
        </div>
      </div>

      <div class="pt-2 flex justify-end">
        <button onclick="closeFeaturesModal()" class="px-5 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500">
          Close
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: OPERATOR SIGN IN -->
  <!-- ========================================================================= -->
  <div id="modal-signin" class="fixed inset-0 bg-black/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[#071A31] border border-[#183452] rounded-3xl max-w-sm w-full p-6 shadow-2xl space-y-5 animate-fade-in text-center">
      <div class="w-12 h-12 rounded-full bg-blue-600/20 border border-blue-500/40 mx-auto flex items-center justify-center text-blue-400">
        <i data-lucide="shield" class="w-6 h-6"></i>
      </div>

      <div class="space-y-1">
        <h3 class="text-base font-bold text-white">Operator Authentication</h3>
        <p class="text-xs text-slate-400">DEOC Darrang Early Warning Session</p>
      </div>

      <div class="p-3 rounded-xl bg-slate-900 border border-slate-800 text-left text-xs space-y-1">
        <div class="text-[10px] text-slate-400 uppercase font-bold">Authorized Role</div>
        <div class="text-emerald-400 font-bold">District Emergency Operation Centre (DEOC)</div>
        <div class="text-[11px] text-slate-400">Jurisdiction: Darrang District, Assam</div>
      </div>

      <div class="space-y-2">
        <button onclick="confirmSignInAndEnter()" class="w-full py-3 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-md flex items-center justify-center gap-2">
          <span>Enter Command Center</span>
          <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
        </button>
        <button onclick="closeSignInModal()" class="w-full py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white">
          Cancel
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: ALERT DETAIL DRAWER / INSPECTION -->
  <!-- ========================================================================= -->
  <div id="modal-alert-detail" class="fixed inset-0 bg-black/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[#071A31] border border-[#183452] rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4 animate-fade-in text-slate-200">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-red-600/30 flex items-center justify-center text-red-400">
            <i data-lucide="alert-octagon" class="w-5 h-5 animate-pulse"></i>
          </div>
          <div>
            <h3 class="text-sm font-bold text-white">CRITICAL FLOOD ALERT</h3>
            <p class="text-[10px] text-slate-400">Incident Reference: #ALT-2026-0828-99</p>
          </div>
        </div>
        <button onclick="closeAlertDetailModal()" class="text-slate-400 hover:text-white">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-3 text-xs">
        <div class="grid grid-cols-2 gap-2">
          <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
            <div class="text-[10px] text-slate-400">Station</div>
            <div class="font-bold text-white text-xs mt-0.5">NH15 Crossing Fakirpara Tangni</div>
          </div>
          <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
            <div class="text-[10px] text-slate-400">Location</div>
            <div class="font-bold text-white text-xs mt-0.5">Darrang, Assam</div>
          </div>
        </div>

        <div class="p-3 rounded-xl bg-red-950/60 border border-red-800/80 space-y-1.5">
          <div class="flex justify-between items-center">
            <span class="text-red-300 font-bold">Prediction: HIGH WATER within 6 hours</span>
            <span class="px-2 py-0.5 rounded bg-red-600 text-white font-black text-[10px]">99% PROB</span>
          </div>
          <div class="text-[11px] text-slate-300">
            Risk: <strong class="text-red-400">CRITICAL</strong> | Escalation: <strong class="text-amber-300">STATE</strong>
          </div>
        </div>

        <div class="space-y-1">
          <div class="text-[10px] text-slate-400 font-bold uppercase">Recommended Action:</div>
          <p class="text-slate-300 bg-slate-900 p-2.5 rounded-xl border border-slate-800 leading-relaxed">
            Authorities should increase monitoring and prepare for possible flood conditions. Deploy DEOC rapid response units to low-lying embankment sectors.
          </p>
        </div>
      </div>

      <div class="pt-2 flex justify-between gap-2">
        <button onclick="navigateAppPage('map'); closeAlertDetailModal();" class="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 text-cyan-300 hover:bg-slate-700">
          View on Map
        </button>
        <button onclick="closeAlertDetailModal()" class="px-5 py-2 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500">
          Acknowledge & Close
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: LOGOUT CONFIRMATION -->
  <!-- ========================================================================= -->
  <div id="modal-logout" class="fixed inset-0 bg-black/75 backdrop-blur-xs z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-[#071A31] border border-[#183452] rounded-3xl max-w-sm w-full p-6 shadow-2xl space-y-4 animate-fade-in text-center">
      <div class="w-12 h-12 rounded-full bg-red-600/20 border border-red-500/40 mx-auto flex items-center justify-center text-red-400">
        <i data-lucide="log-out" class="w-6 h-6"></i>
      </div>

      <div class="space-y-1">
        <h3 class="text-base font-bold text-white">Log Out Confirmation</h3>
        <p class="text-xs text-slate-300">You have been logged out of the DEOC Darrang Command Center. Session preferences have been cleared.</p>
      </div>

      <div class="space-y-2 pt-2">
        <button onclick="confirmLogoutAndReturn()" class="w-full py-3 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 shadow-md">
          Go to Landing Page
        </button>
        <button onclick="closeLogoutModal()" class="w-full py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white">
          Cancel
        </button>
      </div>
    </div>
  </div>

  <!-- Load Main JavaScript Application -->
  <script src="app.js"></script>
</body>
</html>
'''

# 2. frontend/styles.css
css_content = '''/* FloodSense AI Locked Theme Styles */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

body {
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Custom Scrollbars for Dark Shell */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #031226;
}
::-webkit-scrollbar-thumb {
  background: #183452;
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: #2563eb;
}

/* Leaflet Container styling */
.leaflet-container {
  font-family: inherit;
  background: #031226;
}
'''

# 3. frontend/app.js
js_content = r'''// FloodSense AI — Multi-Screen Engine with Route Persistence & Interaction Suite

let trendChart = null;
let stationMap = null;
let regionalMap = null;
let currentTrendHours = 24;
let fullHistoryData = [];
let unreadAlertsCount = 3;

// Helper: Format technical underscores into clean human text
function formatLabel(str) {
  if (!str) return '';
  return str.replace(/_/g, ' ').toUpperCase();
}

// Initial Mock Fallback State
const initialData = {
  station: "NH15 Crossing Fakirpara Tangni",
  district: "Darrang",
  state: "Assam",
  data_source: "HYDROLOGY_BRIDGE",
  data_mode: "DERIVED_HYDROLOGY",
  timestamp: "2026-08-28T20:00:00",
  current_water_level: 60.31,
  prediction: 1,
  prediction_label: "HIGH WATER",
  probability: 0.99,
  risk_level: "CRITICAL",
  escalation_level: "STATE",
  status: "ACTIVE"
};

const initialHistory = [
  { timestamp: "2026-08-28T14:00:00", current_water_level: 60.18, prediction: 1, prediction_label: "HIGH WATER", probability: 0.92, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T15:00:00", current_water_level: 60.22, prediction: 1, prediction_label: "HIGH WATER", probability: 0.95, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T16:00:00", current_water_level: 60.28, prediction: 1, prediction_label: "HIGH WATER", probability: 0.96, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T17:00:00", current_water_level: 60.32, prediction: 1, prediction_label: "HIGH WATER", probability: 0.98, risk_level: "HIGH", escalation_level: "DISTRICT", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T18:00:00", current_water_level: 60.32, prediction: 1, prediction_label: "HIGH WATER", probability: 0.99, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T19:00:00", current_water_level: 60.32, prediction: 1, prediction_label: "HIGH WATER", probability: 0.99, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" },
  { timestamp: "2026-08-28T20:00:00", current_water_level: 60.31, prediction: 1, prediction_label: "HIGH WATER", probability: 0.99, risk_level: "CRITICAL", escalation_level: "STATE", data_source: "HYDROLOGY_BRIDGE", status: "ACTIVE" }
];

// App Initialization & URL Hash Route Detection
document.addEventListener('DOMContentLoaded', () => {
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
    // If accessing protected app page, ensure session location exists or default to Darrang
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
  window.location.hash = pageId;
}

function setActiveAppPage(pageId) {
  // Hide all pages
  document.querySelectorAll('.app-page').forEach(p => p.classList.add('hidden'));
  
  // Reset all nav items to inactive
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.remove('active', 'bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-600/30');
    n.classList.add('text-slate-300');
  });

  const targetPage = document.getElementById(`page-${pageId}`);
  const targetNav = document.getElementById(`nav-${pageId}`);

  if (targetPage) {
    targetPage.classList.remove('hidden');
    targetPage.classList.add('animate-fade-in');
  }

  if (targetNav) {
    targetNav.classList.add('active', 'bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-600/30');
    targetNav.classList.remove('text-slate-300');
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
  if (submenu.classList.contains('hidden')) {
    submenu.classList.remove('hidden');
    chevron.style.transform = 'rotate(180deg)';
  } else {
    submenu.classList.add('hidden');
    chevron.style.transform = 'rotate(0deg)';
  }
}

function showDifferentLocationNotice() {
  document.getElementById('diff-location-box').classList.remove('hidden');
}

function hideDifferentLocationNotice() {
  document.getElementById('diff-location-box').classList.add('hidden');
}

// Modals: About, Features, Sign In, Alerts, Logout
function openAboutModal() {
  document.getElementById('modal-about').classList.remove('hidden');
}
function closeAboutModal() {
  document.getElementById('modal-about').classList.add('hidden');
}

function openFeaturesModal() {
  document.getElementById('modal-features').classList.remove('hidden');
}
function closeFeaturesModal() {
  document.getElementById('modal-features').classList.add('hidden');
}

function openSignInModal() {
  document.getElementById('modal-signin').classList.remove('hidden');
}
function closeSignInModal() {
  document.getElementById('modal-signin').classList.add('hidden');
}
function confirmSignInAndEnter() {
  closeSignInModal();
  confirmLocationAndEnter();
}

function openAlertDetailModal(alertId) {
  document.getElementById('modal-alert-detail').classList.remove('hidden');
  if (unreadAlertsCount > 1) {
    unreadAlertsCount = 2;
    document.getElementById('sidebar-alert-badge').innerText = unreadAlertsCount;
    document.getElementById('alerts-count-badge').innerText = `${unreadAlertsCount} ACTIVE ALERTS`;
  }
}
function closeAlertDetailModal() {
  document.getElementById('modal-alert-detail').classList.add('hidden');
}

function promptLogout() {
  document.getElementById('modal-logout').classList.remove('hidden');
}
function closeLogoutModal() {
  document.getElementById('modal-logout').classList.add('hidden');
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
    console.warn('Live fetch warning (using verified local state):', err);
  } finally {
    if (btnRefresh) {
      btnRefresh.classList.remove('animate-spin');
    }
  }
}

// Update View from Data
function updateCurrentView(data) {
  document.getElementById('hdr-station').innerText = data.station || 'NH15 Crossing Fakirpara Tangni';
  document.getElementById('hdr-district').innerText = `${data.district || 'Darrang'}, ${data.state || 'Assam'}`;
  
  if (data.timestamp) {
    const d = new Date(data.timestamp);
    const timeStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    document.getElementById('hdr-timestamp').innerText = timeStr;
    document.getElementById('card-updated-time').innerText = `Observed: ${String(d.getHours()).padStart(2, '0')}:00`;
  }

  // Hero Card
  const risk = (data.risk_level || 'LOW').toUpperCase();
  document.getElementById('hero-risk-level').innerText = risk;
  
  const probPercent = Math.round((data.probability || 0) * 100);
  document.getElementById('hero-prob-val').innerText = `${probPercent}%`;
  document.getElementById('hero-pred-label').innerText = formatLabel(data.prediction_label) || 'HIGH WATER';

  const offset = 201.06 - (201.06 * (data.probability || 0));
  const probCircle = document.getElementById('prob-circle');
  if (probCircle) probCircle.style.strokeDashoffset = offset;

  // Water Level
  const wl = data.current_water_level !== null ? Number(data.current_water_level).toFixed(2) : '60.31';
  document.getElementById('card-water-level').innerText = wl;
  document.getElementById('card-prediction-label').innerText = formatLabel(data.prediction_label) || 'HIGH WATER';

  // Data Source
  const srcTitle = document.getElementById('src-title');
  const srcSubtitle = document.getElementById('src-subtitle');
  if (data.data_source === 'NWDP') {
    srcTitle.innerText = 'NWDP WATER-LEVEL DATA';
    srcSubtitle.innerText = 'Government ground telemetry';
  } else {
    srcTitle.innerText = 'HYDROLOGY BRIDGE';
    srcSubtitle.innerText = 'Derived Hydrology';
  }

  if (window.lucide) {
    lucide.createIcons();
  }
}

// Leaflet Map on Dashboard
function initStationMap() {
  const container = document.getElementById('stationMap');
  if (!container || stationMap) return;

  const lat = 26.5083;
  const lon = 92.1164;

  stationMap = L.map('stationMap', {
    center: [lat, lon],
    zoom: 13,
    zoomControl: false
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OSM'
  }).addTo(stationMap);

  const marker = L.marker([lat, lon]).addTo(stationMap);
  marker.bindPopup('<b>NH15 Crossing Fakirpara Tangni</b><br>Darrang, Assam').openPopup();
}

// Leaflet Map on Map View Page (Regional Overview)
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
    attribution: '© OpenStreetMap'
  }).addTo(regionalMap);

  // Critical Darrang Circle Marker
  const darrangCircle = L.circle([26.5083, 92.1164], {
    color: '#EF233C',
    fillColor: '#EF233C',
    fillOpacity: 0.35,
    radius: 20000
  }).addTo(regionalMap);

  darrangCircle.bindPopup('<b>Darrang District — CRITICAL RISK</b><br>Station: NH15 Crossing Fakirpara Tangni<br>Prediction: High Water within 6 Hours').openPopup();

  // Neighboring Districts (Bongaigaon, Sonitpur, Nagaon)
  L.circle([26.4767, 90.5584], { color: '#22C55E', fillColor: '#22C55E', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Bongaigaon</b><br>Risk: LOW');
  L.circle([26.7271, 92.8336], { color: '#F59E0B', fillColor: '#F59E0B', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Sonitpur</b><br>Risk: MODERATE');
  L.circle([26.3464, 92.6840], { color: '#22C55E', fillColor: '#22C55E', fillOpacity: 0.2, radius: 15000 }).addTo(regionalMap).bindPopup('<b>Nagaon</b><br>Risk: LOW');
}

// Chart.js initialization
function initTrendChart() {
  const ctx = document.getElementById('trendChart');
  if (!ctx || trendChart) return;

  trendChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
      datasets: [
        {
          label: 'Water Level (m)',
          data: [57.5, 58.2, 58.9, 59.5, 60.1, 60.31],
          borderColor: '#126BFF',
          backgroundColor: 'rgba(18, 107, 255, 0.12)',
          fill: true,
          tension: 0.35,
          pointRadius: 3,
          pointHoverRadius: 6,
          pointBackgroundColor: '#126BFF',
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
          backgroundColor: '#031226',
          titleFont: { size: 11, weight: 'bold' },
          bodyFont: { size: 11 },
          padding: 8,
          cornerRadius: 8
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { font: { size: 10 }, color: '#64748b' }
        },
        y: {
          min: 56.0,
          suggestedMax: 62.0,
          grid: { color: '#f1f5f9' },
          ticks: { font: { size: 10 }, color: '#64748b' }
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
    latestPill.innerText = `● ${Number(latestVal).toFixed(2)} m`;
  }
}

function setTrendRange(hours) {
  currentTrendHours = hours;
  [6, 12, 24].forEach(h => {
    const btn = document.getElementById(`btn-range-${h}`);
    if (btn) {
      if (h === hours) {
        btn.className = 'px-2 py-0.5 rounded bg-blue-600 text-white shadow-xs font-bold';
      } else {
        btn.className = 'px-2 py-0.5 rounded hover:bg-white transition-all text-slate-600 font-semibold';
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
          No historical records found for the selected filters.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = sortedDesc.map(r => {
    const d = new Date(r.timestamp);
    const dateStr = d.toLocaleString('en-GB', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
    const risk = (r.risk_level || 'LOW').toUpperCase();

    let riskBadge = 'bg-emerald-950 text-emerald-400 border-emerald-800';
    if (risk === 'CRITICAL') riskBadge = 'bg-red-950 text-red-400 border-red-800';
    else if (risk === 'HIGH') riskBadge = 'bg-orange-950 text-orange-400 border-orange-800';
    else if (risk === 'MODERATE') riskBadge = 'bg-amber-950 text-amber-400 border-amber-800';

    const cleanPred = formatLabel(r.prediction_label);
    const cleanSource = formatLabel(r.data_source);

    return `
      <tr class="hover:bg-slate-800/60 transition-colors">
        <td class="py-3 px-3 font-mono text-slate-300">${dateStr}</td>
        <td class="py-3 px-3 font-bold text-white">${Number(r.current_water_level).toFixed(2)}</td>
        <td class="py-3 px-3 font-semibold text-purple-400">${cleanPred}</td>
        <td class="py-3 px-3 font-bold text-slate-200">${Math.round((r.probability || 0) * 100)}%</td>
        <td class="py-3 px-3"><span class="px-2 py-0.5 rounded text-[10px] font-bold border ${riskBadge}">${risk}</span></td>
        <td class="py-3 px-3 font-semibold text-slate-300">${r.escalation_level}</td>
        <td class="py-3 px-3 font-mono text-[11px] text-slate-400">${cleanSource}</td>
        <td class="py-3 px-3 text-emerald-400 font-semibold">${r.status}</td>
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

// Export CSV
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
  link.setAttribute('download', `floodsense_history_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Simulation Page Controls
function updatePageSimSlider(val) {
  document.getElementById('page-sim-level-display').innerText = `${Number(val).toFixed(2)} m`;
}

function resetSimSlider() {
  document.getElementById('page-sim-level-slider').value = 59.8;
  updatePageSimSlider(59.8);
}

async function executePageSimulation() {
  const slider = document.getElementById('page-sim-level-slider');
  const level = parseFloat(slider.value);
  const btn = document.getElementById('btn-page-run-sim');

  btn.disabled = true;
  btn.innerText = 'Evaluating AI...';

  try {
    const res = await fetch('/api/flood/predict-custom', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ water_level: level })
    });

    if (res.ok) {
      const data = await res.json();
      document.getElementById('page-sim-pred-label').innerText = formatLabel(data.prediction_label);
      document.getElementById('page-sim-prob').innerText = `${Math.round(data.probability * 100)}%`;
      document.getElementById('page-sim-risk').innerText = data.risk_level;
      document.getElementById('page-sim-escalation').innerText = data.escalation_level;
    }
  } catch (err) {
    alert('Simulation error: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.innerText = 'Run AI Inference';
  }
}
'''

Path('frontend/index.html').write_text(html_content.strip(), encoding='utf-8')
Path('frontend/styles.css').write_text(css_content.strip(), encoding='utf-8')
Path('frontend/app.js').write_text(js_content.strip(), encoding='utf-8')

print('SUCCESSFULLY_UPDATED_ALL_INTERACTIVE_MVP_UI_FILES')

print('ALL_FRONTEND_FILES_WRITTEN_SUCCESSFULLY')
