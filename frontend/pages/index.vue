<template>
<div class="bg-background text-on-surface font-body min-h-screen flex flex-col relative overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container scroll-smooth">

  <!-- ========================================================================= -->
  <!-- 1. STICKY TOP NAVIGATION BAR                                              -->
  <!-- ========================================================================= -->
  <header class="sticky top-0 w-full z-50 bg-surface/85 backdrop-blur-md border-b border-outline-variant/30 shadow-xs transition-all duration-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-12 h-14 sm:h-20 flex items-center justify-between">
      
      <!-- Logo -->
      <NuxtLink to="/" class="flex items-center gap-2 sm:gap-3 group active:scale-95 transition-transform shrink-0">
        <div class="w-8 sm:w-10 h-8 sm:h-10 rounded-xl bg-primary text-on-primary flex items-center justify-center shadow-md shadow-primary/25 group-hover:scale-105 transition-transform duration-200">
          <span class="material-symbols-outlined text-lg sm:text-2xl">all_inclusive</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="font-display font-extrabold text-lg sm:text-2xl text-primary tracking-tight">SkillLoop</span>
          <span class="text-[10px] font-label font-semibold tracking-wide bg-surface-container-high text-primary px-2 py-0.5 rounded-full border border-outline-variant/30 hidden sm:inline-block">
            Campus Edition
          </span>
        </div>
      </NuxtLink>

      <!-- Center Navigation (Desktop only) -->
      <nav class="hidden md:flex items-center gap-7 lg:gap-8 font-headline text-sm lg:text-base font-semibold">
        <button
          @click="scrollToSection('how-it-works')"
          :class="activeSection === 'how-it-works' ? 'text-primary font-bold border-b-2 border-primary pb-1' : 'text-on-surface-variant hover:text-primary pb-1'"
          class="transition-colors duration-200 cursor-pointer"
        >How It Works</button>
        <button
          @click="scrollToSection('features')"
          :class="activeSection === 'features' ? 'text-primary font-bold border-b-2 border-primary pb-1' : 'text-on-surface-variant hover:text-primary pb-1'"
          class="transition-colors duration-200 cursor-pointer"
        >Features</button>
        <button
          @click="scrollToSection('leaderboard')"
          :class="activeSection === 'leaderboard' ? 'text-primary font-bold border-b-2 border-primary pb-1' : 'text-on-surface-variant hover:text-primary pb-1'"
          class="transition-colors duration-200 cursor-pointer"
        >Leaderboard</button>
      </nav>

      <!-- Right Action Buttons -->
      <div class="flex items-center gap-2 shrink-0">
        <template v-if="currentUser">
          <NuxtLink
            to="/dashboard"
            class="px-3 sm:px-5 py-2 sm:py-2.5 rounded-xl font-headline text-xs sm:text-sm font-bold bg-primary text-on-primary shadow-md shadow-primary/20 hover:bg-primary-dim transition-all duration-200 active:scale-95 flex items-center gap-1.5 whitespace-nowrap"
          >
            <span class="material-symbols-outlined text-base">space_dashboard</span>
            <span>Dashboard</span>
          </NuxtLink>
        </template>
        <template v-else>
          <NuxtLink
            to="/login"
            class="hidden sm:block px-4 py-2 text-xs sm:text-sm font-headline font-semibold text-primary hover:bg-surface-container/60 rounded-xl transition-all active:scale-95 duration-150"
          >Login</NuxtLink>
          <NuxtLink
            to="/register"
            class="px-3 sm:px-5 py-2 sm:py-2.5 text-xs sm:text-sm font-headline font-semibold text-on-primary bg-primary hover:bg-primary-dim shadow-md shadow-primary/20 rounded-xl transition-all active:scale-95 duration-150 flex items-center gap-1"
          >
            <span class="hidden sm:inline">Get Started Free</span>
            <span class="sm:hidden">Get Started</span>
            <span class="material-symbols-outlined text-base">arrow_forward</span>
          </NuxtLink>
        </template>

        <!-- Mobile Hamburger -->
        <button
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 rounded-xl text-on-surface-variant hover:bg-surface-container transition-colors ml-1"
          :aria-expanded="mobileMenuOpen"
          aria-label="Toggle navigation"
        >
          <span class="material-symbols-outlined text-2xl">{{ mobileMenuOpen ? 'close' : 'menu' }}</span>
        </button>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <Transition name="slide-down">
      <div
        v-if="mobileMenuOpen"
        class="md:hidden bg-surface/98 backdrop-blur-xl border-t border-outline-variant/20 shadow-xl"
      >
        <div class="px-4 py-3 space-y-1">
          <button
            @click="scrollToSection('how-it-works'); mobileMenuOpen = false"
            class="w-full text-left px-4 py-3.5 rounded-2xl font-headline text-base font-semibold text-on-surface hover:text-primary hover:bg-primary/5 transition-all flex items-center gap-3"
          >
            <span class="material-symbols-outlined text-xl text-primary">info</span>
            How It Works
          </button>
          <button
            @click="scrollToSection('features'); mobileMenuOpen = false"
            class="w-full text-left px-4 py-3.5 rounded-2xl font-headline text-base font-semibold text-on-surface hover:text-primary hover:bg-primary/5 transition-all flex items-center gap-3"
          >
            <span class="material-symbols-outlined text-xl text-primary">auto_awesome</span>
            Platform Features
          </button>
          <button
            @click="scrollToSection('leaderboard'); mobileMenuOpen = false"
            class="w-full text-left px-4 py-3.5 rounded-2xl font-headline text-base font-semibold text-on-surface hover:text-primary hover:bg-primary/5 transition-all flex items-center gap-3"
          >
            <span class="material-symbols-outlined text-xl text-primary">leaderboard</span>
            Leaderboard
          </button>
          <div class="pt-3 border-t border-outline-variant/20 space-y-2 pb-2">
            <NuxtLink to="/login" @click="mobileMenuOpen = false" class="w-full block text-center px-4 py-3 rounded-2xl font-headline text-sm font-semibold text-primary border border-primary/30 hover:bg-primary/5 transition-all">
              Login to Your Account
            </NuxtLink>
            <NuxtLink to="/register" @click="mobileMenuOpen = false" class="w-full block text-center px-4 py-3.5 rounded-2xl font-headline text-sm font-bold text-on-primary bg-primary hover:bg-primary-dim shadow-md transition-all">
              🚀 Get Started Free — Zero Cost
            </NuxtLink>
          </div>
        </div>
      </div>
    </Transition>
  </header>

  <!-- ========================================================================= -->
  <!-- 2. HERO SECTION WITH AMBIENT VIDEO BACKGROUND                             -->
  <!-- ========================================================================= -->
  <section class="relative isolate min-h-[85vh] md:min-h-0 pt-10 pb-10 md:pt-20 md:pb-20 overflow-hidden flex flex-col items-center justify-center">
    
    <!-- Ambient Video Canvas (Desktop) / Gradient Fallback (Mobile) -->
    <!-- Mobile: CSS gradient is always shown. Video is mounted but hidden on mobile to save battery & avoid autoplay blocks -->
    <div class="absolute inset-0 w-full h-full overflow-hidden pointer-events-none z-0">
      <!-- Mobile-first gradient background (replaces video on small screens) -->
      <div class="absolute inset-0 md:hidden bg-gradient-to-br from-[#e8e0ff] via-[#f3eeff] to-[#ddd6f3]"></div>
      <!-- Decorative orbs for mobile (mimics video aesthetic) -->
      <div class="absolute top-1/4 left-1/4 w-48 h-48 rounded-full bg-primary/20 blur-3xl md:hidden"></div>
      <div class="absolute bottom-1/4 right-1/4 w-48 h-48 rounded-full bg-secondary/15 blur-3xl md:hidden"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-tertiary/10 blur-3xl md:hidden"></div>

      <!-- Desktop Video (hidden on mobile) -->
      <video
        ref="heroVideoRef"
        autoplay
        loop
        muted
        :muted="true"
        playsinline
        preload="auto"
        class="hidden md:block w-full h-full object-cover object-center pointer-events-none opacity-90"
        @error="handleVideoError"
      >
        <source src="/hero-loop.mp4" type="video/mp4" />
      </video>
    </div>

    <!-- Soft Central Sheen & Seamless Bottom Feather into Page -->
    <div class="absolute inset-0 bg-white/25 pointer-events-none z-1"></div>
    <div class="absolute bottom-0 inset-x-0 h-36 bg-gradient-to-b from-transparent via-[#fbf4ff]/80 to-[#fbf4ff] pointer-events-none z-2"></div>

    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-12 text-center relative z-10 flex flex-col items-center">
      
      <!-- Badges Row -->
      <div class="flex flex-wrap items-center justify-center gap-2 mb-5">
        <!-- Video Play/Pause badge (hidden on mobile since no video) -->
        <button
          @click="toggleVideoPlay"
          class="hidden md:inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-label font-medium text-primary bg-white/90 shadow-sm border border-outline-variant/30 backdrop-blur-md hover:bg-white transition-all cursor-pointer"
          title="Click to play/pause background video"
        >
          <span class="w-2 h-2 rounded-full" :class="isVideoPlaying ? 'bg-emerald-500 animate-ping' : 'bg-amber-500'"></span>
          <span class="material-symbols-outlined text-sm">{{ isVideoPlaying ? 'videocam' : 'videocam_off' }}</span>
          <span>{{ isVideoPlaying ? 'Ambient Motion Video Active' : 'Motion Background Paused' }}</span>
        </button>

        <div class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-label font-semibold text-secondary-dim bg-white/80 md:bg-secondary-fixed/50 border border-outline-variant/40 shadow-xs backdrop-blur-sm">
          <span class="material-symbols-outlined text-sm text-secondary">auto_awesome</span>
          <span>Zero Cash Needed • 100% Peer-to-Peer</span>
        </div>
      </div>

      <!-- Headline -->
      <h1 class="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-headline font-extrabold text-on-surface tracking-tight leading-[1.1] max-w-4xl mb-5 px-2 sm:px-0">
        Trade What You Know.
        <br/>
        <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#543ce0] via-[#7c3aed] to-[#a855f7]">
          Learn What You Want.
        </span>
      </h1>

      <!-- Subheadline -->
      <p class="text-sm sm:text-lg md:text-xl text-on-surface-variant max-w-2xl font-body leading-relaxed mb-8 px-2 sm:px-0">
        <span class="hidden sm:inline">The decentralized campus skill marketplace. Connect with verified university peers to learn any skill, share your passions, and grow together—</span>
        <span class="sm:hidden">Connect with verified campus peers to swap skills and grow together—</span>
        zero money exchanged.
      </p>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto mb-10 max-w-sm sm:max-w-none mx-auto px-4 sm:px-0">
        <NuxtLink
          :to="currentUser ? '/dashboard' : '/register'"
          class="w-full sm:w-auto px-7 py-3.5 sm:py-4 rounded-xl bg-gradient-to-r from-primary to-secondary text-on-primary font-headline font-bold text-sm sm:text-base shadow-lg shadow-primary/30 hover:shadow-primary/45 hover:scale-[1.02] active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 group"
        >
          <span>{{ currentUser ? 'Open Your Dashboard' : 'Start Swapping Skills' }}</span>
          <span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform">arrow_forward</span>
        </NuxtLink>

        <button
          @click="scrollToSection('how-it-works')"
          class="w-full sm:w-auto px-6 py-3.5 sm:py-4 rounded-xl bg-white/80 backdrop-blur-md text-on-surface font-headline font-semibold text-sm sm:text-base hover:bg-white/95 border border-outline-variant/40 shadow-sm hover:scale-[1.02] active:scale-95 transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer"
        >
          <span class="material-symbols-outlined text-primary text-xl">play_circle</span>
          <span>How It Works</span>
        </button>
      </div>

      <!-- Verified Metric Bar Strip -->
      <div class="w-full max-w-sm sm:max-w-4xl bg-white/85 backdrop-blur-md rounded-2xl p-4 sm:p-5 border border-white/90 shadow-sm grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-6 text-center">
        <div class="flex flex-col items-center">
          <span class="text-2xl sm:text-3xl font-headline font-extrabold text-primary">2,400+</span>
          <span class="text-xs sm:text-sm font-label text-on-surface-variant font-medium mt-0.5">Swaps Completed</span>
        </div>
        <div class="flex flex-col items-center border-l border-outline-variant/20">
          <span class="text-2xl sm:text-3xl font-headline font-extrabold text-secondary">98%</span>
          <span class="text-xs sm:text-sm font-label text-on-surface-variant font-medium mt-0.5">5-Star Reviews</span>
        </div>
        <div class="flex flex-col items-center border-l md:border-l border-outline-variant/20">
          <span class="text-2xl sm:text-3xl font-headline font-extrabold text-primary">15+</span>
          <span class="text-xs sm:text-sm font-label text-on-surface-variant font-medium mt-0.5">Universities Active</span>
        </div>
        <div class="flex flex-col items-center border-l border-outline-variant/20">
          <span class="text-2xl sm:text-3xl font-headline font-extrabold text-tertiary">100%</span>
          <span class="text-xs sm:text-sm font-label text-on-surface-variant font-medium mt-0.5">Free Peer Network</span>
        </div>
      </div>

    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- 3. HOW SKILLLOOP WORKS (3-STEP PROCESS)                                   -->
  <!-- ========================================================================= -->
  <section class="py-24 bg-surface-container-low px-4 sm:px-6 lg:px-12 relative overflow-hidden" id="how-it-works">
    <!-- Ambient subtle background circle -->
    <div class="absolute -right-32 top-1/2 -translate-y-1/2 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="max-w-7xl mx-auto">
      <div class="text-center max-w-3xl mx-auto mb-16">
        <span class="text-xs font-label font-bold tracking-widest text-primary uppercase bg-primary-container/30 px-3 py-1 rounded-full border border-primary/20">
          Seamless Campus Workflow
        </span>
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-headline font-extrabold text-on-surface tracking-tight mt-3">
          How SkillLoop Works
        </h2>
        <p class="text-on-surface-variant font-body text-base sm:text-lg mt-3">
          No credit cards. No predatory tutoring fees. Pure reciprocal knowledge transfer governed by campus trust credits.
        </p>
      </div>

      <!-- 3-Step Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
        <!-- Connecting Line for Desktop -->
        <div class="hidden md:block absolute top-1/3 left-1/6 right-1/6 h-0.5 border-t-2 border-dashed border-outline-variant/50 -z-0"></div>

        <!-- Step 1 -->
        <div class="bg-surface-container-lowest rounded-3xl p-8 border border-outline-variant/30 shadow-xs hover:shadow-lg transition-all duration-300 relative z-10 flex flex-col items-start group">
          <div class="w-14 h-14 rounded-2xl bg-primary text-on-primary flex items-center justify-center font-headline font-extrabold text-xl shadow-md shadow-primary/25 mb-6 group-hover:scale-110 transition-transform">
            1
          </div>
          <span class="text-xs font-label font-bold text-primary uppercase tracking-wider mb-1">Step One</span>
          <h3 class="text-xl font-headline font-bold text-on-surface mb-3">List Your Skillset</h3>
          <p class="text-on-surface-variant text-sm font-body leading-relaxed mb-6">
            Input what you can comfortably coach (e.g. Python coding, Figma design, Conversational French) and the skills you want to learn.
          </p>
          <div class="mt-auto w-full p-3 rounded-xl bg-surface-container-low border border-outline-variant/30 flex items-center justify-between text-xs font-label">
            <span class="text-on-surface font-semibold">1 Credit Allocated Free</span>
            <span class="text-emerald-700 font-bold">Auto-assigned</span>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="bg-surface-container-lowest rounded-3xl p-8 border border-outline-variant/30 shadow-xs hover:shadow-lg transition-all duration-300 relative z-10 flex flex-col items-start group">
          <div class="w-14 h-14 rounded-2xl bg-secondary text-on-secondary flex items-center justify-center font-headline font-extrabold text-xl shadow-md shadow-secondary/25 mb-6 group-hover:scale-110 transition-transform">
            2
          </div>
          <span class="text-xs font-label font-bold text-secondary uppercase tracking-wider mb-1">Step Two</span>
          <h3 class="text-xl font-headline font-bold text-on-surface mb-3">Instant Peer Match &amp; AI Quiz</h3>
          <p class="text-on-surface-variant text-sm font-body leading-relaxed mb-6">
            Take a 5-minute diagnostic micro-quiz generated by AI to earn your verified badge. Our algorithmic matching connects you with students with symmetric mutual learning goals.
          </p>
          <div class="mt-auto w-full p-3 rounded-xl bg-surface-container-low border border-outline-variant/30 flex items-center justify-between text-xs font-label">
            <span class="text-on-surface font-semibold">Micro-Assessment</span>
            <span class="text-primary font-bold">5 Mins Avg</span>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="bg-surface-container-lowest rounded-3xl p-8 border border-outline-variant/30 shadow-xs hover:shadow-lg transition-all duration-300 relative z-10 flex flex-col items-start group">
          <div class="w-14 h-14 rounded-2xl bg-tertiary text-on-tertiary flex items-center justify-center font-headline font-extrabold text-xl shadow-md shadow-tertiary/25 mb-6 group-hover:scale-110 transition-transform">
            3
          </div>
          <span class="text-xs font-label font-bold text-tertiary uppercase tracking-wider mb-1">Step Three</span>
          <h3 class="text-xl font-headline font-bold text-on-surface mb-3">Connect &amp; Learn</h3>
          <p class="text-on-surface-variant text-sm font-body leading-relaxed mb-6">
            Hop into the high-def 1-on-1 WebRTC video hub with collaborative chat, or meet up at your student union. Once the session ends, Time Credits transfer automatically.
          </p>
          <div class="mt-auto w-full p-3 rounded-xl bg-surface-container-low border border-outline-variant/30 flex items-center justify-between text-xs font-label">
            <span class="text-on-surface font-semibold">WebRTC Protected</span>
            <span class="text-secondary font-bold">Zero Platform Cut</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- 4. PLATFORM SUPERPOWERS BENTO GRID                                        -->
  <!-- ========================================================================= -->
  <section class="py-24 bg-surface px-4 sm:px-6 lg:px-12 relative" id="features">
    <div class="max-w-7xl mx-auto">
      
      <div class="text-center max-w-3xl mx-auto mb-16">
        <span class="text-xs font-label font-bold tracking-widest text-primary uppercase bg-surface-container-high px-3 py-1 rounded-full border border-outline-variant/30">
          Engineered for Students
        </span>
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-headline font-extrabold text-on-surface tracking-tight mt-3">
          Platform Superpowers
        </h2>
        <p class="text-on-surface-variant font-body text-base sm:text-lg mt-3">
          Everything you need to verify expertise, swap without awkward friction, and translate your hours into career capital.
        </p>
      </div>

      <!-- Bento Grid (2x2 Asymmetric) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Card 1: AI-Verified Skill Badges (7 cols) -->
        <div class="lg:col-span-7 bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-outline-variant/30 shadow-xs hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mb-5">
              <span class="material-symbols-outlined text-2xl" data-icon="verified">verified</span>
            </div>
            <h3 class="text-2xl font-headline font-bold text-on-surface mb-2">AI-Verified Skill Badges</h3>
            <p class="text-on-surface-variant font-body text-sm max-w-lg mb-6 leading-relaxed">
              Skip claims without proof. Our proctored dynamic AI assessment confirms practical coding, math problem solving, or language comprehension before granting verified mentor badges.
            </p>
          </div>

          <!-- Micro-UI Mockup: Quiz Score Pill & Preview -->
          <div class="bg-surface-container-low rounded-2xl p-5 border border-outline-variant/30">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-xs font-headline font-bold text-on-surface">Data Structures &amp; Algo Test</span>
              </div>
              <span class="text-xs font-label font-bold text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-full">
                86% Score • Level 4 Granted
              </span>
            </div>
            <div class="w-full bg-outline-variant/20 rounded-full h-2 mb-4">
              <div class="bg-gradient-to-r from-primary to-emerald-500 h-2 rounded-full w-[86%]"></div>
            </div>
            <div class="flex flex-wrap items-center justify-between text-xs text-on-surface-variant font-label gap-2">
              <span>Proctored by Gemini 2.0 Evaluation Model</span>
              <span class="text-primary font-semibold flex items-center gap-1">
                <span class="material-symbols-outlined text-sm" data-icon="check_circle">check_circle</span>
                Verified on Campus Ledger
              </span>
            </div>
          </div>
        </div>

        <!-- Card 2: Peer Video Hub & Live Chat (5 cols) -->
        <div class="lg:col-span-5 bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-outline-variant/30 shadow-xs hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-secondary/10 text-secondary flex items-center justify-center mb-5">
              <span class="material-symbols-outlined text-2xl" data-icon="video_chat">video_chat</span>
            </div>
            <h3 class="text-2xl font-headline font-bold text-on-surface mb-2">Peer Video Hub &amp; Live Chat</h3>
            <p class="text-on-surface-variant font-body text-sm mb-6 leading-relaxed">
              Ultra-low latency browser WebRTC video rooms with built-in text chat, audio switching, and collaborative learning with zero downloads required.
            </p>
          </div>

          <!-- Micro-UI Mockup: Video call UI -->
          <div class="bg-inverse-surface text-surface rounded-2xl p-4 shadow-inner">
            <div class="flex items-center justify-between mb-3 border-b border-outline/30 pb-2">
              <div class="flex items-center gap-2">
                <div class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></div>
                <span class="text-xs font-label text-inverse-on-surface">1-on-1 Campus Video Hub</span>
              </div>
              <span class="text-xs font-mono text-tertiary-fixed">Live Room</span>
            </div>
            <div class="grid grid-cols-2 gap-2 mb-3">
              <div class="aspect-video bg-surface/10 rounded-lg flex items-center justify-center text-xs text-inverse-on-surface font-label border border-outline/20">
                Peer 1 (Cam On)
              </div>
              <div class="aspect-video bg-surface/10 rounded-lg flex items-center justify-center text-xs text-inverse-on-surface font-label border border-outline/20">
                Peer 2 (Cam On)
              </div>
            </div>
            <div class="flex items-center justify-center gap-3">
              <span class="p-1.5 rounded-lg bg-surface/20 hover:bg-surface/30 cursor-pointer text-xs flex items-center">
                <span class="material-symbols-outlined text-base" data-icon="mic">mic</span>
              </span>
              <span class="p-1.5 rounded-lg bg-surface/20 hover:bg-surface/30 cursor-pointer text-xs flex items-center">
                <span class="material-symbols-outlined text-base" data-icon="videocam">videocam</span>
              </span>
              <span class="p-1.5 rounded-lg bg-surface/20 hover:bg-surface/30 cursor-pointer text-xs flex items-center">
                <span class="material-symbols-outlined text-base" data-icon="screen_share">screen_share</span>
              </span>
              <span class="p-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 cursor-pointer text-xs flex items-center">
                <span class="material-symbols-outlined text-base" data-icon="call_end">call_end</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Card 3: Campus Karma & Leaderboard (5 cols) -->
        <div class="lg:col-span-5 bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-outline-variant/30 shadow-xs hover:shadow-md transition-all flex flex-col justify-between" id="leaderboard">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-700 flex items-center justify-center mb-5">
              <span class="material-symbols-outlined text-2xl" data-icon="leaderboard">leaderboard</span>
            </div>
            <h3 class="text-2xl font-headline font-bold text-on-surface mb-2">Campus Karma &amp; Leaderboard</h3>
            <p class="text-on-surface-variant font-body text-sm mb-6 leading-relaxed">
              Climb the ranks by helping fellow students. High karma unlocks priority swaps, university ambassador badges, and partner company referrals.
            </p>
          </div>

          <!-- Micro-UI Mockup: Top Mentors -->
          <div class="space-y-2 bg-surface-container-low rounded-2xl p-4 border border-outline-variant/20">
            <div class="flex items-center justify-between text-xs font-label p-2 rounded-lg bg-surface-container-lowest border border-outline-variant/20">
              <div class="flex items-center gap-2">
                <span class="font-bold text-amber-600">#1</span>
                <span class="font-headline font-bold text-on-surface">Top Campus Mentor</span>
              </div>
              <span class="font-bold text-primary">128 hrs taught</span>
            </div>
            <div class="flex items-center justify-between text-xs font-label p-2 rounded-lg bg-surface-container-lowest border border-outline-variant/20">
              <div class="flex items-center gap-2">
                <span class="font-bold text-slate-500">#2</span>
                <span class="font-headline font-bold text-on-surface">Active Peer Tutor</span>
              </div>
              <span class="font-bold text-primary">94 hrs taught</span>
            </div>
            <div class="flex items-center justify-between text-xs font-label p-2 rounded-lg bg-surface-container-lowest border border-outline-variant/20">
              <div class="flex items-center gap-2">
                <span class="font-bold text-amber-700">#3</span>
                <span class="font-headline font-bold text-on-surface">Rising Contributor</span>
              </div>
              <span class="font-bold text-primary">76 hrs taught</span>
            </div>
          </div>
        </div>

        <!-- Card 4: AI Resume Studio (7 cols) -->
        <div class="lg:col-span-7 bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-outline-variant/30 shadow-xs hover:shadow-md transition-all flex flex-col justify-between">
          <div>
            <div class="w-12 h-12 rounded-2xl bg-tertiary/10 text-tertiary flex items-center justify-center mb-5">
              <span class="material-symbols-outlined text-2xl" data-icon="description">description</span>
            </div>
            <h3 class="text-2xl font-headline font-bold text-on-surface mb-2">AI Resume Studio</h3>
            <p class="text-on-surface-variant font-body text-sm max-w-lg mb-6 leading-relaxed">
              Turn your teaching hours into tangible career results. Automatically convert your peer tutoring feedback, topic mastery, and swap volume into ATS-ready resume bullet points.
            </p>
          </div>

          <!-- Micro-UI Mockup: Resume bullet point snippet -->
          <div class="bg-surface-container-low rounded-2xl p-5 border border-outline-variant/30 space-y-3 font-body">
            <div class="flex items-center justify-between">
              <span class="text-xs font-label font-bold text-primary uppercase">Generated Bullet for Internship Applications</span>
              <button
                @click="copySnippet"
                class="text-xs font-label font-semibold text-primary hover:underline flex items-center gap-1 cursor-pointer"
              >
                <span class="material-symbols-outlined text-sm">{{ isCopied ? 'done' : 'content_copy' }}</span>
                <span>{{ isCopied ? 'Copied!' : 'Copy' }}</span>
              </button>
            </div>
            <div class="p-3 bg-surface-container-lowest rounded-xl border border-outline-variant/20 text-xs text-on-surface leading-relaxed">
              "• Conducted <strong>35+ hours of peer technical mentorship</strong> on programming &amp; system architecture; evaluated student comprehension and resolved technical blockers with a 4.95/5.0 peer satisfaction rating."
            </div>
            <div class="flex items-center gap-2 text-[11px] font-label text-on-surface-variant">
              <span class="material-symbols-outlined text-sm text-emerald-600" data-icon="lock">lock</span>
              <span>Cryptographically signed by SkillLoop Smart Campus Ledger</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- 5. HIGH-CONVERSION FINAL CALL TO ACTION                                   -->
  <!-- ========================================================================= -->
  <section class="py-20 px-4 sm:px-6 lg:px-12 bg-surface relative">
    <div class="max-w-6xl mx-auto rounded-3xl bg-gradient-to-br from-primary via-secondary to-[#482cd4] p-8 sm:p-14 text-on-primary shadow-2xl shadow-primary/30 relative overflow-hidden">
      
      <!-- Decorative background glow rings -->
      <div class="absolute -right-16 -top-16 w-80 h-80 rounded-full bg-white/10 blur-2xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-80 h-80 rounded-full bg-tertiary-container/20 blur-2xl pointer-events-none"></div>

      <div class="relative z-10 max-w-3xl mx-auto text-center">
        <span class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-xs font-label font-bold tracking-wide bg-white/15 backdrop-blur-md text-surface-bright mb-6 border border-white/20">
          <span class="material-symbols-outlined text-sm" data-icon="school">school</span>
          Over 15 Campus Chapters Open
        </span>
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-headline font-extrabold tracking-tight leading-tight mb-6">
          Ready to Learn Without Paying a Dime? <br class="hidden sm:inline"/>
          Join Your Campus Loop Today.
        </h2>
        <p class="text-surface-container-highest font-body text-base sm:text-lg mb-8 max-w-2xl mx-auto leading-relaxed">
          Sign up with your university email address. Receive an instant <strong>2-credit welcome bonus</strong> to book your very first peer session right away.
        </p>

        <!-- University Email Input form -->
        <form @submit.prevent="handleQuickSignup" class="flex flex-col sm:flex-row items-center justify-center gap-3 max-w-xl mx-auto">
          <div class="relative w-full">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant">
              <span class="material-symbols-outlined text-lg" data-icon="mail">mail</span>
            </span>
            <input
              v-model="quickEmail"
              class="w-full pl-11 pr-4 py-3.5 rounded-xl bg-white text-on-surface text-sm font-body placeholder:text-on-surface-variant/70 focus:outline-none focus:ring-2 focus:ring-tertiary-fixed shadow-md"
              placeholder="Enter your university email (.edu, .ac.in)..."
              required
              type="email"
            />
          </div>
          <button
            class="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-tertiary-fixed hover:bg-tertiary-fixed-dim text-on-tertiary-fixed font-headline font-bold text-sm whitespace-nowrap shadow-lg transition-transform active:scale-95 duration-150 flex items-center justify-center gap-1.5 cursor-pointer"
            type="submit"
          >
            <span>Claim 2 Free Credits</span>
            <span class="material-symbols-outlined text-base" data-icon="bolt">bolt</span>
          </button>
        </form>

        <p class="text-xs font-label text-surface-container-high/80 mt-4">
          Strict verification: Only enrolled students with valid campus domains (.edu, .ac.uk, .edu.in) are admitted.
        </p>
      </div>
    </div>
  </section>

  <!-- ========================================================================= -->
  <!-- 6. FOOTER                                                                 -->
  <!-- ========================================================================= -->
  <footer class="bg-surface-container-lowest border-t border-outline-variant/30 transition-colors mt-auto">
    <div class="w-full py-12 px-4 sm:px-6 lg:px-12 max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
      
      <!-- Brand & Copyright -->
      <div class="flex flex-col sm:flex-row items-center gap-4 text-center sm:text-left">
        <NuxtLink to="/" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-lg bg-primary text-on-primary flex items-center justify-center font-bold">
            <span class="material-symbols-outlined text-lg" data-icon="all_inclusive">all_inclusive</span>
          </div>
          <span class="font-display font-bold text-lg text-primary">SkillLoop</span>
        </NuxtLink>
        <span class="hidden sm:inline text-outline-variant">•</span>
        <p class="font-body text-sm text-on-surface-variant">
          &copy; 2026 SkillLoop Campus Edition. All rights reserved.
        </p>
      </div>

      <!-- Links -->
      <div class="flex flex-wrap items-center justify-center gap-6 font-body text-sm text-on-surface-variant">
        <a class="hover:text-primary transition-colors cursor-pointer" @click="scrollToSection('how-it-works')">How It Works</a>
        <a class="hover:text-primary transition-colors cursor-pointer" @click="scrollToSection('features')">Platform Features</a>
        <a class="hover:text-primary transition-colors cursor-pointer" @click="scrollToSection('leaderboard')">Campus Leaderboard</a>
      </div>
    </div>
  </footer>

