<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col justify-between relative overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
    <!-- Ambient Glow -->
    <div class="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
      <div class="absolute -top-40 -left-20 w-[550px] h-[550px] bg-primary-container/20 rounded-full blur-[110px]"></div>
      <div class="absolute top-1/4 right-0 w-[500px] h-[500px] bg-tertiary-container/15 rounded-full blur-[130px]"></div>
      <div class="absolute -bottom-32 left-1/3 w-[600px] h-[600px] bg-secondary-container/25 rounded-full blur-[140px]"></div>
      <div class="absolute top-24 left-[15%] hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-lowest/80 border border-surface-container shadow-sm backdrop-blur-md animate-bounce duration-1000">
        <span class="material-symbols-outlined text-primary text-sm" style="font-variation-settings: 'FILL' 1;">bolt</span>
        <span class="text-xs font-semibold text-on-surface">UI/UX ⇄ Python &amp; ML</span>
      </div>
      <div class="absolute bottom-28 right-[14%] hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-container-lowest/80 border border-surface-container shadow-sm backdrop-blur-md">
        <span class="text-amber-500 text-sm">✦</span>
        <span class="text-xs font-semibold text-on-surface">1 hr peer swap = 1 hr return</span>
      </div>
    </div>

    <!-- Header -->
    <header class="w-full bg-surface-bright/80 backdrop-blur-md z-40 border-b border-surface-container-high/60">
      <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <NuxtLink to="/" class="flex items-center gap-2.5 group">
          <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm group-hover:scale-105 transition-transform duration-200">
            <span class="material-symbols-outlined text-2xl font-bold">sync_alt</span>
          </div>
          <span class="font-display text-2xl font-bold tracking-tight text-primary">SkillLoop</span>
        </NuxtLink>
        <NuxtLink to="/" class="flex items-center gap-1.5 text-sm font-headline font-semibold text-on-surface-variant hover:text-primary transition-colors py-2 px-3.5 rounded-full hover:bg-surface-container-low">
          <span class="material-symbols-outlined text-base">arrow_back</span>
          <span>Back to Home</span>
        </NuxtLink>
      </div>
    </header>

    <!-- Main Login -->
    <main class="flex-1 flex items-center justify-center px-4 py-12 md:py-16">
      <div class="w-full max-w-[480px]">
        <div class="bg-surface-container-lowest border border-surface-container-high/80 rounded-3xl p-8 md:p-10 shadow-xl shadow-secondary/5 relative">
          <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-surface-container-highest/60 border border-surface-container-high rounded-full backdrop-blur-md flex items-center gap-1.5 shadow-sm">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span class="text-[11px] font-semibold text-secondary tracking-wide uppercase">Campus Peer Network</span>
          </div>
          <div class="text-center mt-2 mb-8">
            <h1 class="font-display text-2xl md:text-3xl font-bold text-on-surface tracking-tight">Welcome back to SkillLoop</h1>
            <p class="mt-2 text-sm text-on-surface-variant leading-relaxed">Log in to swap skills and earn campus karma with verified peers.</p>
          </div>

          <!-- Error Alert -->
          <div v-if="error" class="mb-5 bg-red-50 text-red-700 p-3 rounded-xl text-sm flex items-center gap-2 border border-red-200">
            <span class="material-symbols-outlined text-base">error</span>
            {{ error }}
          </div>

          <form class="space-y-5" @submit.prevent="handleLogin">
            <!-- Username -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5" for="username">Username</label>
              <div class="relative rounded-2xl transition-all duration-200 focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-1">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">person</span>
                </div>
                <input
                  id="username"
                  v-model="username"
                  class="w-full pl-10 pr-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="Enter your username"
                  required
                  type="text"
                />
              </div>
            </div>
            <!-- Password -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5" for="password">Password</label>
              <div class="relative rounded-2xl transition-all duration-200 focus-within:ring-2 focus-within:ring-primary focus-within:ring-offset-1">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">lock</span>
                </div>
                <input
                  id="password"
                  v-model="password"
                  class="w-full pl-10 pr-11 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="••••••••••••"
                  required
                  :type="showPassword ? 'text' : 'password'"
                />
                <button
                  type="button"
                  class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-outline hover:text-primary transition-colors focus:outline-none"
                  @click="showPassword = !showPassword"
                >
                  <span class="material-symbols-outlined text-lg">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
                </button>
              </div>
            </div>

            <!-- Submit -->
            <button
              type="submit"
              :disabled="loading"
              class="w-full mt-2 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-primary to-secondary text-on-primary font-headline font-semibold text-sm shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 active:scale-[0.99] transition-all duration-200 flex items-center justify-center gap-2 group disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <span>{{ loading ? 'Logging in...' : 'Login' }}</span>
              <span class="material-symbols-outlined text-base group-hover:translate-x-1 transition-transform">arrow_forward</span>
            </button>
          </form>

          <!-- Register Link -->
          <p class="text-center text-xs text-on-surface-variant mt-7">
            Don't have an account?
            <NuxtLink class="font-headline font-semibold text-primary hover:text-primary-dim underline decoration-primary/40 underline-offset-2 transition-colors" to="/register">Register here</NuxtLink>
          </p>

          <div class="mt-6 pt-5 border-t border-surface-container-high/60 flex items-center justify-center gap-2 text-center text-[11px] text-on-surface-variant font-label">
            <span class="material-symbols-outlined text-xs text-primary" style="font-variation-settings: 'FILL' 1;">verified_user</span>
            <span>Verified .edu Student Network • Zero platform fees</span>
          </div>
        </div>
      </div>
    </main>

    <footer class="w-full bg-surface-container-lowest border-t border-surface-container-high">
      <div class="max-w-7xl mx-auto px-6 py-6 flex flex-col md:flex-row items-center justify-between gap-4 font-body text-sm">
        <span class="font-display text-xl font-bold text-primary">SkillLoop</span>
        <span class="text-on-surface-variant text-xs">© 2025 SkillLoop. Built for campus peer learning.</span>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)
const showPassword = ref(false)

const handleLogin = async () => {
  error.value = null
  loading.value = true
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    const data = await res.json()
    if (res.ok) {
      window.location.href = '/dashboard'
    } else {
      error.value = data.error || 'Invalid credentials. Please try again.'
    }
  } catch (e) {
    error.value = 'Unable to connect to the server. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
