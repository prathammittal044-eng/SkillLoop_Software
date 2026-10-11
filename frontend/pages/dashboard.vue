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
        <div class="flex justify-between items-center w-full px-3.5 sm:px-6 py-2.5 sm:py-3 max-w-7xl mx-auto">
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
              <NuxtLink to="/profile" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">
                <span class="material-symbols-outlined text-lg">person</span>
                Profile
              </NuxtLink>
            </nav>
          </div>
          <div class="flex items-center gap-1.5 sm:gap-3 shrink-0">
            <div class="flex items-center gap-1 bg-surface-container-lowest px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full border border-secondary-fixed shadow-sm text-xs sm:text-sm font-label font-bold text-on-surface whitespace-nowrap shrink-0">
              <span class="material-symbols-outlined text-primary text-base sm:text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
              <span>{{ user.time_credits || 0 }} <span class="hidden sm:inline">Credits</span><span class="sm:hidden">cr</span></span>
            </div>
            <!-- Notification Bell & Flyout Container -->
            <div class="relative shrink-0">
              <button 
                @click="showNotificationsPanel = !showNotificationsPanel" 
                class="relative w-8 sm:w-9 h-8 sm:h-9 rounded-full bg-surface-container-low border border-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors shrink-0"
                :class="{ 'ring-2 ring-primary/40 text-primary bg-surface-container': showNotificationsPanel }"
                title="Notifications"
                aria-label="Toggle notifications"
              >
                <span class="material-symbols-outlined text-lg sm:text-xl">notifications</span>
                <span 
                  v-if="totalBadgeCount > 0" 
                  class="absolute -top-1 -right-1 min-w-[1.1rem] h-4 sm:h-5 px-1 rounded-full bg-error text-on-error text-[9px] sm:text-[10px] font-extrabold flex items-center justify-center shadow-sm animate-pulse"
                >
                  {{ totalBadgeCount > 99 ? '99+' : totalBadgeCount }}
                </span>
              </button>

              <!-- Backdrop overlay for mobile & click outside -->
              <div 
                v-if="showNotificationsPanel" 
                @click="showNotificationsPanel = false" 
                class="fixed inset-0 z-40 bg-black/20 sm:bg-transparent"
              ></div>

              <!-- Notifications Flyout Dropdown -->
              <div 
                v-if="showNotificationsPanel" 
                class="absolute right-0 top-full mt-2 w-[calc(100vw-2rem)] sm:w-96 max-w-sm bg-surface-container-lowest rounded-2xl shadow-2xl border border-surface-container-high z-50 overflow-hidden flex flex-col max-h-[80vh] sm:max-h-[34rem] origin-top-right transition-all"
              >
                <!-- Flyout Header -->
                <div class="px-4 py-3 bg-surface-container-low/80 border-b border-surface-container flex items-center justify-between shrink-0">
                  <div class="flex items-center gap-2">
                    <span class="font-headline font-bold text-sm sm:text-base text-on-surface">Notifications</span>
                    <span 
                      v-if="totalBadgeCount > 0" 
                      class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] font-bold"
                    >
                      {{ totalBadgeCount }} new
                    </span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <button 
                      v-if="unreadNotifsCount > 0" 
                      @click="markAllNotificationsRead" 
                      class="text-[11px] font-semibold text-primary hover:text-primary-dim hover:underline px-1.5 py-0.5 rounded transition-colors"
                      title="Mark all as read"
                    >
                      Mark all read
                    </button>
                    <button 
                      @click="showNotificationsPanel = false" 
                      class="w-7 h-7 rounded-lg text-on-surface-variant hover:text-on-surface hover:bg-surface-container flex items-center justify-center transition-colors"
                    >
                      <span class="material-symbols-outlined text-base">close</span>
                    </button>
                  </div>
                </div>

                <!-- Scrollable Body -->
                <div class="overflow-y-auto divide-y divide-surface-container/60 flex-1">
                  <!-- Section 1: Pending Connection Requests (Actionable) -->
                  <div v-if="pendingConnections.length > 0" class="p-3 bg-primary/5 border-b border-primary/10">
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-[11px] font-bold uppercase tracking-wider text-primary flex items-center gap-1">
                        <span class="material-symbols-outlined text-sm">person_add</span> Connection Requests ({{ pendingConnections.length }})
                      </span>
                    </div>
                    <div class="space-y-2">
                      <div 
                        v-for="pc in pendingConnections" 
                        :key="'pconn-' + pc.id"
                        class="p-2.5 rounded-xl bg-surface-container-lowest border border-primary/20 shadow-xs space-y-2"
                      >
                        <div class="flex items-center gap-2.5">
                          <div class="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xs shrink-0 overflow-hidden">
                            <img v-if="pc.profile_picture" :src="pc.profile_picture" @error="pc.profile_picture = null" class="w-full h-full object-cover" />
                            <span v-else>{{ (pc.full_name || pc.username || 'U').charAt(0) }}</span>
                          </div>
                          <div class="flex-1 min-w-0">
                            <p class="text-xs font-bold text-on-surface truncate">{{ pc.full_name || pc.username }}</p>
                            <p class="text-[11px] text-on-surface-variant truncate">
                              <span class="font-medium text-primary">Offers:</span> {{ pc.skill_offered || 'Skills' }}
                            </p>
                          </div>
                        </div>
                        <div class="flex items-center gap-1.5 pt-1">
                          <button 
                            @click="respondConnection(pc.id, 'accepted')" 
                            class="flex-1 py-1.5 px-2 rounded-lg bg-primary text-on-primary text-xs font-bold shadow-xs hover:bg-primary-dim transition-all flex items-center justify-center gap-1"
                          >
                            <span class="material-symbols-outlined text-sm">check</span> Accept
                          </button>
                          <button 
                            @click="respondConnection(pc.id, 'rejected')" 
                            class="py-1.5 px-2.5 rounded-lg bg-surface-container-low text-on-surface-variant hover:text-error text-xs font-semibold transition-all"
                          >
                            Decline
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Section 2: General & Realtime Notifications -->
                  <div v-if="notificationsList.length > 0" class="divide-y divide-surface-container/40">
                    <div 
                      v-for="item in notificationsList" 
                      :key="'notif-' + item.id"
                      @click="handleNotificationClick(item)"
                      class="p-3 hover:bg-surface-container-low/60 transition-colors cursor-pointer flex items-start gap-3 relative group"
                      :class="{ 'bg-primary/5 font-medium': !item.is_read }"
                    >
                      <!-- Type Icon -->
                      <div 
                        class="w-8 h-8 rounded-xl flex items-center justify-center shrink-0 shadow-xs"
                        :class="getNotifColorClass(item.type)"
                      >
                        <span class="material-symbols-outlined text-base">{{ getNotifIcon(item.type) }}</span>
                      </div>

                      <!-- Details -->
                      <div class="flex-1 min-w-0 pr-4">
                        <div class="flex items-center justify-between gap-1 mb-0.5">
                          <p class="text-xs font-bold text-on-surface truncate">{{ item.title }}</p>
                          <span class="text-[10px] text-on-surface-variant/70 shrink-0">{{ formatNotifTime(item.created_at) }}</span>
                        </div>
                        <p class="text-[11px] text-on-surface-variant leading-relaxed line-clamp-2">{{ item.message }}</p>
                      </div>

                      <!-- Unread Indicator Dot & Delete Button -->
                      <div class="shrink-0 flex items-center gap-1">
                        <span v-if="!item.is_read" class="w-2 h-2 rounded-full bg-primary shrink-0"></span>
                        <button 
                          @click.stop="deleteNotificationItem(item.id)" 
                          class="opacity-0 group-hover:opacity-100 p-1 text-on-surface-variant/60 hover:text-error rounded transition-opacity"
                          title="Dismiss"
                        >
                          <span class="material-symbols-outlined text-sm">close</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Empty State -->
                  <div 
                    v-if="notificationsList.length === 0 && pendingConnections.length === 0" 
                    class="py-12 px-6 text-center space-y-3"
                  >
                    <div class="w-12 h-12 rounded-full bg-surface-container mx-auto flex items-center justify-center text-on-surface-variant">
                      <span class="material-symbols-outlined text-2xl">notifications_off</span>
                    </div>
                    <div>
                      <p class="text-xs sm:text-sm font-bold text-on-surface">All caught up!</p>
                      <p class="text-[11px] text-on-surface-variant mt-0.5">No notifications or pending requests right now.</p>
                    </div>
                  </div>
                </div>

                <!-- Flyout Footer -->
                <div 
                  v-if="notificationsList.length > 0" 
                  class="px-4 py-2.5 bg-surface-container-low/50 border-t border-surface-container flex items-center justify-between shrink-0"
                >
                  <button 
                    @click="clearAllNotifications" 
                    class="text-[11px] font-semibold text-on-surface-variant hover:text-error transition-colors flex items-center gap-1"
                  >
                    <span class="material-symbols-outlined text-sm">delete_sweep</span> Clear all
                  </button>
                  <NuxtLink 
                    to="/chat" 
                    @click="showNotificationsPanel = false" 
                    class="text-[11px] font-bold text-primary hover:underline flex items-center gap-0.5"
                  >
                    Open Messages <span class="material-symbols-outlined text-xs">arrow_forward</span>
                  </NuxtLink>
                </div>
              </div>
            </div>
            <NuxtLink to="/profile" class="relative w-8 sm:w-9 h-8 sm:h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-xs sm:text-sm uppercase shadow-sm overflow-hidden hover:ring-2 hover:ring-primary/40 transition-all shrink-0">
              <img v-if="user.profile_picture" :src="user.profile_picture" @error="user.profile_picture = null" class="w-full h-full object-cover" />
              <span v-else>{{ (user.full_name || user.username || 'U').charAt(0) }}</span>
            </NuxtLink>
            <button @click="logout" class="hidden sm:inline text-xs text-on-surface-variant hover:text-error transition-colors font-semibold">Logout</button>
          </div>

        </div>
      </header>


      <!-- ==================== MAIN DASHBOARD CONTAINER ==================== -->
      <main id="command-center" class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-6 pb-28 md:pb-10 space-y-6">

        <!-- ── SECTION 1: WELCOME & TELEMETRY COMMAND CENTER BANNER ── -->
        <section class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-surface-container-lowest via-surface-container-low to-surface-container p-5 sm:p-7 border border-surface-container shadow-sm">
          <!-- Ambient gradient glow -->
          <div class="absolute -right-20 -top-20 w-64 h-64 bg-primary/10 rounded-full blur-3xl pointer-events-none"></div>
          <div class="absolute -left-20 -bottom-20 w-64 h-64 bg-secondary-fixed/30 rounded-full blur-3xl pointer-events-none"></div>

          <div class="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <!-- Greeting & Dynamic Context Status -->
            <div class="space-y-2.5 max-w-2xl">
              <div class="flex items-center gap-2 flex-wrap">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container/60 text-on-secondary-container text-xs font-semibold font-label">
                  <span class="material-symbols-outlined text-sm">school</span>
                  <span>{{ user.department || 'Campus Student' }} &bull; Semester {{ user.semester || 1 }}</span>
                </div>
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200/80 text-emerald-800 text-xs font-semibold uppercase tracking-wider font-label shadow-xs">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <span>Campus Network Live</span>
                </div>
                <div v-if="cycles.length > 0" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold font-label">
                  <span class="material-symbols-outlined text-sm">hub</span>
                  <span>{{ cycles.length }} Loop Match{{ cycles.length > 1 ? 'es' : '' }}</span>
                </div>
                <div v-if="pendingConnections.length > 0" class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold font-label">
                  <span class="material-symbols-outlined text-sm">notifications</span>
                  <span>{{ pendingConnections.length }} Pending Inbound</span>
                </div>
              </div>

              <h1 class="font-headline text-2xl sm:text-3xl lg:text-4xl font-extrabold text-on-surface tracking-tight">
                Welcome back, {{ user.full_name?.split(' ')[0] || user.username }} <span class="text-primary">✨</span>
              </h1>

              <p class="text-on-surface-variant font-body text-xs sm:text-sm leading-relaxed">
                <template v-if="cycles.length > 0">
                  Our algorithm detected <span class="font-bold text-primary">{{ cycles.length }} reciprocal learning loop{{ cycles.length > 1 ? 's' : '' }}</span> for your skills. Connect below to swap knowledge without currency.
                </template>
                <template v-else-if="teaches.length === 0">
                  Ready to start? Add skills you can teach to unlock 1-on-1 peer learning sessions and time credits.
                </template>
                <template v-else>
                  Your peer exchange profile is active with <span class="font-bold text-primary">{{ teaches.length }} skill{{ teaches.length > 1 ? 's' : '' }} offered</span> and <span class="font-bold text-secondary">{{ learns.length }} learning target{{ learns.length > 1 ? 's' : '' }}</span>.
                </template>
              </p>
            </div>

            <!-- Quick CTAs Group -->
            <div class="flex flex-wrap items-center gap-2.5 shrink-0">
              <button 
                @click="isAdding = !isAdding" 
                class="px-4 py-2.5 rounded-xl bg-primary text-on-primary font-headline text-xs sm:text-sm font-semibold shadow hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-2 cursor-pointer"
              >
                <span class="material-symbols-outlined text-base">{{ isAdding ? 'close' : 'sync_alt' }}</span>
                <span>{{ isAdding ? 'Close Drawer' : 'Propose New Swap' }}</span>
              </button>
              <button 
                @click="openAeeModal(teaches.length > 0 ? teaches[0].name : '')"
                class="px-4 py-2.5 rounded-xl bg-surface-container-lowest border border-outline-variant text-on-surface font-headline text-xs sm:text-sm font-semibold hover:bg-surface-container active:scale-95 transition-all flex items-center gap-2 cursor-pointer shadow-2xs"
              >
                <span class="material-symbols-outlined text-base text-primary">verified</span>
                <span>Log A.E.E. Session</span>
              </button>
              <NuxtLink 
                to="/quiz" 
                class="px-3.5 py-2.5 rounded-xl bg-surface-container-lowest border border-surface-container text-on-surface hover:text-primary hover:bg-surface-container font-headline text-xs sm:text-sm font-semibold active:scale-95 transition-all flex items-center gap-1.5 shadow-2xs"
                title="AI Verification Quiz"
              >
                <span class="material-symbols-outlined text-base text-secondary">psychology</span>
                <span>Take Quiz</span>
              </NuxtLink>
              <NuxtLink 
                to="/resume" 
                class="px-3 py-2.5 rounded-xl bg-surface-container text-on-surface-variant hover:text-primary transition-all active:scale-95 flex items-center gap-1.5"
                title="ATS Verified Resume Studio"
              >
                <span class="material-symbols-outlined text-base">badge</span>
              </NuxtLink>
            </div>
          </div>

          <!-- Telemetry 4-Column Grid -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mt-6 pt-5 border-t border-surface-container-high/60">
            <!-- Telemetry 1: Escrow Balance -->
            <div class="p-4 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-sm border border-surface-container">
              <div class="flex items-center justify-between text-xs text-on-surface-variant font-medium">
                <span>Escrow Balance</span>
                <span class="material-symbols-outlined text-amber-500 text-sm" style="font-variation-settings: 'FILL' 1;">lock_clock</span>
              </div>
              <div class="mt-2 flex items-baseline gap-1.5 flex-wrap">
                <span class="font-mono text-2xl font-bold text-on-surface">{{ (user.time_credits || 0).toFixed(1) }}</span>
                <span class="text-xs font-mono font-medium text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded">
                  {{ activeSessionsList.length }} session{{ activeSessionsList.length !== 1 ? 's' : '' }} held
                </span>
              </div>
              <p class="text-[11px] text-on-surface-variant mt-1">1 hr taught = 1.0 Time Credit</p>
            </div>

            <!-- Telemetry 2: Level & XP Progression -->
            <div class="p-4 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-sm border border-surface-container">
              <div class="flex items-center justify-between text-xs text-on-surface-variant font-medium">
                <span>Level {{ user.level || 1 }} Peer</span>
                <span class="font-mono text-xs font-bold text-primary">{{ user.xp || 0 }} XP</span>
              </div>
              <div class="w-full bg-surface-container h-2 rounded-full overflow-hidden mt-3">
                <div class="bg-primary h-full rounded-full transition-all duration-500" :style="`width: ${Math.min(((user.xp || 0) % 100), 100)}%;`"></div>
              </div>
              <div class="mt-2 flex justify-between items-center text-[11px] text-on-surface-variant font-label">
                <span>Tier Progress</span>
                <span class="text-primary font-semibold">{{ 100 - ((user.xp || 0) % 100) }} XP to Next Level</span>
              </div>
            </div>

            <!-- Telemetry 3: Active Barter Loops -->
            <div class="p-4 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-sm border border-surface-container">
              <div class="flex items-center justify-between text-xs text-on-surface-variant font-medium">
                <span>Active Barter Loops</span>
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
              </div>
              <div class="mt-2 flex items-baseline gap-1.5 flex-wrap">
                <span class="font-mono text-2xl font-bold text-on-surface">{{ cycles.length }} Loops</span>
                <span class="text-xs font-semibold text-primary bg-primary/10 px-1.5 py-0.5 rounded">
                  {{ pendingConnections.length }} Inbound
                </span>
              </div>
              <p class="text-[11px] text-on-surface-variant mt-1">Circular multi-peer solver ready</p>
            </div>

            <!-- Telemetry 4: Consensus Trust Score -->
            <div class="p-4 rounded-2xl bg-surface-container-lowest/80 backdrop-blur-sm border border-surface-container">
              <div class="flex items-center justify-between text-xs text-on-surface-variant font-medium">
                <span>Consensus Trust Score</span>
                <span class="material-symbols-outlined text-amber-500 text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
              </div>
              <div class="mt-2 flex items-baseline gap-1.5 flex-wrap">
                <span class="font-mono text-2xl font-bold text-on-surface">{{ user.rating_avg > 0 ? user.rating_avg.toFixed(1) : '5.0' }}</span>
                <span class="text-xs font-label text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded font-semibold">100% On-Time</span>
              </div>
              <p class="text-[11px] text-on-surface-variant mt-1">From {{ user.rating_count || 0 }} Verified Peer Audits</p>
            </div>
          </div>
        </section>

        <!-- ── ADD SKILL DRAWER (Shown when isAdding) ── -->
        <div v-if="isAdding" class="bg-surface-container-lowest rounded-3xl p-5 sm:p-6 border border-primary/30 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary text-xl">add_circle</span>
              <h3 class="font-headline font-bold text-base text-on-surface">Propose New Skill Barter</h3>
            </div>
            <button @click="isAdding = false" class="text-on-surface-variant hover:text-on-surface p-1 rounded-lg">
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="space-y-2">
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block">I Can Teach (Skill Offered)</label>
              <div class="flex gap-2">
                <input v-model="newTeach" placeholder="e.g. Python, UI/UX, Guitar, Calculus" class="flex-1 px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-xs sm:text-sm focus:outline-none focus:border-primary transition-colors"/>
                <button @click="addSkill('teaches')" :disabled="!newTeach.trim()" class="px-4 py-2.5 rounded-xl bg-primary text-on-primary text-xs sm:text-sm font-bold hover:bg-primary-dim disabled:opacity-50 transition-colors cursor-pointer">Add</button>
              </div>
            </div>
            <div class="space-y-2">
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block">I Want to Learn (Learning Target)</label>
              <div class="flex gap-2">
                <input v-model="newLearn" placeholder="e.g. Machine Learning, Figma, Public Speaking" class="flex-1 px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-xs sm:text-sm focus:outline-none focus:border-primary transition-colors"/>
                <button @click="addSkill('learns')" :disabled="!newLearn.trim()" class="px-4 py-2.5 rounded-xl bg-secondary text-on-secondary text-xs sm:text-sm font-bold hover:bg-secondary-dim disabled:opacity-50 transition-colors cursor-pointer">Add</button>
              </div>
            </div>
          </div>
        </div>

        <!-- ── INCOMING A.E.E. PROOF-OF-WORK REQUESTS ── -->
        <div v-if="incomingAee.length > 0" class="p-5 rounded-3xl bg-gradient-to-r from-primary/10 via-surface-container-low to-secondary-container/20 border-2 border-primary/30 shadow-md space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2.5">
            <div class="flex items-center gap-2.5 min-w-0">
              <span class="w-8 h-8 rounded-xl bg-primary text-on-primary flex items-center justify-center shadow-xs shrink-0">
                <span class="material-symbols-outlined text-lg">verified</span>
              </span>
              <div class="min-w-0">
                <h3 class="font-headline font-bold text-sm text-on-surface">A.E.E. Proof-of-Work Confirmation Required</h3>
                <p class="text-xs text-on-surface-variant">A learning partner logged an Applied Exchange session. Confirm to verify their proof-of-work.</p>
              </div>
            </div>
            <span class="px-2.5 py-0.5 rounded-full bg-primary text-on-primary text-xs font-bold font-label shrink-0">{{ incomingAee.length }} Pending</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
            <div 
              v-for="item in incomingAee" 
              :key="item.id"
              class="p-4 rounded-2xl bg-surface-container-lowest border border-surface-container shadow-xs flex flex-col justify-between gap-3"
            >
              <div>
                <div class="flex items-center justify-between mb-1">
                  <div class="flex items-center gap-2">
                    <div class="w-7 h-7 rounded-lg bg-primary/10 text-primary font-bold text-xs flex items-center justify-center uppercase">
                      {{ (item.teacher_name || item.teacher_username || '?').charAt(0) }}
                    </div>
                    <span class="font-headline font-bold text-xs text-on-surface">{{ item.teacher_name }} (@{{ item.teacher_username }})</span>
                  </div>
                  <span class="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-800 text-[10px] font-bold uppercase">{{ item.skill_name }}</span>
                </div>
                <p class="text-xs text-on-surface-variant mt-1 leading-relaxed">
                  <span class="font-semibold text-on-surface">Topic:</span> {{ item.topic_notes || 'Peer teaching & execution session' }} 
                  <span class="text-[10px] text-on-surface-variant font-mono">({{ item.duration_minutes }}m)</span>
                </p>
              </div>

              <div class="flex items-center gap-2 pt-2 border-t border-surface-container/60">
                <button 
                  @click="respondAee(item.id, 'confirm')"
                  class="flex-1 py-1.5 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all flex items-center justify-center gap-1 shadow-xs cursor-pointer"
                >
                  <span class="material-symbols-outlined text-sm">check_circle</span>
                  <span>Confirm &amp; Award +15 XP</span>
                </button>
                <button 
                  @click="respondAee(item.id, 'reject')"
                  class="py-1.5 px-3 rounded-xl bg-surface-container-low text-on-surface-variant hover:text-error hover:bg-error/10 font-headline text-xs font-semibold active:scale-95 transition-all cursor-pointer"
                >
                  Decline
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== MAIN 12-COLUMN BENTO GRID ==================== -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

          <!-- ================= LEFT / CENTER REGION (8 COLS) ================= -->
          <div class="lg:col-span-8 space-y-6">

            <!-- 2.A: Time Credit Escrow & Scheduled Sessions -->
            <section id="sessions-section" class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm">
              <!-- Smart Escrow Notice -->
              <div class="flex items-start gap-3 p-3.5 rounded-2xl bg-surface-container-low border border-surface-container-high mb-5">
                <span class="material-symbols-outlined text-primary text-xl mt-0.5">verified_user</span>
                <div class="text-xs leading-relaxed">
                  <span class="font-bold text-on-surface">Smart Escrow Protection Active:</span>
                  <span class="text-on-surface-variant ml-1">Credits are securely locked until both students mutually confirm session completion via cryptographic consensus verification.</span>
                </div>
              </div>

              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
                <div>
                  <h2 class="font-headline text-lg font-bold text-on-surface flex items-center gap-2">
                    <span>Scheduled Peer Sessions</span>
                    <span class="px-2 py-0.5 rounded-full text-xs font-mono font-bold bg-primary-container text-on-primary-container">
                      {{ activeSessionsList.length }} Upcoming
                    </span>
                  </h2>
                  <p class="text-xs text-on-surface-variant">Verify attendance and release escrow instantly upon completion</p>
                </div>

                <!-- Tab Switcher & Schedule Action -->
                <div class="flex items-center gap-2 flex-wrap">
                  <div class="bg-surface-container-low p-1 rounded-xl flex gap-1 text-xs font-semibold">
                    <button
                      type="button"
                      @click="sessionTab = 'active'"
                      class="px-3 py-1 rounded-lg transition-all"
                      :class="sessionTab === 'active' ? 'bg-white shadow-xs text-primary font-bold' : 'text-on-surface-variant hover:text-on-surface'"
                    >
                      Active ({{ activeSessionsList.length }})
                    </button>
                    <button
                      type="button"
                      @click="sessionTab = 'history'"
                      class="px-3 py-1 rounded-lg transition-all"
                      :class="sessionTab === 'history' ? 'bg-white shadow-xs text-primary font-bold' : 'text-on-surface-variant hover:text-on-surface'"
                    >
                      History ({{ historySessionsList.length }})
                    </button>
                  </div>

                  <button
                    type="button"
                    @click="openBookModal(null)"
                    class="px-3 py-1.5 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-xs flex items-center gap-1 shrink-0 cursor-pointer"
                  >
                    <span class="material-symbols-outlined text-sm">add</span>
                    <span>Schedule</span>
                  </button>
                </div>
              </div>

              <!-- Active & Pending Tab Content -->
              <div v-if="sessionTab === 'active'">
                <!-- Empty State when no active sessions -->
                <div 
                  v-if="activeSessionsList.length === 0" 
                  class="p-5 sm:p-6 rounded-2xl bg-gradient-to-r from-surface-container-low via-surface-bright to-surface-container-low border border-primary/20 shadow-xs flex flex-col md:flex-row items-center justify-between gap-4"
                >
                  <div class="flex items-center gap-3.5">
                    <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-primary to-secondary text-on-primary flex items-center justify-center shrink-0 shadow-sm">
                      <span class="material-symbols-outlined text-xl">event_available</span>
                    </div>
                    <div class="space-y-0.5">
                      <div class="flex items-center gap-2">
                        <h4 class="font-headline font-bold text-sm text-on-surface">No Active Sessions Staged</h4>
                        <span class="px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-bold">Escrow Ready</span>
                      </div>
                      <p class="text-xs text-on-surface-variant max-w-xl">
                        <template v-if="cycles.length > 0">
                          An algorithmic loop is ready with <strong class="text-on-surface">{{ getCyclePeer(cycles[0])?.name || 'a peer' }}</strong>. Schedule a 1:1 session to lock credits safely.
                        </template>
                        <template v-else>
                          Book a 1:1 peer learning session with your {{ (user.time_credits || 0).toFixed(1) }} available credits—escrow safely locks credits until you confirm completion.
                        </template>
                      </p>
                    </div>
                  </div>

                  <button
                    type="button"
                    @click="openBookModal(cycles.length > 0 ? getCyclePeer(cycles[0]) : null, cycles.length > 0 ? getCyclePeer(cycles[0])?.teaches_next : null)"
                    class="w-full sm:w-auto px-4 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-sm flex items-center justify-center gap-1.5 cursor-pointer shrink-0"
                  >
                    <span class="material-symbols-outlined text-sm">event</span>
                    <span>{{ cycles.length > 0 ? 'Schedule Matched Peer' : 'Schedule 1:1 Session' }}</span>
                  </button>
                </div>

                <!-- Active Sessions List -->
                <div v-else class="space-y-3.5">
                  <div
                    v-for="item in activeSessionsList"
                    :key="'sess_' + item.id"
                    class="p-4 sm:p-5 rounded-2xl border border-surface-container-high hover:border-primary/40 bg-surface-container-lowest transition-all"
                  >
                    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div class="flex items-center gap-3.5">
                        <div
                          class="w-12 h-12 rounded-2xl text-white font-bold text-sm flex items-center justify-center uppercase shrink-0 shadow-xs ring-2 ring-surface-container"
                          :style="{ background: item.peer_avatar || '#543ce0' }"
                        >
                          {{ (item.peer_name || item.peer_username || '?').charAt(0) }}
                        </div>
                        <div>
                          <div class="flex items-center gap-2">
                            <h3 class="font-headline text-sm font-bold text-on-surface">{{ item.peer_name }}</h3>
                            <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-surface-container text-on-surface-variant">
                              {{ item.my_role === 'teacher' ? 'Learner: ' : 'Teacher: ' }}@{{ item.peer_username }}
                            </span>
                          </div>
                          <div class="flex flex-wrap items-center gap-1.5 text-xs mt-1 text-on-surface-variant">
                            <span class="font-medium text-primary bg-surface-container-low px-1.5 py-0.2 rounded text-[11px]">
                              Skill: {{ item.skill_name }} ({{ item.duration_minutes }}m)
                            </span>
                            <span v-if="item.topic_notes" class="text-on-surface-variant text-[11px] truncate max-w-xs">
                              &bull; "{{ item.topic_notes }}"
                            </span>
                          </div>
                        </div>
                      </div>

                      <!-- Timing Info -->
                      <div class="flex sm:flex-col items-center sm:items-end justify-between text-right">
                        <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 text-xs font-mono font-semibold">
                          <span class="material-symbols-outlined text-sm">schedule</span>
                          <span>{{ formatSessionTime(item.scheduled_at) }}</span>
                        </span>
                        <span class="text-[11px] text-on-surface-variant mt-1">Virtual Loop Sandbox</span>
                      </div>
                    </div>

                    <!-- Action Footer -->
                    <div class="mt-4 pt-3.5 border-t border-surface-container-low flex flex-wrap items-center justify-between gap-3">
                      <div class="flex items-center gap-2 text-xs text-on-surface-variant">
                        <span class="material-symbols-outlined text-amber-500 text-base">lock</span>
                        <span class="font-mono">Escrow: {{ item.credit_cost }} Credit Staged</span>
                      </div>

                      <div class="flex items-center gap-2">
                        <!-- Teacher pending approval -->
                        <template v-if="item.status === 'pending' && item.my_role === 'teacher'">
                          <button
                            type="button"
                            @click="respondSession(item.id, 'accept')"
                            class="px-3.5 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-sm flex items-center gap-1 cursor-pointer"
                          >
                            <span class="material-symbols-outlined text-sm">check_circle</span>
                            <span>Accept Session</span>
                          </button>
                          <button
                            type="button"
                            @click="respondSession(item.id, 'reject')"
                            class="px-3 py-1.5 rounded-lg bg-surface-container text-on-surface-variant hover:text-error font-headline text-xs font-semibold active:scale-95 transition-all cursor-pointer"
                          >
                            Decline
                          </button>
                        </template>

                        <!-- Learner pending waiting -->
                        <template v-else-if="item.status === 'pending' && item.my_role === 'learner'">
                          <span class="text-[11px] text-amber-700 font-mono">Awaiting @{{ item.peer_username }}</span>
                          <button
                            type="button"
                            @click="cancelSession(item.id)"
                            class="text-[11px] text-error hover:underline font-semibold cursor-pointer"
                          >
                            Cancel &amp; Refund
                          </button>
                        </template>

                        <!-- Accepted Session: Chat & Call + Complete -->
                        <template v-else-if="item.status === 'accepted'">
                          <NuxtLink
                            :to="'/chat?id=' + item.peer_id"
                            class="px-3 py-1.5 rounded-lg bg-surface-container text-on-surface hover:bg-surface-container-high font-headline text-xs font-semibold transition-all flex items-center gap-1.5"
                          >
                            <span class="material-symbols-outlined text-sm">chat</span>
                            <span>Chat &amp; Call</span>
                          </NuxtLink>
                          <button
                            type="button"
                            @click="completeSessionAction(item)"
                            class="px-3.5 py-1.5 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 font-headline text-xs font-semibold transition-all shadow-sm flex items-center gap-1.5 cursor-pointer"
                            title="Complete session and release escrow"
                          >
                            <span class="material-symbols-outlined text-sm">check_circle</span>
                            <span>Complete &amp; Release Escrow</span>
                          </button>
                        </template>

                        <!-- Completed Review -->
                        <template v-else-if="item.status === 'completed' && !item.my_review">
                          <button
                            type="button"
                            @click="openReviewModal(item)"
                            class="px-3.5 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-headline text-xs font-semibold shadow-sm flex items-center gap-1 cursor-pointer"
                          >
                            <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
                            <span>Review Peer</span>
                          </button>
                        </template>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- History Tab Content -->
              <div v-else-if="sessionTab === 'history'">
                <div v-if="historySessionsList.length === 0" class="py-8 px-4 text-center rounded-2xl bg-surface-bright/50 border border-dashed border-surface-container text-xs text-on-surface-variant">
                  No completed or past exchange sessions yet.
                </div>
                <div v-else class="space-y-3">
                  <div
                    v-for="item in historySessionsList"
                    :key="'hist_' + item.id"
                    class="p-4 rounded-xl border bg-surface-container-lowest border-surface-container shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                  >
                    <div class="flex items-center gap-3">
                      <div
                        class="w-9 h-9 rounded-xl text-white font-bold text-xs flex items-center justify-center uppercase shrink-0"
                        :style="{ background: item.peer_avatar || '#543ce0' }"
                      >
                        {{ (item.peer_name || item.peer_username || '?').charAt(0) }}
                      </div>
                      <div>
                        <p class="text-xs font-bold text-on-surface">{{ item.peer_name }} &bull; {{ item.skill_name }}</p>
                        <p class="text-[10px] text-on-surface-variant font-mono">{{ formatSessionTime(item.scheduled_at) }} &bull; {{ item.duration_minutes }}m</p>
                      </div>
                    </div>
                    <div class="flex items-center gap-2 self-end sm:self-center">
                      <span
                        class="px-2 py-0.5 rounded-md text-[10px] font-bold uppercase"
                        :class="item.status === 'completed' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'"
                      >
                        {{ item.status }}
                      </span>
                      <button
                        v-if="item.status === 'completed' && !item.my_review"
                        type="button"
                        @click="openReviewModal(item)"
                        class="px-2.5 py-1 rounded-lg bg-amber-500 text-white text-[11px] font-bold hover:bg-amber-600 cursor-pointer"
                      >
                        Review ★
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- 2.B: Algorithmic Loop Exchanges Card -->
            <section id="loops-section" class="bg-surface-container-lowest rounded-3xl border border-secondary-container p-5 sm:p-6 shadow-sm relative overflow-hidden">
              <div class="absolute -right-16 -top-16 w-44 h-44 bg-surface-container-high/40 rounded-full blur-2xl pointer-events-none"></div>

              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                <div>
                  <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-primary-container/40 text-on-primary-container text-[11px] font-bold font-mono uppercase tracking-wider mb-1">
                    <span class="material-symbols-outlined text-sm">hub</span> Circular Barter Engine
                  </div>
                  <h2 class="font-headline text-lg font-bold text-on-surface">
                    {{ cycles.length > 0 ? `${cycles.length} Algorithmic Loop Match${cycles.length > 1 ? 'es' : ''} Ready` : 'Circular Barter Solver' }}
                  </h2>
                </div>
                <div v-if="cycles.length > 0" class="flex items-center gap-1.5 bg-emerald-50 text-emerald-700 px-3 py-1 rounded-full text-xs font-mono font-semibold">
                  <span class="material-symbols-outlined text-base">auto_awesome</span>
                  <span>{{ cycles[0]?.score || 98 }}% Synergy &bull; Zero Deadlock</span>
                </div>
              </div>

              <p class="text-xs text-on-surface-variant mb-5">
                SkillLoop resolves barter deadlocks using multi-party circular chains. No direct bilateral trade required—everyone gives to one student and receives from another without money.
              </p>

              <!-- Loading State -->
              <div v-if="isLoadingCycles" class="p-8 text-center text-on-surface-variant text-xs flex flex-col items-center justify-center gap-3">
                <span class="w-6 h-6 rounded-full border-2 border-primary border-t-transparent animate-spin"></span>
                <span class="font-headline font-semibold">Traversing campus skill graph...</span>
              </div>

              <!-- Empty State -->
              <div v-else-if="cycles.length === 0" class="p-8 rounded-2xl bg-surface-container-low/50 border border-dashed border-surface-container text-center space-y-2">
                <div class="w-12 h-12 rounded-2xl bg-surface-container text-on-surface-variant flex items-center justify-center mx-auto">
                  <span class="material-symbols-outlined text-2xl">hub</span>
                </div>
                <p class="font-headline font-bold text-sm text-on-surface">No circular loops found right now</p>
                <p class="text-xs text-on-surface-variant max-w-sm mx-auto leading-relaxed">
                  Loop matching connects 2 or 3 students where each teaches one and learns from another. Add more teaching and learning targets to unlock matches!
                </p>
                <button @click="isAdding = true" class="mt-2 px-4 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all shadow-2xs cursor-pointer">
                  + Expand My Skills
                </button>
              </div>

              <!-- Cycle Cards List -->
              <div v-else class="space-y-4">
                <div
                  v-for="(cycle, cIdx) in cycles"
                  :key="cIdx"
                  class="p-4 sm:p-5 rounded-2xl bg-surface-container-low/50 border border-surface-container space-y-4"
                >
                  <div class="flex items-center justify-between text-xs">
                    <span class="font-mono font-bold text-primary">{{ cycle.length }}-Party Closed Loop Match</span>
                    <span class="font-mono text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold">{{ cycle.score }}% Match Score</span>
                  </div>

                  <!-- Circular Graph Visual Component -->
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 relative">
                    <div
                      v-for="(node, nIdx) in cycle.nodes"
                      :key="nIdx"
                      class="p-3.5 rounded-xl bg-surface-container-lowest border shadow-sm flex flex-col justify-between"
                      :class="node.name?.toLowerCase() === user.full_name?.toLowerCase() || node.name?.toLowerCase() === user.username?.toLowerCase() ? 'border-2 border-primary' : 'border-surface-container-high'"
                    >
                      <div>
                        <div class="flex items-center gap-2 mb-2">
                          <span class="w-6 h-6 rounded-full text-white text-xs font-bold flex items-center justify-center font-mono" :class="nIdx === 0 ? 'bg-primary' : (nIdx === 1 ? 'bg-secondary' : 'bg-tertiary')">
                            {{ nIdx + 1 }}
                          </span>
                          <span class="font-headline text-xs font-bold text-on-surface truncate">
                            {{ node.name }}
                            <span v-if="node.name?.toLowerCase() === user.full_name?.toLowerCase() || node.name?.toLowerCase() === user.username?.toLowerCase()" class="text-primary font-normal">(You)</span>
                          </span>
                        </div>
                        <div class="text-[11px] space-y-1">
                          <p class="text-on-surface-variant"><span class="font-semibold text-primary">Teaches:</span> {{ node.teaches_next }}</p>
                          <p class="text-on-surface-variant"><span class="font-semibold text-secondary">To:</span> {{ cycle.nodes[(nIdx + 1) % cycle.nodes.length]?.name || 'Next Peer' }}</p>
                        </div>
                      </div>
                      <div class="mt-3 pt-2 border-t border-surface-container text-[10px] text-emerald-700 font-mono font-semibold flex items-center gap-1">
                        <span class="material-symbols-outlined text-xs">check</span>
                        <span>Matched in Loop</span>
                      </div>
                    </div>
                  </div>

                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-3 border-t border-surface-container">
                    <span class="text-xs font-mono text-on-surface-variant flex items-center gap-1.5">
                      <span class="material-symbols-outlined text-primary text-base">repeat</span>
                      <span>Loop Status: <strong class="text-on-surface">Mutual Match Confirmed</strong></span>
                    </span>

                    <div v-if="getCyclePeer(cycle)" class="flex items-center gap-2">
                      <template v-if="isPeerConnected(getCyclePeer(cycle).user_id)">
                        <button
                          type="button"
                          @click="openBookModal(getCyclePeer(cycle), getCyclePeer(cycle)?.teaches_next)"
                          class="px-3.5 py-1.5 rounded-lg bg-surface-container text-on-surface hover:bg-surface-container-high text-xs font-semibold font-headline transition-all cursor-pointer"
                        >
                          Schedule 1:1
                        </button>
                        <NuxtLink
                          :to="'/chat?id=' + getCyclePeer(cycle).user_id"
                          class="px-4 py-1.5 rounded-lg bg-primary text-on-primary hover:bg-primary-dim text-xs font-semibold font-headline transition-all shadow-sm"
                        >
                          Chat &amp; Call
                        </NuxtLink>
                      </template>
                      <button
                        v-else
                        type="button"
                        @click="sendConnectRequest(getCyclePeer(cycle).user_id)"
                        class="px-4 py-1.5 rounded-lg bg-primary text-on-primary hover:bg-primary-dim text-xs font-semibold font-headline transition-all shadow-sm flex items-center gap-1 cursor-pointer"
                      >
                        <span class="material-symbols-outlined text-sm">bolt</span>
                        <span>Connect Loop Partner</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <!-- 2.C: Skill Inventory & Proof-of-Work Telemetry -->
            <section id="skills-section" class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-5">
                <div>
                  <h2 class="font-headline text-lg font-bold text-on-surface">Skill Inventory &amp; Proof-of-Work</h2>
                  <p class="text-xs text-on-surface-variant">180-Day cryptographic decay protocol maintains campus instructional accuracy</p>
                </div>
                <!-- Skill Tabs -->
                <div class="inline-flex p-1 rounded-xl bg-surface-container text-xs font-headline font-semibold">
                  <button 
                    @click="skillInventoryTab = 'teaching'"
                    class="px-3 py-1 rounded-lg transition-all"
                    :class="skillInventoryTab === 'teaching' ? 'bg-surface-container-lowest text-primary shadow-sm font-bold' : 'text-on-surface-variant hover:text-on-surface'"
                  >
                    Skills I Teach ({{ teaches.length }})
                  </button>
                  <button 
                    @click="skillInventoryTab = 'learning'"
                    class="px-3 py-1 rounded-lg transition-all"
                    :class="skillInventoryTab === 'learning' ? 'bg-surface-container-lowest text-primary shadow-sm font-bold' : 'text-on-surface-variant hover:text-on-surface'"
                  >
                    Learning Targets ({{ learns.length }})
                  </button>
                </div>
              </div>

              <!-- Skills I Teach List with Decay Pulse -->
              <div v-if="skillInventoryTab === 'teaching'" class="space-y-3">
                <div v-if="teaches.length === 0" class="p-6 rounded-2xl bg-surface-container-low/50 border border-dashed border-surface-container text-center space-y-2">
                  <p class="text-xs text-on-surface-variant">No teaching skills listed yet. Offer what you know to earn time credits!</p>
                  <button @click="isAdding = true" class="px-3.5 py-1.5 rounded-xl bg-primary text-on-primary text-xs font-bold hover:bg-primary-dim cursor-pointer">
                    + Add Teaching Skill
                  </button>
                </div>

                <div 
                  v-for="skill in teaches" 
                  :key="skill.id"
                  class="p-4 rounded-xl bg-surface border border-surface-container flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                >
                  <div class="flex items-start gap-3">
                    <div class="p-2 rounded-lg bg-primary/10 text-primary mt-0.5">
                      <span class="material-symbols-outlined text-lg">code</span>
                    </div>
                    <div>
                      <div class="flex items-center gap-2">
                        <h3 class="font-headline text-sm font-bold text-on-surface capitalize">{{ skill.name }}</h3>
                        <span v-if="getSkillVerification(skill.name)" class="px-2 py-0.5 rounded text-[10px] font-mono bg-primary-container text-on-primary-container font-semibold">
                          Lvl: {{ getSkillVerification(skill.name).verified_level || 'Mentor' }}
                        </span>
                      </div>
                      <div class="flex items-center gap-3 text-xs text-on-surface-variant mt-1">
                        <!-- Proof-of-Work Heartbeat indicator -->
                        <template v-if="getSkillVerification(skill.name)">
                          <span v-if="getSkillVerification(skill.name).decay_status === 'active'" class="flex items-center gap-1 text-emerald-600 font-mono font-medium">
                            <span class="relative flex h-2 w-2">
                              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                            </span>
                            PoW Active: {{ getSkillVerification(skill.name).days_remaining }}d left
                          </span>
                          <span v-else-if="getSkillVerification(skill.name).decay_status === 'expiring_soon'" class="flex items-center gap-1 text-amber-600 font-mono font-medium animate-pulse">
                            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                            PoW Expiring in {{ getSkillVerification(skill.name).days_remaining }}d!
                          </span>
                          <span v-else class="text-slate-500 font-mono">
                            Decayed &bull; Teach to revive
                          </span>
                        </template>
                        <span v-else class="text-on-surface-variant/70 text-[11px]">Unverified &bull; Quiz available</span>
                      </div>
                    </div>
                  </div>

                  <div class="flex items-center gap-2 self-end sm:self-center">
                    <button 
                      v-if="getSkillVerification(skill.name)"
                      type="button"
                      @click="openAeeModal(skill.name)"
                      class="px-3 py-1.5 rounded-lg border border-surface-container-high hover:bg-surface-container text-xs font-semibold font-headline text-on-surface transition-all cursor-pointer"
                      title="Log Applied Exchange session"
                    >
                      Log A.E.E.
                    </button>
                    <NuxtLink 
                      v-else
                      to="/quiz"
                      class="px-3 py-1.5 rounded-lg bg-surface-container text-primary hover:bg-surface-container-high text-xs font-semibold font-headline transition-all"
                    >
                      Verify (+XP)
                    </NuxtLink>
                    <button 
                      @click="removeSkill(skill.id)" 
                      class="text-on-surface-variant/60 hover:text-error p-1 rounded-lg"
                      title="Remove skill"
                    >
                      <span class="material-symbols-outlined text-sm">delete</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Learning Targets List -->
              <div v-else class="space-y-3">
                <div v-if="learns.length === 0" class="p-6 rounded-2xl bg-surface-container-low/50 border border-dashed border-surface-container text-center space-y-2">
                  <p class="text-xs text-on-surface-variant">No learning targets added yet. Add what you want to learn to unlock barter loops!</p>
                  <button @click="isAdding = true" class="px-3.5 py-1.5 rounded-xl bg-secondary text-white text-xs font-bold hover:bg-secondary-dim cursor-pointer">
                    + Add Learning Target
                  </button>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  <div 
                    v-for="(skill, lIdx) in learns" 
                    :key="skill.id" 
                    class="p-3.5 rounded-xl bg-surface border border-surface-container flex items-center justify-between gap-2"
                  >
                    <div class="flex items-center gap-2 min-w-0">
                      <span class="material-symbols-outlined text-secondary text-base shrink-0">track_changes</span>
                      <span class="font-headline font-bold text-xs sm:text-sm text-on-surface capitalize truncate">{{ skill.name }}</span>
                    </div>
                    <div class="flex items-center gap-1.5 shrink-0">
                      <span class="px-1.5 py-0.5 rounded text-[10px] font-bold font-mono" :class="lIdx === 0 ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700'">
                        {{ lIdx === 0 ? 'HIGH' : 'MED' }}
                      </span>
                      <button @click="removeSkill(skill.id)" class="text-on-surface-variant/60 hover:text-error p-1 rounded">
                        <span class="material-symbols-outlined text-sm">close</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Active Learning Targets Chips Strip -->
              <div v-if="learns.length > 0" class="mt-5 pt-4 border-t border-surface-container">
                <div class="flex items-center justify-between mb-2.5">
                  <span class="font-headline text-xs font-bold text-on-surface uppercase tracking-wider">Active Learning Targets</span>
                  <button @click="isAdding = true" class="text-xs font-headline font-semibold text-primary hover:underline flex items-center gap-1 cursor-pointer">
                    <span class="material-symbols-outlined text-sm">add_circle</span> Add Target
                  </button>
                </div>
                <div class="flex flex-wrap gap-2">
                  <div 
                    v-for="(target, tIdx) in learns" 
                    :key="'chip_' + target.id" 
                    class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-surface border border-surface-container text-xs"
                  >
                    <span class="font-medium text-on-surface capitalize">{{ target.name }}</span>
                    <span class="px-1.5 py-0.2 rounded text-[9px] font-bold font-mono" :class="tIdx === 0 ? 'bg-red-100 text-red-700' : 'bg-primary/10 text-primary'">
                      {{ tIdx === 0 ? 'PRIORITY' : 'TARGET' }}
                    </span>
                  </div>
                </div>
              </div>
            </section>

            <!-- 2.D: Campus Peer Directory -->
            <section id="directory-section" class="bg-surface-container-lowest rounded-3xl p-5 sm:p-6 border border-surface-container shadow-sm space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div class="flex items-center gap-2.5">
                  <div class="w-9 h-9 rounded-xl bg-primary/10 text-primary flex items-center justify-center shrink-0">
                    <span class="material-symbols-outlined text-lg">person_search</span>
                  </div>
                  <div>
                    <h2 class="font-headline text-base sm:text-lg font-bold text-on-surface">Campus Peer Directory</h2>
                    <p class="text-xs text-on-surface-variant">Live search by student name, @username, or department</p>
                  </div>
                </div>

                <!-- Live Search Bar -->
                <div class="relative w-full sm:w-64">
                  <span class="material-symbols-outlined absolute left-3 top-2.5 text-outline text-base pointer-events-none">search</span>
                  <input
                    v-model="searchPeerQuery"
                    @input="searchPeers"
                    type="text"
                    placeholder="Search peers..."
                    class="w-full pl-9 pr-8 py-2 text-xs rounded-full bg-surface-container-lowest border border-surface-container-high focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent font-body"
                  />
                  <button
                    v-if="searchPeerQuery"
                    @click="searchPeerQuery = ''; searchPeerResults = []"
                    class="absolute right-2.5 top-2 text-on-surface-variant hover:text-on-surface"
                  >
                    <span class="material-symbols-outlined text-xs">close</span>
                  </button>
                  <span v-else-if="isSearchingPeers" class="absolute right-2.5 top-2.5 w-3.5 h-3.5 rounded-full border-2 border-primary border-t-transparent animate-spin"></span>
                </div>
              </div>

              <!-- Search Results Grid -->
              <div v-if="searchPeerResults.length > 0" class="pt-2 border-t border-surface-container space-y-3">
                <p class="text-[11px] font-mono text-on-surface-variant uppercase font-semibold">Found {{ searchPeerResults.length }} Campus Peers</p>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div
                    v-for="p in searchPeerResults"
                    :key="p.id"
                    class="p-3.5 rounded-2xl bg-surface border border-surface-container flex flex-col justify-between gap-3"
                  >
                    <div class="flex items-center gap-3">
                      <div class="relative shrink-0">
                        <img
                          v-if="p.profile_picture"
                          :src="p.profile_picture"
                          :alt="p.full_name || p.username"
                          class="w-10 h-10 rounded-xl object-cover ring-2 ring-primary/20"
                          @error="p.profile_picture = null"
                        />
                        <div
                          v-else
                          class="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-secondary text-white font-bold text-xs flex items-center justify-center uppercase shadow-2xs"
                        >
                          {{ (p.full_name || p.username).charAt(0) }}
                        </div>
                      </div>
                      <div class="min-w-0">
                        <h4 class="font-headline font-bold text-xs text-on-surface truncate">{{ p.full_name }}</h4>
                        <p class="text-[11px] text-on-surface-variant truncate">@{{ p.username }} &bull; {{ p.department || 'Student' }}</p>
                        <p v-if="p.teaches && p.teaches.length" class="text-[10px] text-primary font-semibold truncate mt-0.5">
                          Teaches: {{ p.teaches.slice(0, 2).join(', ') }}
                        </p>
                      </div>
                    </div>

                    <div class="pt-2 border-t border-surface-container flex items-center justify-end">
                      <NuxtLink
                        v-if="p.connection_status === 'connected'"
                        :to="'/chat?id=' + p.id"
                        class="px-3 py-1.5 rounded-lg bg-emerald-600 text-white font-headline text-xs font-bold hover:bg-emerald-700 transition-all flex items-center gap-1"
                      >
                        <span class="material-symbols-outlined text-xs">chat</span>
                        <span>Chat &amp; Call</span>
                      </NuxtLink>
                      <button
                        v-else-if="p.connection_status === 'pending_received'"
                        type="button"
                        @click="respondConnection(p.connection_id, 'accepted')"
                        class="px-3 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim transition-all flex items-center gap-1 cursor-pointer"
                      >
                        <span>Accept Request</span>
                      </button>
                      <span
                        v-else-if="p.connection_status === 'pending_sent'"
                        class="px-3 py-1.5 rounded-lg bg-surface-container text-on-surface-variant font-headline text-xs font-semibold"
                      >
                        Pending Sent
                      </span>
                      <button
                        v-else
                        type="button"
                        @click="connectWithPeer(p)"
                        class="px-3 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-xs font-bold hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-1 cursor-pointer"
                      >
                        <span class="material-symbols-outlined text-xs">person_add</span>
                        <span>Connect</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="searchPeerQuery && !isSearchingPeers" class="text-center py-3 text-xs text-on-surface-variant">
                No students found matching "<strong class="text-on-surface">{{ searchPeerQuery }}</strong>".
              </div>
            </section>
          </div>

          <!-- ================= RIGHT COLUMN ASIDE (4 COLS) ================= -->
          <aside class="lg:col-span-4 space-y-6 lg:sticky lg:top-20">

            <!-- 2.E: Student Credential Bento Tile -->
            <div class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm">
              <div class="flex items-start justify-between">
                <div class="flex items-center gap-3">
                  <div class="relative">
                    <img 
                      v-if="user.profile_picture" 
                      :src="user.profile_picture" 
                      @error="user.profile_picture = null"
                      class="w-14 h-14 rounded-2xl object-cover ring-2 ring-primary"
                      alt="Profile Avatar"
                    />
                    <div 
                      v-else
                      class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-primary to-secondary text-white font-bold text-xl flex items-center justify-center uppercase ring-2 ring-primary"
                    >
                      {{ (user.full_name || user.username || 'U').charAt(0) }}
                    </div>
                    <span class="material-symbols-outlined absolute -bottom-1 -right-1 text-primary bg-white rounded-full text-base" style="font-variation-settings: 'FILL' 1;">verified</span>
                  </div>
                  <div>
                    <h3 class="font-headline text-base font-bold text-on-surface">{{ user.full_name || user.username }}</h3>
                    <p class="text-xs text-on-surface-variant font-mono">ID: #SU-{{ user.id || '9042' }}-{{ user.department?.slice(0, 4)?.toUpperCase() || 'EECS' }}</p>
                    <div class="flex items-center gap-1.5 mt-1">
                      <span class="px-2 py-0.2 rounded bg-emerald-50 text-emerald-700 text-[10px] font-mono font-semibold">.edu VERIFIED</span>
                    </div>
                  </div>
                </div>
                <button @click="showEditModal = true" class="p-1.5 rounded-lg text-on-surface-variant hover:bg-surface-container cursor-pointer" title="Edit Profile Details">
                  <span class="material-symbols-outlined text-base">settings</span>
                </button>
              </div>

              <!-- 3-Stat Ledger -->
              <div class="grid grid-cols-3 gap-2 mt-5 py-3 border-y border-surface-container text-center">
                <div>
                  <span class="font-mono text-base font-bold text-on-surface block">{{ formatTeachingDuration(user.total_teaching_seconds) }}</span>
                  <p class="text-[10px] text-on-surface-variant uppercase tracking-wider font-label">Taught</p>
                </div>
                <div>
                  <span class="font-mono text-base font-bold text-on-surface block">{{ user.total_sessions || user.sessions_completed || 0 }}</span>
                  <p class="text-[10px] text-on-surface-variant uppercase tracking-wider font-label">Sessions</p>
                </div>
                <div>
                  <span class="font-mono text-base font-bold text-primary block">{{ user.rating_avg > 0 ? user.rating_avg.toFixed(1) + ' ★' : '5.0 ★' }}</span>
                  <p class="text-[10px] text-on-surface-variant uppercase tracking-wider font-label">Rating</p>
                </div>
              </div>

              <div class="mt-4">
                <div class="flex items-center justify-between text-xs mb-2">
                  <span class="font-semibold text-on-surface">Campus Attestation Hash</span>
                  <span class="font-mono text-[10px] text-primary">0x9f8c...{{ (user.id || 'SU').toString().padStart(4, '0') }}</span>
                </div>
                <NuxtLink 
                  to="/resume"
                  class="w-full py-2.5 rounded-xl bg-surface-container-low hover:bg-surface-container text-primary font-headline text-xs font-semibold flex items-center justify-center gap-1.5 transition-all shadow-2xs"
                >
                  <span class="material-symbols-outlined text-sm">badge</span>
                  <span>ATS Career Canvas &amp; Proof Sheet</span>
                </NuxtLink>
              </div>
            </div>

            <!-- 2.F: Bilateral Pending Barter Requests -->
            <div id="requests-section" class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-headline text-sm font-bold text-on-surface flex items-center gap-1.5">
                  <span>Pending Inbound Swaps</span>
                  <span class="w-5 h-5 rounded-full bg-secondary-container text-on-secondary-container text-[11px] font-mono font-bold flex items-center justify-center">
                    {{ pendingConnections.length }}
                  </span>
                </h3>
                <span class="text-[11px] text-on-surface-variant font-mono">Consensus Queue</span>
              </div>

              <div v-if="pendingConnections.length === 0" class="py-6 text-center text-xs text-on-surface-variant bg-surface-container-low/40 rounded-2xl border border-dashed border-surface-container">
                No pending inbound barter requests.
              </div>

              <div v-else class="space-y-3.5">
                <div
                  v-for="conn in pendingConnections"
                  :key="conn.id"
                  class="p-3.5 rounded-2xl bg-surface border border-surface-container space-y-2.5"
                >
                  <div class="flex items-center gap-3">
                    <div class="relative shrink-0">
                      <img
                        v-if="conn.profile_picture"
                        :src="conn.profile_picture"
                        :alt="conn.full_name || conn.username"
                        class="w-9 h-9 rounded-xl object-cover ring-1 ring-primary/20"
                        @error="conn.profile_picture = null"
                      />
                      <div
                        v-else
                        class="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary to-secondary text-white font-bold text-xs flex items-center justify-center uppercase"
                      >
                        {{ (conn.full_name || conn.username || '?').charAt(0) }}
                      </div>
                    </div>
                    <div class="min-w-0">
                      <h4 class="font-headline text-xs font-bold text-on-surface truncate">{{ conn.full_name }}</h4>
                      <p class="text-[10px] text-on-surface-variant font-mono truncate">@{{ conn.username }} &bull; {{ conn.department || 'Peer' }}</p>
                    </div>
                  </div>

                  <div class="text-[11px] font-mono bg-surface-container-lowest p-2 rounded-xl border border-surface-container space-y-0.5">
                    <div class="text-emerald-700 truncate">Offers: {{ conn.skill_offered }}</div>
                    <div class="text-primary truncate">Wants: {{ conn.skill_wanted }}</div>
                  </div>

                  <div class="flex items-center gap-2 pt-1">
                    <button
                      type="button"
                      @click="respondConnection(conn.id, 'accepted')"
                      class="flex-1 py-1.5 rounded-lg bg-primary text-on-primary font-headline text-xs font-semibold hover:bg-primary-dim transition-all cursor-pointer"
                    >
                      Accept Loop
                    </button>
                    <button
                      type="button"
                      @click="respondConnection(conn.id, 'rejected')"
                      class="px-3 py-1.5 rounded-lg bg-surface-container text-on-surface-variant hover:text-error font-headline text-xs font-semibold transition-all cursor-pointer"
                    >
                      Decline
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- 2.G: My Learning Partners -->
            <div class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm space-y-3.5">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                  <h3 class="font-headline text-sm font-bold text-on-surface">My Learning Partners</h3>
                </div>
                <span class="text-xs font-mono font-bold text-primary">{{ activeConnections.length }}</span>
              </div>

              <div v-if="activeConnections.length === 0" class="py-6 text-center text-xs text-on-surface-variant bg-surface-container-low/40 rounded-2xl border border-dashed border-surface-container">
                No active learning partners connected yet. Connect with peers from Loop Exchanges above!
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="c in activeConnections.slice(0, 4)"
                  :key="c.id"
                  class="p-3 rounded-2xl bg-surface border border-surface-container flex items-center justify-between gap-3"
                >
                  <div class="flex items-center gap-2.5 min-w-0">
                    <div class="relative shrink-0">
                      <img
                        v-if="c.profile_picture"
                        :src="c.profile_picture"
                        :alt="c.full_name || c.username"
                        class="w-8 h-8 rounded-xl object-cover ring-1 ring-primary/20"
                        @error="c.profile_picture = null"
                      />
                      <div
                        v-else
                        class="w-8 h-8 rounded-xl bg-gradient-to-tr from-primary to-secondary text-white font-bold text-xs flex items-center justify-center uppercase"
                      >
                        {{ (c.full_name || c.username).charAt(0) }}
                      </div>
                      <span class="absolute -bottom-0.5 -right-0.5 w-2 h-2 rounded-full bg-emerald-500 ring-1 ring-white"></span>
                    </div>
                    <div class="min-w-0">
                      <h4 class="font-headline font-bold text-xs text-on-surface truncate">{{ c.full_name }}</h4>
                      <p class="text-[10px] text-on-surface-variant truncate">@{{ c.username }}</p>
                    </div>
                  </div>

                  <div class="flex items-center gap-1.5 shrink-0">
                    <button
                      type="button"
                      @click="openBookModal(c)"
                      class="px-2 py-1 rounded-lg border border-primary/30 text-primary hover:bg-primary/5 text-[11px] font-bold cursor-pointer"
                    >
                      Book
                    </button>
                    <NuxtLink
                      :to="'/chat?id=' + c.user_id"
                      class="px-2.5 py-1 rounded-lg bg-primary text-on-primary text-[11px] font-bold hover:bg-primary-dim"
                    >
                      Chat
                    </NuxtLink>
                  </div>
                </div>
              </div>
            </div>

            <!-- 2.H: Campus Leaderboard & Diagnostic Badges -->
            <div class="bg-surface-container-lowest rounded-3xl border border-surface-container p-5 sm:p-6 shadow-sm space-y-4">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-[11px] font-mono text-on-surface-variant uppercase font-semibold">Peer Standing</span>
                  <h3 class="font-headline text-sm font-bold text-on-surface">Campus Level {{ user.level || 1 }}</h3>
                </div>
                <div class="text-right">
                  <span class="px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container text-xs font-mono font-bold">Top 5% Campus</span>
                  <p class="text-[10px] text-on-surface-variant mt-0.5">+{{ 100 - ((user.xp || 0) % 100) }} XP to Next Tier</p>
                </div>
              </div>

              <!-- Mini Podium -->
              <div class="flex items-end justify-center gap-2 pt-2 pb-1 text-center font-mono">
                <div class="flex-1 bg-surface-container-low rounded-t-lg p-2 h-14 flex flex-col justify-end">
                  <span class="text-[10px] text-on-surface-variant">Tier I</span>
                  <span class="text-xs font-bold text-on-surface">100 XP</span>
                </div>
                <div class="flex-1 bg-primary/15 border-t-2 border-primary rounded-t-lg p-2 h-18 flex flex-col justify-end">
                  <span class="text-[10px] font-bold text-primary">You</span>
                  <span class="text-xs font-bold text-primary">{{ user.xp || 0 }} XP</span>
                </div>
                <div class="flex-1 bg-surface-container-low rounded-t-lg p-2 h-20 flex flex-col justify-end">
                  <span class="text-[10px] text-on-surface-variant">Master</span>
                  <span class="text-xs font-bold text-on-surface">500 XP</span>
                </div>
              </div>

              <!-- Skill Diagnostic Quiz CTA Card -->
              <div class="p-3.5 rounded-2xl bg-gradient-to-br from-surface-container-low to-surface-container border border-secondary-container">
                <div class="flex items-center gap-2 mb-1 text-primary font-headline text-xs font-bold">
                  <span class="material-symbols-outlined text-base">psychology</span>
                  <span>Skill Verification Quiz</span>
                </div>
                <p class="text-xs text-on-surface-variant mb-3">
                  Take the 10-minute diagnostic proctored quiz to claim +25 XP and a Mentor verified badge.
                </p>
                <NuxtLink 
                  to="/quiz"
                  class="w-full py-2 rounded-xl bg-primary text-on-primary hover:bg-primary-dim font-headline text-xs font-semibold transition-all flex items-center justify-center gap-1 shadow-xs"
                >
                  <span>Take Diagnostic Quiz</span>
                </NuxtLink>
              </div>
            </div>

          </aside>
        </div>

        <!-- ── MOBILE BOTTOM APP DOCK (Auto-detected mobile view) ── -->
        <nav class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-surface-container-lowest/95 backdrop-blur-md border-t border-surface-container py-2 px-4 flex justify-around items-center shadow-lg">
          <button @click="scrollToSection('command-center')" class="flex flex-col items-center gap-0.5 text-primary text-[10px] font-bold">
            <span class="material-symbols-outlined text-xl">home</span>
            <span>Home</span>
          </button>
          <button @click="scrollToSection('loops-section')" class="flex flex-col items-center gap-0.5 text-on-surface-variant hover:text-primary text-[10px] font-semibold">
            <span class="material-symbols-outlined text-xl">hub</span>
            <span>Loops</span>
          </button>
          <button @click="scrollToSection('skills-section')" class="flex flex-col items-center gap-0.5 text-on-surface-variant hover:text-primary text-[10px] font-semibold">
            <span class="material-symbols-outlined text-xl">psychology</span>
            <span>Skills</span>
          </button>
          <button @click="scrollToSection('sessions-section')" class="flex flex-col items-center gap-0.5 text-on-surface-variant hover:text-primary text-[10px] font-semibold">
            <span class="material-symbols-outlined text-xl">event_available</span>
            <span>Sessions</span>
          </button>
          <NuxtLink to="/chat" class="flex flex-col items-center gap-0.5 text-on-surface-variant hover:text-primary text-[10px] font-semibold">
            <span class="material-symbols-outlined text-xl">chat</span>
            <span>Chat</span>
          </NuxtLink>
          <button @click="showEditModal = true" class="flex flex-col items-center gap-0.5 text-on-surface-variant hover:text-primary text-[10px] font-semibold">
            <span class="material-symbols-outlined text-xl">account_circle</span>
            <span>Profile</span>
          </button>
        </nav>

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

      <!-- ── LOG A.E.E. SESSION MODAL ─────────────────────────────────── -->
      <div v-if="showAeeModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 shadow-2xl w-full max-w-md border border-surface-container-high space-y-5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-xl">bolt</span>
              </div>
              <div>
                <h2 class="font-display text-lg font-bold text-on-surface">Log A.E.E. Execution</h2>
                <p class="text-[11px] text-on-surface-variant">Proof-of-Work heartbeat renewal</p>
              </div>
            </div>
            <button @click="showAeeModal = false" class="p-1.5 rounded-full hover:bg-surface-container text-on-surface-variant transition-colors">
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Verified Skill Being Taught</label>
              <input :value="aeeForm.skill_name" disabled class="w-full px-4 py-2.5 rounded-xl bg-surface-container-low border border-surface-container-high text-sm font-bold text-primary capitalize cursor-not-allowed"/>
            </div>

            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Learning Partner (Peer)</label>
              <select v-model="aeeForm.learner_id" class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors">
                <option value="" disabled>Select a connected peer...</option>
                <option v-for="c in activeConnections" :key="c.id" :value="c.user_id">
                  {{ c.full_name }} (@{{ c.username }})
                </option>
              </select>
              <p v-if="activeConnections.length === 0" class="text-[11px] text-amber-600 mt-1">
                You need at least one connected learning partner to log an A.E.E. session. Connect with peers from Loop Exchanges or search!
              </p>
            </div>

            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Session Duration</label>
              <div class="grid grid-cols-4 gap-2">
                <button 
                  v-for="d in [15, 30, 45, 60]" 
                  :key="d"
                  type="button"
                  @click="aeeForm.duration_minutes = d"
                  class="py-2 rounded-xl border text-xs font-bold transition-all"
                  :class="aeeForm.duration_minutes === d ? 'border-primary bg-primary text-on-primary' : 'border-surface-container-high bg-surface-bright text-on-surface hover:border-primary/40'"
                >
                  {{ d }}m
                </button>
              </div>
            </div>

            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Execution / Teaching Summary</label>
              <textarea 
                v-model="aeeForm.topic_notes" 
                rows="3" 
                class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors resize-none"
                placeholder="Briefly describe what was taught or executed (e.g. Debugged state issues in React, walked through useEffect and custom hooks)..."
              ></textarea>
            </div>
          </div>

          <div class="p-3.5 rounded-2xl bg-surface-container-low text-[11px] text-on-surface-variant space-y-1">
            <p class="font-bold text-on-surface flex items-center gap-1">
              <span class="material-symbols-outlined text-xs text-primary">info</span>
              <span>Two-Sided Peer Confirmation</span>
            </p>
            <p>Your partner will receive a confirmation prompt on their dashboard. Upon confirmation, your 180-day heartbeat resets and you earn +25 XP.</p>
          </div>

          <div class="flex gap-3 pt-2">
            <button 
              @click="submitAeeLog" 
              :disabled="isSubmittingAee || !aeeForm.learner_id || !aeeForm.topic_notes.trim()"
              class="flex-1 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-semibold text-sm hover:bg-primary-dim active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xs flex items-center justify-center gap-2"
            >
              <span v-if="isSubmittingAee" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
              <span>{{ isSubmittingAee ? 'Sending Request...' : 'Send for Peer Confirmation' }}</span>
            </button>
            <button @click="showAeeModal = false" class="px-5 py-2.5 rounded-xl border border-surface-variant text-on-surface-variant hover:bg-surface-container font-headline font-semibold text-sm transition-all">Cancel</button>
          </div>
        </div>
      </div>

      <!-- ── BOOK SKILL EXCHANGE SESSION MODAL (PILLAR 1 ESCROW) ──── -->
      <div v-if="showBookModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 shadow-2xl w-full max-w-md border border-surface-container-high space-y-5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-xl">event_available</span>
              </div>
              <div>
                <h2 class="font-display text-lg font-bold text-on-surface">Book Skill Exchange</h2>
                <p class="text-[11px] text-on-surface-variant">Time credit escrow &amp; live scheduling</p>
              </div>
            </div>
            <button @click="showBookModal = false" class="p-1.5 rounded-full hover:bg-surface-container text-on-surface-variant transition-colors">
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </div>

          <div class="space-y-4">
            <!-- Learning Partner Selector / Info -->
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Learning Partner (Teacher) *</label>
              <div v-if="activeConnections.length > 0">
                <select
                  v-model="bookForm.teacher_id"
                  @change="onSelectPeerChange"
                  class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-xs sm:text-sm focus:outline-none focus:border-primary transition-colors font-medium text-on-surface"
                >
                  <option :value="''" disabled>Select a learning partner...</option>
                  <option
                    v-for="c in activeConnections"
                    :key="c.id"
                    :value="c.user_id || c.id"
                  >
                    {{ c.full_name || c.username }} (@{{ c.username }}) {{ c.teaches && c.teaches.length ? '— Teaches: ' + (Array.isArray(c.teaches) ? c.teaches.join(', ') : c.teaches) : '' }}
                  </option>
                </select>
              </div>
              <div v-else-if="bookTargetPeer" class="p-3 bg-surface-container-low rounded-2xl flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-primary/20 text-primary font-bold text-sm flex items-center justify-center uppercase">
                  {{ (bookTargetPeer.full_name || bookTargetPeer.name || bookTargetPeer.username || '?').charAt(0) }}
                </div>
                <div>
                  <h4 class="font-headline font-bold text-xs text-on-surface">{{ bookTargetPeer.full_name || bookTargetPeer.name }}</h4>
                  <p class="text-[10px] text-on-surface-variant">Teacher • @{{ bookTargetPeer.username || 'peer' }}</p>
                </div>
              </div>
              <div v-else class="p-3 bg-amber-50 rounded-xl border border-amber-200 text-xs text-amber-800">
                You don't have any active learning partners yet. Connect with a peer first to book an exchange session.
              </div>
            </div>

            <!-- Skill Name -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider">Skill to Learn *</label>
                <span v-if="bookTargetPeerTeaches.length > 0" class="text-[10px] text-primary font-semibold">Click to auto-fill</span>
              </div>
              <input
                v-model="bookForm.skill_name"
                type="text"
                placeholder="e.g. React, Python, Data Structures..."
                class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors font-medium"
              />
              <div v-if="bookTargetPeerTeaches.length > 0" class="flex flex-wrap gap-1.5 mt-2">
                <button
                  v-for="s in bookTargetPeerTeaches"
                  :key="s"
                  type="button"
                  @click="bookForm.skill_name = s"
                  class="px-2.5 py-1 rounded-lg text-xs font-medium transition-all"
                  :class="bookForm.skill_name.toLowerCase() === s.toLowerCase() ? 'bg-primary text-on-primary shadow-xs' : 'bg-primary/10 text-primary hover:bg-primary/20'"
                >
                  {{ s }}
                </button>
              </div>
            </div>

            <!-- Duration Selector -->
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Session Duration &amp; Cost</label>
              <div class="grid grid-cols-2 gap-2.5">
                <button
                  type="button"
                  @click="bookForm.duration_minutes = 30"
                  class="p-3 rounded-2xl border text-left transition-all"
                  :class="bookForm.duration_minutes === 30 ? 'border-primary bg-primary/10 text-primary shadow-xs' : 'border-surface-container bg-surface-bright text-on-surface hover:border-primary/40'"
                >
                  <span class="font-headline font-bold text-sm block">30 Minutes</span>
                  <span class="text-[11px] font-mono text-on-surface-variant">0.5 Time Credit</span>
                </button>
                <button
                  type="button"
                  @click="bookForm.duration_minutes = 60"
                  class="p-3 rounded-2xl border text-left transition-all"
                  :class="bookForm.duration_minutes === 60 ? 'border-primary bg-primary/10 text-primary shadow-xs' : 'border-surface-container bg-surface-bright text-on-surface hover:border-primary/40'"
                >
                  <span class="font-headline font-bold text-sm block">60 Minutes</span>
                  <span class="text-[11px] font-mono text-on-surface-variant">1.0 Time Credit</span>
                </button>
              </div>
            </div>

            <!-- Date & Time (Optional for immediate vs scheduled) -->
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Scheduled Date &amp; Time (Optional)</label>
              <input
                v-model="bookForm.scheduled_at"
                type="datetime-local"
                class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-xs sm:text-sm focus:outline-none focus:border-primary transition-colors text-on-surface"
              />
              <p class="text-[10px] text-on-surface-variant mt-1">Leave empty to conduct the session right now via Chat.</p>
            </div>

            <!-- Topic Notes -->
            <div>
              <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Session Goals / Questions</label>
              <textarea
                v-model="bookForm.topic_notes"
                rows="2"
                placeholder="What specific problems or topics do you want to cover?"
                class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors resize-none"
              ></textarea>
            </div>
          </div>

          <!-- Escrow Trust Notice -->
          <div class="p-3 rounded-2xl bg-primary/5 border border-primary/20 text-[11px] text-on-surface-variant flex items-start gap-2">
            <span class="material-symbols-outlined text-base text-primary shrink-0">lock</span>
            <div>
              <p class="font-bold text-on-surface">Escrow Guarantee</p>
              <p>{{ bookForm.duration_minutes <= 30 ? '0.5' : '1.0' }} Time Credit will be held in escrow. It is only released to the teacher when the session is completed. If cancelled, it is immediately refunded.</p>
            </div>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              @click="submitBookSession"
              :disabled="isBooking || !bookForm.skill_name.trim()"
              class="flex-1 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-semibold text-sm hover:bg-primary-dim active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xs flex items-center justify-center gap-2"
            >
              <span v-if="isBooking" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
              <span>{{ isBooking ? 'Booking...' : 'Book & Hold Escrow' }}</span>
            </button>
            <button @click="showBookModal = false" class="px-5 py-2.5 rounded-xl border border-surface-variant text-on-surface-variant hover:bg-surface-container font-headline font-semibold text-sm transition-all">Cancel</button>
          </div>
        </div>
      </div>

      <!-- ── POST-SESSION RATING & REVIEW MODAL ───────────────────────── -->
      <div v-if="showReviewModal && reviewingSession" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 shadow-2xl w-full max-w-md border border-surface-container-high space-y-5">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2.5">
              <div class="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
                <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">star</span>
              </div>
              <div>
                <h2 class="font-display text-lg font-bold text-on-surface">Rate Your Exchange</h2>
                <p class="text-[11px] text-on-surface-variant">Build campus trust &amp; verified peer reputation</p>
              </div>
            </div>
            <button @click="showReviewModal = false" class="p-1.5 rounded-full hover:bg-surface-container text-on-surface-variant transition-colors">
              <span class="material-symbols-outlined text-base">close</span>
            </button>
          </div>

          <!-- Peer info -->
          <div class="p-3 bg-surface-container-low rounded-2xl flex items-center gap-3">
            <div
              class="w-10 h-10 rounded-xl text-white font-bold text-sm flex items-center justify-center uppercase shadow-xs"
              :style="{ background: reviewingSession.peer_avatar || '#543ce0' }"
            >
              {{ (reviewingSession.peer_name || reviewingSession.peer_username || '?').charAt(0) }}
            </div>
            <div>
              <h4 class="font-headline font-bold text-sm text-on-surface">{{ reviewingSession.peer_name }}</h4>
              <p class="text-xs text-on-surface-variant">Session: {{ reviewingSession.skill_name }} ({{ reviewingSession.duration_minutes }}m)</p>
            </div>
          </div>

          <!-- Star Selector -->
          <div class="text-center space-y-2 py-2">
            <div class="flex items-center justify-center gap-2">
              <button
                v-for="star in 5"
                :key="'star_' + star"
                type="button"
                @click="reviewForm.rating = star"
                class="transition-transform active:scale-125 focus:outline-none"
              >
                <span
                  class="material-symbols-outlined text-3xl"
                  :class="star <= reviewForm.rating ? 'text-amber-500' : 'text-surface-container-highest'"
                  :style="star <= reviewForm.rating ? `font-variation-settings: 'FILL' 1;` : ''"
                >
                  star
                </span>
              </button>
            </div>
            <p class="text-xs font-bold font-headline text-on-surface">
              {{ reviewForm.rating === 5 ? 'Exceptional Mentor! ⭐⭐⭐⭐⭐' : (reviewForm.rating === 4 ? 'Very Helpful & Clear ⭐⭐⭐⭐' : (reviewForm.rating === 3 ? 'Good Session ⭐⭐⭐' : 'Needs Improvement')) }}
            </p>
          </div>

          <!-- Tag Badges -->
          <div>
            <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1.5 block">Endorse Strengths (Optional)</label>
            <div class="flex flex-wrap gap-1.5">
              <button
                v-for="tag in ['Clear Explanations', 'Hands-on Code', 'Patient', 'Great Mentor', 'Punctual', 'Debugging Pro']"
                :key="tag"
                type="button"
                @click="toggleReviewTag(tag)"
                class="px-2.5 py-1 rounded-xl text-xs font-bold transition-all"
                :class="reviewForm.tags.includes(tag) ? 'bg-primary text-on-primary shadow-xs' : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-container'"
              >
                {{ tag }}
              </button>
            </div>
          </div>

          <!-- Comment -->
          <div>
            <label class="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1 block">Feedback / Testimonial</label>
            <textarea
              v-model="reviewForm.comment"
              rows="2"
              placeholder="What made this session great?"
              class="w-full px-4 py-2.5 rounded-xl bg-surface-bright border border-surface-container-high text-sm focus:outline-none focus:border-primary transition-colors resize-none"
            ></textarea>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              @click="submitReview"
              :disabled="isSubmittingReview"
              class="flex-1 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-semibold text-sm hover:bg-primary-dim active:scale-95 transition-all shadow-xs flex items-center justify-center gap-2"
            >
              <span v-if="isSubmittingReview" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
              <span>{{ isSubmittingReview ? 'Submitting...' : 'Submit Review' }}</span>
            </button>
            <button @click="showReviewModal = false" class="px-5 py-2.5 rounded-xl border border-surface-variant text-on-surface-variant hover:bg-surface-container font-headline font-semibold text-sm transition-all">Skip</button>
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
import { onMounted, onUnmounted, ref, computed, reactive } from 'vue'
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
const skillInventoryTab = ref('teaching') // 'teaching' or 'learning'
const scrollToSection = (id) => {
  if (typeof document !== 'undefined') {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }
}

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