</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const heroVideoRef = ref(null)
const isVideoPlaying = ref(true)
const activeSection = ref('how-it-works')
const currentUser = ref(null)
const quickEmail = ref('')
const isCopied = ref(false)
const mobileMenuOpen = ref(false)

function scrollToSection(sectionId) {
  activeSection.value = sectionId
  const el = document.getElementById(sectionId)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function toggleVideoPlay() {
  if (!heroVideoRef.value) return
  if (heroVideoRef.value.paused) {
    heroVideoRef.value.play()
    isVideoPlaying.value = true
  } else {
    heroVideoRef.value.pause()
    isVideoPlaying.value = false
  }
}

function handleVideoError() {
  console.warn('Hero background video fallback triggered.')
}

function handleQuickSignup() {
  if (!quickEmail.value) return
  navigateTo(`/register?email=${encodeURIComponent(quickEmail.value)}`)
}

function copySnippet() {
  const text = "• Conducted 35+ hours of peer technical mentorship on programming & system architecture; evaluated student comprehension and resolved technical blockers with a 4.95/5.0 peer satisfaction rating."
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      isCopied.value = true
      setTimeout(() => { isCopied.value = false }, 2500)
    })
  }
}

onMounted(() => {
  try {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      currentUser.value = JSON.parse(storedUser)
    }
  } catch (err) {
    console.error('Error reading user session:', err)
  }

  // Ensure video autoplay is properly triggered
  if (heroVideoRef.value) {
    heroVideoRef.value.muted = true
    const playPromise = heroVideoRef.value.play()
    if (playPromise !== undefined) {
      playPromise.then(() => {
        isVideoPlaying.value = true
      }).catch(err => {
        console.warn('Hero video autoplay:', err)
      })
    }
  }

  // Intersection observer to highlight current nav section
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        activeSection.value = entry.target.id
      }
    })
  }, { threshold: 0.3 })

  const sections = ['how-it-works', 'features', 'leaderboard']
  sections.forEach(id => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
})
</script>

<style scoped>
.scrollbar-none::-webkit-scrollbar {
  display: none;
}
.scrollbar-none {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
/* Mobile Drawer slide animation */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease-out;
  overflow: hidden;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
.slide-down-enter-to,
.slide-down-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
