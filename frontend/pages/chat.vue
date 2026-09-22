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

          <NuxtLink to="/login" class="text-xs text-on-surface-variant hover:text-error transition-colors font-semibold whitespace-nowrap">
            Logout
          </NuxtLink>
        </div>
      </div>
    </header>

    <!-- MAIN TWO-COLUMN WORKSPACE -->
    <main class="flex-1 max-w-[1720px] w-full mx-auto p-3 sm:p-5 flex gap-4 min-h-0 overflow-hidden">
      <!-- LEFT SIDEBAR: PEER CONVERSATIONS -->
      <aside class="w-full md:w-[360px] lg:w-[380px] bg-white rounded-2xl border border-[#eaddff] flex flex-col h-full overflow-hidden shadow-sm flex-shrink-0">
        <!-- Search & Filter Bar -->
        <div class="p-4 border-b border-[#eaddff]/70 space-y-3 bg-gradient-to-b from-[#fdfaff] to-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="font-headline font-bold text-lg text-[#1e1a2b]">Loop Partners</h2>
              <span class="px-2 py-0.5 rounded-full text-[11px] font-bold bg-[#543ce0]/10 text-[#543ce0]">{{ peers.length }} Connected</span>
            </div>
          </div>
          <!-- Search input -->
          <div class="relative">
            <span class="material-symbols-outlined absolute left-3 top-2.5 text-[#6b6680] text-lg">search</span>
            <input
              v-model="searchQuery"
              class="w-full pl-9 pr-4 py-2 bg-[#f6effe]/70 border border-[#eaddff] rounded-xl text-xs font-medium placeholder-[#6b6680]/70 focus:outline-none focus:ring-2 focus:ring-[#543ce0]/20 focus:border-[#543ce0] transition-all"
              placeholder="Search connected partners..."
              type="text"
            />
          </div>
        </div>

        <!-- Peer List (Scrollable) -->
        <div class="flex-1 overflow-y-auto divide-y divide-[#eaddff]/40 p-2 space-y-1 flex flex-col">
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
            :class="activePeer?.id === peer.id ? 'bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#543ce0]/30 shadow-sm' : 'hover:bg-[#f6effe]/60 border border-transparent'"
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
            <div v-if="activePeer?.id === peer.id" class="absolute left-0 top-3 bottom-3 w-1 bg-[#543ce0] rounded-r-full"></div>
          </div>
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
              <!-- Test Camera & Mic Button -->
              <button
                @click="testMediaDevices"
                :disabled="isCallActive"
                class="px-4 py-2 rounded-xl bg-white border border-[#eaddff] hover:bg-[#f6effe] text-[#543ce0] text-xs font-bold font-headline flex items-center gap-2 shadow-sm transition-all transform hover:-translate-y-0.5 active:scale-95 disabled:opacity-50"
                title="Test Camera and Microphone before calling"
              >
                <span class="material-symbols-outlined text-base">settings_video_camera</span>
                <span class="hidden sm:inline">Test Setup</span>
              </button>

              <!-- Start Video Call Button -->
              <button
                @click="startCall"
                :disabled="isCallActive"
                class="px-4 py-2 rounded-xl bg-[#543ce0] hover:bg-[#432dbb] text-white text-xs font-bold font-headline flex items-center gap-2 shadow-md shadow-[#543ce0]/25 transition-all transform hover:-translate-y-0.5 active:scale-95 disabled:opacity-50"
              >
                <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">videocam</span>
                <span>Start Video Call</span>
              </button>
            </div>
          </header>

          <!-- 2. SCROLLABLE MESSAGES FEED -->
          <div ref="messageContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-gradient-to-b from-[#fdfaff]/60 via-[#fbf4ff]/30 to-[#fdfaff]">
            <!-- Peer Escrow Banner -->
            <div class="max-w-xl mx-auto p-3 bg-gradient-to-r from-[#f6effe] to-[#fbf4ff] border border-[#eaddff] rounded-2xl flex items-center gap-3 text-xs shadow-xs">
              <div class="w-9 h-9 rounded-xl bg-white border border-[#eaddff] flex items-center justify-center text-[#543ce0] flex-shrink-0 shadow-xs">
                <span class="material-symbols-outlined text-xl" style="font-variation-settings: 'FILL' 1;">lock_clock</span>
              </div>
              <div class="flex-1">
                <p class="font-bold text-[#1e1a2b]">SkillLoop Direct Exchange Channel</p>
                <p class="text-[#6b6680]">Messages and video calls are direct peer-to-peer and verified on your campus node.</p>
              </div>
              <span class="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[10px] font-extrabold rounded-full">Encrypted</span>
            </div>

            <div v-if="messages.length === 0" class="text-center py-12 text-xs text-[#6b6680]">
              No messages yet with {{ activePeer.full_name }}. Send a note or launch a video call!
            </div>

            <!-- Messages List -->
            <template v-for="msg in messages" :key="msg.id">
              <!-- Outgoing message (Current User) -->
              <div v-if="msg.sender_id === currentUser.id" class="flex items-end justify-end gap-2.5 max-w-lg ml-auto">
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

        <!-- No Peer Selected State -->
        <div v-else class="flex-1 flex items-center justify-center text-center p-6 space-y-3">
          <div class="w-16 h-16 rounded-2xl bg-[#f6effe] text-[#543ce0] flex items-center justify-center mx-auto shadow-xs">
            <span class="material-symbols-outlined text-3xl">chat</span>
          </div>
          <div>
            <h3 class="font-headline font-bold text-base text-[#1e1a2b]">Select a peer to start messaging</h3>
            <p class="text-xs text-[#6b6680] mt-1">Choose any connected peer from the left sidebar to exchange notes or start a video call.</p>
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

        <!-- 5. FLOATING PICTURE-IN-PICTURE / ACTIVE VIDEO CALL OVERLAY -->
        <div v-if="isCallActive" class="absolute top-18 right-5 w-96 sm:w-[460px] bg-slate-900 rounded-2xl shadow-2xl border-2 border-white/90 overflow-hidden z-30 transition-all">
          <!-- Video Feeds Container -->
          <div class="relative h-64 sm:h-72 w-full bg-slate-950 flex items-center justify-center overflow-hidden">
            <!-- Remote Peer Video -->
            <video ref="remoteVideoRef" autoplay playsinline class="w-full h-full object-cover"></video>

            <!-- Autoplay Unlock Overlay (For Brave / Chrome autoplay policy) -->
            <div
              v-if="isAutoplayBlocked"
              @click="resumeRemoteVideo"
              class="absolute inset-0 bg-black/85 backdrop-blur-sm flex flex-col items-center justify-center p-4 text-center cursor-pointer z-40 transition-all hover:bg-black/75"
            >
              <div class="w-14 h-14 rounded-full bg-[#543ce0] text-white flex items-center justify-center mb-3 animate-pulse shadow-lg shadow-[#543ce0]/50">
                <span class="material-symbols-outlined text-3xl">play_arrow</span>
              </div>
              <p class="font-bold text-sm text-white font-headline">Click here to enable video & audio</p>
              <p class="text-[11px] text-white/70 mt-1">Brave/Chrome requires one click to allow live remote playback</p>
            </div>

            <!-- Video Header Badges -->
            <div class="absolute top-3 left-3 right-3 flex items-center justify-between pointer-events-none z-20">
              <div class="flex items-center gap-2 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/10 text-white text-xs font-semibold">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
                </span>
                <span>Live Exchange</span>
                <span class="text-white/40">|</span>
                <span class="text-[#c084fc] font-bold">{{ activePeer?.full_name || 'Peer' }}</span>
              </div>
              <div class="flex items-center gap-1.5 bg-black/60 backdrop-blur-md px-2.5 py-1 rounded-full border border-white/10 text-white text-[10px] font-medium">
                <span class="material-symbols-outlined text-xs text-emerald-400" style="font-variation-settings: 'FILL' 1;">verified_user</span>
                <span>{{ iceConnectionStatus || 'P2P WebRTC' }}</span>
              </div>
            </div>

            <!-- Self Preview (Bottom-Right corner) -->
            <div class="absolute bottom-16 right-3 w-28 h-20 rounded-xl overflow-hidden border-2 border-white shadow-lg bg-slate-800 z-20">
              <video ref="localVideoRef" autoplay playsinline muted class="w-full h-full object-cover"></video>
              <div class="absolute bottom-1 left-1.5 text-[9px] font-bold text-white bg-black/60 px-1 py-0.5 rounded">
                You {{ isMicMuted ? '(Muted)' : '' }}
              </div>
            </div>

            <!-- Controls (Bottom Floating Bar) -->
            <div class="absolute bottom-3 left-3 right-3 flex items-center justify-center gap-2.5 bg-black/75 backdrop-blur-xl py-2 px-4 rounded-2xl border border-white/15 shadow-xl z-20">
              <!-- Mic Mute/Unmute -->
              <button
                @click="toggleMic"
                class="w-9 h-9 rounded-full flex items-center justify-center transition-all active:scale-90"
                :class="isMicMuted ? 'bg-rose-600 text-white' : 'bg-white/20 hover:bg-white/30 text-white'"
                :title="isMicMuted ? 'Unmute Mic' : 'Mute Mic'"
              >
                <span class="material-symbols-outlined text-lg">{{ isMicMuted ? 'mic_off' : 'mic' }}</span>
              </button>

              <!-- Camera On/Off -->
              <button
                @click="toggleCamera"
                class="w-9 h-9 rounded-full flex items-center justify-center transition-all active:scale-90"
                :class="isCameraOff ? 'bg-rose-600 text-white' : 'bg-white/20 hover:bg-white/30 text-white'"
                :title="isCameraOff ? 'Turn Camera On' : 'Turn Camera Off'"
              >
                <span class="material-symbols-outlined text-lg">{{ isCameraOff ? 'videocam_off' : 'videocam' }}</span>
              </button>

              <!-- Screen Share -->
              <button
                @click="toggleScreenShare"
                class="w-9 h-9 rounded-full flex items-center justify-center transition-all active:scale-90"
                :class="isScreenSharing ? 'bg-emerald-600 text-white' : 'bg-white/20 hover:bg-white/30 text-white'"
                title="Share Screen"
              >
                <span class="material-symbols-outlined text-lg">present_to_all</span>
              </button>

              <div class="h-5 w-px bg-white/20 mx-0.5"></div>

              <!-- End Call Button -->
              <button
                @click="endCall"
                class="h-9 px-4 rounded-full bg-rose-600 hover:bg-rose-700 text-white text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-rose-600/40 transition-all active:scale-90"
                title="End Call"
              >
                <span class="material-symbols-outlined text-base" style="font-variation-settings: 'FILL' 1;">call_end</span>
                <span>End Call</span>
              </button>
            </div>
            
            <!-- DEBUG STATUS STRIP -->
            <div v-if="callDebugStatus" class="absolute top-12 left-3 right-3 bg-black/75 backdrop-blur-md text-amber-300 text-[10px] font-mono py-1 px-2.5 rounded-lg border border-amber-400/30 z-20 text-center pointer-events-none">
              {{ callDebugStatus }}
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { io } from 'socket.io-client'

const currentUser = ref(null)
const peers = ref([])
const activePeer = ref(null)
const messages = ref([])
const inputMessage = ref('')
const searchQuery = ref('')
const isLoadingPeers = ref(true)
const messageContainer = ref(null)

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

onMounted(async () => {
  await fetchCurrentUser()
  await fetchPeers()
  await fetchTurnCredentials()
  setupSocket()
})

onUnmounted(() => {
  endCall()
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
      window.location.href = '/login'
    }
  } catch (e) {
    console.error(e)
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

const selectPeer = async (peer) => {
  activePeer.value = peer
  peer.unread_count = 0
  await fetchMessages(peer.id)
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

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    }
  })
}