// ─── Exchange Sessions & Escrow (Pillar 1) ──────────────────────────────────
const exchangeSessions = ref([])
const loadingSessions = ref(true)
const sessionTab = ref('active') // 'active' or 'history'

const activeSessionsList = computed(() => {
  return exchangeSessions.value.filter(s => s.status === 'pending' || s.status === 'accepted' || (s.status === 'completed' && !s.my_review))
})

const historySessionsList = computed(() => {
  return exchangeSessions.value.filter(s => (s.status === 'completed' && s.my_review) || s.status === 'rejected' || s.status === 'cancelled')
})

const showBookModal = ref(false)
const isBooking = ref(false)
const bookTargetPeer = ref(null)
const bookForm = reactive({
  teacher_id: '',
  skill_name: '',
  duration_minutes: 30,
  scheduled_at: '',
  topic_notes: ''
})

const bookTargetPeerTeaches = computed(() => {
  if (!bookTargetPeer.value) return []
  const t = bookTargetPeer.value.teaches || bookTargetPeer.value.teach_skills || bookTargetPeer.value.skills_offered
  if (Array.isArray(t)) return t
  if (typeof t === 'string' && t.trim()) return t.split(',').map(s => s.trim()).filter(Boolean)
  return []
})

const formatSessionTime = (isoStr) => {
  if (!isoStr) return 'Flexible / Instant'
  try {
    const d = new Date(isoStr)
    if (isNaN(d.getTime())) return 'Flexible time'
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) + ' at ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  } catch {
    return 'Flexible time'
  }
}

