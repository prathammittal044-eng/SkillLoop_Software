<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col">
    <!-- Loading State -->
    <div v-if="pending" class="min-h-screen flex items-center justify-center">
      <div class="text-center space-y-3">
        <div class="w-12 h-12 rounded-full border-4 border-primary/30 border-t-primary animate-spin mx-auto"></div>
        <p class="text-on-surface-variant text-sm">Loading your dashboard...</p>
      </div>
    </div>

    <!-- Error State (Not Authenticated) -->
    <div v-else-if="error" class="min-h-screen flex items-center justify-center">
      <div class="text-center space-y-4">
        <span class="material-symbols-outlined text-5xl text-error">lock</span>
        <p class="text-on-surface text-lg font-headline font-bold">Session Expired</p>
        <NuxtLink to="/login" class="px-6 py-3 rounded-xl bg-primary text-on-primary font-semibold inline-block hover:bg-primary-dim transition-colors">Go to Login</NuxtLink>
      </div>
    </div>

    <!-- Main Dashboard -->
    <template v-else-if="user">
      <!-- Top Navigation -->
      <header class="bg-surface-container-low shadow-sm sticky top-0 z-40">
        <div class="flex justify-between items-center w-full px-6 py-3 max-w-7xl mx-auto">
          <div class="flex items-center gap-8">
            <NuxtLink to="/" class="font-display text-xl font-bold text-primary tracking-tight flex items-center gap-2">
              <div class="w-9 h-9 rounded-xl bg-primary text-on-primary flex items-center justify-center shadow-sm">
                <span class="material-symbols-outlined text-2xl leading-none">all_inclusive</span>
              </div>
              <span>SkillLoop</span>
            </NuxtLink>
            <nav class="hidden md:flex items-center space-x-6 font-headline text-sm font-semibold tracking-tight">
              <span class="text-primary font-bold border-b-2 border-primary pb-1 flex items-center gap-1.5">
                <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">space_dashboard</span>
                Dashboard
              </span>
              <NuxtLink to="/chat" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">
                <span class="material-symbols-outlined text-lg">chat</span>
                Chat & Video
              </NuxtLink>
              <NuxtLink to="/quiz" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Quiz</NuxtLink>
              <NuxtLink to="/leaderboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Leaderboard</NuxtLink>
              <NuxtLink to="/resume" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Resume</NuxtLink>
            </nav>
          </div>
          <div class="flex items-center gap-3">
            <div class="flex items-center gap-1.5 bg-surface-container-lowest px-3 py-1.5 rounded-full border border-secondary-fixed shadow-sm text-sm font-label font-bold text-on-surface">
              <span class="material-symbols-outlined text-primary text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
              <span>{{ user.time_credits || 0 }} Credits</span>
            </div>
            <!-- Notification Bell -->
            <button @click="showNotificationsPanel = !showNotificationsPanel" class="relative w-9 h-9 rounded-full bg-surface-container-low border border-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors">
              <span class="material-symbols-outlined text-xl">notifications</span>
              <span v-if="pendingConnections.length > 0 || liveNotifCount > 0" class="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-error text-on-error text-[10px] font-extrabold flex items-center justify-center shadow-sm">
                {{ pendingConnections.length + liveNotifCount }}
              </span>
            </button>
            <div class="relative w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-sm uppercase shadow-sm">
              {{ (user.full_name || user.username || 'U').charAt(0) }}
            </div>
            <button @click="logout" class="text-xs text-on-surface-variant hover:text-error transition-colors font-semibold">Logout</button>
          </div>
        </div>
      </header>


      <!-- Main Content -->
      <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-6 md:py-8 space-y-8">

        <!-- Welcome Banner -->
        <section class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-surface-container shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden">
          <div class="relative z-10 space-y-1.5 max-w-2xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-low text-primary text-xs font-semibold uppercase tracking-wider font-label mb-1">
              <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
              Campus Exchange Live
            </div>
            <h1 class="font-display text-2xl sm:text-3xl font-bold text-on-surface tracking-tight">
              Welcome back, {{ user.full_name?.split(' ')[0] || user.username }} ✨
            </h1>
            <p class="text-on-surface-variant font-body text-sm sm:text-base leading-relaxed">
              You have <span class="font-semibold text-primary">{{ pendingConnections.length }} pending requests</span> waiting for you.
            </p>
          </div>
          <div class="relative z-10 flex items-center flex-wrap gap-3">
            <button @click="isAdding = !isAdding" class="px-5 py-2.5 rounded-xl bg-primary text-on-primary font-headline text-sm font-bold shadow-sm hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-2">
              <span class="material-symbols-outlined text-lg">add</span>
              <span>Add Skill</span>
            </button>
            <NuxtLink to="/quiz" class="px-4 py-2.5 rounded-xl bg-surface-container-low text-on-surface-variant font-headline text-sm font-semibold hover:text-primary hover:bg-surface-container active:scale-95 transition-all flex items-center gap-2 border border-surface-variant/50">
              <span class="material-symbols-outlined text-lg">quiz</span>
              <span>Take Quiz</span>
            </NuxtLink>
            <NuxtLink to="/resume" class="px-4 py-2.5 rounded-xl bg-surface-container-low text-on-surface-variant font-headline text-sm font-semibold hover:text-primary hover:bg-surface-container active:scale-95 transition-all flex items-center gap-2 border border-surface-variant/50">
              <span class="material-symbols-outlined text-lg">description</span>
              <span>Resume Studio</span>
            </NuxtLink>
          </div>
          <div class="absolute -right-16 -top-16 w-48 h-48 bg-secondary-container/30 rounded-full blur-3xl pointer-events-none"></div>
        </section>

        <!-- Add Skill Form (shown when isAdding) -->
        <div v-if="isAdding" class="bg-surface-container-lowest rounded-2xl p-6 border border-primary/30 shadow-sm space-y-4">
          <h3 class="font-headline font-bold text-on-surface">Add New Skill</h3>
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1 space-y-2">
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider">I Can Teach</label>
              <div class="flex gap-2">
                <input v-model="newTeach" placeholder="e.g. Python, Guitar, Yoga" class="flex-1 px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors"/>
                <button @click="addSkill('teaches')" :disabled="!newTeach.trim()" class="px-4 py-2.5 rounded-xl bg-primary text-on-primary text-sm font-bold hover:bg-primary-dim disabled:opacity-50 transition-colors">Add</button>
              </div>
            </div>
            <div class="flex-1 space-y-2">
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider">I Want to Learn</label>
              <div class="flex gap-2">
                <input v-model="newLearn" placeholder="e.g. Spanish, Chess, Design" class="flex-1 px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors"/>
                <button @click="addSkill('learns')" :disabled="!newLearn.trim()" class="px-4 py-2.5 rounded-xl bg-tertiary text-on-tertiary text-sm font-bold hover:bg-tertiary-dim disabled:opacity-50 transition-colors">Add</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 3 Column Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

          <!-- LEFT: Profile Card -->
          <aside class="lg:col-span-4 bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-6">
            <div class="flex flex-col items-center text-center space-y-3 pt-2">
              <div class="relative">
                <div class="w-24 h-24 rounded-full bg-gradient-to-tr from-primary to-tertiary-container flex items-center justify-center text-on-primary font-display font-bold text-3xl shadow-md">
                  {{ (user.full_name || user.username || 'U').charAt(0).toUpperCase() }}
                </div>
                <div v-if="verifiedSkills.length > 0" class="absolute -bottom-1 -right-1 bg-primary text-on-primary rounded-full p-1.5 shadow-sm" title="Verified Member">
                  <span class="material-symbols-outlined text-sm leading-none" style="font-variation-settings: 'FILL' 1;">verified</span>
                </div>
              </div>
              <div>
                <div class="flex items-center justify-center gap-1.5">
                  <h2 class="font-display text-xl font-bold text-on-surface">{{ user.full_name || user.username }}</h2>
                </div>
                <p class="text-xs font-medium text-on-surface-variant font-label">@{{ user.username }}</p>
              </div>
              <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-xs font-semibold text-secondary font-headline">
                <span class="material-symbols-outlined text-sm">school</span>
                {{ user.department || 'No Department' }} • Semester {{ user.semester }}
              </div>
            </div>

            <!-- XP Progress -->
            <div class="bg-surface-container-low rounded-2xl p-4 space-y-3 border border-surface-container/60">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="w-8 h-8 rounded-lg bg-tertiary-container/30 text-tertiary flex items-center justify-center">
                    <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">military_tech</span>
                  </span>
                  <div>
                    <p class="text-xs font-bold text-on-surface uppercase tracking-wide font-headline">Level {{ user.level || 1 }}</p>
                    <p class="text-[11px] text-on-surface-variant">Campus Peer</p>
                  </div>
                </div>
                <span class="text-xs font-bold text-primary font-headline">{{ user.xp || 0 }} XP</span>
              </div>
              <div class="w-full h-2.5 bg-surface-container-highest rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-primary to-tertiary-fixed rounded-full transition-all" :style="`width: ${Math.min(((user.xp || 0) % 100), 100)}%`"></div>
              </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-surface-container-lowest border border-surface-container rounded-2xl p-3 text-center">
                <span class="text-base font-bold font-headline text-on-surface block">{{ user.sessions_completed || 0 }}</span>
                <span class="text-[11px] font-medium text-on-surface-variant">Sessions</span>
              </div>
              <div class="bg-surface-container-lowest border border-surface-container rounded-2xl p-3 text-center">
                <span class="text-base font-bold font-headline text-on-surface block">{{ user.time_credits || 0 }}</span>
                <span class="text-[11px] font-medium text-on-surface-variant">Credits</span>
              </div>
            </div>

            <button @click="showEditModal = true" class="w-full py-2.5 rounded-xl border border-primary/40 text-primary hover:bg-primary/5 active:scale-95 font-headline font-semibold text-sm transition-all duration-150 flex items-center justify-center gap-2">
              <span class="material-symbols-outlined text-base">edit</span>
              <span>Edit Profile</span>
            </button>
          </aside>

          <!-- CENTER: Skills -->
          <section class="lg:col-span-5 space-y-6">
            <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-6">
              <div class="flex items-center justify-between pb-3 border-b border-surface-container/50">
                <div class="flex items-center gap-2.5">
                  <div class="w-8 h-8 rounded-xl bg-secondary-container text-on-secondary-container flex items-center justify-center">
                    <span class="material-symbols-outlined text-lg">psychology</span>
                  </div>
                  <h2 class="font-display text-xl font-bold text-on-surface tracking-tight">My Skills</h2>
                </div>
              </div>

              <!-- Teaching Skills -->
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-primary"></span>
                    <h3 class="font-headline text-sm font-bold text-on-surface">Skills I Teach</h3>
                  </div>
                  <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary font-label text-xs font-bold">{{ teaches.length }} Offered</span>
                </div>
                <div v-if="teaches.length === 0" class="p-4 rounded-2xl bg-surface-container-low/60 border border-dashed border-surface-container text-center text-on-surface-variant text-xs">
                  No skills added yet. Click "Add Skill" above to get started!
                </div>
                <div v-for="skill in teaches" :key="skill.id" class="p-3.5 rounded-2xl bg-surface-container-low border border-surface-container/80 flex items-center justify-between hover:border-primary/40 transition-colors group">
                  <div class="flex items-center gap-2">
                    <span class="font-headline font-semibold text-sm text-on-surface">{{ skill.name }}</span>
                    <span v-if="verifiedSkills.find(v => v.skill_name?.toLowerCase() === skill.name?.toLowerCase())" class="px-2 py-0.5 rounded-md bg-primary/10 text-[10px] font-bold text-primary uppercase">Verified</span>
                  </div>
                  <button @click="removeSkill(skill.id)" class="opacity-0 group-hover:opacity-100 text-on-surface-variant hover:text-error transition-all text-xs">
                    <span class="material-symbols-outlined text-sm">close</span>
                  </button>
                </div>
              </div>

              <!-- Learning Skills -->
              <div class="space-y-3 pt-2">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-tertiary"></span>
                    <h3 class="font-headline text-sm font-bold text-on-surface">Skills I Want to Learn</h3>
                  </div>
                  <span class="px-2 py-0.5 rounded-full bg-tertiary/10 text-tertiary font-label text-xs font-bold">{{ learns.length }} Goals</span>
                </div>
                <div v-if="learns.length === 0" class="p-4 rounded-2xl bg-surface-container-low/60 border border-dashed border-surface-container text-center text-on-surface-variant text-xs">
                  Add skills you want to learn to find matching peers!
                </div>
                <div v-for="skill in learns" :key="skill.id" class="p-3 rounded-2xl bg-surface-container-low/70 border border-surface-container/80 flex items-center justify-between group">
                  <span class="font-headline font-semibold text-sm text-on-surface">{{ skill.name }}</span>
                  <button @click="removeSkill(skill.id)" class="opacity-0 group-hover:opacity-100 text-on-surface-variant hover:text-error transition-all text-xs">
                    <span class="material-symbols-outlined text-sm">close</span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Smart Cycle Matches -->
            <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-5">
              <div class="flex items-center justify-between pb-3 border-b border-surface-container/50">
                <div class="flex items-center gap-2.5">
                  <div class="w-8 h-8 rounded-xl bg-primary-container/40 text-primary flex items-center justify-center">
                    <span class="material-symbols-outlined text-lg">sync_alt</span>
                  </div>
                  <div>
                    <h2 class="font-display text-xl font-bold text-on-surface tracking-tight">Loop Exchanges</h2>
                    <p class="text-xs text-on-surface-variant font-body">Multi-peer cycles detected by algorithm</p>
                  </div>
                </div>
                <span v-if="cycles.length > 0" class="px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-bold font-label">
                  {{ cycles.length }} Available
                </span>
              </div>

              <!-- Loading State -->
              <div v-if="isLoadingCycles" class="p-6 text-center text-on-surface-variant text-xs flex items-center justify-center gap-2">
                <span class="w-4 h-4 rounded-full border-2 border-primary border-t-transparent animate-spin"></span>
                <span>Finding loop cycles...</span>
              </div>

              <!-- Empty State -->
              <div v-else-if="cycles.length === 0" class="p-6 rounded-2xl bg-surface-container-low/60 border border-dashed border-surface-container text-center space-y-1">
                <p class="font-headline font-semibold text-sm text-on-surface">No loops found yet</p>
                <p class="text-xs text-on-surface-variant">Add more teaching and learning skills to unlock multi-peer exchange cycles!</p>
              </div>

              <!-- Cycle Cards List -->
              <div v-else class="space-y-4">
                <div
                  v-for="(cycle, cIdx) in cycles"
                  :key="cIdx"
                  class="p-4 rounded-2xl bg-surface-container-low border border-surface-container/80 space-y-3 hover:border-primary/40 transition-all duration-200"
                >
                  <!-- Cycle Header Badge -->
                  <div class="flex items-center justify-between">
                    <span class="px-2 py-0.5 rounded-md bg-secondary-container text-on-secondary-container text-[11px] font-bold uppercase tracking-wide font-label">
                      {{ cycle.length }}-Party Loop • {{ cycle.quality }}
                    </span>
                    <span class="text-xs font-bold text-primary font-headline">{{ cycle.score }} Match Score</span>
                  </div>

                  <!-- Chain Flow -->
                  <div class="flex items-center flex-wrap gap-2 pt-1 text-xs">
                    <template v-for="(node, nIdx) in cycle.nodes" :key="nIdx">
                      <div class="flex items-center gap-1.5 bg-surface-container-lowest px-2.5 py-1.5 rounded-xl border border-surface-container shadow-xs">
                        <div class="w-6 h-6 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-[10px] uppercase">
                          {{ node.name.charAt(0) }}
                        </div>
                        <div>
                          <span class="font-headline font-bold text-on-surface">{{ node.name }}</span>
                          <span class="text-[10px] text-tertiary block font-semibold">teaches {{ node.teaches_next }}</span>
                        </div>
                      </div>
                      <span v-if="nIdx < cycle.nodes.length - 1" class="text-primary font-bold">➔</span>
                    </template>
                    <span class="text-primary font-bold">➔</span>
                    <span class="text-[11px] font-semibold text-primary font-label">Loop Closed ✨</span>
                  </div>

                  <!-- Quick Connect Button -->
                  <div class="pt-2 border-t border-surface-container/50 flex items-center justify-between">
                    <span class="text-[11px] text-on-surface-variant">Everyone learns & gives knowledge</span>
                    <div v-if="getCyclePeer(cycle)" class="flex items-center gap-2">
                      <NuxtLink
                        v-if="isPeerConnected(getCyclePeer(cycle).user_id)"
                        :to="'/chat?id=' + getCyclePeer(cycle).user_id"
                        class="px-3 py-1.5 rounded-xl bg-emerald-600 text-white font-headline text-xs font-bold hover:bg-emerald-700 active:scale-95 transition-all shadow-xs flex items-center gap-1"
                      >
                        <span>Chat & Call</span>
                        <span class="material-symbols-outlined text-sm">chat</span>
                      </NuxtLink>
                      <button
                        v-else
                        @click="sendConnectRequest(getCyclePeer(cycle).user_id)"
                        class="px-3 py-1.5 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-xs flex items-center gap-1"
                      >
                        <span>Connect Loop</span>
                        <span class="material-symbols-outlined text-sm">bolt</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- RIGHT: Quick Links -->
          <aside class="lg:col-span-3 space-y-4">
            <NuxtLink to="/quiz" class="block bg-surface-container-lowest rounded-3xl p-5 border border-surface-container hover:border-primary/50 shadow-sm hover:shadow-md transition-all duration-200 group">
              <div class="flex items-start justify-between">
                <div class="w-11 h-11 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
                  <span class="material-symbols-outlined text-2xl">quiz</span>
                </div>
                <span class="px-2 py-0.5 rounded-full bg-primary text-on-primary text-[10px] font-bold font-label tracking-wide">+XP</span>
              </div>
              <div class="mt-4 space-y-1">
                <h3 class="font-display text-base font-bold text-on-surface group-hover:text-primary transition-colors">Skill Quiz</h3>
                <p class="text-xs text-on-surface-variant font-body leading-relaxed">Verify your skills and earn time credits instantly.</p>
              </div>
              <div class="mt-4 pt-3 border-t border-surface-container-low flex items-center justify-between text-xs font-bold text-primary font-headline">
                <span>Start Quiz</span>
                <span class="material-symbols-outlined text-sm transform group-hover:translate-x-1 transition-transform">arrow_forward</span>
              </div>
            </NuxtLink>

            <NuxtLink to="/leaderboard" class="block bg-surface-container-lowest rounded-3xl p-5 border border-surface-container hover:border-tertiary/50 shadow-sm hover:shadow-md transition-all duration-200 group">
              <div class="flex items-start justify-between">
                <div class="w-11 h-11 rounded-2xl bg-tertiary-container/30 text-tertiary flex items-center justify-center">
                  <span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">emoji_events</span>
                </div>
              </div>
              <div class="mt-4 space-y-1">
                <h3 class="font-display text-base font-bold text-on-surface group-hover:text-tertiary transition-colors">Campus Leaderboard</h3>
                <p class="text-xs text-on-surface-variant font-body leading-relaxed">See how you rank against campus peers.</p>
              </div>
              <div class="mt-4 pt-3 border-t border-surface-container-low flex items-center justify-between text-xs font-bold text-tertiary font-headline">
                <span>View Ranks</span>
                <span class="material-symbols-outlined text-sm transform group-hover:translate-x-1 transition-transform">arrow_forward</span>
              </div>
            </NuxtLink>

            <NuxtLink to="/resume" class="block bg-surface-container-lowest rounded-3xl p-5 border border-surface-container hover:border-secondary/50 shadow-sm hover:shadow-md transition-all duration-200 group">
              <div class="flex items-start justify-between">
                <div class="w-11 h-11 rounded-2xl bg-secondary-container/50 text-secondary flex items-center justify-center">
                  <span class="material-symbols-outlined text-2xl">workspace_premium</span>
                </div>
                <span class="px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container text-[10px] font-bold font-label">PDF</span>
              </div>
              <div class="mt-4 space-y-1">
                <h3 class="font-display text-base font-bold text-on-surface group-hover:text-secondary transition-colors">Verified Resume</h3>
                <p class="text-xs text-on-surface-variant font-body leading-relaxed">Export your peer-endorsed credentials.</p>
              </div>
              <div class="mt-4 pt-3 border-t border-surface-container-low flex items-center justify-between text-xs font-bold text-secondary font-headline">
                <span>Generate CV</span>
                <span class="material-symbols-outlined text-sm transform group-hover:translate-x-1 transition-transform">arrow_forward</span>
              </div>
            </NuxtLink>
          </aside>
        </div>

        <!-- Find & Connect with Campus Peers -->
        <section class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-lg">person_search</span>
              </div>
              <div>
                <h2 class="font-display text-xl font-bold text-on-surface tracking-tight">Find & Connect Peers</h2>
                <p class="text-xs text-on-surface-variant font-body">Search by @username or name to connect directly</p>
              </div>
            </div>
            <!-- Search Bar -->
            <div class="relative max-w-sm w-full">
              <span class="material-symbols-outlined absolute left-3 top-2.5 text-on-surface-variant text-base">search</span>
              <input
                v-model="searchPeerQuery"
                @input="searchPeers"
                type="text"
                placeholder="e.g. @mittalserenity or Krishna"
                class="w-full pl-9 pr-4 py-2 rounded-xl bg-surface-bright border border-surface-container-high text-xs focus:outline-none focus:border-primary transition-all font-body"
              />
            </div>
          </div>

          <!-- Search Results Dropdown/Grid -->
          <div v-if="searchPeerResults.length > 0" class="pt-2 border-t border-surface-container/50 space-y-2">
            <p class="text-[11px] font-bold uppercase tracking-wider text-on-surface-variant">Search Results</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div
                v-for="p in searchPeerResults"
                :key="p.id"
                class="p-3.5 rounded-2xl bg-surface-container-low border border-surface-container/80 flex items-center justify-between gap-3 hover:border-primary/40 transition-all"
              >
                <div class="flex items-center gap-2.5 min-w-0">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary/20 to-tertiary/20 text-primary font-bold text-sm flex items-center justify-center shrink-0 uppercase">
                    {{ (p.full_name || p.username).charAt(0) }}
                  </div>
                  <div class="min-w-0">
                    <h4 class="font-headline font-bold text-xs text-on-surface truncate">{{ p.full_name }}</h4>
                    <p class="text-[10px] text-on-surface-variant truncate">@{{ p.username }}</p>
                    <p v-if="p.teaches && p.teaches.length" class="text-[10px] text-primary font-semibold truncate">
                      Teaches: {{ p.teaches.join(', ') }}
                    </p>
                  </div>
                </div>

                <div class="shrink-0">
                  <NuxtLink
                    v-if="p.connection_status === 'connected'"
                    :to="'/chat?id=' + p.id"
                    class="px-2.5 py-1.5 rounded-lg bg-emerald-600 text-white font-headline text-[11px] font-bold hover:bg-emerald-700 active:scale-95 transition-all flex items-center gap-1"
                  >
                    <span>Chat</span>
                    <span class="material-symbols-outlined text-xs">chat</span>
                  </NuxtLink>
                  <button
                    v-else-if="p.connection_status === 'pending_received'"
                    @click="respondConnection(p.connection_id, 'accepted')"
                    class="px-2.5 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-[11px] font-bold hover:bg-primary-dim active:scale-95 transition-all"
                  >
                    Accept
                  </button>
                  <span
                    v-else-if="p.connection_status === 'pending_sent'"
                    class="px-2.5 py-1 rounded-lg bg-surface-container text-on-surface-variant font-headline text-[11px] font-semibold"
                  >
                    Pending
                  </span>
                  <button
                    v-else
                    @click="connectWithPeer(p)"
                    class="px-2.5 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-[11px] font-bold hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-1"
                  >
                    <span>Connect</span>
                    <span class="material-symbols-outlined text-xs">person_add</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Pending Connection Requests -->
        <section class="space-y-4 pt-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h2 class="font-display text-xl font-bold text-on-surface">Pending Requests</h2>
              <span v-if="pendingConnections.length > 0" class="px-2.5 py-0.5 rounded-full bg-primary text-on-primary text-xs font-bold font-label shadow-xs">{{ pendingConnections.length }} New</span>
            </div>
          </div>

          <div v-if="pendingConnections.length === 0" class="p-6 rounded-3xl bg-surface-container-lowest border border-surface-container text-center text-on-surface-variant text-sm">
            No pending requests right now. Share your @{{ user.username }} profile with campus peers!
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div v-for="conn in pendingConnections" :key="conn.id" class="bg-surface-container-lowest rounded-3xl p-6 border border-primary/30 shadow-sm flex flex-col justify-between space-y-4 hover:border-primary transition-colors">
              <div class="space-y-3">
                <div class="flex items-center gap-3.5">
                  <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-primary to-tertiary text-on-primary font-bold text-lg flex items-center justify-center shadow-sm shrink-0 uppercase">
                    {{ (conn.full_name || conn.username || '?').charAt(0) }}
                  </div>
                  <div>
                    <h3 class="font-display text-base font-bold text-on-surface">{{ conn.full_name || conn.username }}</h3>
                    <p class="text-xs text-primary font-semibold">@{{ conn.username }} • {{ conn.department || 'Campus Peer' }}</p>
                  </div>
                </div>
                <div class="p-3 rounded-2xl bg-surface-container-low border border-surface-container/60 space-y-1 text-xs">
                  <span class="text-[11px] font-bold text-on-surface-variant uppercase tracking-wider block font-label">Skill Exchange Match</span>
                  <div class="flex flex-wrap items-center gap-1.5 font-headline font-semibold text-on-surface">
                    <span class="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md border border-emerald-200">Offers: {{ conn.skill_offered }}</span>
                    <span class="text-primary font-bold">⇌</span>
                    <span class="text-primary bg-primary/10 px-2 py-0.5 rounded-md border border-primary/20">Wants: {{ conn.skill_wanted }}</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center gap-2 pt-2 border-t border-surface-container-low">
                <button @click="respondConnection(conn.id, 'accepted')" class="flex-1 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-xs hover:bg-primary-dim active:scale-95 transition-all flex items-center justify-center gap-1.5">
                  <span class="material-symbols-outlined text-base">check_circle</span>
                  <span>Accept Connection</span>
                </button>
                <button @click="respondConnection(conn.id, 'rejected')" class="py-2 px-3 rounded-xl bg-surface-container-low text-on-surface-variant hover:text-error hover:bg-error/10 font-headline text-xs font-semibold active:scale-95 transition-all">Decline</button>
              </div>
            </div>
          </div>
        </section>

        <!-- Active Connected Peers (My Learning Network) -->
        <section class="space-y-4 pt-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <h2 class="font-display text-xl font-bold text-on-surface">My Learning Partners</h2>
              <span v-if="activeConnections.length > 0" class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold font-label shadow-xs">{{ activeConnections.length }} Connected</span>
            </div>
            <NuxtLink to="/chat" class="text-xs font-bold text-primary hover:underline flex items-center gap-1">
              <span>Open Chat Hub</span>
              <span class="material-symbols-outlined text-sm">arrow_forward</span>
            </NuxtLink>
          </div>

          <div v-if="activeConnections.length === 0" class="p-6 rounded-3xl bg-surface-container-lowest border border-surface-container text-center text-on-surface-variant text-sm">
            You don't have active learning partners yet. Connect with peers from Loop Exchanges above or search by username!
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="c in activeConnections"
              :key="c.id"
              class="p-4 rounded-3xl bg-surface-container-lowest border border-surface-container shadow-sm flex items-center justify-between gap-3 hover:border-primary/40 transition-all"
            >
              <div class="flex items-center gap-3 min-w-0">
                <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-primary/20 to-tertiary/20 text-primary font-bold text-base flex items-center justify-center shrink-0 uppercase shadow-xs">
                  {{ (c.full_name || c.username).charAt(0) }}
                </div>
                <div class="min-w-0">
                  <h4 class="font-headline font-bold text-sm text-on-surface truncate">{{ c.full_name }}</h4>
                  <p class="text-xs text-on-surface-variant truncate">@{{ c.username }}</p>
                  <p v-if="c.teaches && c.teaches.length" class="text-[11px] text-primary font-semibold truncate">
                    Teaches {{ c.teaches[0] }}
                  </p>
                </div>
              </div>
              <NuxtLink
                :to="'/chat?id=' + c.user_id"
                class="px-3 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-xs flex items-center gap-1.5 shrink-0"
              >
                <span>Chat &amp; Call</span>
                <span class="material-symbols-outlined text-sm">videocam</span>
              </NuxtLink>
            </div>
          </div>
        </section>
      </main>

      <!-- Footer -->
      <footer class="bg-surface-container-lowest mt-12 border-t border-surface-container">
        <div class="w-full py-8 px-6 max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="font-display text-sm font-bold text-primary">SkillLoop</span>
            <span class="font-body text-xs text-on-surface-variant">© 2025 • Empowering Peer-to-Peer Learning</span>
          </div>
        </div>
      </footer>

      <!-- Edit Profile Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-surface-container-lowest rounded-3xl p-8 shadow-2xl w-full max-w-lg border border-surface-container-high space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="font-display text-xl font-bold text-on-surface">Edit Profile</h2>
            <button @click="showEditModal = false" class="p-2 rounded-full hover:bg-surface-container transition-colors">
              <span class="material-symbols-outlined text-on-surface-variant">close</span>
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Full Name</label>
              <input v-model="editProfile.full_name" class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors" placeholder="Your full name"/>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Department</label>
                <input v-model="editProfile.department" class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors" placeholder="e.g. CS, MBA"/>
              </div>
              <div>
                <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Semester</label>
                <input v-model.number="editProfile.semester" type="number" min="1" max="12" class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors"/>
              </div>
            </div>
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Bio</label>
              <textarea v-model="editProfile.bio" rows="3" class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors resize-none" placeholder="Tell peers about yourself..."></textarea>
            </div>
          </div>
          <div class="flex gap-3 pt-2">
            <button @click="saveProfile" class="flex-1 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-semibold text-sm hover:bg-primary-dim active:scale-95 transition-all">Save Changes</button>
            <button @click="showEditModal = false" class="px-6 py-2.5 rounded-xl border border-surface-variant text-on-surface-variant hover:bg-surface-container font-headline font-semibold text-sm transition-all">Cancel</button>
          </div>
        </div>
      </div>
    </template>

    <!-- ── LIVE INCOMING CONNECTION REQUEST MODAL ─────────────────── -->
    <transition name="slide-in">
      <div v-if="liveRequest" class="fixed bottom-6 right-6 z-[100] w-80 bg-white rounded-3xl shadow-2xl border-2 border-primary/30 p-5 space-y-4">
        <div class="flex items-start justify-between gap-2">
          <div class="flex items-center gap-2">
            <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-primary to-tertiary text-white font-bold text-base flex items-center justify-center shadow-sm shrink-0 uppercase">
              {{ (liveRequest.full_name || liveRequest.username || '?').charAt(0) }}
            </div>
            <div>
              <p class="font-headline font-bold text-sm text-on-surface">{{ liveRequest.full_name }}</p>
              <p class="text-[11px] text-primary font-semibold">@{{ liveRequest.username }}</p>
            </div>
          </div>
          <button @click="liveRequest = null" class="p-1 rounded-full hover:bg-surface-container text-on-surface-variant transition-colors shrink-0">
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>
        <div class="px-3 py-2 bg-surface-container-low rounded-2xl text-xs space-y-1">
          <p class="font-bold text-on-surface-variant uppercase tracking-wider text-[10px]">🔔 New Loop Request</p>
          <p class="text-on-surface font-semibold">{{ liveRequest.full_name }} wants to connect with you!</p>
          <div v-if="liveRequest.teaches && liveRequest.teaches.length" class="flex flex-wrap gap-1 pt-1">
            <span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-[10px] font-bold rounded-md">Offers: {{ liveRequest.teaches.slice(0,2).join(', ') }}</span>
            <span v-if="liveRequest.learns && liveRequest.learns.length" class="px-2 py-0.5 bg-primary/10 text-primary text-[10px] font-bold rounded-md">Wants: {{ liveRequest.learns.slice(0,2).join(', ') }}</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button @click="acceptLiveRequest" class="flex-1 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all flex items-center justify-center gap-1.5">
            <span class="material-symbols-outlined text-base">check_circle</span>
            Accept Connection
          </button>
          <button @click="declineLiveRequest" class="py-2 px-3 rounded-xl bg-surface-container-low text-on-surface-variant hover:text-error hover:bg-error/10 font-headline text-xs font-semibold active:scale-95 transition-all">Decline</button>
        </div>
      </div>
    </transition>

    <!-- ── CONNECTION ACCEPTED TOAST ──────────────────────────────── -->
    <transition name="slide-in">
      <div v-if="acceptedToast" class="fixed bottom-6 left-6 z-[100] w-72 bg-emerald-600 text-white rounded-2xl shadow-2xl p-4 flex items-center gap-3">
        <span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">check_circle</span>
        <div>
          <p class="font-headline font-bold text-sm">Connection Accepted!</p>
          <p class="text-xs text-emerald-100">{{ acceptedToast }} accepted your request.</p>
        </div>
        <button @click="acceptedToast = null" class="ml-auto shrink-0 opacity-70 hover:opacity-100">
          <span class="material-symbols-outlined text-base">close</span>
        </button>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, computed } from 'vue'