// ─── WebSocket Setup ────────────────────────────────────────────────────────
const setupSocket = () => {
  // Same-origin so Flask session cookies always ride with signaling.
  const backendUrl = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:3000'

  socket.value = io(backendUrl, {
    withCredentials: true,
    transports: ['websocket', 'polling'],
    upgrade: true
  })

  socket.value.on('receive_message', (msg) => {
    if (activePeer.value && (msg.sender_id === activePeer.value.id || msg.receiver_id === activePeer.value.id)) {
      messages.value.push(msg)
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

  // Do NOT wipe queued ICE here — candidates often arrive before the ringing event.
  socket.value.on('incoming_call', async (data) => {
    incomingCall.value = data
  })

  socket.value.on('call_answered', async (data) => {
    if (peerConnection) {
      await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
      console.log('[WebRTC] Remote description set (answer)')
      await drainQueuedIce()
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
}

// ─── Text & Media Messaging ──────────────────────────────────────────────────
const sendMessage = () => {
  if (!inputMessage.value.trim() || !activePeer.value || !socket.value) return

  const payload = {
    receiver_id: activePeer.value.id,
    content: inputMessage.value.trim(),
    message_type: 'text'
  }

  socket.value.emit('send_message', payload)
  inputMessage.value = ''
}

const handleFileUpload = async (event) => {
  const file = event.target.files?.[0]
  if (!file || !activePeer.value) return

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
      socket.value.emit('send_message', {
        receiver_id: activePeer.value.id,
        content: data.file_name,
        message_type: data.message_type,
        file_url: data.file_url,
        file_name: data.file_name,
        file_size: data.file_size
      })
      event.target.value = ''
    } else {
      alert("Failed to upload file.")
    }
  } catch (e) {
    console.error(e)
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

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert("⚠️ Camera/Microphone Blocked by Browser:\n\nPlease enable the insecure origin flag in chrome://flags or run launch-testing-browser.bat.")
    return
  }

  currentCallPeerId = callData.caller_id
  const callerPeer = peers.value.find(p => p.id === callData.caller_id)
  activePeer.value = callerPeer || { id: callData.caller_id, full_name: callData.caller_name || 'Caller' }

  try {
    await fetchTurnCredentials()
    iceRetryCount = 0
    iceTransportPolicy = 'all'
    console.log('[WebRTC] Requesting local media (accept)...')
    localStream = await requestUserMediaSafe()
    console.log('[WebRTC] Got local stream (accept):', localStream.getTracks().map(t => t.kind))

    isCallActive.value = true
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

const endCall = () => {
  const targetId = currentCallPeerId || activePeer.value?.id
  if (targetId && socket.value && isCallActive.value) {
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
  isMicMuted.value = false
  isCameraOff.value = false
  isScreenSharing.value = false
  isAutoplayBlocked.value = false
  callDebugStatus.value = ''
}
</script>