const showReviewModal = ref(false)
const reviewingSession = ref(null)
const isSubmittingReview = ref(false)
const reviewForm = reactive({
  rating: 5,
  tags: [],
  comment: ''
})

// ─── Proof-of-Work Half-Life & A.E.E. State ─────────────────────────────────
const incomingAee = ref([])
const outboundAee = ref([])
const showAeeModal = ref(false)
const isSubmittingAee = ref(false)
const aeeForm = reactive({
  learner_id: '',
  skill_name: '',
  duration_minutes: 30,
  topic_notes: ''
})

const getSkillVerification = (name) => {
  if (!name || !verifiedSkills.value) return null
  return verifiedSkills.value.find(v => v.skill_name?.toLowerCase() === name.toLowerCase())
}

const openAeeModal = (skillName) => {
  aeeForm.skill_name = skillName
  aeeForm.learner_id = activeConnections.value.length > 0 ? activeConnections.value[0].user_id : ''
  aeeForm.duration_minutes = 30
  aeeForm.topic_notes = ''
  showAeeModal.value = true
}

const fetchAeePending = async () => {
  try {
    const res = await fetch('/api/aee/pending', { credentials: 'include' })
    if (res.ok) {
      const d = await res.json()
      incomingAee.value = d.incoming || []
      outboundAee.value = d.outbound || []
    }
  } catch (e) {
    console.error('Error loading AEE pending:', e)
  }
}

