<template>
<div class="bg-background text-on-surface font-body min-h-screen flex flex-col relative overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container scroll-smooth">

  <!-- Ambient light background circles with subtle movement -->
  <div class="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
    <div class="absolute -top-24 right-1/4 w-96 h-96 bg-secondary-fixed/35 rounded-full blur-3xl animate-pulse-glow"></div>
    <div class="absolute top-1/3 left-0 w-80 h-80 bg-surface-container-high/60 rounded-full blur-3xl"></div>
    <div class="absolute -bottom-20 right-1/3 w-[500px] h-[500px] bg-primary-fixed/20 rounded-full blur-[120px]"></div>
  </div>

  <!-- TopNavBar (Sticky with Working Section Links) -->
  <header class="sticky top-0 w-full z-50 bg-surface-bright/95 backdrop-blur-md border-b border-surface-container-high/80 shadow-xs transition-all duration-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 sm:h-20 flex items-center justify-between">
      <!-- Brand Logo -->
      <NuxtLink class="flex items-center gap-2 sm:gap-2.5 font-display text-xl sm:text-2xl font-bold tracking-tight text-primary transition-all duration-200 active:scale-95 shrink-0 group" to="/">
        <span class="w-8 sm:w-10 h-8 sm:h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm group-hover:scale-105 transition-transform duration-200">
          <span class="material-symbols-outlined text-xl sm:text-2xl" data-icon="all_inclusive">all_inclusive</span>
        </span>
        <span>SkillLoop</span>
      </NuxtLink>

      <!-- Navigation Links with Working Smooth Scroll -->
      <nav class="hidden md:flex items-center gap-8 font-headline text-sm lg:text-base font-semibold">
        <button
          @click="scrollToSection('explore')"
          :class="activeSection === 'explore' ? 'text-primary font-bold border-b-2 border-primary pb-0.5' : 'text-on-surface-variant hover:text-primary pb-0.5'"
          class="transition-colors duration-200 cursor-pointer flex items-center gap-1.5"
        >
          <span class="material-symbols-outlined text-base">explore</span>
          <span>Explore</span>
        </button>
        <button
          @click="scrollToSection('how-it-works')"
          :class="activeSection === 'how-it-works' ? 'text-primary font-bold border-b-2 border-primary pb-0.5' : 'text-on-surface-variant hover:text-primary pb-0.5'"
          class="transition-colors duration-200 cursor-pointer flex items-center gap-1.5"
        >
          <span class="material-symbols-outlined text-base">sync_alt</span>
          <span>How It Works</span>
        </button>
        <button
          @click="scrollToSection('features')"
          :class="activeSection === 'features' ? 'text-primary font-bold border-b-2 border-primary pb-0.5' : 'text-on-surface-variant hover:text-primary pb-0.5'"
          class="transition-colors duration-200 cursor-pointer flex items-center gap-1.5"
        >
          <span class="material-symbols-outlined text-base">featured_play_list</span>
          <span>Features</span>
        </button>
      </nav>

      <!-- Trailing Action Buttons -->
      <div class="flex items-center gap-2 sm:gap-3 shrink-0">
        <template v-if="currentUser">
          <NuxtLink class="px-3 sm:px-5 py-2 sm:py-2.5 rounded-xl font-headline text-xs sm:text-sm font-bold bg-primary text-on-primary shadow-sm hover:bg-primary-dim transition-all duration-200 active:scale-95 flex items-center gap-1.5 sm:gap-2 whitespace-nowrap shrink-0 hover:shadow-md" to="/dashboard">
            <span class="material-symbols-outlined text-base">space_dashboard</span>
            <span class="hidden sm:inline">Go to </span><span>Dashboard</span>
            <span class="material-symbols-outlined text-base" data-icon="arrow_forward">arrow_forward</span>
          </NuxtLink>
        </template>
        <template v-else>
          <NuxtLink class="px-3 sm:px-5 py-2 sm:py-2.5 rounded-xl font-headline text-xs sm:text-sm font-semibold text-primary border border-outline-variant hover:bg-surface-container transition-all duration-200 active:scale-95 shrink-0" to="/login">
            Login
          </NuxtLink>
          <NuxtLink class="px-3 sm:px-5 py-2 sm:py-2.5 rounded-xl font-headline text-xs sm:text-sm font-semibold bg-primary text-on-primary shadow-sm hover:bg-primary-dim transition-all duration-200 active:scale-95 flex items-center gap-1 sm:gap-1.5 shrink-0 hover:shadow-md" to="/register">
            <span>Get Started</span>
            <span class="material-symbols-outlined text-base" data-icon="arrow_forward">arrow_forward</span>
          </NuxtLink>
        </template>
      </div>
    </div>

    <!-- Mobile Sub-Nav Bar (Clean Interactive Pills) -->
    <div class="md:hidden flex items-center justify-around px-2 py-2 bg-surface-container-low/90 border-t border-surface-container-high/50 text-xs font-headline font-semibold backdrop-blur-xs">
      <button
        @click="scrollToSection('explore')"
        :class="activeSection === 'explore' ? 'text-primary bg-primary/10 font-bold' : 'text-on-surface-variant'"
        class="px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1"
      >
        <span class="material-symbols-outlined text-sm">explore</span>
        <span>Explore</span>
      </button>
      <button
        @click="scrollToSection('how-it-works')"
        :class="activeSection === 'how-it-works' ? 'text-primary bg-primary/10 font-bold' : 'text-on-surface-variant'"
        class="px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1"
      >
        <span class="material-symbols-outlined text-sm">sync_alt</span>
        <span>How It Works</span>
      </button>
      <button
        @click="scrollToSection('features')"
        :class="activeSection === 'features' ? 'text-primary bg-primary/10 font-bold' : 'text-on-surface-variant'"
        class="px-3 py-1.5 rounded-lg transition-colors cursor-pointer flex items-center gap-1"
      >
        <span class="material-symbols-outlined text-sm">featured_play_list</span>
        <span>Features</span>
      </button>
    </div>
  </header>

  <!-- Main Landing Content -->
  <main class="flex-1">

    <!-- ========================================== -->
    <!-- 1. HERO SECTION WITH ANIMATIONS & FLOATS   -->
    <!-- ========================================== -->
    <section class="relative overflow-hidden pt-10 pb-16 md:pt-16 md:pb-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-8 items-center">

          <!-- Left Text Column -->
          <div class="lg:col-span-7 flex flex-col items-start space-y-6">
            <!-- Campus Badge with Pulsing Ping -->
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container border border-surface-container-high text-primary font-label text-xs font-semibold tracking-wide shadow-2xs hover:bg-surface-container-high transition-colors">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span>Campus Peer-to-Peer Learning Network</span>
            </div>

            <!-- Headline -->
            <h1 class="font-headline text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-on-background leading-[1.12]">
              Trade what you know. <br class="hidden sm:inline"/>
              <span class="text-primary underline decoration-secondary-container decoration-wavy decoration-2 inline-block hover:scale-[1.01] transition-transform">
                Learn what you love.
              </span>
            </h1>

            <!-- Subtitle -->
            <p class="font-body text-base sm:text-lg text-on-surface-variant max-w-xl leading-relaxed">
              SkillLoop connects verified university students to swap skills 1-on-1. No cash, no awkward tutor rates — just pure, credentialed knowledge exchange.
            </p>

            <!-- Call to Actions -->
            <div class="flex flex-wrap items-center gap-4 pt-2 w-full sm:w-auto">
              <template v-if="currentUser">
                <NuxtLink class="w-full sm:w-auto inline-flex justify-center items-center gap-2 px-7 py-3.5 rounded-xl font-headline text-base font-bold bg-primary text-on-primary shadow-md hover:bg-primary-dim transition-all duration-200 active:scale-95 group" to="/dashboard">
                  <span class="material-symbols-outlined text-lg">space_dashboard</span>
                  <span>Welcome back, {{ currentUser.full_name?.split(' ')[0] || currentUser.username }} — Open Dashboard</span>
                  <span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
                </NuxtLink>
              </template>
              <template v-else>
                <NuxtLink class="w-full sm:w-auto inline-flex justify-center items-center gap-2 px-7 py-3.5 rounded-xl font-headline text-base font-bold bg-primary text-on-primary shadow-md hover:bg-primary-dim transition-all duration-200 active:scale-95 group" to="/register">
                  <span>Get Started Free</span>
                  <span class="material-symbols-outlined text-lg group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
                </NuxtLink>
                <NuxtLink class="w-full sm:w-auto inline-flex justify-center items-center px-7 py-3.5 rounded-xl font-headline text-base font-semibold border-2 border-outline-variant text-on-surface hover:bg-surface-container-low transition-all duration-200 active:scale-95" to="/login">
                  Login
                </NuxtLink>
              </template>
            </div>

            <!-- Trust proof micro-copy -->
            <div class="flex items-center gap-2 text-on-surface-variant font-label text-xs sm:text-sm pt-1">
              <span class="w-4 h-4 rounded-full bg-emerald-500/20 text-emerald-600 flex items-center justify-center font-bold text-xs">✓</span>
              <span>100% Free for college students • Verified .edu network</span>
            </div>

            <!-- Interactive Popular Skill Tags -->
            <div class="flex flex-wrap items-center gap-2 pt-2">
              <span class="text-xs font-semibold text-on-surface-variant">Popular this week:</span>
              <button
                v-for="tag in popularSkillTags"
                :key="tag.label"
                @click="filterFromTag(tag)"
                class="px-2.5 py-1 bg-surface-container hover:bg-primary hover:text-white rounded-lg text-xs font-medium text-on-surface transition-all duration-200 cursor-pointer active:scale-95 shadow-2xs hover:shadow-xs flex items-center gap-1 group"
              >
                <span>{{ tag.label }}</span>
                <span class="text-[11px] opacity-70 group-hover:opacity-100">{{ tag.icon }}</span>
              </button>
            </div>
          </div>

          <!-- Right Column: Interactive Animated Hero Composition -->
          <div class="lg:col-span-5 flex justify-center lg:justify-end relative">
            <div class="relative w-full max-w-md">

              <!-- Floating Micro-Badge 1 (Top Left) -->
              <div class="absolute -top-5 -left-5 z-20 hidden sm:flex items-center gap-2.5 px-3.5 py-2 rounded-2xl bg-white/95 backdrop-blur-md border border-primary/20 shadow-xl animate-float-slow">
                <div class="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center font-bold text-sm shrink-0">
                  <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
                </div>
                <div class="leading-tight">
                  <p class="text-xs font-bold text-on-surface">Active 1:1 Match</p>
                  <p class="text-[11px] text-primary font-semibold">Python ⇄ UI/UX</p>
                </div>
              </div>

              <!-- Floating Micro-Badge 2 (Bottom Right) -->
              <div class="absolute -bottom-5 -right-3 z-20 hidden sm:flex items-center gap-2.5 px-3.5 py-2 rounded-2xl bg-white/95 backdrop-blur-md border border-emerald-500/20 shadow-xl animate-float-delayed">
                <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center font-bold text-sm shrink-0">
                  <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">verified_user</span>
                </div>
                <div class="leading-tight">
                  <p class="text-xs font-bold text-on-surface">Verified .edu</p>
                  <p class="text-[11px] text-emerald-600 font-semibold">1 hr taught = 1 credit</p>
                </div>
              </div>

              <!-- Decorative subtle background glow card -->
              <div class="absolute -inset-2 bg-gradient-to-r from-primary-fixed to-secondary-container rounded-3xl opacity-50 blur-lg animate-pulse-glow"></div>

              <!-- Main Card Container -->
              <div class="relative bg-surface-container-lowest rounded-3xl p-4 sm:p-6 border border-surface-container-high shadow-lg transition-transform duration-300 hover:-translate-y-1">
                <!-- Floating top pill in the card -->
                <div class="flex items-center justify-between pb-3.5 mb-3 border-b border-surface-container-low">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span class="font-headline text-xs font-bold text-on-surface">Active Session Match</span>
                  </div>
                  <span class="font-label text-xs px-2.5 py-1 bg-surface-container text-primary font-semibold rounded-full flex items-center gap-1">
                    <span class="material-symbols-outlined text-xs">sync</span>
                    <span>1 : 1 Trade</span>
                  </span>
                </div>

                <!-- Verified Image Anchor -->
                <div class="w-full aspect-square rounded-2xl overflow-hidden bg-surface-container-low flex items-center justify-center p-2 relative group">
                  <img alt="SkillLoop Hero Illustration" class="w-full h-full object-contain drop-shadow-sm rounded-xl transition-transform duration-500 group-hover:scale-105" src="/hero.jpg"/>
                  <div class="absolute bottom-3 left-3 bg-black/60 backdrop-blur-md text-white text-[11px] font-semibold px-2.5 py-1 rounded-full flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    <span>Live Peer Session</span>
                  </div>
                </div>

                <!-- Live Cycling Ticker (Changes dynamically every 3.2s) -->
                <div class="mt-4 pt-3 border-t border-surface-container-low flex items-center justify-between font-label text-xs text-on-surface-variant min-h-[32px]">
                  <transition name="fade-slide" mode="out-in">
                    <div :key="currentTradeIndex" class="flex items-center gap-2 w-full justify-between">
                      <div class="flex items-center gap-1.5 truncate">
                        <span class="material-symbols-outlined text-base text-primary shrink-0">{{ currentTrade.icon }}</span>
                        <span class="font-semibold text-on-surface truncate">{{ currentTrade.give }}</span>
                        <span class="text-outline">⇄</span>
                        <span class="font-semibold text-primary truncate">{{ currentTrade.get }}</span>
                      </div>
                      <span class="font-bold text-primary font-headline shrink-0 bg-primary/10 px-2 py-0.5 rounded-md">{{ currentTrade.xp }}</span>
                    </div>
                  </transition>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- 2. SOCIAL PROOF / STATS BANNER             -->
    <!-- ========================================== -->
    <section class="border-y border-surface-container-high bg-surface-container-low py-10">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-surface-container-high">
          <div class="pt-4 md:pt-0 group cursor-default">
            <div class="font-display text-3xl sm:text-4xl font-extrabold text-primary group-hover:scale-105 transition-transform">45+</div>
            <div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Campus Nodes</div>
            <p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Active at top universities nationwide</p>
          </div>
          <div class="pt-4 md:pt-0 group cursor-default">
            <div class="font-display text-3xl sm:text-4xl font-extrabold text-primary group-hover:scale-105 transition-transform">2,400+</div>
            <div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Hours Swapped</div>
            <p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Zero student tuition or tutoring fees spent</p>
          </div>
          <div class="pt-4 md:pt-0 group cursor-default">
            <div class="font-display text-3xl sm:text-4xl font-extrabold text-primary group-hover:scale-105 transition-transform">4.9 ★</div>
            <div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Average Peer Rating</div>
            <p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Verified feedback on every session</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- 3. INTERACTIVE EXPLORE SECTION (#explore)  -->
    <!-- ========================================== -->
    <section id="explore" class="py-20 md:py-28 bg-surface scroll-mt-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <!-- Section Header -->
        <div class="text-center max-w-2xl mx-auto mb-12">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary font-label text-xs font-semibold mb-3">
            <span class="material-symbols-outlined text-sm">explore</span>
            <span>Live Campus Marketplace</span>
          </div>
          <h2 class="font-headline text-3xl sm:text-4xl font-extrabold text-on-background tracking-tight">
            Explore Campus Skill Swaps
          </h2>
          <p class="font-body text-base text-on-surface-variant mt-3">
            Browse skills currently being exchanged by verified students across campus departments.
          </p>

          <!-- Live Search Bar -->
          <div class="mt-8 relative max-w-lg mx-auto">
            <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-outline">
              <span class="material-symbols-outlined text-xl">search</span>
            </div>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search skills (e.g. Python, Figma, Guitar, Chemistry)..."
              class="w-full pl-11 pr-10 py-3.5 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-all shadow-xs"
            />
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-outline hover:text-on-surface transition-colors cursor-pointer"
            >
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </div>
        </div>

        <!-- Category Tabs -->
        <div class="flex items-center justify-center gap-2 overflow-x-auto pb-4 mb-8 no-scrollbar">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            :class="selectedCategory === cat.id ? 'bg-primary text-on-primary shadow-sm font-bold' : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container'"
            class="px-4 py-2 rounded-xl text-xs sm:text-sm font-headline font-semibold transition-all duration-200 cursor-pointer whitespace-nowrap active:scale-95 flex items-center gap-1.5 shrink-0"
          >
            <span>{{ cat.icon }}</span>
            <span>{{ cat.name }}</span>
            <span v-if="selectedCategory === cat.id" class="w-1.5 h-1.5 rounded-full bg-white ml-0.5"></span>
          </button>
        </div>

        <!-- Filtered Skill Cards Grid -->
        <div v-if="filteredCards.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="card in filteredCards"
            :key="card.id"
            class="group bg-surface-container-lowest rounded-3xl p-6 border border-surface-container-high shadow-xs hover:shadow-lg hover:border-primary/40 hover:-translate-y-1 transition-all duration-300 flex flex-col justify-between relative overflow-hidden"
          >
            <!-- Card Ambient Gradient Accent -->
            <div class="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-2xl group-hover:bg-primary/10 transition-colors pointer-events-none"></div>

            <div>
              <!-- User Profile Header -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                  <div
                    class="w-11 h-11 rounded-2xl flex items-center justify-center font-bold text-white text-base shadow-xs shrink-0"
                    :style="{ background: card.avatarColor }"
                  >
                    {{ card.name.charAt(0) }}
                  </div>
                  <div>
                    <h4 class="font-headline font-bold text-sm text-on-surface leading-tight">{{ card.name }}</h4>
                    <p class="font-body text-xs text-on-surface-variant">{{ card.dept }} • {{ card.semester }}</p>
                  </div>
                </div>
                <div class="flex items-center gap-1 text-xs font-bold text-amber-500 bg-amber-500/10 px-2 py-0.5 rounded-lg">
                  <span>★</span>
                  <span>{{ card.rating }}</span>
                </div>
              </div>

              <!-- Skill Exchange Box -->
              <div class="p-3.5 rounded-2xl bg-surface-container-low/80 border border-surface-container space-y-2.5">
                <!-- Offers to Teach -->
                <div class="flex items-center justify-between text-xs">
                  <span class="text-on-surface-variant font-medium flex items-center gap-1">
                    <span class="material-symbols-outlined text-sm text-primary">school</span>
                    <span>Teaches:</span>
                  </span>
                  <span class="font-bold text-primary px-2.5 py-0.5 rounded-md bg-primary/10">{{ card.teaches }}</span>
                </div>

                <div class="border-t border-surface-container-high/60 my-1"></div>

                <!-- Wants to Learn -->
                <div class="flex items-center justify-between text-xs">
                  <span class="text-on-surface-variant font-medium flex items-center gap-1">
                    <span class="material-symbols-outlined text-sm text-secondary">psychology</span>
                    <span>Wants:</span>
                  </span>
                  <span class="font-bold text-secondary px-2.5 py-0.5 rounded-md bg-secondary/10">{{ card.learns }}</span>
                </div>
              </div>

              <p class="font-body text-xs text-on-surface-variant mt-3.5 leading-relaxed italic">
                "{{ card.bio }}"
              </p>
            </div>

            <!-- Footer Action -->
            <div class="mt-5 pt-3.5 border-t border-surface-container flex items-center justify-between">
              <span class="text-[11px] font-semibold text-emerald-600 flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>1 hr = 1 Credit</span>
              </span>

              <NuxtLink
                :to="currentUser ? '/chat' : '/register'"
                class="px-3.5 py-1.5 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-xs hover:bg-primary-dim transition-all group-hover:scale-105 active:scale-95 flex items-center gap-1"
              >
                <span>Swap Skill</span>
                <span class="material-symbols-outlined text-xs">arrow_forward</span>
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Empty Search State -->
        <div v-else class="text-center py-16 bg-surface-container-lowest rounded-3xl border border-surface-container p-8 max-w-md mx-auto">
          <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto mb-3">
            <span class="material-symbols-outlined text-2xl">search_off</span>
          </div>
          <h3 class="font-headline font-bold text-base text-on-surface">No skill swaps found</h3>
          <p class="font-body text-xs text-on-surface-variant mt-1 mb-4">No results for "{{ searchQuery }}". Try searching for "Python", "Design", or "Guitar".</p>
          <button
            @click="searchQuery = ''; selectedCategory = 'all'"
            class="px-4 py-2 rounded-xl bg-primary text-on-primary text-xs font-bold shadow-xs hover:bg-primary-dim cursor-pointer"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- 4. HOW IT WORKS SECTION (#how-it-works)    -->
    <!-- ========================================== -->
    <section class="py-20 md:py-28 bg-surface-bright scroll-mt-20" id="how-it-works">
      <div class="max-w-7xl mx-auto px-6">
        <!-- Header -->
        <div class="text-center max-w-2xl mx-auto mb-16">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label text-xs font-semibold mb-3">
            <span class="material-symbols-outlined text-sm" data-icon="auto_awesome">auto_awesome</span>
            <span>Simple &amp; Free Process</span>
          </div>
          <h2 class="font-headline text-3xl sm:text-4xl font-extrabold text-on-background tracking-tight">
            How SkillLoop Works
          </h2>
          <p class="font-body text-base text-on-surface-variant mt-3">
            Level up your skillset in three easy steps with zero financial cost.
          </p>
        </div>

        <!-- 3 Bento-Style Modern Feature Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Card 1 -->
          <div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-xl hover:border-primary-fixed hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-between">
            <div class="absolute top-6 right-6 font-display text-4xl font-extrabold text-surface-container-high/70 select-none group-hover:text-primary/20 transition-colors">
              01
            </div>
            <div>
              <div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-on-primary transition-colors duration-300 mb-6 shadow-xs">
                <span class="material-symbols-outlined text-3xl" data-icon="swap_horiz">swap_horiz</span>
              </div>
              <div class="inline-block px-2.5 py-1 bg-surface-container text-primary rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                Peer Exchange
              </div>
              <h3 class="font-headline text-xl font-bold text-on-background mb-3">
                1. Exchange Skills
              </h3>
              <p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Swap an hour of your Python mastery for an hour of guitar or design. Knowledge is currency — no cash or tutor fees.
              </p>
            </div>
            <div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-primary">
              <span>Time Banking Protocol</span>
              <span class="material-symbols-outlined text-sm group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-xl hover:border-primary-fixed hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-between">
            <div class="absolute top-6 right-6 font-display text-4xl font-extrabold text-surface-container-high/70 select-none group-hover:text-secondary/20 transition-colors">
              02
            </div>
            <div>
              <div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-secondary group-hover:bg-secondary group-hover:text-on-secondary transition-colors duration-300 mb-6 shadow-xs">
                <span class="material-symbols-outlined text-3xl" data-icon="military_tech">military_tech</span>
              </div>
              <div class="inline-block px-2.5 py-1 bg-secondary-container text-on-secondary-container rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                XP &amp; Reputation
              </div>
              <h3 class="font-headline text-xl font-bold text-on-background mb-3">
                2. Gain XP &amp; Badges
              </h3>
              <p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Build your campus reputation with every peer session. Level up and unlock peer mentor accolades on the campus leaderboard.
              </p>
            </div>
            <div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-secondary">
              <span>Dynamic Leaderboards</span>
              <span class="material-symbols-outlined text-sm group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-xl hover:border-primary-fixed hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-between">
            <div class="absolute top-6 right-6 font-display text-4xl font-extrabold text-surface-container-high/70 select-none group-hover:text-tertiary/20 transition-colors">
              03
            </div>
            <div>
              <div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-tertiary group-hover:bg-tertiary group-hover:text-on-tertiary transition-colors duration-300 mb-6 shadow-xs">
                <span class="material-symbols-outlined text-3xl" data-icon="verified">verified</span>
              </div>
              <div class="inline-block px-2.5 py-1 bg-surface-variant text-on-surface rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                Resume Endorsements
              </div>
              <h3 class="font-headline text-xl font-bold text-on-background mb-3">
                3. Get Verified by AI
              </h3>
              <p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Pass anti-cheat AI skill quizzes powered by Google Gemini and export verified credentials directly into your ATS resume.
              </p>
            </div>
            <div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-tertiary">
              <span>Exportable Credential</span>
              <span class="material-symbols-outlined text-sm group-hover:translate-x-1 transition-transform" data-icon="arrow_forward">arrow_forward</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- 5. FEATURES SHOWCASE SECTION (#features)   -->
    <!-- ========================================== -->
    <section id="features" class="py-20 md:py-28 bg-surface scroll-mt-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <!-- Section Header -->
        <div class="text-center max-w-2xl mx-auto mb-16">
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 text-primary font-label text-xs font-semibold mb-3">
            <span class="material-symbols-outlined text-sm">rocket_launch</span>
            <span>Feature-Packed Ecosystem</span>
          </div>
          <h2 class="font-headline text-3xl sm:text-4xl font-extrabold text-on-background tracking-tight">
            Built for Serious Campus Builders
          </h2>
          <p class="font-body text-base text-on-surface-variant mt-3">
            Everything you need to exchange knowledge, verify your real competency, and showcase it to recruiters.
          </p>
        </div>

        <!-- 4-Pillar Feature Bento Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

          <!-- Feature 1: Video Call Hub -->
          <div class="bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-lg hover:border-primary/40 transition-all duration-300 relative overflow-hidden group">
            <div class="flex items-center gap-3.5 mb-5">
              <div class="w-12 h-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center font-bold text-xl group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-2xl">video_camera_front</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-xl text-on-surface">1:1 Live Video &amp; WebRTC</h3>
                <p class="font-body text-xs text-on-surface-variant">Low-latency peer streaming + screen share</p>
              </div>
            </div>
            <p class="font-body text-sm text-on-surface-variant leading-relaxed mb-6">
              Connect directly with student peers across networks using high-performance TURN/STUN relays. Switch camera, share your screen for live code-pairing, and earn session teaching credits automatically.
            </p>
            <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between text-xs font-label">
              <span class="flex items-center gap-1.5 font-bold text-primary">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span>Auto Session Recording</span>
              </span>
              <span class="text-on-surface-variant font-medium">Verified Timer Dock</span>
            </div>
          </div>

          <!-- Feature 2: AI Quizzes -->
          <div class="bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-lg hover:border-primary/40 transition-all duration-300 relative overflow-hidden group">
            <div class="flex items-center gap-3.5 mb-5">
              <div class="w-12 h-12 rounded-2xl bg-secondary/10 text-secondary flex items-center justify-center font-bold text-xl group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-2xl">neurology</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-xl text-on-surface">Gemini AI Skill Verification</h3>
                <p class="font-body text-xs text-on-surface-variant">Dynamic question generation &amp; anti-cheat</p>
              </div>
            </div>
            <p class="font-body text-sm text-on-surface-variant leading-relaxed mb-6">
              Verify your proficiency in any programming language, academic field, or tool. Google Gemini generates fresh, adaptive questions with anti-tab-switching protection and awards verified badges.
            </p>
            <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between text-xs font-label">
              <span class="flex items-center gap-1.5 font-bold text-secondary">
                <span class="material-symbols-outlined text-sm">verified</span>
                <span>Verified Badge Status</span>
              </span>
              <span class="text-on-surface-variant font-medium">3 Difficulty Tiers</span>
            </div>
          </div>

          <!-- Feature 3: Resume Studio -->
          <div class="bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-lg hover:border-primary/40 transition-all duration-300 relative overflow-hidden group">
            <div class="flex items-center gap-3.5 mb-5">
              <div class="w-12 h-12 rounded-2xl bg-tertiary/10 text-tertiary flex items-center justify-center font-bold text-xl group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-2xl">description</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-xl text-on-surface">AI Resume Studio</h3>
                <p class="font-body text-xs text-on-surface-variant">ATS-optimized resume export in 1-click</p>
              </div>
            </div>
            <p class="font-body text-sm text-on-surface-variant leading-relaxed mb-6">
              Turn your verified campus learning and peer endorsements into a job-ready resume. Use built-in AI Polish to craft impactful bullet points and export clean PDFs ready for recruiters.
            </p>
            <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between text-xs font-label">
              <span class="flex items-center gap-1.5 font-bold text-tertiary">
                <span class="material-symbols-outlined text-sm">auto_fix_high</span>
                <span>AI Polish Enabled</span>
              </span>
              <span class="text-on-surface-variant font-medium">ATS-Compliant Formats</span>
            </div>
          </div>

          <!-- Feature 4: Time Banking & Karma -->
          <div class="bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-xs hover:shadow-lg hover:border-primary/40 transition-all duration-300 relative overflow-hidden group">
            <div class="flex items-center gap-3.5 mb-5">
              <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center font-bold text-xl group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-2xl">account_balance_wallet</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-xl text-on-surface">Time Banking Protocol</h3>
                <p class="font-body text-xs text-on-surface-variant">Fair campus economy: 1 hour = 1 credit</p>
              </div>
            </div>
            <p class="font-body text-sm text-on-surface-variant leading-relaxed mb-6">
              Every student begins with 5 welcome credits. Teach for 60 minutes, earn 1 credit. Spend that credit to learn any new skill from any student on campus. Fair, zero-cost, and merit-driven.
            </p>
            <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between text-xs font-label">
              <span class="flex items-center gap-1.5 font-bold text-emerald-600">
                <span class="material-symbols-outlined text-sm">savings</span>
                <span>5 Free Credits on Signup</span>
              </span>
              <span class="text-on-surface-variant font-medium">Zero Platform Fees</span>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- ========================================== -->
    <!-- 6. CAMPUS CALL TO ACTION STRIP             -->
    <!-- ========================================== -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 pb-20">
      <div class="bg-gradient-to-r from-primary via-primary-dim to-secondary rounded-3xl p-8 sm:p-12 text-on-primary flex flex-col md:flex-row items-center justify-between gap-8 shadow-md hover:shadow-xl transition-shadow relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-60 h-60 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>

        <div class="max-w-xl text-center md:text-left relative z-10">
          <span class="px-3.5 py-1.5 bg-surface-container-lowest/20 rounded-full font-label text-xs font-bold uppercase tracking-wider text-on-primary">
            Join Your Campus Network
          </span>
          <h3 class="font-headline text-2xl sm:text-3xl lg:text-4xl font-extrabold mt-3.5 mb-2 leading-tight">
            Ready to swap skills with peers?
          </h3>
          <p class="font-body text-sm sm:text-base text-on-primary/90 leading-relaxed">
            Sign in with your university student credentials and find a skill partner in under 5 minutes.
          </p>
        </div>

        <div class="flex-shrink-0 relative z-10">
          <NuxtLink
            class="px-8 py-4 rounded-xl bg-surface-container-lowest text-primary font-headline text-base font-bold shadow hover:bg-surface-bright transition-all duration-200 active:scale-95 inline-flex items-center gap-2 hover:shadow-lg"
            :to="currentUser ? '/dashboard' : '/register'"
          >
            <span>{{ currentUser ? 'Open Dashboard' : 'Find a Partner' }}</span>
            <span class="material-symbols-outlined text-lg">school</span>
          </NuxtLink>
        </div>
      </div>
    </section>
  </main>

  <!-- ========================================== -->
  <!-- 7. FOOTER                                  -->
  <!-- ========================================== -->
  <footer class="w-full bg-surface-container-lowest border-t border-surface-container-high">
    <div class="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-6 font-body text-sm">
      <!-- Brand & Copyright -->
      <div class="flex flex-col sm:flex-row items-center gap-3 sm:gap-6 text-center sm:text-left">
        <NuxtLink class="font-display text-xl font-bold text-primary flex items-center gap-1.5" to="/">
          <span class="material-symbols-outlined text-xl" data-icon="all_inclusive">all_inclusive</span>
          <span>SkillLoop</span>
        </NuxtLink>
        <span class="text-on-surface-variant font-body">© 2026 SkillLoop. Built for campus peer learning.</span>
      </div>

      <!-- Working Footer Links -->
      <nav class="flex flex-wrap items-center justify-center gap-6 font-medium text-xs sm:text-sm">
        <button @click="scrollToSection('explore')" class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer">Explore</button>
        <button @click="scrollToSection('how-it-works')" class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer">How It Works</button>
        <button @click="scrollToSection('features')" class="text-on-surface-variant hover:text-primary transition-colors cursor-pointer">Features</button>
        <NuxtLink class="text-on-surface-variant hover:text-primary transition-colors" to="/leaderboard">Leaderboard</NuxtLink>
        <NuxtLink class="text-on-surface-variant hover:text-primary transition-colors" to="/quiz">Quiz</NuxtLink>
      </nav>
    </div>
  </footer>
</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const currentUser = ref(null)
const activeSection = ref('explore')
const searchQuery = ref('')
const selectedCategory = ref('all')

// Live Trade Ticker Cycling in Hero Card
const liveTrades = [
  { give: '1 hr Python 🐍', get: '1 hr Figma 🎨', xp: '+100 XP', icon: 'code' },
  { give: '1 hr Acoustic Guitar 🎸', get: '1 hr Calculus 📐', xp: '+120 XP', icon: 'music_note' },
  { give: '1 hr UI/UX Design 🎨', get: '1 hr Machine Learning 🤖', xp: '+150 XP', icon: 'palette' },
  { give: '1 hr Spanish 🗣️', get: '1 hr React Native 📱', xp: '+100 XP', icon: 'translate' },
  { give: '1 hr Organic Chem 🧪', get: '1 hr Video Editing 🎬', xp: '+110 XP', icon: 'science' },
]
const currentTradeIndex = ref(0)
const currentTrade = computed(() => liveTrades[currentTradeIndex.value])

let tradeTimer = null

// Popular tags in Hero
const popularSkillTags = [
  { label: 'Python', icon: '🐍', cat: 'tech' },
  { label: 'UI/UX Design', icon: '🎨', cat: 'design' },
  { label: 'Acoustic Guitar', icon: '🎸', cat: 'music' },
  { label: 'Organic Chem', icon: '🧪', cat: 'academic' },
]

// Explore Categories
const categories = [
  { id: 'all', name: 'All Skills', icon: '🌟' },
  { id: 'tech', name: 'Tech & Code', icon: '💻' },
  { id: 'design', name: 'Design & 3D', icon: '🎨' },
  { id: 'music', name: 'Music & Arts', icon: '🎸' },
  { id: 'academic', name: 'Academics & STEM', icon: '📚' },
  { id: 'languages', name: 'Languages', icon: '🗣️' },
]

// Sample live peer cards representing active campus swaps
const peerCards = [
  {
    id: 1,
    name: 'Aarav Sharma',
    dept: 'Computer Science',
    semester: 'Sem 5',
    category: 'tech',
    teaches: 'Python & FastAPI',
    learns: 'Figma & UI Design',
    rating: '5.0',
    avatarColor: 'linear-gradient(135deg, #667eea, #764ba2)',
    bio: 'Building backend microservices. Looking to learn clean design systems for portfolio projects.'
  },
  {
    id: 2,
    name: 'Priya Patel',
    dept: 'Design & Media',
    semester: 'Sem 4',
    category: 'design',
    teaches: 'UI/UX & Figma',
    learns: 'React & Tailwind',
    rating: '4.9',
    avatarColor: 'linear-gradient(135deg, #f093fb, #f5576c)',
    bio: 'Experienced in mobile wireframes and interaction design. Want to build frontend web prototypes.'
  },
  {
    id: 3,
    name: 'Rohan Verma',
    dept: 'Mechanical Eng',
    semester: 'Sem 3',
    category: 'music',
    teaches: 'Acoustic Guitar & Chords',
    learns: 'Calculus & Linear Algebra',
    rating: '5.0',
    avatarColor: 'linear-gradient(135deg, #FF6B6B, #FF8E53)',
    bio: 'Self-taught guitarist of 5 years. Need help prepping for engineering mathematics midterms.'
  },
  {
    id: 4,
    name: 'Ananya Roy',
    dept: 'Biotechnology',
    semester: 'Sem 6',
    category: 'academic',
    teaches: 'Organic Chemistry & Lab',
    learns: 'Python Data Science',
    rating: '4.9',
    avatarColor: 'linear-gradient(135deg, #43e97b, #38f9d7)',
    bio: 'Top of class in organic mechanisms. Want to learn NumPy and Pandas for bioinformatics research.'
  },
  {
    id: 5,
    name: 'Kavya Singh',
    dept: 'AI & Data Science',
    semester: 'Sem 4',
    category: 'tech',
    teaches: 'PyTorch & Machine Learning',
    learns: 'Blender 3D Modeling',
    rating: '5.0',
    avatarColor: 'linear-gradient(135deg, #4facfe, #00f2fe)',
    bio: 'Deep learning researcher. Excited to learn 3D digital art and game asset creation.'
  },
  {
    id: 6,
    name: 'Aditya Nair',
    dept: 'Liberal Arts',
    semester: 'Sem 3',
    category: 'languages',
    teaches: 'Conversational Spanish',
    learns: 'Prompt Engineering & AI',
    rating: '4.8',
    avatarColor: 'linear-gradient(135deg, #fa709a, #fee140)',
    bio: 'DELE B2 certified Spanish speaker. Eager to master prompt engineering and generative workflows.'
  }
]

// Computed filtered cards based on category and search query
const filteredCards = computed(() => {
  return peerCards.filter(card => {
    const matchesCategory = selectedCategory.value === 'all' || card.category === selectedCategory.value
    const q = searchQuery.value.toLowerCase().trim()
    if (!q) return matchesCategory

    const matchesQuery =
      card.teaches.toLowerCase().includes(q) ||
      card.learns.toLowerCase().includes(q) ||
      card.name.toLowerCase().includes(q) ||
      card.dept.toLowerCase().includes(q) ||
      card.bio.toLowerCase().includes(q)

    return matchesCategory && matchesQuery
  })
})

// Scroll smoothly to section
const scrollToSection = (id) => {
  activeSection.value = id
  if (typeof document !== 'undefined') {
    const el = document.getElementById(id)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }
}

// When popular tag is clicked in hero
const filterFromTag = (tag) => {
  selectedCategory.value = tag.cat
  searchQuery.value = tag.label
  scrollToSection('explore')
}

onMounted(async () => {
  // Start trade cycling ticker
  tradeTimer = setInterval(() => {
    currentTradeIndex.value = (currentTradeIndex.value + 1) % liveTrades.length
  }, 3200)

  // Auth check
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      if (data.user) {
        currentUser.value = data.user
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('skillloop_auth_active', 'true')
        }
      }
    } else {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('skillloop_auth_active')
      }
    }
  } catch (e) {}
})

onUnmounted(() => {
  if (tradeTimer) clearInterval(tradeTimer)
})
</script>

<style scoped>
@keyframes floatSlow {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-9px) rotate(1deg);
  }
}

@keyframes floatDelayed {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(8px) rotate(-1deg);
  }
}

@keyframes pulseGlow {
  0%, 100% {
    opacity: 0.35;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.04);
  }
}

.animate-float-slow {
  animation: floatSlow 5.5s ease-in-out infinite;
}

.animate-float-delayed {
  animation: floatDelayed 6.5s ease-in-out 1.2s infinite;
}

.animate-pulse-glow {
  animation: pulseGlow 4s ease-in-out infinite;
}

/* Ticker transition animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Hide scrollbar for category pills on mobile */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