import { io } from 'socket.io-client'

const user = ref(null)
const teaches = ref([])
const learns = ref([])
const cycles = ref([])
const newTeach = ref('')
const newLearn = ref('')
const isAdding = ref(false)
const isLoadingCycles = ref(false)
const pending = ref(true)
const error = ref(null)

const pendingConnections = ref([])
const activeConnections = ref([])
const loadingConnections = ref(true)

const searchPeerQuery = ref('')
const searchPeerResults = ref([])
const isSearchingPeers = ref(false)

const showEditModal = ref(false)
const verifiedSkills = ref([])
const editProfile = ref({
  full_name: '', department: '', semester: 1,
  bio: '', education: '', qualifications: '', experience: '', github: '', linkedin: ''
})

// Real-time notification state
const liveRequest = ref(null)         // incoming connection request popup
const acceptedToast = ref(null)       // "someone accepted your request" toast
const liveNotifCount = ref(0)         // extra badge count beyond pendingConnections
const showNotificationsPanel = ref(false)
let dashSocket = null

const setupDashSocket = () => {
  const backendUrl = typeof window !== 'undefined'
    ? ((window.location.protocol === 'https:' || !window.location.port)
        ? window.location.origin
        : `${window.location.protocol}//${window.location.hostname}:5000`)
    : 'http://localhost:5000'
  dashSocket = io(backendUrl, { withCredentials: true, transports: ['polling', 'websocket'] })

  dashSocket.on('connection_request', (data) => {
    liveRequest.value = data
    liveNotifCount.value++
    // Also add to pendingConnections list immediately
    pendingConnections.value.unshift({
      id: data.connection_id,
      user_id: data.requester_id,
      username: data.username,
      full_name: data.full_name,
      department: data.department,
      skill_offered: data.teaches?.join(', ') || 'Various Skills',
      skill_wanted: data.learns?.join(', ') || 'New Skills',
      teaches: data.teaches || [],
      learns: data.learns || [],
    })
  })

  dashSocket.on('connection_accepted', (data) => {
    acceptedToast.value = data.accepted_by_name
    // Auto-dismiss toast after 5s
    setTimeout(() => { acceptedToast.value = null }, 5000)
    // Refresh connections list
    fetchConnections()
    fetchCycles()
  })
}