const submitAeeLog = async () => {
  if (!aeeForm.learner_id || !aeeForm.topic_notes.trim()) {
    alert("Please select a learning partner and enter what was taught.")
    return
  }
  isSubmittingAee.value = true
  try {
    const res = await fetch('/api/aee/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(aeeForm)
    })
    const d = await res.json()
    if (res.ok) {
      showAeeModal.value = false
      alert(d.message || "A.E.E. session logged! Sent confirmation request to your learning partner.")
      await fetchAeePending()
    } else {
      alert(d.error || "Failed to log A.E.E. session.")
    }
  } catch (e) {
    console.error(e)
    alert("Network error while logging A.E.E. session.")
  } finally {
    isSubmittingAee.value = false
  }
}

const respondAee = async (sessionId, action) => {
  try {
    const res = await fetch('/api/aee/respond', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ session_id: sessionId, action })
    })
    const d = await res.json()
    if (res.ok) {
      alert(d.message || "Action completed!")
      await Promise.all([fetchVerifications(), fetchAeePending()])
      const uRes = await fetch('/api/user/me', { credentials: 'include' })
      if (uRes.ok) {
        const uData = await uRes.json()
        user.value = uData.user
      }
    } else {
      alert(d.error || "Failed to respond.")
    }
  } catch (e) {
    console.error(e)
  }
}

