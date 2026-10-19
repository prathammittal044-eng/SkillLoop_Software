<template>
  <div class="app-wrapper w-full min-h-screen bg-surface text-on-surface flex flex-col" :class="{ 'pb-16 md:pb-0': showMobileNav }">
    <NuxtPage />

    <!-- MOBILE BOTTOM NAVIGATION DOCK (Native App Experience) -->
    <nav
      v-if="showMobileNav"
      class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-xl border-t border-[#eaddff]/80 px-2 py-1.5 shadow-[0_-4px_20px_rgba(0,0,0,0.06)]"
    >
      <div class="flex items-center justify-around max-w-md mx-auto">
        <!-- 1. Dashboard -->
        <NuxtLink
          to="/dashboard"
          class="flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all"
          :class="route.path === '/dashboard' ? 'text-[#543ce0] font-bold scale-105' : 'text-[#6b6680] hover:text-[#1e1a2b] font-medium'"
        >
          <span
            class="material-symbols-outlined text-[22px] transition-transform"
            :style="route.path === '/dashboard' ? 'font-variation-settings: \'FILL\' 1;' : ''"
          >space_dashboard</span>
          <span class="text-[10px] mt-0.5 tracking-tight">Home</span>
        </NuxtLink>

        <!-- 2. Chat -->
        <NuxtLink
          to="/chat"
          class="flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all"
          :class="route.path === '/chat' ? 'text-[#543ce0] font-bold scale-105' : 'text-[#6b6680] hover:text-[#1e1a2b] font-medium'"
        >
          <span
            class="material-symbols-outlined text-[22px] transition-transform"
            :style="route.path === '/chat' ? 'font-variation-settings: \'FILL\' 1;' : ''"
          >chat</span>
          <span class="text-[10px] mt-0.5 tracking-tight">Chat</span>
        </NuxtLink>

        <!-- 3. Quiz -->
        <NuxtLink
          to="/quiz"
          class="flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all"
          :class="route.path === '/quiz' ? 'text-[#543ce0] font-bold scale-105' : 'text-[#6b6680] hover:text-[#1e1a2b] font-medium'"
        >
          <span
            class="material-symbols-outlined text-[22px] transition-transform"
            :style="route.path === '/quiz' ? 'font-variation-settings: \'FILL\' 1;' : ''"
          >quiz</span>
          <span class="text-[10px] mt-0.5 tracking-tight">Quiz</span>
        </NuxtLink>

        <!-- 4. Leaderboard -->
        <NuxtLink
          to="/leaderboard"
          class="flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all"
          :class="route.path === '/leaderboard' ? 'text-[#543ce0] font-bold scale-105' : 'text-[#6b6680] hover:text-[#1e1a2b] font-medium'"
        >
          <span
            class="material-symbols-outlined text-[22px] transition-transform"
            :style="route.path === '/leaderboard' ? 'font-variation-settings: \'FILL\' 1;' : ''"
          >leaderboard</span>
          <span class="text-[10px] mt-0.5 tracking-tight">Ranks</span>
        </NuxtLink>

        <!-- 5. Profile -->
        <NuxtLink
          to="/profile"
          class="flex flex-col items-center justify-center py-1 px-3 rounded-xl transition-all"
          :class="route.path === '/profile' ? 'text-[#543ce0] font-bold scale-105' : 'text-[#6b6680] hover:text-[#1e1a2b] font-medium'"
        >
          <span
            class="material-symbols-outlined text-[22px] transition-transform"
            :style="route.path === '/profile' ? 'font-variation-settings: \'FILL\' 1;' : ''"
          >person</span>
          <span class="text-[10px] mt-0.5 tracking-tight">Profile</span>
        </NuxtLink>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRuntimeConfig } from '#imports'

const route = useRoute()
const config = useRuntimeConfig()
const apiBase = (config.public?.apiBase || 'https://zoggy-skillloop-backend.hf.space').toString().trim().replace(/\/+$/, '')

// Patch window.fetch globally across all pages so relative /api/ and /uploads/ route to Hugging Face
if (typeof window !== 'undefined' && window.fetch && !window.__SKILLLOOP_FETCH_PATCHED__) {
  window.__SKILLLOOP_FETCH_PATCHED__ = true
  const originalFetch = window.fetch
  window.fetch = function (input, init) {
    if (typeof input === 'string') {
      if (input.startsWith('/api/') || input.startsWith('/uploads/')) {
        input = `${apiBase}${input}`
        init = { ...init, credentials: init?.credentials || 'include' }
      }
    } else if (input instanceof URL) {
      if (input.pathname.startsWith('/api/') || input.pathname.startsWith('/uploads/')) {
        input = new URL(input.pathname + input.search, apiBase)
        init = { ...init, credentials: init?.credentials || 'include' }
      }
    } else if (typeof Request !== 'undefined' && input instanceof Request) {
      const url = new URL(input.url)
      if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/uploads/')) {
        const targetUrl = new URL(url.pathname + url.search, apiBase)
        input = new Request(targetUrl.toString(), {
          ...input,
          credentials: input.credentials || 'include'
        })
      }
    }
    return originalFetch.call(this, input, init)
  }
}

const showMobileNav = computed(() => {
  const p = route.path
  // Hide on public landing and auth pages
  if (p === '/' || p === '/login' || p === '/register') return false
  // On chat page, let chat take 100% full screen for typing
  if (p === '/chat') return false
  return true
})

onMounted(() => {
  // Proactively wake up backend on first load and keep it warm
  const pingBackend = () => {
    try {
      fetch('/api/test', { priority: 'low' }).catch(() => {})
    } catch (e) {}
  }
  pingBackend()
  // Keep warm every 8 minutes (Render sleeps after 15 minutes)
  setInterval(pingBackend, 8 * 60 * 1000)
})
</script>

<style>
body {
  margin: 0;
  background-color: #fbf4ff;
  color: #1e1a2b;
  -webkit-tap-highlight-color: transparent;
}
</style>