const acceptLiveRequest = async () => {
  if (!liveRequest.value) return
  const connId = liveRequest.value.connection_id
  liveNotifCount.value = Math.max(0, liveNotifCount.value - 1)
  liveRequest.value = null
  await respondConnection(connId, 'accepted')
}

const declineLiveRequest = async () => {
  if (!liveRequest.value) return
  const connId = liveRequest.value.connection_id
  liveNotifCount.value = Math.max(0, liveNotifCount.value - 1)
  liveRequest.value = null
  await respondConnection(connId, 'rejected')
}

const getCyclePeer = (cycle) => {
  if (!cycle || !cycle.nodes) return null
  return cycle.nodes.find(n => n.user_id !== user.value?.id)
}

const isPeerConnected = (peerId) => {
  return activeConnections.value.some(c => c.user_id === peerId)
}

const searchPeers = async () => {
  const q = searchPeerQuery.value.trim()
  if (!q) {
    searchPeerResults.value = []
    return
  }
  isSearchingPeers.value = true
  try {
    const res = await fetch(`/api/users/search?q=${encodeURIComponent(q)}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      searchPeerResults.value = data.users || []
    }
  } catch (e) {
    console.error(e)
  } finally {
    isSearchingPeers.value = false
  }
}

const connectWithPeer = async (peer) => {
  await sendConnectRequest(peer.id)
  await searchPeers()
}

const sendConnectRequest = async (receiverId) => {
  try {
    const res = await fetch('/api/connect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ receiver_id: receiverId })
    })
    const data = await res.json()
    if (!res.ok) {
      alert(data.error || "Could not send connection request.")
    }
    await Promise.all([fetchConnections(), fetchCycles()])
  } catch (e) {
    console.error(e)
  }
}

const respondConnection = async (connId, status) => {
  try {
    const res = await fetch(`/api/connect/${connId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status })
    })
    if (res.ok) {
      await Promise.all([fetchConnections(), fetchCycles()])
    }
  } catch(e) { console.error(e) }
}