// Real-time notification state
const liveRequest = ref(null)         // incoming connection request popup
const acceptedToast = ref(null)       // "someone accepted your request" toast
const liveNotifCount = ref(0)         // extra badge count beyond pendingConnections
const showNotificationsPanel = ref(false)
const notificationsList = ref([])
const unreadNotifsCount = ref(0)
const isLoadingNotifs = ref(false)

const totalBadgeCount = computed(() => {
  return (pendingConnections.value?.length || 0) + (unreadNotifsCount.value || 0)
})

const formatNotifTime = (dateStr) => {
  if (!dateStr) return 'Just now'
  try {
    const d = new Date(dateStr)
    if (isNaN(d.getTime())) return 'Recently'
    const diffSec = Math.floor((Date.now() - d.getTime()) / 1000)
    if (diffSec < 60) return 'Just now'
    if (diffSec < 3600) return `${Math.floor(diffSec / 60)}m ago`
    if (diffSec < 86400) return `${Math.floor(diffSec / 3600)}h ago`
    if (diffSec < 604800) return `${Math.floor(diffSec / 86400)}d ago`
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  } catch {
    return 'Recently'
  }
}

const getNotifIcon = (type) => {
  switch (type) {
    case 'connection_request': return 'person_add'
    case 'connection_accepted': return 'how_to_reg'
    case 'session_requested': return 'event'
    case 'session_accepted': return 'event_available'
    case 'teaching_time': return 'school'
    case 'learning_time': return 'menu_book'
    case 'aee_request':
    case 'aee_confirmed': return 'verified'
    default: return 'notifications'
  }
}

