<template>
  <div class="bg-[#fbf4ff] text-[#1e1a2b] font-body h-screen flex flex-col antialiased overflow-hidden selection:bg-[#543ce0]/20 selection:text-[#543ce0]">
    <!-- TOP NAVIGATION BAR -->
    <header class="bg-surface-container-low shadow-sm sticky top-0 z-40 flex-shrink-0">
      <div class="flex justify-between items-center w-full px-4 sm:px-6 py-3 max-w-7xl mx-auto">
        <div class="flex items-center gap-8">
          <NuxtLink to="/" class="font-display text-xl font-bold text-primary tracking-tight flex items-center gap-2 shrink-0">
            <div class="w-9 h-9 rounded-xl bg-primary text-on-primary flex items-center justify-center shadow-sm">
              <span class="material-symbols-outlined text-2xl leading-none">all_inclusive</span>
            </div>
            <span>SkillLoop</span>
          </NuxtLink>
          <nav class="hidden md:flex items-center space-x-6 font-headline text-sm font-semibold tracking-tight">
            <NuxtLink to="/dashboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">
              <span class="material-symbols-outlined text-lg">space_dashboard</span>
              Dashboard
            </NuxtLink>
            <span class="text-primary font-bold border-b-2 border-primary pb-1 flex items-center gap-1.5 whitespace-nowrap">
              <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">chat</span>
              Chat &amp; Video
            </span>
            <NuxtLink to="/quiz" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1 whitespace-nowrap">
              Quiz
            </NuxtLink>
            <NuxtLink to="/leaderboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1 whitespace-nowrap">
              Leaderboard
            </NuxtLink>
            <NuxtLink to="/resume" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1 whitespace-nowrap">
              Resume
            </NuxtLink>
          </nav>
        </div>

        <div class="flex items-center gap-3 shrink-0">
          <div class="hidden lg:flex items-center gap-2 px-3 py-1 bg-emerald-50 border border-emerald-200/80 rounded-full text-xs font-semibold text-emerald-700 whitespace-nowrap">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>Realtime Network Active</span>
          </div>

          <div v-if="currentUser" class="flex items-center gap-1.5 bg-surface-container-lowest px-3 py-1.5 rounded-full border border-secondary-fixed shadow-sm text-sm font-label font-bold text-on-surface whitespace-nowrap shrink-0">
            <span class="material-symbols-outlined text-primary text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
            <span>{{ currentUser.time_credits || 0 }} Credits</span>
          </div>

          <NuxtLink
            to="/dashboard"
            class="relative w-9 h-9 rounded-full bg-surface-container-low border border-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors shrink-0"
            title="Dashboard"
          >
            <span class="material-symbols-outlined text-xl">space_dashboard</span>
          </NuxtLink>

          <div v-if="currentUser" class="relative w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-sm uppercase shadow-sm shrink-0">
            {{ (currentUser.full_name || currentUser.username || 'U').charAt(0) }}
          </div>

          <button @click="logout" class="text-xs text-on-surface-variant hover:text-error transition-colors font-semibold whitespace-nowrap">
            Logout
          </button>
        </div>
      </div>
    </header>

    <!-- MAIN TWO-COLUMN WORKSPACE -->
    <main class="flex-1 max-w-[1720px] w-full mx-auto p-3 sm:p-5 flex gap-4 min-h-0 overflow-hidden">
      <!-- LEFT SIDEBAR: PEER CONVERSATIONS -->
      <aside class="w-full md:w-[360px] lg:w-[380px] bg-white rounded-2xl border border-[#eaddff] flex flex-col h-full overflow-hidden shadow-sm flex-shrink-0">
        <!-- Header & Tabs -->
        <div class="p-3.5 border-b border-[#eaddff]/70 space-y-2.5 bg-gradient-to-b from-[#fdfaff] to-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="font-headline font-bold text-base text-[#1e1a2b]">Conversations</h2>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#543ce0]/10 text-[#543ce0]">
                {{ sidebarTab === 'peers' ? `${peers.length} Peers` : `${groups.length} Groups` }}
              </span>
            </div>
            <button
              v-if="sidebarTab === 'groups'"
              @click="openCreateGroupModal"
              class="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-[#543ce0] text-white text-[11px] font-bold hover:bg-[#432ec4] active:scale-95 transition-all shadow-sm"
              title="Create new group"
            >
              <span class="material-symbols-outlined text-sm">add</span>
              <span>New</span>
            </button>
          </div>

          <!-- Tabs: Partners / Groups -->
          <div class="flex items-center p-1 bg-[#f6effe] rounded-xl border border-[#eaddff]/80">
            <button
              @click="sidebarTab = 'peers'"
              class="flex-1 py-1.5 px-2 rounded-lg text-xs font-bold font-headline transition-all flex items-center justify-center gap-1.5"
              :class="sidebarTab === 'peers' ? 'bg-white text-[#543ce0] shadow-xs' : 'text-[#6b6680] hover:text-[#1e1a2b]'"
            >
              <span class="material-symbols-outlined text-sm">chat_bubble</span>
              <span>Partners ({{ peers.length }})</span>
            </button>
            <button
              @click="sidebarTab = 'groups'"
              class="flex-1 py-1.5 px-2 rounded-lg text-xs font-bold font-headline transition-all flex items-center justify-center gap-1.5"
              :class="sidebarTab === 'groups' ? 'bg-white text-[#543ce0] shadow-xs' : 'text-[#6b6680] hover:text-[#1e1a2b]'"
            >
              <span class="material-symbols-outlined text-sm">groups</span>
              <span>Groups ({{ groups.length }})</span>
            </button>
          </div>

          <!-- Search input -->
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-2 text-[#6b6680] text-base">search</span>
            <input
              v-model="searchQuery"
              class="w-full pl-8 pr-4 py-1.5 bg-[#f6effe]/60 border border-[#eaddff] rounded-xl text-xs font-medium placeholder-[#6b6680]/70 focus:outline-none focus:ring-2 focus:ring-[#543ce0]/20 focus:border-[#543ce0] transition-all"
              :placeholder="sidebarTab === 'peers' ? 'Search connected partners...' : 'Search groups...'"
              type="text"
            />
          </div>
        </div>

        <!-- Scrollable Conversations List (Peers or Groups) -->
        <div class="flex-1 overflow-y-auto divide-y divide-[#eaddff]/40 p-2 space-y-1 flex flex-col">
          <!-- 1. LOOP PARTNERS TAB -->
          <template v-if="sidebarTab === 'peers'">
            <div v-if="isLoadingPeers" class="p-6 text-center text-xs text-[#6b6680] flex items-center justify-center gap-2 m-auto">
              <span class="w-4 h-4 rounded-full border-2 border-[#543ce0] border-t-transparent animate-spin"></span>
              <span>Loading loop partners...</span>
            </div>

            <div v-else-if="peers.length === 0" class="p-6 text-center space-y-3 m-auto">
              <div class="w-12 h-12 rounded-2xl bg-[#543ce0]/10 text-[#543ce0] flex items-center justify-center mx-auto">
                <span class="material-symbols-outlined text-2xl">sync_alt</span>
              </div>
              <div class="space-y-1">
                <h3 class="font-headline font-bold text-sm text-[#1e1a2b]">No Connected Peers Yet</h3>
                <p class="text-xs text-[#6b6680] leading-relaxed">
                  Connect with peers through Loop Exchanges on your Dashboard to chat and video call here.
                </p>
              </div>
              <NuxtLink to="/dashboard" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#543ce0] text-white text-xs font-bold font-headline shadow-sm hover:bg-[#432ec4] active:scale-95 transition-all">
                <span>View Loop Exchanges</span>
                <span class="material-symbols-outlined text-sm">arrow_forward</span>
              </NuxtLink>
            </div>

            <div v-else-if="filteredPeers.length === 0" class="p-6 text-center text-xs text-[#6b6680]">
              No connected peers match "{{ searchQuery }}".
            </div>

            <div
              v-for="peer in filteredPeers"
              :key="peer.id"
              @click="selectPeer(peer)"
              class="group p-3 rounded-xl transition-all cursor-pointer relative"
              :class="activePeer?.id === peer.id && !activeGroup ? 'bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#543ce0]/30 shadow-sm' : 'hover:bg-[#f6effe]/60 border border-transparent'"
            >
              <div class="flex items-start gap-3">
                <div class="relative flex-shrink-0">
                  <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-[#543ce0]/20 to-[#99366c]/20 text-[#543ce0] flex items-center justify-center font-bold font-headline text-base shadow-xs">
                    {{ (peer.full_name || peer.username).charAt(0).toUpperCase() }}
                  </div>
                  <span class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-500 border-2 border-white rounded-full"></span>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-0.5">
                    <h3 class="font-headline font-bold text-sm text-[#1e1a2b] truncate">{{ peer.full_name }}</h3>
                    <span class="text-[10px] font-medium text-[#6b6680]">@{{ peer.username }}</span>
                  </div>
                  <div class="flex items-center gap-1.5 mb-1">
                    <span v-if="peer.connection_status === 'connected'" class="px-1.5 py-0.5 bg-emerald-100 text-emerald-800 text-[9px] font-bold rounded">
                      Connected
                    </span>
                    <span class="px-1.5 py-0.5 bg-[#f6effe] border border-[#eaddff] text-[10px] font-semibold text-[#543ce0] rounded">
                      {{ peer.department || 'Campus Peer' }}
                    </span>
                    <span v-if="peer.teaches && peer.teaches.length" class="px-1.5 py-0.5 bg-[#99366c]/10 text-[10px] font-bold text-[#99366c] rounded truncate">
                      {{ peer.teaches[0] }}
                    </span>
                  </div>
                  <div class="flex items-center justify-between">
                    <p class="text-xs text-[#6b6680] truncate">{{ peer.last_message }}</p>
                    <span v-if="peer.unread_count > 0" class="w-4 h-4 rounded-full bg-[#543ce0] text-white text-[10px] font-bold flex items-center justify-center ml-1 flex-shrink-0">
                      {{ peer.unread_count }}
                    </span>
                  </div>
                </div>
              </div>
              <!-- Selection bar -->
              <div v-if="activePeer?.id === peer.id && !activeGroup" class="absolute left-0 top-3 bottom-3 w-1 bg-[#543ce0] rounded-r-full"></div>
            </div>
          </template>

          <!-- 2. GROUPS TAB -->
          <template v-else-if="sidebarTab === 'groups'">
            <div v-if="isLoadingGroups" class="p-6 text-center text-xs text-[#6b6680] flex items-center justify-center gap-2 m-auto">
              <span class="w-4 h-4 rounded-full border-2 border-[#543ce0] border-t-transparent animate-spin"></span>
              <span>Loading groups...</span>
            </div>

            <div v-else-if="groups.length === 0" class="p-6 text-center space-y-3 m-auto">
              <div class="w-12 h-12 rounded-2xl bg-[#543ce0]/10 text-[#543ce0] flex items-center justify-center mx-auto">
                <span class="material-symbols-outlined text-2xl">groups</span>
              </div>
              <div class="space-y-1">
                <h3 class="font-headline font-bold text-sm text-[#1e1a2b]">No Groups Yet</h3>
                <p class="text-xs text-[#6b6680] leading-relaxed">
                  Create a study squad, project team, or skill cohort to chat together in real-time.
                </p>
              </div>
              <button
                @click="openCreateGroupModal"
                class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#543ce0] text-white text-xs font-bold font-headline shadow-sm hover:bg-[#432ec4] active:scale-95 transition-all"
              >
                <span class="material-symbols-outlined text-sm">add</span>
                <span>Create First Group</span>
              </button>
            </div>

            <div v-else-if="filteredGroups.length === 0" class="p-6 text-center text-xs text-[#6b6680]">
              No groups match "{{ searchQuery }}".
            </div>

            <div
              v-for="group in filteredGroups"
              :key="'grp_' + group.id"
              @click="selectGroup(group)"
              class="group p-3 rounded-xl transition-all cursor-pointer relative"
              :class="activeGroup?.id === group.id ? 'bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#543ce0]/30 shadow-sm' : 'hover:bg-[#f6effe]/60 border border-transparent'"
            >
              <div class="flex items-start gap-3">
                <div class="relative flex-shrink-0">
                  <div
                    class="w-11 h-11 rounded-xl text-white flex items-center justify-center font-bold font-headline text-base shadow-xs"
                    :style="{ background: group.avatar_color || '#543ce0' }"
                  >
                    {{ group.name.charAt(0).toUpperCase() }}
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-0.5">
                    <h3 class="font-headline font-bold text-sm text-[#1e1a2b] truncate">{{ group.name }}</h3>
                    <span v-if="group.last_message_time" class="text-[10px] text-[#6b6680]">{{ group.last_message_time }}</span>
                  </div>
                  <div class="flex items-center gap-1.5 mb-1">
                    <span class="px-1.5 py-0.5 bg-[#f6effe] border border-[#eaddff] text-[10px] font-semibold text-[#543ce0] rounded">
                      {{ group.member_count }} {{ group.member_count === 1 ? 'member' : 'members' }}
                    </span>
                    <span v-if="group.role === 'admin'" class="px-1.5 py-0.5 bg-amber-50 text-amber-800 text-[9px] font-bold rounded border border-amber-200">
                      Admin
                    </span>
                  </div>
                  <div class="flex items-center justify-between">
                    <p class="text-xs text-[#6b6680] truncate">
                      {{ group.last_message || 'Created group' }}
                    </p>
                  </div>
                </div>
              </div>
              <!-- Selection bar -->
              <div v-if="activeGroup?.id === group.id" class="absolute left-0 top-3 bottom-3 w-1 bg-[#543ce0] rounded-r-full"></div>
            </div>
          </template>
        </div>

        <!-- Left Sidebar Footer -->
        <div class="p-3 bg-[#fdfaff] border-t border-[#eaddff] flex items-center justify-between text-xs text-[#6b6680]">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span class="font-medium">Active Peer Trading</span>
          </div>
          <span class="font-bold text-[#543ce0]">P2P Hub</span>
        </div>
      </aside>

      <!-- RIGHT: ACTIVE CHAT & VIDEO WORKSPACE -->
      <section class="flex-1 bg-white rounded-2xl border border-[#eaddff] flex flex-col h-full overflow-hidden shadow-sm relative">
        <template v-if="activePeer">
          <!-- 1. CHAT HEADER -->
          <header class="p-3.5 sm:px-6 border-b border-[#eaddff] bg-gradient-to-r from-white via-[#fdfaff] to-[#f6effe]/40 flex flex-wrap items-center justify-between gap-3 z-10 shadow-sm flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="relative">
                <div class="w-11 h-11 rounded-xl bg-gradient-to-tr from-[#543ce0] to-[#99366c] text-white flex items-center justify-center font-bold font-headline text-lg shadow-sm">
                  {{ (activePeer.full_name || activePeer.username).charAt(0).toUpperCase() }}
                </div>
                <span class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-emerald-500 border-2 border-white rounded-full"></span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h2 class="font-headline font-bold text-base text-[#1e1a2b]">{{ activePeer.full_name }}</h2>
                  <span class="px-2 py-0.5 bg-[#f6effe] border border-[#eaddff] text-[#543ce0] text-[10px] font-bold rounded-full">
                    {{ activePeer.department }} • Sem {{ activePeer.semester }}
                  </span>
                  <span class="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Online
                  </span>
                </div>
                <!-- Skill Loop Bar -->
                <div class="flex items-center gap-2 mt-0.5 text-xs text-[#6b6680]">
                  <span v-if="activePeer.learns && activePeer.learns.length" class="inline-flex items-center gap-1 font-semibold text-[#1e1a2b]">
                    <span class="material-symbols-outlined text-xs text-[#543ce0]">school</span>
                    <span>Wants: {{ activePeer.learns.slice(0, 2).join(', ') }}</span>
                  </span>
                  <span class="text-[#99366c] font-black">⇄</span>
                  <span v-if="activePeer.teaches && activePeer.teaches.length" class="inline-flex items-center gap-1 font-semibold text-[#99366c]">
                    <span class="material-symbols-outlined text-xs">psychology</span>
                    <span>Offers: {{ activePeer.teaches.slice(0, 2).join(', ') }}</span>
                  </span>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2.5">
              <!-- Schedule Session Button -->
              <button
                @click="openBookModal(activePeer)"
                class="px-3.5 py-2 rounded-xl bg-gradient-to-r from-[#543ce0]/10 to-[#99366c]/10 border border-[#543ce0]/30 hover:border-[#543ce0] text-[#543ce0] text-xs font-bold font-headline flex items-center gap-1.5 shadow-xs transition-all transform hover:-translate-y-0.5 active:scale-95"
                title="Schedule a dedicated skill exchange session"
              >
                <span class="material-symbols-outlined text-base">event</span>
                <span>Schedule Session</span>
              </button>

              <!-- Test Camera & Mic Button -->
              <button
                @click="testMediaDevices"
                :disabled="isCallActive"
                class="px-3 sm:px-4 py-2 rounded-xl bg-white border border-[#eaddff] hover:bg-[#f6effe] text-[#543ce0] text-xs font-bold font-headline flex items-center gap-2 shadow-sm transition-all transform hover:-translate-y-0.5 active:scale-95 disabled:opacity-50"
                title="Test Camera and Microphone before calling"
              >
                <span class="material-symbols-outlined text-base">settings_video_camera</span>
                <span class="hidden sm:inline">Test Setup</span>
              </button>

              <!-- Start Video Call Button -->
              <button
                @click="startCall"
                :disabled="isCallActive"
                class="px-3 sm:px-4 py-2 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white text-xs font-bold font-headline flex items-center gap-2 shadow-md shadow-[#543ce0]/25 transition-all transform hover:-translate-y-0.5 active:scale-95 disabled:opacity-50"
              >
                <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">videocam</span>
                <span class="hidden sm:inline">Start Video Call</span>
              </button>
            </div>
          </header>

          <!-- 2. SCROLLABLE MESSAGES FEED -->
          <div ref="messageContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-gradient-to-b from-[#fdfaff]/60 via-[#fbf4ff]/30 to-[#fdfaff]">
            <!-- Dynamic Escrow & Session Lifecycle Banner (Pillar 1) -->
            <div
              v-if="activePeerSession"
              class="max-w-2xl mx-auto p-4 rounded-2xl border transition-all shadow-sm"
              :class="{
                'bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-white border-amber-300': activePeerSession.status === 'pending',
                'bg-gradient-to-r from-[#543ce0]/10 via-[#99366c]/10 to-white border-[#543ce0]/40': activePeerSession.status === 'accepted',
                'bg-gradient-to-r from-emerald-500/10 via-emerald-500/5 to-white border-emerald-300': activePeerSession.status === 'completed'
              }"
            >
              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div class="flex items-center gap-3">
                  <div
                    class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0 shadow-xs"
                    :class="{
                      'bg-amber-500/20 text-amber-700': activePeerSession.status === 'pending',
                      'bg-[#543ce0]/20 text-[#543ce0]': activePeerSession.status === 'accepted',
                      'bg-emerald-500/20 text-emerald-700': activePeerSession.status === 'completed'
                    }"
                  >
                    <span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">
                      {{ activePeerSession.status === 'pending' ? 'hourglass_top' : (activePeerSession.status === 'accepted' ? 'handshake' : 'verified') }}
                    </span>
                  </div>
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="font-headline font-bold text-sm text-[#1e1a2b]">
                        {{ activePeerSession.status === 'pending' ? 'Exchange Pending Approval' : (activePeerSession.status === 'accepted' ? 'Active Skill Exchange' : 'Session Completed') }}
                      </span>
                      <span
                        class="px-2 py-0.5 rounded-full text-[10px] font-bold font-mono"
                        :class="{
                          'bg-amber-100 text-amber-800': activePeerSession.status === 'pending',
                          'bg-[#543ce0]/15 text-[#543ce0]': activePeerSession.status === 'accepted',
                          'bg-emerald-100 text-emerald-800': activePeerSession.status === 'completed'
                        }"
                      >
                        {{ activePeerSession.credit_cost }} Escrow Credit
                      </span>
                    </div>
                    <p class="text-xs text-[#6b6680] mt-0.5">
                      Skill: <strong class="text-[#1e1a2b]">{{ activePeerSession.skill_name }}</strong> • {{ activePeerSession.duration_minutes }} min
                      <span>• {{ formatSessionTime(activePeerSession.scheduled_at) }}</span>
                    </p>
                    <p v-if="activePeerSession.topic_notes" class="text-[11px] text-[#6b6680] italic mt-0.5">
                      "{{ activePeerSession.topic_notes }}"
                    </p>
                  </div>
                </div>

                <!-- Action Controls -->
                <div class="flex items-center gap-2 self-end sm:self-center">
                  <!-- Pending Teacher -->
                  <template v-if="activePeerSession.status === 'pending' && activePeerSession.my_role === 'teacher'">
                    <button
                      @click="respondSession(activePeerSession.id, 'accept')"
                      class="px-3 py-1.5 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white font-headline text-xs font-bold active:scale-95 transition-all shadow-xs flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-sm">check_circle</span>
                      <span>Accept</span>
                    </button>
                    <button
                      @click="respondSession(activePeerSession.id, 'reject')"
                      class="px-2.5 py-1.5 rounded-xl bg-white border border-[#eaddff] text-[#6b6680] hover:text-rose-600 hover:border-rose-300 font-headline text-xs font-semibold active:scale-95 transition-all"
                    >
                      Decline
                    </button>
                  </template>

                  <!-- Pending Learner -->
                  <template v-else-if="activePeerSession.status === 'pending' && activePeerSession.my_role === 'learner'">
                    <span class="text-[11px] text-amber-700 font-medium">Awaiting teacher...</span>
                    <button
                      @click="cancelSession(activePeerSession.id)"
                      class="px-2.5 py-1.5 rounded-xl bg-white border border-rose-200 text-rose-600 hover:bg-rose-50 text-[11px] font-bold active:scale-95 transition-all"
                    >
                      Cancel &amp; Refund
                    </button>
                  </template>

                  <!-- Accepted: Direct Completion (Works for text or video) -->
                  <template v-else-if="activePeerSession.status === 'accepted'">
                    <button
                      @click="completeSessionAction(activePeerSession)"
                      class="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-headline text-xs font-bold active:scale-95 transition-all shadow-sm flex items-center gap-1.5"
                      title="Complete session and release locked escrow to teacher"
                    >
                      <span class="material-symbols-outlined text-base">task_alt</span>
                      <span>Complete &amp; Release Escrow</span>
                    </button>
                  </template>

                  <!-- Completed: Review -->
                  <template v-else-if="activePeerSession.status === 'completed' && !activePeerSession.my_review">
                    <button
                      @click="openReviewModal(activePeerSession)"
                      class="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-headline text-xs font-bold active:scale-95 transition-all shadow-xs flex items-center gap-1"
                    >
                      <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">star</span>
                      <span>Review Mentor</span>
                    </button>
                  </template>
                </div>
              </div>
            </div>

            <!-- Default info banner if no active session -->
            <div v-else class="max-w-xl mx-auto p-3 bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#eaddff] rounded-2xl flex items-center justify-between gap-3 text-xs shadow-xs">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-white border border-[#eaddff] flex items-center justify-center text-[#543ce0] flex-shrink-0 shadow-xs">
                  <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">lock_clock</span>
                </div>
                <div>
                  <p class="font-bold text-[#1e1a2b]">SkillLoop Direct Exchange Channel</p>
                  <p class="text-[#6b6680]">Live chat, direct escrow guarantee, and campus peer verification.</p>
                </div>
              </div>
              <button
                @click="openBookModal(activePeer)"
                class="px-2.5 py-1 rounded-xl bg-[#543ce0]/10 hover:bg-[#543ce0]/20 text-[#543ce0] font-headline font-bold text-xs shrink-0 active:scale-95 transition-all flex items-center gap-1"
              >
                <span class="material-symbols-outlined text-sm">event</span>
                <span>Schedule Session</span>
              </button>
            </div>

            <div v-if="messages.length === 0" class="text-center py-12 text-xs text-[#6b6680]">
              No messages yet with {{ activePeer.full_name }}. Send a note or launch a video call!
            </div>

            <!-- Messages List -->
            <template v-for="msg in messages" :key="msg.id">
              <!-- Outgoing message (Current User) -->
              <div v-if="msg.sender_id === currentUser?.id" class="flex items-end justify-end gap-2.5 max-w-lg ml-auto">
                <div class="space-y-1 text-right">
                  <!-- Text message -->
                  <div v-if="msg.message_type === 'text'" class="bg-[#543ce0] text-white p-3.5 rounded-2xl rounded-br-sm text-xs leading-relaxed shadow-md shadow-[#543ce0]/15 text-left">
                    {{ msg.content }}
                  </div>
                  <!-- Image message -->
                  <div v-else-if="msg.message_type === 'image'" class="p-1.5 bg-[#543ce0] rounded-2xl rounded-br-sm shadow-md shadow-[#543ce0]/15 overflow-hidden">
                    <img :src="msg.file_url" :alt="msg.file_name" class="w-64 max-h-64 object-cover rounded-xl"/>
                    <p class="text-[11px] text-white/90 p-1 text-left truncate">{{ msg.file_name }} ({{ msg.file_size }})</p>
                  </div>
                  <!-- File/Doc message -->
                  <div v-else-if="msg.message_type === 'file'" class="p-3 bg-[#543ce0] text-white rounded-2xl rounded-br-sm shadow-md flex items-center gap-3 text-left">
                    <span class="material-symbols-outlined text-2xl">description</span>
                    <div class="flex-1 min-w-0">
                      <a :href="msg.file_url" target="_blank" download class="text-xs font-bold underline truncate block">{{ msg.file_name }}</a>
                      <span class="text-[10px] text-white/80">{{ msg.file_size }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-end gap-1 px-1 text-[10px] text-[#6b6680]">
                    <span>{{ msg.created_at }}</span>
                    <span class="material-symbols-outlined text-sm text-[#543ce0]" style="font-variation-settings: 'FILL' 1;">done_all</span>
                  </div>
                </div>
              </div>

              <!-- Incoming message (Peer) -->
              <div v-else class="flex items-end gap-2.5 max-w-lg">
                <div class="w-7 h-7 rounded-lg bg-[#543ce0]/20 text-[#543ce0] flex items-center justify-center font-bold text-xs mb-1 ring-1 ring-[#eaddff]">
                  {{ (activePeer.full_name || activePeer.username).charAt(0) }}
                </div>
                <div class="space-y-1">
                  <!-- Text message -->
                  <div v-if="msg.message_type === 'text'" class="bg-[#f6effe] border border-[#eaddff]/80 text-[#1e1a2b] p-3.5 rounded-2xl rounded-bl-sm text-xs leading-relaxed shadow-xs">
                    {{ msg.content }}
                  </div>
                  <!-- Image message -->
                  <div v-else-if="msg.message_type === 'image'" class="p-1.5 bg-[#f6effe] border border-[#eaddff] rounded-2xl rounded-bl-sm shadow-xs overflow-hidden">
                    <img :src="msg.file_url" :alt="msg.file_name" class="w-64 max-h-64 object-cover rounded-xl"/>
                    <p class="text-[11px] text-[#1e1a2b] p-1 truncate">{{ msg.file_name }} ({{ msg.file_size }})</p>
                  </div>
                  <!-- File message -->
                  <div v-else-if="msg.message_type === 'file'" class="p-3 bg-[#f6effe] border border-[#eaddff] text-[#1e1a2b] rounded-2xl rounded-bl-sm shadow-xs flex items-center gap-3">
                    <span class="material-symbols-outlined text-2xl text-[#99366c]">description</span>
                    <div class="flex-1 min-w-0">
                      <a :href="msg.file_url" target="_blank" download class="text-xs font-bold text-[#543ce0] hover:underline truncate block">{{ msg.file_name }}</a>
                      <span class="text-[10px] text-[#6b6680]">{{ msg.file_size }}</span>
                    </div>
                  </div>
                  <div class="flex items-center gap-1.5 px-1 text-[10px] text-[#6b6680]">
                    <span>{{ activePeer.full_name }}</span>
                    <span>•</span>
                    <span>{{ msg.created_at }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- 3. BOTTOM INPUT BAR -->
          <footer class="p-3 sm:p-4 bg-white border-t border-[#eaddff] relative z-10 flex-shrink-0">
            <form @submit.prevent="sendMessage" class="flex items-center gap-2 bg-[#fdfaff] border border-[#eaddff] rounded-2xl p-1.5 sm:p-2 focus-within:border-[#543ce0] focus-within:ring-2 focus-within:ring-[#543ce0]/20 transition-all shadow-xs">
              <!-- File Attachment Button -->
              <label class="w-9 h-9 rounded-xl flex items-center justify-center text-[#6b6680] hover:text-[#543ce0] hover:bg-[#f6effe] transition-colors cursor-pointer" title="Attach Document">
                <span class="material-symbols-outlined text-xl">attach_file</span>
                <input type="file" class="hidden" @change="handleFileUpload"/>
              </label>

              <!-- Image Upload Button -->
              <label class="w-9 h-9 rounded-xl flex items-center justify-center text-[#6b6680] hover:text-[#543ce0] hover:bg-[#f6effe] transition-colors cursor-pointer" title="Upload Image">
                <span class="material-symbols-outlined text-xl">image</span>
                <input type="file" accept="image/*" class="hidden" @change="handleFileUpload"/>
              </label>

              <!-- Text Input -->
              <input
                v-model="inputMessage"
                class="flex-1 bg-transparent border-0 text-xs sm:text-sm text-[#1e1a2b] placeholder-[#6b6680]/60 focus:outline-none px-2"
                :placeholder="`Type a message to ${activePeer.full_name}... (Press Enter)`"
                type="text"
              />

              <!-- Send Button -->
              <button
                type="submit"
                :disabled="!inputMessage.trim()"
                class="w-10 h-10 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white flex items-center justify-center shadow-md shadow-[#543ce0]/25 transition-all active:scale-95 flex-shrink-0 disabled:opacity-40"
                title="Send message"
              >
                <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">send</span>
              </button>
            </form>
          </footer>
        </template>

        <!-- ACTIVE GROUP CHAT WORKSPACE -->
        <template v-else-if="activeGroup">
          <!-- 1. GROUP CHAT HEADER -->
          <header class="p-3.5 sm:px-6 border-b border-[#eaddff] bg-gradient-to-r from-white via-[#fdfaff] to-[#f6effe]/40 flex flex-wrap items-center justify-between gap-3 z-10 shadow-sm flex-shrink-0">
            <div class="flex items-center gap-3">
              <div class="relative">
                <div
                  class="w-11 h-11 rounded-xl text-white flex items-center justify-center font-bold font-headline text-lg shadow-sm"
                  :style="{ background: activeGroup.avatar_color || '#543ce0' }"
                >
                  {{ activeGroup.name.charAt(0).toUpperCase() }}
                </div>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h2 class="font-headline font-bold text-base text-[#1e1a2b]">{{ activeGroup.name }}</h2>
                  <span class="px-2 py-0.5 bg-[#543ce0]/10 border border-[#543ce0]/20 text-[#543ce0] text-[10px] font-bold rounded-full">
                    {{ activeGroup.member_count || groupMembers.length }} Members
                  </span>
                  <span v-if="activeGroupRole === 'admin'" class="px-2 py-0.5 bg-amber-50 border border-amber-200 text-amber-700 text-[10px] font-bold rounded-full">
                    Admin
                  </span>
                </div>
                <p class="text-xs text-[#6b6680] truncate max-w-md">
                  {{ activeGroup.description || 'WhatsApp-style Campus Group Discussion' }}
                </p>
              </div>
            </div>

            <!-- Group Header Actions -->
            <div class="flex items-center gap-2">
              <button
                @click="openGroupInfoModal"
                class="px-3.5 py-1.5 rounded-xl bg-white border border-[#eaddff] hover:bg-[#f6effe] text-[#543ce0] text-xs font-bold font-headline flex items-center gap-1.5 shadow-sm transition-all transform hover:-translate-y-0.5 active:scale-95"
                title="View group members and info"
              >
                <span class="material-symbols-outlined text-base">group</span>
                <span>Group Info</span>
              </button>
            </div>
          </header>

          <!-- 2. SCROLLABLE GROUP MESSAGES FEED -->
          <div ref="groupMessageContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-gradient-to-b from-[#fdfaff]/60 via-[#fbf4ff]/30 to-[#fdfaff]">
            <!-- Group Banner -->
            <div class="max-w-xl mx-auto p-3 bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#eaddff] rounded-2xl flex items-center gap-3 text-xs shadow-xs">
              <div class="w-9 h-9 rounded-xl bg-white border border-[#eaddff] flex items-center justify-center text-[#543ce0] flex-shrink-0 shadow-xs">
                <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">groups</span>
              </div>
              <div class="flex-1">
                <p class="font-bold text-[#1e1a2b]">SkillLoop Campus Circle: {{ activeGroup.name }}</p>
                <p class="text-[#6b6680]">Messages in this group are shared in real-time with all members.</p>
              </div>
              <span class="px-2.5 py-1 bg-[#543ce0]/10 text-[#543ce0] text-[10px] font-extrabold rounded-full">Group Room</span>
            </div>

            <div v-if="groupMessages.length === 0" class="text-center py-12 text-xs text-[#6b6680]">
              No messages in {{ activeGroup.name }} yet. Start the conversation!
            </div>

            <!-- Messages List -->
            <template v-for="msg in groupMessages" :key="'gmsg_' + msg.id">
              <!-- Outgoing message (Current User) -->
              <div v-if="msg.sender_id === currentUser?.id" class="flex items-end justify-end gap-2.5 max-w-lg ml-auto">
                <div class="space-y-1 text-right">
                  <!-- Text message -->
                  <div v-if="msg.message_type === 'text'" class="bg-[#543ce0] text-white p-3.5 rounded-2xl rounded-br-sm text-xs leading-relaxed shadow-md shadow-[#543ce0]/15 text-left">
                    {{ msg.content }}
                  </div>
                  <!-- Image message -->
                  <div v-else-if="msg.message_type === 'image'" class="p-1.5 bg-[#543ce0] rounded-2xl rounded-br-sm shadow-md shadow-[#543ce0]/15 overflow-hidden">
                    <img :src="msg.file_url" :alt="msg.file_name" class="w-64 max-h-64 object-cover rounded-xl"/>
                    <p class="text-[11px] text-white/90 p-1 text-left truncate">{{ msg.file_name }} ({{ msg.file_size }})</p>
                  </div>
                  <!-- File/Doc message -->
                  <div v-else-if="msg.message_type === 'file'" class="p-3 bg-[#543ce0] text-white rounded-2xl rounded-br-sm shadow-md flex items-center gap-3 text-left">
                    <span class="material-symbols-outlined text-2xl">description</span>
                    <div class="flex-1 min-w-0">
                      <a :href="msg.file_url" target="_blank" download class="text-xs font-bold underline truncate block">{{ msg.file_name }}</a>
                      <span class="text-[10px] text-white/80">{{ msg.file_size }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-end gap-1 px-1 text-[10px] text-[#6b6680]">
                    <span>{{ msg.created_at }}</span>
                    <span class="material-symbols-outlined text-sm text-[#543ce0]" style="font-variation-settings: 'FILL' 1;">done_all</span>
                  </div>
                </div>
              </div>

              <!-- Incoming message (Group Peer) -->
              <div v-else class="flex items-end gap-2.5 max-w-lg">
                <div
                  class="w-7 h-7 rounded-lg text-white flex items-center justify-center font-bold text-xs mb-1 ring-1 ring-[#eaddff] flex-shrink-0"
                  :style="{ background: msg.sender_avatar_color || '#543ce0' }"
                >
                  {{ (msg.sender_name || msg.sender_username || 'U').charAt(0).toUpperCase() }}
                </div>
                <div class="space-y-1">
                  <!-- Sender name display above incoming bubble -->
                  <div class="flex items-center gap-1.5 px-1">
                    <span class="text-[11px] font-bold text-[#543ce0]">{{ msg.sender_name || msg.sender_username }}</span>
                    <span class="text-[9px] text-[#6b6680]">@{{ msg.sender_username }}</span>
                  </div>
                  <!-- Text message -->
                  <div v-if="msg.message_type === 'text'" class="bg-[#f6effe] border border-[#eaddff]/80 text-[#1e1a2b] p-3.5 rounded-2xl rounded-bl-sm text-xs leading-relaxed shadow-xs">
                    {{ msg.content }}
                  </div>
                  <!-- Image message -->
                  <div v-else-if="msg.message_type === 'image'" class="p-1.5 bg-[#f6effe] border border-[#eaddff] rounded-2xl rounded-bl-sm shadow-xs overflow-hidden">
                    <img :src="msg.file_url" :alt="msg.file_name" class="w-64 max-h-64 object-cover rounded-xl"/>
                    <p class="text-[11px] text-[#1e1a2b] p-1 truncate">{{ msg.file_name }} ({{ msg.file_size }})</p>
                  </div>
                  <!-- File message -->
                  <div v-else-if="msg.message_type === 'file'" class="p-3 bg-[#f6effe] border border-[#eaddff] text-[#1e1a2b] rounded-2xl rounded-bl-sm shadow-xs flex items-center gap-3">
                    <span class="material-symbols-outlined text-2xl text-[#99366c]">description</span>
                    <div class="flex-1 min-w-0">
                      <a :href="msg.file_url" target="_blank" download class="text-xs font-bold text-[#543ce0] hover:underline truncate block">{{ msg.file_name }}</a>
                      <span class="text-[10px] text-[#6b6680]">{{ msg.file_size }}</span>
                    </div>
                  </div>
                  <div class="flex items-center gap-1.5 px-1 text-[10px] text-[#6b6680]">
                    <span>{{ msg.created_at }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- 3. GROUP BOTTOM INPUT BAR -->
          <footer class="p-3 sm:p-4 bg-white border-t border-[#eaddff] relative z-10 flex-shrink-0">
            <form @submit.prevent="sendMessage" class="flex items-center gap-2 bg-[#fdfaff] border border-[#eaddff] rounded-2xl p-1.5 sm:p-2 focus-within:border-[#543ce0] focus-within:ring-2 focus-within:ring-[#543ce0]/20 transition-all shadow-xs">
              <!-- File Attachment Button -->
              <label class="w-9 h-9 rounded-xl flex items-center justify-center text-[#6b6680] hover:text-[#543ce0] hover:bg-[#f6effe] transition-colors cursor-pointer" title="Attach Document">
                <span class="material-symbols-outlined text-xl">attach_file</span>
                <input type="file" class="hidden" @change="handleFileUpload"/>
              </label>

              <!-- Image Upload Button -->
              <label class="w-9 h-9 rounded-xl flex items-center justify-center text-[#6b6680] hover:text-[#543ce0] hover:bg-[#f6effe] transition-colors cursor-pointer" title="Upload Image">
                <span class="material-symbols-outlined text-xl">image</span>
                <input type="file" accept="image/*" class="hidden" @change="handleFileUpload"/>
              </label>

              <!-- Text Input -->
              <input
                v-model="inputMessage"
                class="flex-1 bg-transparent border-0 text-xs sm:text-sm text-[#1e1a2b] placeholder-[#6b6680]/60 focus:outline-none px-2"
                :placeholder="`Message in ${activeGroup.name}... (Press Enter)`"
                type="text"
              />

              <!-- Send Button -->
              <button
                type="submit"
                :disabled="!inputMessage.trim()"
                class="w-10 h-10 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white flex items-center justify-center shadow-md shadow-[#543ce0]/25 transition-all active:scale-95 flex-shrink-0 disabled:opacity-40"
                title="Send message"
              >
                <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">send</span>
              </button>
            </form>
          </footer>
        </template>

        <!-- No Peer or Group Selected State -->
        <div v-else class="flex-1 flex items-center justify-center text-center p-6 space-y-3">
          <div class="w-16 h-16 rounded-2xl bg-[#f6effe] text-[#543ce0] flex items-center justify-center mx-auto shadow-xs">
            <span class="material-symbols-outlined text-3xl">chat</span>
          </div>
          <div>
            <h3 class="font-headline font-bold text-base text-[#1e1a2b]">Select a conversation to start messaging</h3>
            <p class="text-xs text-[#6b6680] mt-1 max-w-sm mx-auto">
              Choose any connected partner or group from the left sidebar to exchange notes, discuss projects, or collaborate.
            </p>
          </div>
        </div>

        <!-- 4. INCOMING CALL NOTIFICATION BANNER -->
        <div v-if="incomingCall" class="absolute top-4 left-1/2 -translate-x-1/2 bg-slate-900 text-white p-4 rounded-2xl shadow-2xl border-2 border-[#543ce0] z-50 flex items-center gap-4 animate-bounce">
          <div class="w-10 h-10 rounded-full bg-emerald-500 text-white flex items-center justify-center animate-pulse">
            <span class="material-symbols-outlined text-xl">phone_in_talk</span>
          </div>
          <div>
            <p class="text-xs font-bold text-white">{{ incomingCall.caller_name }} is calling you...</p>
            <p class="text-[10px] text-white/70">SkillLoop P2P Video Session</p>
          </div>
          <div class="flex items-center gap-2">
            <button @click="acceptCall" class="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold shadow-md">
              Accept
            </button>
            <button @click="rejectCall" class="px-3 py-1.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold shadow-md">
              Decline
            </button>
          </div>
        </div>

        <!-- 5. FULL-SCREEN IMMERSIVE VIDEO CALL OVERLAY & PIP MODE -->
        <div
          v-if="isCallActive"
          class="transition-all duration-300 z-50 overflow-hidden flex flex-col font-body"
          :class="isCallMinimized 
            ? 'fixed bottom-5 right-5 w-80 sm:w-96 h-56 sm:h-64 rounded-2xl shadow-2xl border-2 border-white/20 bg-[#0c0915] text-white' 
            : 'fixed inset-0 bg-[#0b0814] text-white'"
        >
          <!-- FULLSCREEN TOP BAR (Shown in full screen mode) -->
          <div
            v-if="!isCallMinimized"
            class="h-16 px-6 bg-black/60 backdrop-blur-xl border-b border-white/10 flex items-center justify-between shrink-0 z-30"
          >
            <!-- Left: Session & Teacher Indicator -->
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-xl bg-[#543ce0] text-white flex items-center justify-center shadow-md">
                <span class="material-symbols-outlined text-xl">all_inclusive</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-bold text-white uppercase tracking-wider font-headline">SkillLoop Live</span>
                  <span class="text-white/30">•</span>
                  <span class="text-xs font-semibold text-[#c084fc] bg-[#543ce0]/20 px-2.5 py-0.5 rounded-full border border-[#543ce0]/40">
                    🎓 {{ currentCallSkillName }}
                  </span>
                </div>
                <div class="flex items-center gap-2 text-xs text-white/70 mt-0.5">
                  <span>Teacher: <strong class="text-white">{{ activeTeacherName }}</strong></span>
                  <button
                    @click="toggleTeacherRole"
                    class="text-[10px] font-semibold text-[#c084fc] hover:text-white bg-white/10 hover:bg-white/20 px-2 py-0.5 rounded transition-all"
                    title="Click to switch who is teaching this session"
                  >
                    ⇄ Switch Role
                  </button>
                </div>
              </div>
            </div>

            <!-- Center: LIVE TEACHING TIMER & RECORDING STATUS -->
            <div class="flex items-center gap-2 bg-black/70 backdrop-blur-md px-4 py-1.5 rounded-full border border-white/15 shadow-inner">
              <span class="relative flex h-2.5 w-2.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
              </span>
              <span class="text-xs font-semibold text-rose-300 font-mono tracking-wider">REC</span>
              <span class="text-white/40">|</span>
              <div class="flex items-center gap-1.5 font-mono font-bold text-sm text-white">
                <span class="material-symbols-outlined text-base text-amber-400">timer</span>
                <span>{{ formattedCallDuration }}</span>
              </div>
              <span class="hidden md:inline text-[11px] text-white/50 pl-1">
                (Recording to {{ activeTeacherName }}'s record)
              </span>
            </div>

            <!-- Right: Quality & Window Controls -->
            <div class="flex items-center gap-2">
              <div class="hidden sm:flex items-center gap-1.5 bg-white/10 px-3 py-1 rounded-full text-[11px] text-white/80 border border-white/10">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>{{ iceConnectionStatus || 'HD Connected' }}</span>
              </div>
              <button
                @click="toggleCallMinimized"
                class="w-9 h-9 rounded-xl bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-all"
                title="Minimize to Picture-in-Picture to view chat"
              >
                <span class="material-symbols-outlined text-lg">close_fullscreen</span>
              </button>
              <button
                @click="toggleBrowserFullscreen"
                class="w-9 h-9 rounded-xl bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-all"
                title="Toggle Fullscreen"
              >
                <span class="material-symbols-outlined text-lg">{{ isBrowserFullscreen ? 'fullscreen_exit' : 'fullscreen' }}</span>
              </button>
            </div>
          </div>

          <!-- MINIMIZED TOP BAR (Shown when in small PiP mode) -->
          <div
            v-else
            class="h-9 px-3 bg-black/80 border-b border-white/10 flex items-center justify-between shrink-0 z-30"
          >
            <div class="flex items-center gap-2 text-xs">
              <span class="w-2 h-2 rounded-full bg-rose-500 animate-pulse"></span>
              <span class="font-mono font-bold text-white">{{ formattedCallDuration }}</span>
              <span class="text-[10px] text-white/60 truncate max-w-[120px]">{{ activePeer?.full_name }}</span>
            </div>
            <div class="flex items-center gap-1">
              <button
                @click="toggleCallMinimized"
                class="w-6 h-6 rounded bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition-all"
                title="Maximize to Full Screen"
              >
                <span class="material-symbols-outlined text-sm">open_in_full</span>
              </button>
            </div>
          </div>

          <!-- VIDEO STAGE CONTAINER -->
          <div class="relative flex-1 w-full bg-[#07050d] flex items-center justify-center overflow-hidden">
            <!-- STATE A: CALLING / RINGING SCREEN (Waiting for Peer to answer) -->
            <div
              v-if="callStatus === 'calling'"
              class="w-full h-full flex flex-col items-center justify-center p-6 text-center select-none z-20"
            >
              <div class="relative flex items-center justify-center mb-6">
                <div class="absolute w-44 h-44 rounded-full bg-[#543ce0]/20 animate-ping"></div>
                <div class="absolute w-36 h-36 rounded-full bg-[#543ce0]/30 animate-pulse"></div>
                <div
                  class="w-28 h-28 rounded-full flex items-center justify-center text-white text-4xl font-bold shadow-2xl z-10 border-4 border-white/20"
                  :style="{ background: activePeer?.avatar_color || '#543ce0' }"
                >
                  {{ (activePeer?.full_name || activePeer?.username || 'P').charAt(0).toUpperCase() }}
                </div>
              </div>

              <h2 class="text-2xl sm:text-3xl font-bold font-headline text-white tracking-tight">
                Calling {{ activePeer?.full_name || 'Peer' }}...
              </h2>
              <p class="text-sm text-white/70 mt-2 max-w-sm">
                Waiting for them to accept the incoming video exchange request.
              </p>

              <div class="mt-4 px-4 py-1.5 rounded-full bg-white/10 text-xs text-white/80 border border-white/10 flex items-center gap-2">
                <span class="material-symbols-outlined text-sm text-[#c084fc]">school</span>
                <span>Topic: {{ currentCallSkillName }}</span>
              </div>

              <div class="mt-8 flex items-center gap-4">
                <button
                  @click="endCall"
                  class="px-6 py-2.5 rounded-full bg-rose-600 hover:bg-rose-700 text-white font-bold flex items-center gap-2 shadow-lg shadow-rose-600/40 active:scale-95 transition-all text-sm"
                >
                  <span class="material-symbols-outlined text-base">call_end</span>
                  <span>Cancel Call</span>
                </button>
              </div>

              <!-- Floating local preview while calling -->
              <div class="absolute bottom-6 right-6 w-32 h-24 sm:w-40 sm:h-28 rounded-2xl overflow-hidden border-2 border-white/20 shadow-2xl bg-slate-900 z-30">
                <video ref="localVideoRef" autoplay playsinline muted class="w-full h-full object-cover"></video>
                <div class="absolute bottom-1.5 left-2 text-[9px] font-bold text-white bg-black/60 px-1.5 py-0.5 rounded">
                  You
                </div>
              </div>
            </div>

            <!-- STATE B: CONNECTED ACTIVE CALL -->
            <template v-else>
              <!-- Remote Video Stream -->
              <video
                ref="remoteVideoRef"
                autoplay
                playsinline
                class="w-full h-full object-contain sm:object-cover transition-opacity duration-300"
                :class="{ 'opacity-0': !hasRemoteVideo || isRemoteVideoMuted }"
              ></video>

              <!-- Remote Avatar / Camera Paused Fallback -->
              <div
                v-if="!hasRemoteVideo || isRemoteVideoMuted"
                class="absolute inset-0 flex flex-col items-center justify-center p-6 text-center select-none"
              >
                <div
                  class="w-32 h-32 rounded-full flex items-center justify-center text-white text-5xl font-bold shadow-2xl border-4 border-white/20 mb-4 animate-pulse"
                  :style="{ background: activePeer?.avatar_color || '#543ce0' }"
                >
                  {{ (activePeer?.full_name || activePeer?.username || 'P').charAt(0).toUpperCase() }}
                </div>
                <h3 class="text-xl font-bold font-headline text-white">{{ activePeer?.full_name }}</h3>
                <div class="flex items-center gap-2 mt-2 px-3 py-1 rounded-full bg-white/10 text-xs text-white/70 border border-white/10">
                  <span class="material-symbols-outlined text-sm text-emerald-400">mic</span>
                  <span>Microphone Active • Camera is Paused</span>
                </div>
              </div>

              <!-- Autoplay Unlock Overlay (For Chrome/Brave autoplay policies) -->
              <div
                v-if="isAutoplayBlocked"
                @click="resumeRemoteVideo"
                class="absolute inset-0 bg-black/85 backdrop-blur-md flex flex-col items-center justify-center p-6 text-center cursor-pointer z-40 transition-all hover:bg-black/75"
              >
                <div class="w-16 h-16 rounded-full bg-[#543ce0] text-white flex items-center justify-center mb-4 animate-pulse shadow-lg shadow-[#543ce0]/50">
                  <span class="material-symbols-outlined text-4xl">play_arrow</span>
                </div>
                <p class="font-bold text-base text-white font-headline">Click anywhere to enable live audio &amp; video</p>
                <p class="text-xs text-white/70 mt-1">Browser security requires one user interaction to allow remote audio playback.</p>
              </div>

              <!-- Floating Self Preview (Local Video PiP) -->
              <div
                class="absolute rounded-2xl overflow-hidden border-2 border-white/20 shadow-2xl bg-slate-900 z-30 transition-all duration-300"
                :class="isCallMinimized 
                  ? 'bottom-2 right-2 w-24 h-18' 
                  : 'bottom-20 right-6 w-36 h-28 sm:w-48 sm:h-36'"
              >
                <video ref="localVideoRef" autoplay playsinline muted class="w-full h-full object-cover" :class="{ 'hidden': isCameraOff }"></video>
                <div v-if="isCameraOff" class="w-full h-full bg-slate-800 flex flex-col items-center justify-center text-white/70">
                  <span class="material-symbols-outlined text-2xl">videocam_off</span>
                  <span class="text-[9px] mt-1 font-semibold">Camera Off</span>
                </div>
                <div class="absolute bottom-1.5 left-2 text-[9px] font-bold text-white bg-black/60 px-1.5 py-0.5 rounded flex items-center gap-1">
                  <span>You</span>
                  <span v-if="isMicMuted" class="text-rose-400 font-extrabold">• Muted</span>
                </div>
              </div>
            </template>

            <!-- Debug Status Banner (if active) -->
            <div v-if="callDebugStatus && !isCallMinimized" class="absolute top-4 left-6 bg-black/80 backdrop-blur-md text-amber-300 text-[10px] font-mono py-1 px-3 rounded-lg border border-amber-400/30 z-20 pointer-events-none">
              {{ callDebugStatus }}
            </div>
          </div>

          <!-- BOTTOM CONTROLS DOCK (Zoom / Google Meet Style) -->
          <div
            class="py-3 px-6 bg-black/80 backdrop-blur-xl border-t border-white/10 flex items-center justify-center gap-3 shrink-0 z-30"
            :class="{ 'py-2 px-3 gap-2': isCallMinimized }"
          >
            <!-- Microphone Mute/Unmute -->
            <button
              @click="toggleMic"
              class="rounded-full flex items-center justify-center transition-all active:scale-90"
              :class="[
                isCallMinimized ? 'w-8 h-8' : 'w-11 h-11',
                isMicMuted ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30' : 'bg-white/15 hover:bg-white/25 text-white'
              ]"
              :title="isMicMuted ? 'Unmute Mic' : 'Mute Mic'"
            >
              <span class="material-symbols-outlined" :class="isCallMinimized ? 'text-base' : 'text-xl'">
                {{ isMicMuted ? 'mic_off' : 'mic' }}
              </span>
            </button>

            <!-- Camera Toggle -->
            <button
              @click="toggleCamera"
              class="rounded-full flex items-center justify-center transition-all active:scale-90"
              :class="[
                isCallMinimized ? 'w-8 h-8' : 'w-11 h-11',
                isCameraOff ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30' : 'bg-white/15 hover:bg-white/25 text-white'
              ]"
              :title="isCameraOff ? 'Turn Camera On' : 'Turn Camera Off'"
            >
              <span class="material-symbols-outlined" :class="isCallMinimized ? 'text-base' : 'text-xl'">
                {{ isCameraOff ? 'videocam_off' : 'videocam' }}
              </span>
            </button>

            <!-- Screen Share -->
            <button
              v-if="!isCallMinimized"
              @click="toggleScreenShare"
              class="w-11 h-11 rounded-full flex items-center justify-center transition-all active:scale-90"
              :class="isScreenSharing ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30' : 'bg-white/15 hover:bg-white/25 text-white'"
              :title="isScreenSharing ? 'Stop Screen Share' : 'Share Screen'"
            >
              <span class="material-symbols-outlined text-xl">present_to_all</span>
            </button>

            <!-- Minimize / PiP Toggle Button -->
            <button
              v-if="!isCallMinimized"
              @click="toggleCallMinimized"
              class="w-11 h-11 rounded-full bg-white/15 hover:bg-white/25 text-white flex items-center justify-center transition-all active:scale-90"
              title="Minimize to view chat while staying on call"
            >
              <span class="material-symbols-outlined text-xl">picture_in_picture_alt</span>
            </button>

            <div v-if="!isCallMinimized" class="h-6 w-px bg-white/20 mx-1"></div>

            <!-- End Call Button -->
            <button
              @click="endCall"
              class="rounded-full bg-rose-600 hover:bg-rose-700 text-white font-bold flex items-center justify-center gap-2 shadow-lg shadow-rose-600/40 transition-all active:scale-95"
              :class="isCallMinimized ? 'h-8 px-3 text-[11px]' : 'h-11 px-6 text-sm'"
              title="End Call and save teaching time"
            >
              <span class="material-symbols-outlined" :class="isCallMinimized ? 'text-base' : 'text-xl'" style="font-variation-settings: 'FILL' 1;">call_end</span>
              <span>End Call</span>
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- 6. CREATE GROUP MODAL -->
    <div
      v-if="showCreateGroupModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="showCreateGroupModal = false"
    >
      <div class="bg-white rounded-2xl border border-[#eaddff] shadow-2xl max-w-md w-full overflow-hidden flex flex-col max-h-[85vh]">
        <!-- Modal Header -->
        <div class="p-4 border-b border-[#eaddff] bg-gradient-to-r from-white to-[#f6effe]/40 flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-[#543ce0]/10 text-[#543ce0] flex items-center justify-center">
              <span class="material-symbols-outlined text-xl">group_add</span>
            </div>
            <div>
              <h3 class="font-headline font-bold text-base text-[#1e1a2b]">Create New Group</h3>
              <p class="text-[11px] text-[#6b6680]">WhatsApp-style circle for study & projects</p>
            </div>
          </div>
          <button
            @click="showCreateGroupModal = false"
            class="w-8 h-8 rounded-lg flex items-center justify-center text-[#6b6680] hover:bg-[#f6effe] hover:text-[#1e1a2b] transition-all"
          >
            <span class="material-symbols-outlined text-lg">close</span>
          </button>
        </div>

        <!-- Modal Body -->
        <div class="p-4 sm:p-5 overflow-y-auto space-y-4 flex-1">
          <!-- Group Name -->
          <div>
            <label class="block text-xs font-bold text-[#1e1a2b] mb-1">Group Name *</label>
            <input
              v-model="newGroupName"
              type="text"
              maxlength="40"
              placeholder="e.g. AI Hackathon Squad, DSA Masters..."
              class="w-full px-3 py-2 bg-[#fdfaff] border border-[#eaddff] rounded-xl text-xs sm:text-sm text-[#1e1a2b] placeholder-[#6b6680]/60 focus:outline-none focus:ring-2 focus:ring-[#543ce0]/20 focus:border-[#543ce0]"
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-xs font-bold text-[#1e1a2b] mb-1">Topic / Description</label>
            <textarea
              v-model="newGroupDescription"
              rows="2"
              placeholder="What will you discuss and build here?"
              class="w-full px-3 py-2 bg-[#fdfaff] border border-[#eaddff] rounded-xl text-xs sm:text-sm text-[#1e1a2b] placeholder-[#6b6680]/60 focus:outline-none focus:ring-2 focus:ring-[#543ce0]/20 focus:border-[#543ce0] resize-none"
            ></textarea>
          </div>

          <!-- Select Members -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="text-xs font-bold text-[#1e1a2b]">Select Members ({{ selectedMemberIds.length }} selected)</label>
              <span class="text-[10px] text-[#6b6680]">From your connected peers</span>
            </div>

            <div class="max-h-48 overflow-y-auto border border-[#eaddff] rounded-xl p-2 divide-y divide-[#eaddff]/40 bg-[#fdfaff]">
              <div v-if="peers.length === 0" class="p-4 text-center text-xs text-[#6b6680]">
                No connected peers found to add.
              </div>
              <label
                v-for="p in peers"
                :key="'sel_' + p.id"
                class="flex items-center gap-2.5 p-2 rounded-lg hover:bg-[#f6effe]/70 cursor-pointer transition-colors"
              >
                <input
                  type="checkbox"
                  :value="p.id"
                  v-model="selectedMemberIds"
                  class="rounded text-[#543ce0] focus:ring-[#543ce0]"
                />
                <div class="w-7 h-7 rounded-lg bg-[#543ce0]/20 text-[#543ce0] flex items-center justify-center font-bold text-xs">
                  {{ (p.full_name || p.username).charAt(0).toUpperCase() }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-bold text-[#1e1a2b] truncate">{{ p.full_name }}</div>
                  <div class="text-[10px] text-[#6b6680]">@{{ p.username }} • {{ p.department || 'Campus Peer' }}</div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="p-4 border-t border-[#eaddff] bg-[#fdfaff] flex items-center justify-end gap-2">
          <button
            @click="showCreateGroupModal = false"
            class="px-4 py-2 rounded-xl border border-[#eaddff] text-xs font-bold text-[#6b6680] hover:bg-[#f6effe] transition-all"
          >
            Cancel
          </button>
          <button
            @click="submitCreateGroup"
            :disabled="!newGroupName.trim() || isSubmittingGroup"
            class="px-4 py-2 rounded-xl bg-[#543ce0] hover:bg-[#432ec4] text-white text-xs font-bold shadow-md shadow-[#543ce0]/20 active:scale-95 disabled:opacity-40 transition-all flex items-center gap-1.5"
          >
            <span v-if="isSubmittingGroup" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            <span>Create Group</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 7. GROUP INFO / MEMBERS MODAL -->
    <div
      v-if="showGroupInfoModal && activeGroup"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="showGroupInfoModal = false"
    >
      <div class="bg-white rounded-2xl border border-[#eaddff] shadow-2xl max-w-md w-full overflow-hidden flex flex-col max-h-[85vh]">
        <!-- Header -->
        <div class="p-4 border-b border-[#eaddff] bg-gradient-to-r from-white to-[#f6effe]/40 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div
              class="w-10 h-10 rounded-xl text-white flex items-center justify-center font-bold font-headline text-base shadow-xs"
              :style="{ background: activeGroup.avatar_color || '#543ce0' }"
            >
              {{ activeGroup.name.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h3 class="font-headline font-bold text-base text-[#1e1a2b]">{{ activeGroup.name }}</h3>
              <p class="text-[11px] text-[#6b6680]">{{ groupMembers.length }} Members</p>
            </div>
          </div>
          <button
            @click="showGroupInfoModal = false"
            class="w-8 h-8 rounded-lg flex items-center justify-center text-[#6b6680] hover:bg-[#f6effe] hover:text-[#1e1a2b] transition-all"
          >
            <span class="material-symbols-outlined text-lg">close</span>
          </button>
        </div>

        <!-- Body -->
        <div class="p-4 sm:p-5 overflow-y-auto space-y-4 flex-1">
          <div v-if="activeGroup.description" class="p-3 bg-[#f6effe]/50 border border-[#eaddff] rounded-xl text-xs text-[#1e1a2b]">
            <span class="font-bold block text-[10px] text-[#6b6680] uppercase tracking-wider mb-0.5">Description</span>
            {{ activeGroup.description }}
          </div>

          <!-- Add Member section (admin only) -->
          <div v-if="activeGroupRole === 'admin'" class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-[#1e1a2b]">Add New Member</span>
              <button
                @click="showAddMemberRow = !showAddMemberRow"
                class="text-[11px] font-bold text-[#543ce0] hover:underline"
              >
                {{ showAddMemberRow ? 'Hide' : '+ Add from Peers' }}
              </button>
            </div>
            <div v-if="showAddMemberRow" class="p-2 border border-[#eaddff] rounded-xl bg-[#fdfaff] space-y-2">
              <select
                v-model="memberToAddId"
                class="w-full px-2.5 py-1.5 bg-white border border-[#eaddff] rounded-lg text-xs text-[#1e1a2b] focus:outline-none focus:ring-1 focus:ring-[#543ce0]"
              >
                <option value="">Choose peer to add...</option>
                <option
                  v-for="p in availablePeersToAdd"
                  :key="'addp_' + p.id"
                  :value="p.id"
                >
                  {{ p.full_name }} (@{{ p.username }})
                </option>
              </select>
              <button
                @click="addMemberToGroup"
                :disabled="!memberToAddId"
                class="w-full py-1.5 rounded-lg bg-[#543ce0] text-white text-xs font-bold hover:bg-[#432ec4] disabled:opacity-40 transition-all"
              >
                Add to Group
              </button>
            </div>
          </div>

          <!-- Members List -->
          <div>
            <h4 class="text-xs font-bold text-[#1e1a2b] mb-2">Members</h4>
            <div class="divide-y divide-[#eaddff]/50 border border-[#eaddff] rounded-xl overflow-hidden bg-white">
              <div
                v-for="m in groupMembers"
                :key="'mem_' + m.id"
                class="p-2.5 flex items-center justify-between gap-2.5 hover:bg-[#fdfaff]"
              >
                <div class="flex items-center gap-2.5 min-w-0">
                  <div
                    class="w-8 h-8 rounded-lg text-white flex items-center justify-center font-bold text-xs flex-shrink-0"
                    :style="{ background: m.avatar_color || '#543ce0' }"
                  >
                    {{ (m.full_name || m.username || 'U').charAt(0).toUpperCase() }}
                  </div>
                  <div class="min-w-0">
                    <div class="text-xs font-bold text-[#1e1a2b] truncate flex items-center gap-1.5">
                      <span>{{ m.full_name || m.username }}</span>
                      <span v-if="m.id === currentUser?.id" class="text-[9px] text-[#6b6680] font-normal">(You)</span>
                    </div>
                    <div class="text-[10px] text-[#6b6680]">@{{ m.username }}</div>
                  </div>
                </div>

                <div class="flex items-center gap-2">
                  <span
                    class="px-2 py-0.5 rounded text-[10px] font-bold"
                    :class="m.role === 'admin' ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'"
                  >
                    {{ m.role === 'admin' ? 'Admin' : 'Member' }}
                  </span>

                  <!-- Remove button (admin can remove others) -->
                  <button
                    v-if="activeGroupRole === 'admin' && m.id !== currentUser?.id"
                    @click="removeMemberFromGroup(m.id)"
                    class="w-6 h-6 rounded flex items-center justify-center text-rose-500 hover:bg-rose-50"
                    title="Remove member"
                  >
                    <span class="material-symbols-outlined text-sm">person_remove</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="p-4 border-t border-[#eaddff] bg-[#fdfaff] flex items-center justify-between">
          <button
            @click="leaveActiveGroup"
            class="px-3 py-1.5 rounded-xl border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-bold flex items-center gap-1 transition-all"
          >
            <span class="material-symbols-outlined text-sm">logout</span>
            <span>Leave Group</span>
          </button>
          <button
            @click="showGroupInfoModal = false"
            class="px-4 py-2 rounded-xl bg-[#543ce0] text-white text-xs font-bold hover:bg-[#432ec4] transition-all"
          >
            Done
          </button>
        </div>
      </div>
    </div>

    <!-- 8. BOOK / SCHEDULE SESSION MODAL (PILLAR 1 ESCROW ENGINE) -->
    <div
      v-if="showBookModal && bookTargetPeer"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="showBookModal = false"
    >
      <div class="bg-white rounded-3xl border border-[#eaddff] shadow-2xl max-w-md w-full overflow-hidden flex flex-col p-6 space-y-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-[#543ce0]/10 text-[#543ce0] flex items-center justify-center">
              <span class="material-symbols-outlined text-xl">event_available</span>
            </div>
            <div>
              <h3 class="font-headline font-bold text-base text-[#1e1a2b]">Schedule Skill Exchange</h3>
              <p class="text-[11px] text-[#6b6680]">Lock credits in escrow &amp; confirm 1:1 mentorship</p>
            </div>
          </div>
          <button @click="showBookModal = false" class="p-1.5 rounded-full hover:bg-[#f6effe] text-[#6b6680] transition-colors">
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>

        <!-- Peer Info Strip -->
        <div class="p-3 bg-[#f6effe] border border-[#eaddff]/80 rounded-2xl flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-xl text-white font-bold text-sm flex items-center justify-center uppercase shadow-xs shrink-0"
            :style="{ background: bookTargetPeer.avatar_color || '#543ce0' }"
          >
            {{ (bookTargetPeer.full_name || bookTargetPeer.username || '?').charAt(0) }}
          </div>
          <div class="min-w-0">
            <h4 class="font-headline font-bold text-xs text-[#1e1a2b] truncate">{{ bookTargetPeer.full_name }}</h4>
            <p class="text-[10px] text-[#6b6680] truncate">Teacher • @{{ bookTargetPeer.username }} • {{ bookTargetPeer.department || 'Peer' }}</p>
          </div>
        </div>

        <!-- Form fields -->
        <div class="space-y-3.5">
          <!-- Skill Name -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider">Skill to Learn</label>
              <span v-if="bookTargetPeerTeaches.length > 0" class="text-[10px] text-[#543ce0] font-semibold">Click to auto-fill</span>
            </div>
            <input
              v-model="bookForm.skill_name"
              type="text"
              placeholder="e.g. Python, Docker, UI Design..."
              class="w-full px-4 py-2.5 rounded-xl bg-[#fdfaff] border border-[#eaddff] text-sm text-[#1e1a2b] focus:outline-none focus:border-[#543ce0] transition-colors font-medium"
            />
            <div v-if="bookTargetPeerTeaches.length > 0" class="flex flex-wrap gap-1.5 mt-2">
              <button
                v-for="s in bookTargetPeerTeaches"
                :key="s"
                type="button"
                @click="bookForm.skill_name = s"
                class="px-2.5 py-1 rounded-lg text-xs font-medium transition-all"
                :class="bookForm.skill_name.toLowerCase() === s.toLowerCase() ? 'bg-[#543ce0] text-white shadow-xs' : 'bg-[#543ce0]/10 text-[#543ce0] hover:bg-[#543ce0]/20'"
              >
                {{ s }}
              </button>
            </div>
          </div>

          <!-- Duration Selector -->
          <div>
            <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider mb-1 block">Session Duration &amp; Cost</label>
            <div class="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                @click="bookForm.duration_minutes = 30"
                class="p-3 rounded-2xl border text-left transition-all"
                :class="bookForm.duration_minutes === 30 ? 'border-[#543ce0] bg-[#543ce0]/10 text-[#543ce0] shadow-xs' : 'border-[#eaddff] bg-[#fdfaff] text-[#1e1a2b] hover:border-[#543ce0]/40'"
              >
                <span class="font-headline font-bold text-sm block">30 Minutes</span>
                <span class="text-[11px] font-mono text-[#6b6680]">0.5 Time Credit</span>
              </button>
              <button
                type="button"
                @click="bookForm.duration_minutes = 60"
                class="p-3 rounded-2xl border text-left transition-all"
                :class="bookForm.duration_minutes === 60 ? 'border-[#543ce0] bg-[#543ce0]/10 text-[#543ce0] shadow-xs' : 'border-[#eaddff] bg-[#fdfaff] text-[#1e1a2b] hover:border-[#543ce0]/40'"
              >
                <span class="font-headline font-bold text-sm block">60 Minutes</span>
                <span class="text-[11px] font-mono text-[#6b6680]">1.0 Time Credit</span>
              </button>
            </div>
          </div>

          <!-- Date & Time (Optional) -->
          <div>
            <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider mb-1 block">Scheduled Date &amp; Time (Optional)</label>
            <input
              v-model="bookForm.scheduled_at"
              type="datetime-local"
              class="w-full px-4 py-2.5 rounded-xl bg-[#fdfaff] border border-[#eaddff] text-xs sm:text-sm text-[#1e1a2b] focus:outline-none focus:border-[#543ce0] transition-colors"
            />
            <p class="text-[10px] text-[#6b6680] mt-1">Leave empty to conduct the session right now via Chat.</p>
          </div>

          <!-- Topic Notes -->
          <div>
            <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider mb-1 block">Session Goals / Questions</label>
            <textarea
              v-model="bookForm.topic_notes"
              rows="2"
              placeholder="What specific problems or topics do you want to cover?"
              class="w-full px-4 py-2.5 rounded-xl bg-[#fdfaff] border border-[#eaddff] text-sm text-[#1e1a2b] focus:outline-none focus:border-[#543ce0] transition-colors resize-none"
            ></textarea>
          </div>
        </div>

        <!-- Escrow Notice -->
        <div class="p-3 rounded-2xl bg-[#543ce0]/5 border border-[#543ce0]/20 text-[11px] text-[#6b6680] flex items-start gap-2">
          <span class="material-symbols-outlined text-base text-[#543ce0] shrink-0">lock</span>
          <div>
            <p class="font-bold text-[#1e1a2b]">Escrow Guarantee</p>
            <p>{{ bookForm.duration_minutes <= 30 ? '0.5' : '1.0' }} Time Credit will be held in escrow. It is only released to the teacher when the session is completed. If cancelled, it is immediately refunded.</p>
          </div>
        </div>

        <div class="flex gap-3 pt-2">
          <button
            @click="submitBookSession"
            :disabled="isBooking || !bookForm.skill_name.trim()"
            class="flex-1 py-2.5 rounded-xl bg-[#543ce0] text-white font-headline font-semibold text-sm hover:bg-[#432dbb] active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-xs flex items-center justify-center gap-2"
          >
            <span v-if="isBooking" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
            <span>{{ isBooking ? 'Booking...' : 'Book & Hold Escrow' }}</span>
          </button>
          <button @click="showBookModal = false" class="px-5 py-2.5 rounded-xl border border-[#eaddff] text-[#6b6680] hover:bg-[#f6effe] font-headline font-semibold text-sm transition-all">Cancel</button>
        </div>
      </div>
    </div>

    <!-- 9. POST-SESSION RATING & REVIEW MODAL (PILLAR 1 ESCROW ENGINE) -->
    <div
      v-if="showReviewModal && reviewingSession"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
      @click.self="showReviewModal = false"
    >
      <div class="bg-white rounded-3xl border border-[#eaddff] shadow-2xl max-w-md w-full overflow-hidden flex flex-col p-6 space-y-5">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center">
              <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">star</span>
            </div>
            <div>
              <h3 class="font-headline font-bold text-base text-[#1e1a2b]">Rate Your Exchange</h3>
              <p class="text-[11px] text-[#6b6680]">Build campus trust &amp; verified peer reputation</p>
            </div>
          </div>
          <button @click="showReviewModal = false" class="p-1.5 rounded-full hover:bg-[#f6effe] text-[#6b6680] transition-colors">
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>

        <!-- Peer info -->
        <div class="p-3 bg-[#f6effe] border border-[#eaddff]/80 rounded-2xl flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-xl text-white font-bold text-sm flex items-center justify-center uppercase shadow-xs shrink-0"
            :style="{ background: reviewingSession.peer_avatar || '#543ce0' }"
          >
            {{ (reviewingSession.peer_name || reviewingSession.peer_username || '?').charAt(0) }}
          </div>
          <div class="min-w-0">
            <h4 class="font-headline font-bold text-xs text-[#1e1a2b] truncate">{{ reviewingSession.peer_name }}</h4>
            <p class="text-[10px] text-[#6b6680] truncate">Session: {{ reviewingSession.skill_name }} ({{ reviewingSession.duration_minutes }}m)</p>
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
                :class="star <= reviewForm.rating ? 'text-amber-500' : 'text-slate-200'"
                :style="star <= reviewForm.rating ? `font-variation-settings: 'FILL' 1;` : ''"
              >
                star
              </span>
            </button>
          </div>
          <p class="text-xs font-bold font-headline text-[#1e1a2b]">
            {{ reviewForm.rating === 5 ? 'Exceptional Mentor! ⭐⭐⭐⭐⭐' : (reviewForm.rating === 4 ? 'Very Helpful & Clear ⭐⭐⭐⭐' : (reviewForm.rating === 3 ? 'Good Session ⭐⭐⭐' : 'Needs Improvement')) }}
          </p>
        </div>

        <!-- Tag Badges -->
        <div>
          <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider mb-1.5 block">Endorse Strengths (Optional)</label>
          <div class="flex flex-wrap gap-1.5">
            <button
              v-for="tag in ['Clear Explanations', 'Hands-on Code', 'Patient', 'Great Mentor', 'Punctual', 'Debugging Pro']"
              :key="tag"
              type="button"
              @click="toggleReviewTag(tag)"
              class="px-2.5 py-1 rounded-xl text-xs font-bold transition-all"
              :class="reviewForm.tags.includes(tag) ? 'bg-[#543ce0] text-white shadow-xs' : 'bg-[#f6effe] text-[#6b6680] hover:bg-[#eaddff]/60'"
            >
              {{ tag }}
            </button>
          </div>
        </div>

        <!-- Comment -->
        <div>
          <label class="text-xs font-semibold text-[#6b6680] uppercase tracking-wider mb-1 block">Feedback / Testimonial</label>
          <textarea
            v-model="reviewForm.comment"
            rows="2"
            placeholder="What made this session great?"
            class="w-full px-4 py-2.5 rounded-xl bg-[#fdfaff] border border-[#eaddff] text-sm text-[#1e1a2b] focus:outline-none focus:border-[#543ce0] transition-colors resize-none"
          ></textarea>
        </div>

        <div class="flex gap-3 pt-2">
          <button
            @click="submitReview"
            :disabled="isSubmittingReview"
            class="flex-1 py-2.5 rounded-xl bg-[#543ce0] text-white font-headline font-semibold text-sm hover:bg-[#432dbb] active:scale-95 transition-all shadow-xs flex items-center justify-center gap-2"
          >
            <span v-if="isSubmittingReview" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin"></span>
            <span>{{ isSubmittingReview ? 'Submitting...' : 'Submit Review' }}</span>
          </button>
          <button @click="showReviewModal = false" class="px-5 py-2.5 rounded-xl border border-[#eaddff] text-[#6b6680] hover:bg-[#f6effe] font-headline font-semibold text-sm transition-all">Skip</button>
        </div>
      </div>
    </div>

    <!-- 10. POST-CALL TEACHING TIME SUMMARY MODAL -->
    <div
      v-if="showCallSummaryModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      @click.self="showCallSummaryModal = false"
    >
      <div class="bg-white rounded-3xl border border-[#eaddff] shadow-2xl max-w-md w-full overflow-hidden p-6 space-y-5">
        <div class="text-center space-y-2">
          <div class="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-md">
            <span class="material-symbols-outlined text-3xl">verified</span>
          </div>
          <h3 class="font-headline font-bold text-xl text-[#1e1a2b]">Skill Exchange Completed!</h3>
          <p class="text-xs text-[#6b6680]">Live teaching duration has been verified and recorded to the official campus ledger.</p>
        </div>

        <div class="bg-[#f6effe]/60 rounded-2xl p-4 border border-[#eaddff] space-y-3">
          <div class="flex items-center justify-between text-xs">
            <span class="text-[#6b6680] font-medium">Session Topic</span>
            <span class="font-bold text-[#1e1a2b]">{{ lastSummaryData.skillName || currentCallSkillName }}</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-[#6b6680] font-medium">Time Taught This Call</span>
            <span class="font-bold text-emerald-600 font-mono text-sm">⏱️ {{ lastSummaryData.durationFormatted }}</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-[#6b6680] font-medium">Credited Teacher</span>
            <span class="font-bold text-[#543ce0]">🎓 {{ lastSummaryData.teacherName }}</span>
          </div>
          <div v-if="lastSummaryData.totalTeachingFormatted" class="flex items-center justify-between text-xs pt-2 border-t border-[#eaddff]">
            <span class="text-[#6b6680] font-medium">Teacher's Cumulative Record</span>
            <span class="font-bold text-[#1e1a2b]">{{ lastSummaryData.totalTeachingFormatted }}</span>
          </div>
        </div>

        <div class="space-y-2 pt-2">
          <button
            v-if="activePeerSession && activePeerSession.status === 'accepted'"
            @click="showCallSummaryModal = false; completeSessionAction(activePeerSession)"
            class="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-headline text-sm font-bold flex items-center justify-center gap-2 shadow-md transition-all active:scale-95"
          >
            <span class="material-symbols-outlined text-lg">workspace_premium</span>
            <span>Mark Exchange Complete &amp; Review</span>
          </button>
          <button
            @click="showCallSummaryModal = false"
            class="w-full py-3 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white font-headline text-sm font-bold flex items-center justify-center gap-2 shadow-md transition-all active:scale-95"
          >
            <span>Done</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, reactive } from 'vue'
import { io } from 'socket.io-client'

const currentUser = ref(null)
const peers = ref([])
const activePeer = ref(null)
const messages = ref([])
const inputMessage = ref('')
const searchQuery = ref('')
const isLoadingPeers = ref(true)
const messageContainer = ref(null)

// ─── Exchange Sessions & Escrow (Pillar 1) ──────────────────────────────────
const exchangeSessions = ref([])
const loadingSessions = ref(false)

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

const showReviewModal = ref(false)
const reviewingSession = ref(null)
const isSubmittingReview = ref(false)
const reviewForm = reactive({
  rating: 5,
  tags: [],
  comment: ''
})

const activePeerSession = computed(() => {
  if (!activePeer.value || !exchangeSessions.value) return null
  const peerId = activePeer.value.id
  const matching = exchangeSessions.value.filter(s => s.peer_id === peerId)
  return matching.find(s => s.status === 'accepted')
    || matching.find(s => s.status === 'pending')
    || matching.find(s => s.status === 'completed' && !s.my_review)
    || null
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

// Group Chat State
const sidebarTab = ref('peers') // 'peers' or 'groups'
const groups = ref([])
const activeGroup = ref(null)
const groupMessages = ref([])
const groupMembers = ref([])
const activeGroupRole = ref('member')
const isLoadingGroups = ref(false)
const groupMessageContainer = ref(null)

// Create Group Modal state
const showCreateGroupModal = ref(false)
const newGroupName = ref('')
const newGroupDescription = ref('')
const selectedMemberIds = ref([])
const isSubmittingGroup = ref(false)

// Group Info Modal state
const showGroupInfoModal = ref(false)
const showAddMemberRow = ref(false)
const memberToAddId = ref('')

// WebRTC & Call State
const socket = ref(null)
const isCallActive = ref(false)
const incomingCall = ref(null)
const isMicMuted = ref(false)
const isCameraOff = ref(false)
const isScreenSharing = ref(false)
const isAutoplayBlocked = ref(false)
const iceConnectionStatus = ref('Connecting...')
const callDebugStatus = ref('')

const localVideoRef = ref(null)
const remoteVideoRef = ref(null)

// ─── Enhanced Fullscreen Video Call & Live Teaching Recording State ─────────
const callStatus = ref('idle') // 'idle' | 'calling' | 'connected' | 'ended'
const isCallMinimized = ref(false)
const isBrowserFullscreen = ref(false)
const callDurationSeconds = ref(0)
let callTimerInterval = null
let hasRecordedCall = false

const activeCallRole = ref('peer_teaching') // 'peer_teaching' | 'user_teaching'
const hasRemoteVideo = ref(false)
const isRemoteVideoMuted = ref(false)

const showCallSummaryModal = ref(false)
const lastSummaryData = reactive({
  durationFormatted: '',
  teacherName: '',
  totalTeachingFormatted: '',
  skillName: ''
})

const determineInitialCallRole = () => {
  if (activePeerSession.value) {
    if (activePeerSession.value.teacher_id === currentUser.value?.id) {
      activeCallRole.value = 'user_teaching'
    } else {
      activeCallRole.value = 'peer_teaching'
    }
    return
  }
  // If no formal session booked:
  if (activePeer.value?.teaches && activePeer.value.teaches.length > 0) {
    activeCallRole.value = 'peer_teaching'
  } else {
    activeCallRole.value = 'user_teaching'
  }
}

const activeTeacherName = computed(() => {
  if (activeCallRole.value === 'user_teaching') {
    return currentUser.value?.full_name || currentUser.value?.username || 'You'
  }
  return activePeer.value?.full_name || activePeer.value?.username || 'Peer'
})

const activeLearnerName = computed(() => {
  if (activeCallRole.value === 'user_teaching') {
    return activePeer.value?.full_name || activePeer.value?.username || 'Peer'
  }
  return currentUser.value?.full_name || currentUser.value?.username || 'You'
})

const currentCallSkillName = computed(() => {
  if (activePeerSession.value?.skill_name) {
    return activePeerSession.value.skill_name
  }
  if (activeCallRole.value === 'peer_teaching' && activePeer.value?.teaches?.length) {
    return Array.isArray(activePeer.value.teaches) ? activePeer.value.teaches[0] : activePeer.value.teaches
  }
  if (activeCallRole.value === 'user_teaching' && currentUser.value?.skills_taught?.length) {
    return Array.isArray(currentUser.value.skills_taught) ? currentUser.value.skills_taught[0] : currentUser.value.skills_taught
  }
  return 'Skill Exchange'
})

const formattedCallDuration = computed(() => {
  const total = callDurationSeconds.value
  const h = Math.floor(total / 3600)
  const m = Math.floor((total % 3600) / 60)
  const s = total % 60
  const pad = (n) => String(n).padStart(2, '0')
  if (h > 0) {
    return `${h}:${pad(m)}:${pad(s)}`
  }
  return `${pad(m)}:${pad(s)}`
})

const startCallTimer = () => {
  if (callTimerInterval) return
  callDurationSeconds.value = 0
  callTimerInterval = setInterval(() => {
    callDurationSeconds.value++
  }, 1000)
}

const stopCallTimer = () => {
  if (callTimerInterval) {
    clearInterval(callTimerInterval)
    callTimerInterval = null
  }
}

const toggleTeacherRole = () => {
  activeCallRole.value = activeCallRole.value === 'user_teaching' ? 'peer_teaching' : 'user_teaching'
}

const toggleCallMinimized = () => {
  isCallMinimized.value = !isCallMinimized.value
}

const toggleBrowserFullscreen = () => {
  if (typeof document === 'undefined') return
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch(() => {})
    isBrowserFullscreen.value = true
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {})
      isBrowserFullscreen.value = false
    }
  }
}

const recordTeachingSession = async (durationSec) => {
  if (durationSec < 5) return null

  const isUserTeacher = activeCallRole.value === 'user_teaching'
  const teacherId = isUserTeacher ? currentUser.value?.id : activePeer.value?.id
  const learnerId = isUserTeacher ? activePeer.value?.id : currentUser.value?.id
  const skillName = currentCallSkillName.value || 'Skill Exchange'
  const sessionId = activePeerSession.value?.id || null

  if (!teacherId || !learnerId) return null

  try {
    const res = await $fetch('/api/sessions/record-teaching-time', {
      method: 'POST',
      body: {
        teacher_id: teacherId,
        learner_id: learnerId,
        duration_seconds: durationSec,
        skill_name: skillName,
        session_id: sessionId
      }
    })

    lastSummaryData.durationFormatted = res.recorded_duration_formatted || `${durationSec}s`
    lastSummaryData.teacherName = activeTeacherName.value
    lastSummaryData.totalTeachingFormatted = res.total_teaching_formatted || ''
    lastSummaryData.skillName = skillName
    showCallSummaryModal.value = true

    await fetchCurrentUser()
    return res
  } catch (err) {
    console.error('Failed to record teaching time:', err)
    return null
  }
}

let peerConnection = null
let localStream = null
let remoteStream = null
let currentCallPeerId = null
let pendingICECandidates = []  // Queue ICE candidates before remote desc is set
let iceRetryCount = 0
let iceWatchTimer = null
let isMakingOffer = false
let iceTransportPolicy = 'relay'

const resumeRemoteVideo = async () => {
  if (remoteVideoRef.value) {
    try {
      await remoteVideoRef.value.play()
      isAutoplayBlocked.value = false
      console.log('[WebRTC] Remote video resumed manually')
    } catch (e) {
      console.error('[WebRTC] Error resuming remote video:', e)
    }
  }
}

const testMediaDevices = async () => {
  try {
    const stream = await requestUserMediaSafe()
    const tracks = stream.getTracks().map(t => t.kind)
    alert(`✅ Setup Test Successful!\n\nDetected streams: ${tracks.join(', ')}\nYour devices are working perfectly.`)
    // Stop tracks immediately since it's just a test
    stream.getTracks().forEach(t => t.stop())
  } catch (e) {
    if (e.message === 'InsecureContextError') {
      alert("⚠️ Camera Access Blocked (Insecure Context):\n\nBrowsers block camera/mic access on HTTP networks.\n\nPlease either:\n1. Run on localhost (http://localhost:3000)\n2. Serve via HTTPS (e.g. using Cloudflare Tunnel)")
    } else {
      alert(`❌ Setup Test Failed:\n\nCould not access camera/mic: ${e.message}\n\nDetailed Trace:\n${mediaDebugMsg.value}\n\nPlease check browser permissions.`)
    }
  }
}

const fallbackIceServers = [
  { urls: 'stun:stun.l.google.com:19302' },
  { urls: 'stun:stun1.l.google.com:19302' },
  { urls: 'stun:stun.cloudflare.com:3478' },
  {
    urls: [
      'turn:staticauth.openrelay.metered.ca:80',
      'turn:staticauth.openrelay.metered.ca:443',
      'turn:staticauth.openrelay.metered.ca:443?transport=tcp',
      'turns:staticauth.openrelay.metered.ca:443?transport=tcp'
    ],
    username: 'openrelayproject',
    credential: 'openrelayproject'
  }
]

let rtcConfig = {
  iceServers: fallbackIceServers,
  iceCandidatePoolSize: 4,
  bundlePolicy: 'max-bundle',
  rtcpMuxPolicy: 'require',
  iceTransportPolicy: 'all'
}

const getRtcConfig = () => ({
  ...rtcConfig,
  iceTransportPolicy
})

const serializeCandidate = (candidate) => {
  if (!candidate) return null
  if (typeof candidate.toJSON === 'function') return candidate.toJSON()
  return {
    candidate: candidate.candidate,
    sdpMid: candidate.sdpMid,
    sdpMLineIndex: candidate.sdpMLineIndex,
    usernameFragment: candidate.usernameFragment
  }
}

const waitForIceGathering = (pc, timeoutMs = 5000) => new Promise((resolve) => {
  if (!pc || pc.iceGatheringState === 'complete') {
    resolve()
    return
  }
  const finish = () => {
    pc.removeEventListener('icegatheringstatechange', onChange)
    clearTimeout(timer)
    resolve()
  }
  const onChange = () => {
    if (pc.iceGatheringState === 'complete') finish()
  }
  pc.addEventListener('icegatheringstatechange', onChange)
  const timer = setTimeout(finish, timeoutMs)
})

const drainQueuedIce = async () => {
  if (!peerConnection || !peerConnection.remoteDescription?.type) return
  const queued = pendingICECandidates.splice(0)
  for (const candidate of queued) {
    try {
      await peerConnection.addIceCandidate(new RTCIceCandidate(candidate))
      console.log('[WebRTC] Drained queued ICE candidate')
    } catch (e) {
      console.warn('[WebRTC] Error draining ICE candidate', e)
    }
  }
}

const fetchTurnCredentials = async () => {
  try {
    const res = await fetch('/api/turn-credentials', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      const servers = Array.isArray(data.iceServers) && data.iceServers.length
        ? data.iceServers
        : fallbackIceServers
      rtcConfig = { ...rtcConfig, iceServers: servers }
      console.log('[WebRTC] ICE servers loaded:', servers.length, 'hasTurn=', data.hasTurn)
      console.log('=== ICE SERVERS FOR CLAUDE ===')
      console.log(JSON.stringify(servers, null, 2))
      console.log('==============================')
    }
  } catch (e) {
    console.warn('[WebRTC] Could not fetch TURN credentials, using fallback relays:', e)
  }
}

// Helper: attach stream to a video ref, retrying until DOM is ready
const attachStream = async (videoRef, stream, maxWait = 3000) => {
  const start = Date.now()
  while (!videoRef.value) {
    if (Date.now() - start > maxWait) {
      console.warn('[WebRTC] Timed out waiting for video element')
      return
    }
    await new Promise(r => setTimeout(r, 50))
  }
  if (videoRef.value.srcObject !== stream) {
    videoRef.value.srcObject = stream
    try {
      await videoRef.value.play()
      if (videoRef === remoteVideoRef) {
        isAutoplayBlocked.value = false
      }
    } catch (e) {
      if (e.name !== 'AbortError') {
        console.warn('[WebRTC] Autoplay handled:', e)
        if (videoRef === remoteVideoRef) {
          isAutoplayBlocked.value = true
        }
      }
    }
  } else {
    if (videoRef.value.paused) {
      try {
        await videoRef.value.play()
      } catch (e) {
        // Ignored
      }
    }
  }
}

const filteredPeers = computed(() => {
  if (!searchQuery.value.trim()) return peers.value
  const q = searchQuery.value.toLowerCase()
  return peers.value.filter(p =>
    (p.full_name && p.full_name.toLowerCase().includes(q)) ||
    (p.username && p.username.toLowerCase().includes(q)) ||
    (p.department && p.department.toLowerCase().includes(q)) ||
    (p.teaches && p.teaches.some(s => s.toLowerCase().includes(q)))
  )
})

const filteredGroups = computed(() => {
  if (!searchQuery.value.trim()) return groups.value
  const q = searchQuery.value.toLowerCase()
  return groups.value.filter(g =>
    (g.name && g.name.toLowerCase().includes(q)) ||
    (g.description && g.description.toLowerCase().includes(q))
  )
})

const availablePeersToAdd = computed(() => {
  if (!groupMembers.value || !peers.value) return []
  const memberIds = new Set(groupMembers.value.map(m => m.id))
  return peers.value.filter(p => !memberIds.has(p.id))
})

onMounted(async () => {
  await fetchCurrentUser()
  await fetchPeers()
  await fetchGroups()
  await fetchSessions()
  setupSocket()
  startMessageSync()
  // Fetch TURN credentials non-blockingly in the background so socket connects immediately
  fetchTurnCredentials()
  if (typeof window !== 'undefined') {
    window.addEventListener('focus', handleWindowFocus)
    document.addEventListener('visibilitychange', handleVisibilityChange)
  }
})

onUnmounted(() => {
  endCall()
  stopMessageSync()
  if (typeof window !== 'undefined') {
    window.removeEventListener('focus', handleWindowFocus)
    document.removeEventListener('visibilitychange', handleVisibilityChange)
  }
  if (socket.value) {
    socket.value.disconnect()
  }
})

const fetchCurrentUser = async () => {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      currentUser.value = data.user
    } else {
      if (typeof localStorage !== 'undefined') {
        localStorage.removeItem('skillloop_auth_active')
      }
      window.location.href = '/login'
    }
  } catch (e) {
    console.error(e)
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

// ─── Session Methods (Pillar 1) ──────────────────────────────────────────────
const fetchSessions = async () => {
  loadingSessions.value = true
  try {
    const res = await fetch('/api/sessions', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      exchangeSessions.value = data.sessions || []
    }
  } catch (e) {
    console.error('Error fetching sessions in chat:', e)
  } finally {
    loadingSessions.value = false
  }
}

const openBookModal = (peer, defaultSkill = '') => {
  const target = peer || activePeer.value
  if (!target) return
  bookTargetPeer.value = target
  bookForm.teacher_id = target.id || target.user_id
  const teaches = target.teaches || target.teach_skills || target.skills_offered
  const skillList = Array.isArray(teaches) ? teaches : (typeof teaches === 'string' ? teaches.split(',').map(s => s.trim()) : [])
  bookForm.skill_name = defaultSkill || (skillList.length > 0 ? skillList[0] : '')
  bookForm.duration_minutes = 30
  bookForm.scheduled_at = ''
  bookForm.topic_notes = ''
  showBookModal.value = true
}

const submitBookSession = async () => {
  if (!bookForm.teacher_id || !bookForm.skill_name.trim()) {
    alert('Please enter a skill to learn.')
    return
  }
  const cost = bookForm.duration_minutes <= 30 ? 0.5 : 1.0
  if ((currentUser.value?.time_credits || 0) < cost) {
    alert(`Insufficient Time Credits! You have ${currentUser.value?.time_credits || 0} credits, but this session requires ${cost} credits. Earn credits by teaching skills to peers!`)
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
      await Promise.all([fetchSessions(), fetchCurrentUser()])
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
      await Promise.all([fetchSessions(), fetchCurrentUser()])
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
      await Promise.all([fetchSessions(), fetchCurrentUser()])
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
      await Promise.all([fetchSessions(), fetchCurrentUser()])
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

const route = useRoute()

const fetchPeers = async () => {
  isLoadingPeers.value = true
  try {
    const res = await fetch('/api/chat/peers', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      peers.value = data.peers || []
      
      const targetId = route.query.id ? parseInt(route.query.id) : null
      const targetUser = route.query.user ? route.query.user.toString().toLowerCase() : null

      let matchedPeer = null
      if (targetId) {
        matchedPeer = peers.value.find(p => p.id === targetId)
      } else if (targetUser) {
        matchedPeer = peers.value.find(p => p.username.toLowerCase() === targetUser)
      }

      if (matchedPeer) {
        selectPeer(matchedPeer)
      } else if (peers.value.length > 0 && !activePeer.value) {
        selectPeer(peers.value[0])
      }
    }
  } catch (e) {
    console.error(e)
  } finally {
    isLoadingPeers.value = false
  }
}

// Background silent peer sync for sidebar preview and badge updates
const fetchPeersSilent = async () => {
  try {
    const res = await fetch('/api/chat/peers', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      const newPeers = data.peers || []
      for (const np of newPeers) {
        const existing = peers.value.find(p => p.id === np.id)
        if (existing) {
          existing.last_message = np.last_message
          existing.last_message_time = np.last_message_time
          existing.last_message_type = np.last_message_type
          existing.unread_count = np.unread_count
          existing.is_online = np.is_online
        } else {
          peers.value.push(np)
        }
      }
    }
  } catch (e) {
    // Ignore background polling errors
  }
}

const selectPeer = async (peer) => {
  activeGroup.value = null
  activePeer.value = peer
  peer.unread_count = 0
  await Promise.all([
    fetchMessages(peer.id),
    fetchSessions()
  ])
  fetchDeltaMessages(peer.id)
}

const fetchMessages = async (peerId) => {
  try {
    const res = await fetch(`/api/chat/messages/${peerId}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      messages.value = data.messages || []
      scrollToBottom()
    }
  } catch (e) {
    console.error(e)
  }
}

// ─── Group Chat Methods ──────────────────────────────────────────────────────
const fetchGroups = async () => {
  isLoadingGroups.value = true
  try {
    const res = await fetch('/api/chat/groups', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      groups.value = data.groups || []
    }
  } catch (e) {
    console.error('Error loading groups:', e)
  } finally {
    isLoadingGroups.value = false
  }
}

const fetchGroupsSilent = async () => {
  try {
    const res = await fetch('/api/chat/groups', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      const newGroups = data.groups || []
      for (const ng of newGroups) {
        const existing = groups.value.find(g => g.id === ng.id)
        if (existing) {
          existing.name = ng.name
          existing.member_count = ng.member_count
          existing.last_message = ng.last_message
          existing.last_message_time = ng.last_message_time
        } else {
          groups.value.push(ng)
        }
      }
    }
  } catch (e) {
    // Silent background poll error
  }
}

const selectGroup = async (group) => {
  activePeer.value = null
  activeGroup.value = group
  groupMessages.value = []
  await fetchGroupMessages(group.id)
  fetchGroupDetails(group.id)
  fetchGroupDeltaMessages(group.id)
}

const fetchGroupMessages = async (groupId) => {
  try {
    const res = await fetch(`/api/chat/groups/${groupId}/messages`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      groupMessages.value = data.messages || []
      scrollGroupToBottom()
    }
  } catch (e) {
    console.error('Error fetching group messages:', e)
  }
}

const fetchGroupDetails = async (groupId) => {
  try {
    const res = await fetch(`/api/chat/groups/${groupId}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      groupMembers.value = data.members || []
      activeGroupRole.value = data.my_role || 'member'
      if (activeGroup.value) {
        activeGroup.value.member_count = data.members ? data.members.length : activeGroup.value.member_count
      }
    }
  } catch (e) {
    console.error('Error fetching group details:', e)
  }
}

const scrollGroupToBottom = () => {
  nextTick(() => {
    if (groupMessageContainer.value) {
      groupMessageContainer.value.scrollTop = groupMessageContainer.value.scrollHeight
    }
  })
}

const getLastGroupMessageId = () => {
  if (!groupMessages.value || groupMessages.value.length === 0) return 0
  const ids = groupMessages.value
    .map(m => (typeof m.id === 'number' ? m.id : 0))
    .filter(id => id > 0)
  return ids.length > 0 ? Math.max(...ids) : 0
}

let isGroupSyncing = false
const fetchGroupDeltaMessages = async (groupId) => {
  if (!groupId || isGroupSyncing) return
  isGroupSyncing = true
  try {
    const lastId = getLastGroupMessageId()
    const res = await fetch(`/api/chat/groups/${groupId}/messages?after=${lastId}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      const newMsgs = data.messages || []
      if (newMsgs.length > 0) {
        let hasAdded = false
        for (const m of newMsgs) {
          const existingIdx = groupMessages.value.findIndex(
            x => x.id === m.id || (x.sending && x.content === m.content && x.sender_id === m.sender_id)
          )
          if (existingIdx !== -1) {
            groupMessages.value[existingIdx] = m
          } else {
            groupMessages.value.push(m)
            hasAdded = true
          }
        }
        if (hasAdded) {
          scrollGroupToBottom()
        }
        if (activeGroup.value && newMsgs[newMsgs.length - 1]) {
          const last = newMsgs[newMsgs.length - 1]
          activeGroup.value.last_message = last.content || (last.message_type === 'image' ? '[Photo]' : '[File]')
        }
      }
    }
  } catch (e) {
    // Ignore delta tick jitter
  } finally {
    isGroupSyncing = false
  }
}

const openCreateGroupModal = () => {
  newGroupName.value = ''
  newGroupDescription.value = ''
  selectedMemberIds.value = []
  showCreateGroupModal.value = true
}

const submitCreateGroup = async () => {
  if (!newGroupName.value.trim() || isSubmittingGroup.value) return
  isSubmittingGroup.value = true
  try {
    const res = await fetch('/api/chat/groups', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        name: newGroupName.value.trim(),
        description: newGroupDescription.value.trim(),
        member_ids: selectedMemberIds.value
      })
    })
    if (res.ok) {
      const data = await res.json()
      showCreateGroupModal.value = false
      await fetchGroups()
      if (data.group) {
        selectGroup(data.group)
        if (socket.value && socket.value.connected) {
          socket.value.emit('join_group_rooms', { group_id: data.group.id })
        }
      }
    } else {
      const err = await res.json().catch(() => ({}))
      alert(err.error || 'Failed to create group.')
    }
  } catch (e) {
    console.error(e)
    alert('Network error creating group.')
  } finally {
    isSubmittingGroup.value = false
  }
}

const openGroupInfoModal = async () => {
  if (!activeGroup.value) return
  showAddMemberRow.value = false
  memberToAddId.value = ''
  await fetchGroupDetails(activeGroup.value.id)
  showGroupInfoModal.value = true
}

const addMemberToGroup = async () => {
  if (!activeGroup.value || !memberToAddId.value) return
  try {
    const res = await fetch(`/api/chat/groups/${activeGroup.value.id}/members`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ user_ids: [parseInt(memberToAddId.value)] })
    })
    if (res.ok) {
      memberToAddId.value = ''
      showAddMemberRow.value = false
      await fetchGroupDetails(activeGroup.value.id)
      await fetchGroups()
    } else {
      const err = await res.json().catch(() => ({}))
      alert(err.error || 'Failed to add member.')
    }
  } catch (e) {
    console.error(e)
  }
}

const removeMemberFromGroup = async (targetUid) => {
  if (!activeGroup.value || !confirm('Are you sure you want to remove this member?')) return
  try {
    const res = await fetch(`/api/chat/groups/${activeGroup.value.id}/members/${targetUid}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (res.ok) {
      await fetchGroupDetails(activeGroup.value.id)
      await fetchGroups()
    } else {
      const err = await res.json().catch(() => ({}))
      alert(err.error || 'Failed to remove member.')
    }
  } catch (e) {
    console.error(e)
  }
}

const leaveActiveGroup = async () => {
  if (!activeGroup.value || !currentUser.value) return
  if (!confirm(`Are you sure you want to leave ${activeGroup.value.name}?`)) return
  try {
    const res = await fetch(`/api/chat/groups/${activeGroup.value.id}/members/${currentUser.value.id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    if (res.ok) {
      showGroupInfoModal.value = false
      const gid = activeGroup.value.id
      groups.value = groups.value.filter(g => g.id !== gid)
      activeGroup.value = null
      groupMessages.value = []
    } else {
      const err = await res.json().catch(() => ({}))
      alert(err.error || 'Could not leave group.')
    }
  } catch (e) {
    console.error(e)
  }
}

// ─── High-Frequency Smart Delta Sync Engine ─────────────────────────────────
let syncInterval = null
let peersInterval = null
let isSyncing = false

const getLastMessageId = () => {
  if (!messages.value || messages.value.length === 0) return 0
  const ids = messages.value
    .map(m => (typeof m.id === 'number' ? m.id : 0))
    .filter(id => id > 0)
  return ids.length > 0 ? Math.max(...ids) : 0
}

const fetchDeltaMessages = async (peerId) => {
  if (!peerId || isSyncing) return
  isSyncing = true
  try {
    const lastId = getLastMessageId()
    const res = await fetch(`/api/chat/messages/${peerId}?after=${lastId}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      const newMsgs = data.messages || []
      if (newMsgs.length > 0) {
        let hasAdded = false
        for (const m of newMsgs) {
          const existingIdx = messages.value.findIndex(
            x => x.id === m.id || (x.sending && x.content === m.content && x.sender_id === m.sender_id)
          )
          if (existingIdx !== -1) {
            messages.value[existingIdx] = m
          } else {
            messages.value.push(m)
            hasAdded = true
          }
        }
        if (hasAdded) {
          scrollToBottom()
        }
        if (activePeer.value && newMsgs[newMsgs.length - 1]) {
          const last = newMsgs[newMsgs.length - 1]
          activePeer.value.last_message = last.content || (last.message_type === 'image' ? '[Photo]' : '[File]')
        }
      }
    }
  } catch (e) {
    // Ignore delta tick network jitter
  } finally {
    isSyncing = false
  }
}

const startMessageSync = () => {
  stopMessageSync()
  // High-frequency 1-second delta sync guarantees sub-second delivery even if WebSocket is disconnected
  syncInterval = setInterval(() => {
    if (typeof document !== 'undefined' && !document.hidden) {
      if (activePeer.value?.id) {
        fetchDeltaMessages(activePeer.value.id)
      } else if (activeGroup.value?.id) {
        fetchGroupDeltaMessages(activeGroup.value.id)
      }
    }
  }, 1000)

  // Periodically refresh peers and groups list every 4 seconds for sidebar previews and unread badges
  peersInterval = setInterval(() => {
    if (typeof document !== 'undefined' && !document.hidden) {
      if (!isLoadingPeers.value) fetchPeersSilent()
      if (!isLoadingGroups.value) fetchGroupsSilent()
    }
  }, 4000)
}

const stopMessageSync = () => {
  if (syncInterval) {
    clearInterval(syncInterval)
    syncInterval = null
  }
  if (peersInterval) {
    clearInterval(peersInterval)
    peersInterval = null
  }
}

const handleWindowFocus = () => {
  if (activePeer.value?.id) {
    fetchDeltaMessages(activePeer.value.id)
  } else if (activeGroup.value?.id) {
    fetchGroupDeltaMessages(activeGroup.value.id)
  }
  fetchPeersSilent()
  fetchGroupsSilent()
}

const handleVisibilityChange = () => {
  if (typeof document !== 'undefined' && !document.hidden) {
    if (activePeer.value?.id) {
      fetchDeltaMessages(activePeer.value.id)
    } else if (activeGroup.value?.id) {
      fetchGroupDeltaMessages(activeGroup.value.id)
    }
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}

// ─── WebSocket Setup ────────────────────────────────────────────────────────
const getSocketUrl = () => {
  if (typeof window === 'undefined') return 'http://localhost:5000'
  const { protocol, hostname, port, origin } = window.location
  // When running locally on Nuxt dev server (port 3000), Flask Socket.IO is on port 5000
  if (port === '3000') {
    return `${protocol}//${hostname}:5000`
  }
  // When accessed via Ngrok or reverse proxy, traffic routes through tunnel origin
  return origin
}

const setupSocket = () => {
  const backendUrl = getSocketUrl()
  console.log('[SocketIO] Connecting to:', backendUrl)

  // Polling first connects in <30ms with zero timeout delay, then smoothly upgrades to WebSocket
  socket.value = io(backendUrl, {
    withCredentials: true,
    transports: ['polling', 'websocket'],
    upgrade: true,
    reconnection: true,
    reconnectionAttempts: 20,
    reconnectionDelay: 1000
  })

  socket.value.on('connect', () => {
    console.log('[SocketIO] Connected successfully, sid:', socket.value.id)
    if (currentUser.value?.id) {
      socket.value.emit('authenticate', { user_id: currentUser.value.id })
    }
    // Immediate delta sync on connect/reconnect to catch anything sent during transition
    if (activePeer.value?.id) {
      fetchDeltaMessages(activePeer.value.id)
    } else if (activeGroup.value?.id) {
      fetchGroupDeltaMessages(activeGroup.value.id)
    }
  })

  socket.value.on('connect_error', (err) => {
    console.warn('[SocketIO] Connection issue:', err.message)
  })

  socket.value.on('receive_message', (msg) => {
    if (!msg || !activePeer.value) return
    const isCurrentChat = (msg.sender_id === activePeer.value.id && msg.receiver_id === currentUser.value?.id) ||
                          (msg.sender_id === currentUser.value?.id && msg.receiver_id === activePeer.value.id)
    if (isCurrentChat) {
      // Deduplicate if already rendered optimistically or fetched via delta sync
      const existingIdx = messages.value.findIndex(m => m.id === msg.id || (m.sending && m.content === msg.content && m.sender_id === msg.sender_id))
      if (existingIdx !== -1) {
        messages.value[existingIdx] = msg
      } else {
        messages.value.push(msg)
      }
      scrollToBottom()
    }
    // Update last message in sidebar
    const peer = peers.value.find(p => p.id === msg.sender_id || p.id === msg.receiver_id)
    if (peer) {
      peer.last_message = msg.content || (msg.message_type === 'image' ? '[Photo]' : '[File]')
      if (activePeer.value?.id !== peer.id && msg.sender_id === peer.id) {
        peer.unread_count = (peer.unread_count || 0) + 1
      }
    }
  })

  socket.value.on('receive_group_message', (msg) => {
    if (!msg || !msg.group_id) return
    if (activeGroup.value && activeGroup.value.id === msg.group_id) {
      const existingIdx = groupMessages.value.findIndex(m => m.id === msg.id || (m.sending && m.content === msg.content && m.sender_id === msg.sender_id))
      if (existingIdx !== -1) {
        groupMessages.value[existingIdx] = msg
      } else {
        groupMessages.value.push(msg)
      }
      scrollGroupToBottom()
    }
    const grp = groups.value.find(g => g.id === msg.group_id)
    if (grp) {
      grp.last_message = msg.content || (msg.message_type === 'image' ? '[Photo]' : '[File]')
      grp.last_message_time = msg.created_at
    }
  })

  socket.value.on('group_created', (grp) => {
    if (!grp) return
    if (!groups.value.some(g => g.id === grp.id)) {
      groups.value.unshift(grp)
      if (socket.value && socket.value.connected) {
        socket.value.emit('join_group_rooms', { group_id: grp.id })
      }
    }
  })

  socket.value.on('join_group_room', ({ group_id }) => {
    if (socket.value && socket.value.connected && group_id) {
      socket.value.emit('join_group_rooms', { group_id })
    }
  })

  socket.value.on('removed_from_group', ({ group_id }) => {
    groups.value = groups.value.filter(g => g.id !== group_id)
    if (activeGroup.value && activeGroup.value.id === group_id) {
      activeGroup.value = null
      groupMessages.value = []
    }
  })

  // ─── Real-time Exchange Session Listeners (Pillar 1) ───
  socket.value.on('session_requested', (data) => {
    fetchSessions()
  })

  socket.value.on('session_accepted', (data) => {
    fetchSessions()
  })

  socket.value.on('session_rejected', (data) => {
    fetchSessions()
    fetchCurrentUser()
  })

  socket.value.on('session_cancelled', (data) => {
    fetchSessions()
    fetchCurrentUser()
  })

  socket.value.on('session_completed', (data) => {
    fetchSessions()
    fetchCurrentUser()
  })

  // Do NOT wipe queued ICE here — candidates often arrive before the ringing event.
  socket.value.on('incoming_call', async (data) => {
    incomingCall.value = data
  })

  socket.value.on('call_answered', async (data) => {
    if (peerConnection) {
      await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
      console.log('[WebRTC] Remote description set (answer)')
      await drainQueuedIce()
      callStatus.value = 'connected'
      startCallTimer()
    }
  })

  socket.value.on('ice_candidate', async (data) => {
    if (!data.candidate) return
    if (!peerConnection || !peerConnection.remoteDescription || !peerConnection.remoteDescription.type) {
      console.log('[WebRTC] Queuing ICE candidate (connection not ready)')
      pendingICECandidates.push(data.candidate)
      return
    }
    try {
      await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
      console.log('[WebRTC] Added ICE candidate')
    } catch (e) {
      console.error('[WebRTC] Error adding ICE candidate', e)
    }
  })

  socket.value.on('renegotiate', async (data) => {
    if (!peerConnection || !data.offer) return
    try {
      await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer))
      await drainQueuedIce()
      const answer = await peerConnection.createAnswer()
      await peerConnection.setLocalDescription(answer)
      await waitForIceGathering(peerConnection)
      socket.value.emit('renegotiate_answer', {
        target_user_id: data.from_user_id,
        answer: peerConnection.localDescription
      })
    } catch (e) {
      console.error('[WebRTC] renegotiate (callee) failed:', e)
    }
  })

  socket.value.on('renegotiate_answer', async (data) => {
    if (!peerConnection || !data.answer) return
    try {
      await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
      await drainQueuedIce()
    } catch (e) {
      console.error('[WebRTC] renegotiate_answer failed:', e)
    }
  })

  socket.value.on('call_ended', () => {
    endCall(true)
  })

  socket.value.on('teaching_time_recorded', (data) => {
    if (currentUser.value?.id === data.teacher_id) {
      currentUser.value.total_teaching_seconds = data.total_teaching_seconds
    } else if (currentUser.value?.id === data.learner_id) {
      currentUser.value.total_learning_seconds = data.total_learning_seconds
    }
    lastSummaryData.durationFormatted = data.duration_formatted
    lastSummaryData.teacherName = data.teacher_name
    lastSummaryData.totalTeachingFormatted = data.total_teaching_formatted
    lastSummaryData.skillName = data.skill_name
    showCallSummaryModal.value = true
  })
}

// ─── Text & Media Messaging ──────────────────────────────────────────────────
const sendMessage = async () => {
  const text = inputMessage.value.trim()
  if (!text) return
  if (!activePeer.value && !activeGroup.value) return

  const tempId = 'temp_' + Date.now()
  const now = new Date()
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  inputMessage.value = ''

  // 1. Group Message Send
  if (activeGroup.value) {
    const groupId = activeGroup.value.id
    const tempMsg = {
      id: tempId,
      group_id: groupId,
      sender_id: currentUser.value?.id,
      sender_name: currentUser.value?.full_name || currentUser.value?.username || 'You',
      sender_username: currentUser.value?.username || '',
      sender_avatar_color: currentUser.value?.avatar_color || '#543ce0',
      content: text,
      message_type: 'text',
      created_at: timeStr,
      sending: true
    }
    groupMessages.value.push(tempMsg)
    scrollGroupToBottom()

    activeGroup.value.last_message = text
    activeGroup.value.last_message_time = timeStr

    const payload = {
      group_id: groupId,
      content: text,
      message_type: 'text',
      sender_id: currentUser.value?.id
    }

    try {
      const res = await fetch('/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      })

      if (res.ok) {
        const data = await res.json()
        const confirmed = data.message
        const idx = groupMessages.value.findIndex(m => m.id === tempId)
        if (idx !== -1 && confirmed) {
          groupMessages.value[idx] = confirmed
        }
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('send_message', payload, (ack) => {
          if (ack && ack.status === 'sent') {
            const idx = groupMessages.value.findIndex(m => m.id === tempId)
            if (idx !== -1 && ack.message) {
              groupMessages.value[idx] = ack.message
            }
          }
        })
      } else {
        const errData = await res.json().catch(() => ({}))
        alert(errData.error || 'Failed to send message.')
        groupMessages.value = groupMessages.value.filter(m => m.id !== tempId)
        inputMessage.value = text
      }
    } catch (err) {
      if (socket.value && socket.value.connected) {
        socket.value.emit('send_message', payload)
      } else {
        alert('Could not deliver message. Please check your network connection.')
        groupMessages.value = groupMessages.value.filter(m => m.id !== tempId)
        inputMessage.value = text
      }
    }
    return
  }

  // 2. Direct Peer Message Send
  const receiverId = activePeer.value.id
  const tempMsg = {
    id: tempId,
    sender_id: currentUser.value?.id,
    receiver_id: receiverId,
    content: text,
    message_type: 'text',
    created_at: timeStr,
    is_read: 0,
    sending: true
  }
  messages.value.push(tempMsg)
  scrollToBottom()

  if (activePeer.value) {
    activePeer.value.last_message = text
  }

  const payload = {
    receiver_id: receiverId,
    content: text,
    message_type: 'text',
    sender_id: currentUser.value?.id
  }

  // Primary: Send via HTTP REST with guaranteed delivery
  try {
    const res = await fetch('/api/chat/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      const data = await res.json()
      const confirmed = data.message
      const idx = messages.value.findIndex(m => m.id === tempId)
      if (idx !== -1 && confirmed) {
        messages.value[idx] = confirmed
      }
    } else {
      // Fallback: emit via Socket.IO if HTTP returns non-200
      if (socket.value && socket.value.connected) {
        socket.value.emit('send_message', payload, (ack) => {
          if (ack && ack.status === 'sent') {
            const idx = messages.value.findIndex(m => m.id === tempId)
            if (idx !== -1 && ack.message) {
              messages.value[idx] = ack.message
            }
          }
        })
      } else {
        const errData = await res.json().catch(() => ({}))
        alert(errData.error || 'Failed to send message.')
        messages.value = messages.value.filter(m => m.id !== tempId)
        inputMessage.value = text
      }
    }
  } catch (err) {
    console.warn('HTTP send failed, trying Socket.IO fallback:', err)
    if (socket.value && socket.value.connected) {
      socket.value.emit('send_message', payload, (ack) => {
        if (ack && ack.status === 'sent') {
          const idx = messages.value.findIndex(m => m.id === tempId)
          if (idx !== -1 && ack.message) {
            messages.value[idx] = ack.message
          }
        }
      })
    } else {
      alert('Could not deliver message. Please check your network connection.')
      messages.value = messages.value.filter(m => m.id !== tempId)
      inputMessage.value = text
    }
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file || (!activePeer.value && !activeGroup.value)) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('/api/chat/upload', {
      method: 'POST',
      credentials: 'include',
      body: formData
    })
    if (res.ok) {
      const data = await res.json()
      const payload = {
        content: data.file_name,
        message_type: data.message_type,
        file_url: data.file_url,
        file_name: data.file_name,
        file_size: data.file_size,
        sender_id: currentUser.value?.id
      }

      if (activeGroup.value) {
        payload.group_id = activeGroup.value.id
      } else {
        payload.receiver_id = activePeer.value.id
      }

      // Send file message via HTTP
      const sendRes = await fetch('/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      })

      if (sendRes.ok) {
        const sendData = await sendRes.json()
        if (sendData.message) {
          if (activeGroup.value) {
            groupMessages.value.push(sendData.message)
            scrollGroupToBottom()
            activeGroup.value.last_message = data.file_name
          } else {
            messages.value.push(sendData.message)
            scrollToBottom()
            if (activePeer.value) {
              activePeer.value.last_message = data.file_name
            }
          }
        }
      } else if (socket.value && socket.value.connected) {
        socket.value.emit('send_message', payload)
      }
      event.target.value = ''
    } else {
      alert("Failed to upload file.")
    }
  } catch (e) {
    console.error(e)
    alert("Error uploading file.")
  }
}

const mediaDebugMsg = ref('')

// Helper: gracefully request media with fallbacks (HD video+audio -> video+audio -> video-only -> audio-only)
const requestUserMediaSafe = async () => {
  mediaDebugMsg.value = 'Starting media request...'
  if (typeof window !== 'undefined' && window.isSecureContext === false) {
    mediaDebugMsg.value = 'Error: Insecure Context (HTTP)'
    throw new Error('InsecureContextError')
  }

  // 1. Try HD video + audio
  try {
    mediaDebugMsg.value = 'Requesting HD Video + Audio...'
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 } },
      audio: { echoCancellation: true, noiseSuppression: true }
    })
    mediaDebugMsg.value = 'HD Video + Audio SUCCESS!'
    return stream
  } catch (errHD) {
    mediaDebugMsg.value = `HD Request Failed: ${errHD.name} - ${errHD.message}. Trying default...`
    // 2. Try default video + audio
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      mediaDebugMsg.value = 'Default Video + Audio SUCCESS!'
      return stream
    } catch (errFull) {
      mediaDebugMsg.value = `Default Request Failed: ${errFull.name} - ${errFull.message}. Trying Video ONLY...`
      // 3. Try Video only
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        isMicMuted.value = true
        mediaDebugMsg.value = 'Video ONLY SUCCESS! (Mic failed)'
        return stream
      } catch (errVideo) {
        mediaDebugMsg.value = `Video ONLY Failed: ${errVideo.name} - ${errVideo.message}. Trying Audio ONLY...`
        // 4. Try Audio only
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ video: false, audio: true })
          isCameraOff.value = true
          mediaDebugMsg.value = `Audio ONLY SUCCESS! Camera explicitly blocked by browser (${errFull.name}).`
          return stream
        } catch (errAudio) {
          mediaDebugMsg.value = `ALL FAILED. Final Audio Error: ${errAudio.name}`
          throw errFull
        }
      }
    }
  }
}

// ─── WebRTC Video Calling Implementation ─────────────────────────────────────
const startCall = async () => {
  if (!activePeer.value) return
  pendingICECandidates = []
  iceRetryCount = 0
  iceTransportPolicy = 'all'
  hasRecordedCall = false
  hasRemoteVideo.value = false
  isRemoteVideoMuted.value = false
  determineInitialCallRole()

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("⚠️ Camera/Microphone Blocked by Browser:\n\nPlease open this site over HTTPS or enable insecure origin flags.")
    return
  }

  try {
    await fetchTurnCredentials()
    currentCallPeerId = activePeer.value.id
    console.log('[WebRTC] Requesting local media for peer:', currentCallPeerId)
    localStream = await requestUserMediaSafe()
    console.log('[WebRTC] Got local stream:', localStream.getTracks().map(t => t.kind))

    isCallActive.value = true
    callStatus.value = 'calling'
    isCallMinimized.value = false
    await nextTick()
    attachStream(localVideoRef, localStream)

    createPeerConnection()
    localStream.getTracks().forEach(track => {
      peerConnection.addTrack(track, localStream)
    })

    isMakingOffer = true
    const offer = await peerConnection.createOffer({ offerToReceiveAudio: true, offerToReceiveVideo: true })
    await peerConnection.setLocalDescription(offer)
    await waitForIceGathering(peerConnection)
    console.log('[WebRTC] Offer ready (gathering=', peerConnection.iceGatheringState, '), emitting call_user to:', currentCallPeerId)

    socket.value.emit('call_user', {
      target_user_id: currentCallPeerId,
      offer: peerConnection.localDescription
    })
    isMakingOffer = false
  } catch (e) {
    isMakingOffer = false
    console.error('[WebRTC] Could not access camera/mic:', e)
    if (e.message === 'InsecureContextError') {
      alert("⚠️ Camera Access Blocked (Insecure Context):\n\nBrowsers block camera/mic access on HTTP networks.\n\nPlease either:\n1. Run on localhost (http://localhost:3000)\n2. Serve via HTTPS (e.g. using Cloudflare Tunnel)")
    } else if (e.name === 'NotReadableError') {
      alert("⚠️ Camera/Mic in Use:\n\nYour camera is already being used by another application (Zoom, Teams, etc.) or another open browser tab.\n\nPlease close any tabs or apps using your camera and try again.")
    } else if (e.name === 'NotAllowedError' || e.name === 'PermissionDeniedError') {
      alert("⚠️ Permission Blocked in Browser:\n\nPlease click the lock / settings icon on the left of your address bar and toggle:\n• Camera -> Allow\n• Microphone -> Allow\nThen refresh the page.")
    } else if (e.name === 'NotFoundError') {
      alert("⚠️ Device Not Found:\n\nNo camera or microphone was detected on this device.")
    } else {
      alert("Media Error (" + e.name + "): " + e.message)
    }
    endCall()
  }
}

const acceptCall = async () => {
  if (!incomingCall.value) return
  const callData = incomingCall.value
  incomingCall.value = null
  hasRecordedCall = false
  hasRemoteVideo.value = false
  isRemoteVideoMuted.value = false

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("⚠️ Camera/Microphone Blocked by Browser:\n\nPlease enable the insecure origin flag in chrome://flags or run launch-testing-browser.bat.")
    return
  }

  currentCallPeerId = callData.caller_id
  const callerPeer = peers.value.find(p => p.id === callData.caller_id)
  activePeer.value = callerPeer || { id: callData.caller_id, full_name: callData.caller_name || 'Caller' }
  determineInitialCallRole()

  try {
    await fetchTurnCredentials()
    iceRetryCount = 0
    iceTransportPolicy = 'all'
    console.log('[WebRTC] Requesting local media (accept)...')
    localStream = await requestUserMediaSafe()
    console.log('[WebRTC] Got local stream (accept):', localStream.getTracks().map(t => t.kind))

    isCallActive.value = true
    callStatus.value = 'connected'
    isCallMinimized.value = false
    startCallTimer()
    await nextTick()
    attachStream(localVideoRef, localStream)

    createPeerConnection()
    localStream.getTracks().forEach(track => {
      peerConnection.addTrack(track, localStream)
    })

    await peerConnection.setRemoteDescription(new RTCSessionDescription(callData.offer))
    console.log('[WebRTC] Remote description set (offer)')
    await drainQueuedIce()

    const answer = await peerConnection.createAnswer()
    await peerConnection.setLocalDescription(answer)
    await waitForIceGathering(peerConnection)
    console.log('[WebRTC] Answer ready, emitting answer_call to:', currentCallPeerId)

    socket.value.emit('answer_call', {
      target_user_id: currentCallPeerId,
      answer: peerConnection.localDescription
    })
  } catch (e) {
    console.error('[WebRTC] Error accepting call:', e)
    if (e.message === 'InsecureContextError') {
      alert("⚠️ Camera Access Blocked (Insecure Context):\n\nBrowsers block camera/mic access on HTTP networks.\n\nPlease either:\n1. Run on localhost (http://localhost:3000)\n2. Serve via HTTPS (e.g. using Cloudflare Tunnel)")
    } else if (e.name === 'NotReadableError') {
      alert("⚠️ Camera/Mic in Use:\n\nYour camera is already in use by another application or tab.")
    } else if (e.name === 'NotAllowedError' || e.name === 'PermissionDeniedError') {
      alert("⚠️ Permission Blocked in Browser:\n\nPlease allow Camera and Microphone in your browser address bar.")
    } else if (e.name === 'NotFoundError') {
      alert("⚠️ Device Not Found:\n\nNo camera or microphone was detected on this device.")
    } else {
      alert("Media Error (" + e.name + "): " + e.message)
    }
    endCall()
  }
}

const rejectCall = () => {
  if (incomingCall.value) {
    socket.value.emit('end_call', { target_user_id: incomingCall.value.caller_id })
    incomingCall.value = null
  }
}

const updateCallDebug = () => {
  const ice = peerConnection?.iceConnectionState || 'idle'
  const conn = peerConnection?.connectionState || 'idle'
  const rTracks = remoteStream ? remoteStream.getTracks().map(t => t.kind).join('+') : 'none'
  callDebugStatus.value = `ICE: ${ice.toUpperCase()} | Conn: ${conn.toUpperCase()} | Remote: [${rTracks || 'none'}]`
}

const createPeerConnection = () => {
  if (remoteStream) {
    remoteStream.getTracks().forEach(t => t.stop())
  }
  remoteStream = new MediaStream()

  peerConnection = new RTCPeerConnection(rtcConfig)
  console.log('[WebRTC] PeerConnection created')

  peerConnection.onicecandidate = (event) => {
    const targetId = currentCallPeerId || activePeer.value?.id
    if (event.candidate && targetId) {
      console.log('[WebRTC] Sending ICE candidate to:', targetId)
      socket.value.emit('ice_candidate', {
        target_user_id: targetId,
        candidate: event.candidate
      })
    }
  }

  peerConnection.oniceconnectionstatechange = () => {
    const state = peerConnection?.iceConnectionState || 'unknown'
    console.log('[WebRTC] ICE state:', state)
    iceConnectionStatus.value = `ICE: ${state}`
    updateCallDebug()

    if (state === 'failed' && peerConnection?.restartIce) {
      console.warn('[WebRTC] ICE failed, attempting automatic ICE restart...')
      try {
        peerConnection.restartIce()
      } catch (err) {
        console.error('[WebRTC] restartIce error:', err)
      }
    }
  }

  peerConnection.onconnectionstatechange = () => {
    const state = peerConnection?.connectionState || 'unknown'
    console.log('[WebRTC] Connection state:', state)
    if (state === 'connected') {
      callStatus.value = 'connected'
      startCallTimer()
    }
    updateCallDebug()
  }

  peerConnection.ontrack = (event) => {
    console.log('[WebRTC] Got remote track:', event.track.kind, 'id:', event.track.id)
    if (!remoteStream) {
      remoteStream = new MediaStream()
    }
    if (!remoteStream.getTracks().some(t => t.id === event.track.id)) {
      remoteStream.addTrack(event.track)
    }
    if (event.track.kind === 'video') {
      hasRemoteVideo.value = true
      event.track.onmute = () => { isRemoteVideoMuted.value = true }
      event.track.onunmute = () => { isRemoteVideoMuted.value = false }
    }
    attachStream(remoteVideoRef, remoteStream)
    updateCallDebug()
  }

  updateCallDebug()
}

const toggleMic = () => {
  if (!localStream) return
  const audioTrack = localStream.getAudioTracks()[0]
  if (audioTrack) {
    audioTrack.enabled = !audioTrack.enabled
    isMicMuted.value = !audioTrack.enabled
  }
}

const toggleCamera = () => {
  if (!localStream) return
  const videoTrack = localStream.getVideoTracks()[0]
  if (videoTrack) {
    videoTrack.enabled = !videoTrack.enabled
    isCameraOff.value = !videoTrack.enabled
  }
}

const toggleScreenShare = async () => {
  if (!isScreenSharing.value) {
    try {
      const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true })
      const screenTrack = screenStream.getVideoTracks()[0]

      const sender = peerConnection.getSenders().find(s => s.track.kind === 'video')
      if (sender) sender.replaceTrack(screenTrack)

      if (localVideoRef.value) localVideoRef.value.srcObject = screenStream
      isScreenSharing.value = true

      screenTrack.onended = () => {
        stopScreenShare()
      }
    } catch (e) {
      console.error(e)
    }
  } else {
    stopScreenShare()
  }
}

const stopScreenShare = () => {
  if (!localStream) return
  const videoTrack = localStream.getVideoTracks()[0]
  const sender = peerConnection?.getSenders().find(s => s.track.kind === 'video')
  if (sender && videoTrack) sender.replaceTrack(videoTrack)
  if (localVideoRef.value) localVideoRef.value.srcObject = localStream
  isScreenSharing.value = false
}

const endCall = async (fromRemote = false) => {
  const targetId = currentCallPeerId || activePeer.value?.id
  const finalDuration = callDurationSeconds.value
  stopCallTimer()

  if (!hasRecordedCall && finalDuration >= 5) {
    hasRecordedCall = true
    await recordTeachingSession(finalDuration)
  }

  if (targetId && socket.value && isCallActive.value && !fromRemote) {
    socket.value.emit('end_call', { target_user_id: targetId })
  }
  if (peerConnection) {
    peerConnection.close()
    peerConnection = null
  }
  if (localStream) {
    localStream.getTracks().forEach(track => track.stop())
    localStream = null
  }
  if (remoteStream) {
    remoteStream.getTracks().forEach(track => track.stop())
    remoteStream = null
  }
  currentCallPeerId = null
  pendingICECandidates = []
  isCallActive.value = false
  callStatus.value = 'idle'
  isCallMinimized.value = false
  isMicMuted.value = false
  isCameraOff.value = false
  isScreenSharing.value = false
  isAutoplayBlocked.value = false
  hasRemoteVideo.value = false
  isRemoteVideoMuted.value = false
  callDebugStatus.value = ''
}
</script>