onMounted(async () => {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      user.value = data.user
      editProfile.value = {
        full_name: user.value.full_name || '',
        department: user.value.department || '',
        semester: user.value.semester || 1,
        bio: user.value.bio || '',
        education: user.value.education || '',
        qualifications: user.value.qualifications || '',
        experience: user.value.experience || '',
        github: user.value.github || '',
        linkedin: user.value.linkedin || ''
      }
      await Promise.all([fetchSkills(), fetchCycles(), fetchConnections(), fetchVerifications()])
      setupDashSocket()
    } else {
      error.value = 'Not authenticated'
    }
  } catch (e) {
    error.value = e.message
  } finally {
    pending.value = false
  }
})

onUnmounted(() => {
  if (dashSocket) { dashSocket.disconnect(); dashSocket = null }
})

const fetchVerifications = async () => {
  try {
    const res = await fetch('/api/quiz/verified', { credentials: 'include' })
    if (res.ok) { const d = await res.json(); verifiedSkills.value = d.verified || [] }
  } catch(e) { console.error(e) }
}

const fetchSkills = async () => {
  try {
    const res = await fetch('/api/skills', { credentials: 'include' })
    if (res.ok) { const d = await res.json(); teaches.value = d.teaches; learns.value = d.learns }
  } catch(e) { console.error(e) }
}