const getNotifColorClass = (type) => {
  switch (type) {
    case 'connection_request': return 'bg-purple-500/10 text-purple-600'
    case 'connection_accepted': return 'bg-emerald-500/10 text-emerald-600'
    case 'session_requested': return 'bg-amber-500/10 text-amber-600'
    case 'session_accepted': return 'bg-teal-500/10 text-teal-600'
    case 'teaching_time': return 'bg-primary/10 text-primary'
    case 'learning_time': return 'bg-cyan-500/10 text-cyan-600'
    case 'aee_request':
    case 'aee_confirmed': return 'bg-indigo-500/10 text-indigo-600'
    default: return 'bg-surface-container text-on-surface-variant'
  }
}

const fetchNotifications = async () => {
  isLoadingNotifs.value = true
  try {
    const res = await fetch('/api/notifications', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      notificationsList.value = data.notifications || []
      unreadNotifsCount.value = data.unread_count || 0
    }
  } catch (e) {
    console.error('Failed to fetch notifications:', e)
  } finally {
    isLoadingNotifs.value = false
  }
}

const markAllNotificationsRead = async () => {
  try {
    const res = await fetch('/api/notifications/mark-read', {
      method: 'POST',
      credentials: 'include'
    })
    if (res.ok) {
      notificationsList.value.forEach(n => { n.is_read = true })
      unreadNotifsCount.value = 0
    }
  } catch (e) {
    console.error('Failed to mark notifications read:', e)
  }
}

