<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col">
    <!-- Nav -->
    <header class="bg-surface-container-low shadow-sm sticky top-0 z-40">
      <div class="flex justify-between items-center w-full px-6 py-3 max-w-7xl mx-auto">
        <NuxtLink to="/dashboard" class="font-display text-xl font-bold text-primary tracking-tight flex items-center gap-2">
          <div class="w-9 h-9 rounded-xl bg-primary text-on-primary flex items-center justify-center shadow-sm">
            <span class="material-symbols-outlined text-2xl leading-none">all_inclusive</span>
          </div>
          SkillLoop
        </NuxtLink>
        <nav class="hidden md:flex items-center space-x-6 font-headline text-sm font-semibold">
          <NuxtLink to="/dashboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Dashboard</NuxtLink>
          <NuxtLink to="/chat" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Chat &amp; Video</NuxtLink>
          <NuxtLink to="/quiz" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Quiz</NuxtLink>
          <span class="text-primary font-bold border-b-2 border-primary pb-1 whitespace-nowrap">Leaderboard</span>
          <NuxtLink to="/resume" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Resume</NuxtLink>
        </nav>
      </div>
    </header>

    <main class="flex-1 w-full max-w-5xl mx-auto px-4 py-8 space-y-8">
      <!-- Page Header -->
      <div class="text-center space-y-3">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container text-xs font-semibold uppercase tracking-wider">
          <span class="material-symbols-outlined text-sm">emoji_events</span>
          Campus Rankings
        </div>
        <h1 class="font-display text-3xl sm:text-4xl font-bold text-on-surface tracking-tight">Campus Leaderboard</h1>
        <p class="text-sm text-on-surface-variant max-w-xl mx-auto">Top performers ranked by XP, sessions completed and verified skills.</p>
      </div>

      <!-- Loading -->
      <div v-if="pending" class="text-center py-12 text-on-surface-variant">Loading leaderboard...</div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-12 text-error">{{ error }}</div>

      <!-- Top 3 Podium -->
      <div v-else-if="leaderboard.length > 0">
        <div v-if="leaderboard.length >= 3" class="grid grid-cols-3 gap-4 mb-8 items-end">
          <!-- Rank 2 (Silver) -->
          <div class="bg-surface-container-lowest rounded-3xl p-5 border-2 border-slate-200 shadow-md text-center flex flex-col items-center order-1">
            <div class="relative mb-3">
              <div class="w-16 h-16 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center font-display font-bold text-2xl">
                {{ leaderboard[1].username.charAt(0).toUpperCase() }}
              </div>
              <span class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-slate-600 text-white font-bold text-xs flex items-center justify-center">2</span>
            </div>
            <h3 class="font-headline font-bold text-on-surface text-sm">{{ leaderboard[1].username }}</h3>
            <p class="text-xs text-on-surface-variant mb-2">Level {{ leaderboard[1].level }}</p>
            <p class="font-bold text-primary text-sm">{{ leaderboard[1].xp }} XP</p>
          </div>

          <!-- Rank 1 (Gold — taller) -->
          <div class="bg-gradient-to-b from-amber-50 to-surface-container-lowest rounded-3xl p-5 border-2 border-amber-300 shadow-xl text-center flex flex-col items-center transform -translate-y-4 order-2">
            <div class="text-amber-500 mb-1">
              <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">workspace_premium</span>
            </div>
            <div class="relative mb-3">
              <div class="w-20 h-20 rounded-full bg-amber-200 text-amber-900 flex items-center justify-center font-display font-bold text-3xl ring-4 ring-amber-300">
                {{ leaderboard[0].username.charAt(0).toUpperCase() }}
              </div>
              <span class="absolute -bottom-1 -right-1 w-7 h-7 rounded-full bg-amber-500 text-white font-bold text-sm flex items-center justify-center">1</span>
            </div>
            <h3 class="font-headline font-extrabold text-on-surface text-base">{{ leaderboard[0].username }}</h3>
            <p class="text-xs text-amber-700 font-semibold mb-2">Campus Champion · Level {{ leaderboard[0].level }}</p>
            <p class="font-bold text-amber-700 text-base">{{ leaderboard[0].xp }} XP</p>
          </div>

          <!-- Rank 3 (Bronze) -->
          <div class="bg-surface-container-lowest rounded-3xl p-5 border-2 border-orange-200 shadow-md text-center flex flex-col items-center order-3">
            <div class="relative mb-3">
              <div class="w-16 h-16 rounded-full bg-orange-100 text-orange-800 flex items-center justify-center font-display font-bold text-2xl">
                {{ leaderboard[2].username.charAt(0).toUpperCase() }}
              </div>
              <span class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-orange-600 text-white font-bold text-xs flex items-center justify-center">3</span>
            </div>
            <h3 class="font-headline font-bold text-on-surface text-sm">{{ leaderboard[2].username }}</h3>
            <p class="text-xs text-on-surface-variant mb-2">Level {{ leaderboard[2].level }}</p>
            <p class="font-bold text-primary text-sm">{{ leaderboard[2].xp }} XP</p>
          </div>
        </div>

        <!-- Full Leaderboard Table -->
        <div class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm overflow-hidden">
          <div class="p-6 border-b border-surface-container flex items-center gap-3">
            <span class="material-symbols-outlined text-primary">leaderboard</span>
            <h2 class="font-headline font-bold text-on-surface">Full Rankings</h2>
            <span class="ml-auto text-xs text-on-surface-variant">{{ leaderboard.length }} students</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-surface-container text-[11px] font-headline uppercase tracking-wider text-on-surface-variant bg-surface-container-low">
                  <th class="py-3 px-5 text-center w-14">Rank</th>
                  <th class="py-3 px-5 text-left">Student</th>
                  <th class="py-3 px-5 text-center">Level</th>
                  <th class="py-3 px-5 text-center">Sessions</th>
                  <th class="py-3 px-5 text-center">Verified</th>
                  <th class="py-3 px-5 text-right pr-6">Total XP</th>
                </tr>
              </thead>
              <tbody ref="listRef" class="divide-y divide-surface-container/50">
                <tr
                  v-for="(user, index) in leaderboard"
                  :key="user.id"
                  class="hover:bg-surface-container-low/50 transition-colors"
                  :class="{
                    'bg-amber-50/40': index === 0,
                    'bg-slate-50/50': index === 1,
                    'bg-orange-50/30': index === 2
                  }"
                >
                  <td class="py-3.5 px-5 text-center">
                    <span v-if="index < 3" class="inline-flex items-center justify-center w-7 h-7 rounded-full font-headline font-extrabold text-xs"
                      :class="{
                        'bg-amber-300/50 text-amber-900 border border-amber-400': index === 0,
                        'bg-slate-200 text-slate-800 border border-slate-300': index === 1,
                        'bg-orange-100 text-orange-800 border border-orange-300': index === 2
                      }">{{ index + 1 }}</span>
                    <span v-else class="text-on-surface-variant font-semibold">#{{ index + 1 }}</span>
                  </td>
                  <td class="py-3.5 px-5">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-full bg-primary/20 text-primary flex items-center justify-center font-bold text-sm uppercase">
                        {{ user.username.charAt(0) }}
                      </div>
                      <div>
                        <p class="font-headline font-bold text-on-surface">{{ user.username }}</p>
                        <p v-if="user.full_name" class="text-xs text-on-surface-variant">{{ user.full_name }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="py-3.5 px-5 text-center">
                    <span class="px-2 py-0.5 rounded-full bg-surface-container text-on-surface-variant text-xs font-semibold">Lv {{ user.level }}</span>
                  </td>
                  <td class="py-3.5 px-5 text-center font-semibold text-on-surface">{{ user.sessions_completed }}</td>
                  <td class="py-3.5 px-5 text-center">
                    <span v-if="user.verified_skills > 0" class="inline-flex items-center gap-1 text-primary text-xs font-bold">
                      <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">verified</span>
                      {{ user.verified_skills }}
                    </span>
                    <span v-else class="text-on-surface-variant text-xs">—</span>
                  </td>
                  <td class="py-3.5 px-5 text-right pr-6 font-headline font-extrabold"
                    :class="index === 0 ? 'text-amber-700' : index === 1 ? 'text-slate-700' : index === 2 ? 'text-orange-700' : 'text-primary'">
                    {{ user.xp }} XP
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12 text-on-surface-variant">No data available yet. Start completing sessions to appear here!</div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const leaderboard = ref([])
const pending = ref(true)
const error = ref(null)
const listRef = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/leaderboard', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      leaderboard.value = data.leaderboard
    } else {
      error.value = 'Failed to load leaderboard'
    }
  } catch(e) {
    error.value = 'Server connection error'
  } finally {
    pending.value = false
  }
})
</script>