const fetchCycles = async () => {
  isLoadingCycles.value = true
  try {
    const res = await fetch('/api/matches', { credentials: 'include' })
    if (res.ok) { const d = await res.json(); cycles.value = d.cycles }
  } catch(e) { console.error(e) }
  finally { isLoadingCycles.value = false }
}

const fetchConnections = async () => {
  try {
    const res = await fetch('/api/connections', { credentials: 'include' })
    if(res.ok) { const data = await res.json(); pendingConnections.value = data.pending; activeConnections.value = data.active }
  } catch(e) { console.error(e) }
  finally { loadingConnections.value = false }
}

const saveProfile = async () => {
  try {
    const res = await fetch('/api/user/me', { method: 'PUT', headers: { 'Content-Type': 'application/json' }, credentials: 'include', body: JSON.stringify(editProfile.value) })
    if(res.ok) {
      showEditModal.value = false
      const r = await fetch('/api/user/me', { credentials: 'include' })
      if(r.ok) user.value = (await r.json()).user
    }
  } catch(e) { console.error(e) }
}

const addSkill = async (type) => {
  const skillName = type === 'teaches' ? newTeach.value.trim() : newLearn.value.trim()
  if (!skillName) return
  isAdding.value = true
  try {
    const res = await fetch('/api/skills', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'include', body: JSON.stringify({ skill_name: skillName, skill_type: type }) })
    if (res.ok) {
      if (type === 'teaches') newTeach.value = ''
      else newLearn.value = ''
      await Promise.all([fetchSkills(), fetchCycles()])
    }
  } catch (e) { console.error(e) }
  finally { isAdding.value = false }
}

const removeSkill = async (id) => {
  try {
    await fetch(`/api/skills/${id}`, { method: 'DELETE', credentials: 'include' })
    await Promise.all([fetchSkills(), fetchCycles()])
  } catch(e) { console.error(e) }
}

const logout = async () => {
  try {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' })
  } catch(e) {}
  window.location.href = '/login'
}
</script>

<style scoped>
.slide-in-enter-active, .slide-in-leave-active { transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-in-enter-from, .slide-in-leave-to { transform: translateY(20px); opacity: 0; }
</style>