const markSingleNotificationRead = async (notifId) => {
  if (typeof notifId === 'string' && notifId.startsWith('conn_')) return
  try {
    const res = await fetch('/api/notifications/mark-read', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ notification_id: notifId })
    })
    if (res.ok) {
      const target = notificationsList.value.find(n => n.id === notifId)
      if (target && !target.is_read) {
        target.is_read = true
        unreadNotifsCount.value = Math.max(0, unreadNotifsCount.value - 1)
      }
    }
  } catch (e) {
    console.error('Failed to mark notification read:', e)
  }
}

const deleteNotificationItem = async (notifId) => {
  try {
    if (typeof notifId === 'number') {
      await fetch(`/api/notifications/${notifId}`, {
        method: 'DELETE',
        credentials: 'include'
      })
    }
    const idx = notificationsList.value.findIndex(n => n.id === notifId)
    if (idx !== -1) {
      if (!notificationsList.value[idx].is_read) {
        unreadNotifsCount.value = Math.max(0, unreadNotifsCount.value - 1)
      }
      notificationsList.value.splice(idx, 1)
    }
  } catch (e) {
    console.error('Failed to delete notification:', e)
  }
}

const clearAllNotifications = async () => {
  try {
    await fetch('/api/notifications/clear-all', {
      method: 'DELETE',
      credentials: 'include'
    })
    notificationsList.value = []
    unreadNotifsCount.value = 0
  } catch (e) {
    console.error('Failed to clear notifications:', e)
  }
}

const handleNotificationClick = async (item) => {
  if (!item.is_read) {
    await markSingleNotificationRead(item.id)
  }
  if (item.link) {
    showNotificationsPanel.value = false
    navigateTo(item.link)
  }
}

let dashSocket = null

const setupDashSocket = () => {
  const config = useRuntimeConfig()
  const backendUrl = config.public?.apiBase || (typeof window !== 'undefined'
    ? ((window.location.protocol === 'https:' || !window.location.port)
        ? window.location.origin
        : `${window.location.protocol}//${window.location.hostname}:5000`)
    : 'http://localhost:5000')
  dashSocket = io(backendUrl, { withCredentials: true, transports: ['polling', 'websocket'] })

  dashSocket.on('connect', () => {
    if (user.value?.id) {
      dashSocket.emit('authenticate', { user_id: user.value.id })
    }
  })

  dashSocket.on('new_notification', (data) => {
    if (data) {
      notificationsList.value.unshift(data)
      unreadNotifsCount.value++
    }
  })

  dashSocket.on('connection_request', (data) => {
    liveRequest.value = data
    liveNotifCount.value++
    fetchNotifications()
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
    fetchNotifications()
  })

  // ─── Real-time A.E.E. Session Handshake Listeners ───
  dashSocket.on('aee_request_received', (data) => {
    fetchAeePending()
    fetchNotifications()
    liveNotifCount.value++
  })

  dashSocket.on('aee_request_confirmed', (data) => {
    fetchVerifications()
    fetchAeePending()
    fetchNotifications()
    alert(`🎉 Peer Confirmed! Your "${data.skill_name}" verification heartbeat has been renewed for 180 days!`)
  })

  dashSocket.on('aee_request_declined', (data) => {
    fetchAeePending()
    fetchNotifications()
  })

  // ─── Real-time Exchange Session Listeners (Pillar 1) ───
  dashSocket.on('session_requested', (data) => {
    fetchSessions()
    fetchNotifications()
    liveNotifCount.value++
  })

  dashSocket.on('session_accepted', (data) => {
    fetchSessions()
    fetchNotifications()
    alert(`🎉 Session Accepted! ${data.teacher_name || 'Your mentor'} accepted your exchange for ${data.skill_name}.`)
  })

  dashSocket.on('session_rejected', (data) => {
    fetchSessions()
    fetchUserData()
    fetchNotifications()
    alert(`ℹ️ Session for ${data.skill_name} was declined. Your escrow credits have been refunded.`)
  })

  dashSocket.on('session_cancelled', (data) => {
    fetchSessions()
    fetchUserData()
    fetchNotifications()
  })

  dashSocket.on('session_completed', (data) => {
    fetchSessions()
    fetchUserData()
    fetchVerifications()
    fetchNotifications()
  })

  dashSocket.on('teaching_time_recorded', (data) => {
    if (data.teacher_id === user.value?.id) {
      user.value.total_teaching_seconds = data.total_teaching_seconds
    }
    fetchUserData()
    fetchVerifications()
    fetchNotifications()
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
    await Promise.all([fetchConnections(), fetchCycles(), fetchNotifications()])
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
      await Promise.all([fetchConnections(), fetchCycles(), fetchNotifications()])
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
      await Promise.all([fetchSkills(), fetchCycles(), fetchConnections(), fetchVerifications(), fetchAeePending(), fetchSessions(), fetchNotifications()])
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

const formatTeachingDuration = (sec) => {
  if (!sec || sec <= 0) return '0m'
  const h = Math.floor(sec / 3600)
  const m = Math.floor((sec % 3600) / 60)
  if (h > 0) return `${h}h ${m}m`
  return `${m}m`
}

const fetchUserData = async () => {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      user.value = data.user
    }
  } catch (e) {
    console.error('Error fetching user:', e)
  }
}

const fetchSessions = async () => {
  loadingSessions.value = true
  try {
    const res = await fetch('/api/sessions', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      exchangeSessions.value = data.sessions || []
    }
  } catch (e) {
    console.error('Error fetching exchange sessions:', e)
  } finally {
    loadingSessions.value = false
  }
}

const openBookModal = (peer = null, defaultSkill = '') => {
  if (peer) {
    bookTargetPeer.value = {
      ...peer,
      full_name: peer.full_name || peer.name || peer.username,
      username: peer.username || peer.name,
      user_id: peer.user_id || peer.id
    }
    bookForm.teacher_id = peer.user_id || peer.id
  } else {
    if (activeConnections.value.length > 0) {
      const firstConn = activeConnections.value[0]
      bookTargetPeer.value = firstConn
      bookForm.teacher_id = firstConn.user_id || firstConn.id
    } else {
      bookTargetPeer.value = null
      bookForm.teacher_id = ''
    }
  }

  const teaches = bookTargetPeer.value?.teaches
  const skillList = Array.isArray(teaches) ? teaches : (typeof teaches === 'string' ? teaches.split(',').map(s => s.trim()) : [])
  bookForm.skill_name = defaultSkill || (skillList.length > 0 ? skillList[0] : '')
  bookForm.duration_minutes = 30
  bookForm.scheduled_at = ''
  bookForm.topic_notes = ''
  showBookModal.value = true
}

const onSelectPeerChange = () => {
  const found = activeConnections.value.find(c => (c.user_id || c.id) == bookForm.teacher_id)
  bookTargetPeer.value = found || null
  if (found?.teaches) {
    const list = Array.isArray(found.teaches) ? found.teaches : found.teaches.split(',').map(s => s.trim())
    if (list.length > 0 && !bookForm.skill_name) {
      bookForm.skill_name = list[0]
    }
  }
}

const submitBookSession = async () => {
  if (!bookForm.teacher_id) {
    alert('Please select a learning partner.')
    return
  }
  if (!bookForm.skill_name.trim()) {
    alert('Please enter a skill to learn.')
    return
  }
  const cost = bookForm.duration_minutes <= 30 ? 0.5 : 1.0
  if ((user.value?.time_credits || 0) < cost) {
    alert(`Insufficient Time Credits! You have ${user.value?.time_credits || 0} credits, but this session requires ${cost} credits. Earn credits by teaching skills to peers!`)
    return
  }
  isBooking.value = true
  try {
    const res = await fetch('/api/sessions/book', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(bookForm)
    })
    const data = await res.json()
    if (res.ok) {
      showBookModal.value = false
      alert(data.message || 'Session booked! Escrow credits locked until completion.')
      await Promise.all([fetchSessions(), fetchUserData()])
    } else {
      alert(data.error || 'Failed to book session.')
    }
  } catch (e) {
    console.error('Error booking session:', e)
    alert('Network error while booking session.')
  } finally {
    isBooking.value = false
  }
}

const respondSession = async (sessionId, action) => {
  try {
    const res = await fetch(`/api/sessions/${sessionId}/respond`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ action })
    })
    const data = await res.json()
    if (res.ok) {
      alert(data.message || `Session ${action}ed!`)
      await Promise.all([fetchSessions(), fetchUserData()])
    } else {
      alert(data.error || 'Failed to update session.')
    }
  } catch (e) {
    console.error('Error responding to session:', e)
  }
}

const cancelSession = async (sessionId) => {
  if (!confirm('Are you sure you want to cancel this session? Your locked escrow credits will be refunded.')) return
  try {
    const res = await fetch(`/api/sessions/${sessionId}/cancel`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (res.ok) {
      alert(data.message || 'Session cancelled and escrow refunded.')
      await Promise.all([fetchSessions(), fetchUserData()])
    } else {
      alert(data.error || 'Failed to cancel session.')
    }
  } catch (e) {
    console.error('Error cancelling session:', e)
  }
}

const completeSessionAction = async (session) => {
  if (!confirm(`Mark session for "${session.skill_name}" as complete?\n\nThis will release ${session.credit_cost} Time Credit from escrow to the teacher and award XP!`)) return
  try {
    const res = await fetch(`/api/sessions/${session.id}/complete`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await res.json()
    if (res.ok) {
      alert(`🎉 Session completed! ${data.escrow_released} Time Credit transferred and +${data.xp_awarded} XP earned!`)
      await Promise.all([fetchSessions(), fetchUserData(), fetchVerifications()])
      openReviewModal(session)
    } else {
      alert(data.error || 'Failed to complete session.')
    }
  } catch (e) {
    console.error('Error completing session:', e)
  }
}

const openReviewModal = (session) => {
  reviewingSession.value = session
  reviewForm.rating = 5
  reviewForm.tags = []
  reviewForm.comment = ''
  showReviewModal.value = true
}

const toggleReviewTag = (tag) => {
  const idx = reviewForm.tags.indexOf(tag)
  if (idx > -1) {
    reviewForm.tags.splice(idx, 1)
  } else {
    reviewForm.tags.push(tag)
  }
}

const submitReview = async () => {
  if (!reviewingSession.value) return
  isSubmittingReview.value = true
  try {
    const res = await fetch(`/api/sessions/${reviewingSession.value.id}/review`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(reviewForm)
    })
    const data = await res.json()
    if (res.ok) {
      showReviewModal.value = false
      alert(data.message || 'Thank you for rating your peer!')
      await fetchSessions()
    } else {
      alert(data.error || 'Failed to submit review.')
    }
  } catch (e) {
    console.error('Error submitting review:', e)
  } finally {
    isSubmittingReview.value = false
  }
}

const logout = async () => {
  try {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' })
  } catch(e) {}
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('skillloop_auth_active')
  }
  window.location.href = '/login'
}
</script>

<style scoped>
.slide-in-enter-active, .slide-in-leave-active { transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-in-enter-from, .slide-in-leave-to { transform: translateY(20px); opacity: 0; }
</style>



