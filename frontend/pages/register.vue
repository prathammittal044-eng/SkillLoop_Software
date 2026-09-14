<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col relative overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
    <!-- Ambient Glow -->
    <div class="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
      <div class="absolute -top-40 -right-20 w-[500px] h-[500px] bg-tertiary-container/20 rounded-full blur-[100px]"></div>
      <div class="absolute bottom-0 left-0 w-[400px] h-[400px] bg-primary-container/15 rounded-full blur-[120px]"></div>
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
        <NuxtLink to="/login" class="flex items-center gap-1.5 text-sm font-headline font-semibold text-on-surface-variant hover:text-primary transition-colors py-2 px-3.5 rounded-full hover:bg-surface-container-low">
          Already have an account? <span class="text-primary ml-1">Log In</span>
        </NuxtLink>
      </div>
    </header>

    <!-- Main Register -->
    <main class="flex-1 flex items-center justify-center px-4 py-12">
      <div class="w-full max-w-[520px]">
        <div class="bg-surface-container-lowest border border-surface-container-high/80 rounded-3xl p-8 md:p-10 shadow-xl relative">
          <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-surface-container-highest/60 border border-surface-container-high rounded-full backdrop-blur-md flex items-center gap-1.5 shadow-sm whitespace-nowrap">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span class="text-[11px] font-semibold text-secondary tracking-wide uppercase">Join the Campus Network</span>
          </div>

          <div class="text-center mt-2 mb-8">
            <h1 class="font-display text-2xl md:text-3xl font-bold text-on-surface tracking-tight">Create Your Account</h1>
            <p class="mt-2 text-sm text-on-surface-variant leading-relaxed">Start swapping skills and earning time credits with verified campus peers.</p>
          </div>

          <!-- Error -->
          <div v-if="error" class="mb-5 bg-red-50 text-red-700 p-3 rounded-xl text-sm flex items-center gap-2 border border-red-200">
            <span class="material-symbols-outlined text-base">error</span>
            {{ error }}
          </div>

          <form class="space-y-4" @submit.prevent="handleRegister">
            <!-- Full Name -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Full Name</label>
              <div class="relative focus-within:ring-2 focus-within:ring-primary rounded-2xl">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">badge</span>
                </div>
                <input
                  v-model="form.full_name"
                  class="w-full pl-10 pr-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="Your full name"
                  required
                  type="text"
                />
              </div>
            </div>
            <!-- Username -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Username</label>
              <div class="relative focus-within:ring-2 focus-within:ring-primary rounded-2xl">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">alternate_email</span>
                </div>
                <input
                  v-model="form.username"
                  class="w-full pl-10 pr-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="Choose a username"
                  required
                  type="text"
                />
              </div>
            </div>
            <!-- Email -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Campus Email</label>
              <div class="relative focus-within:ring-2 focus-within:ring-primary rounded-2xl">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">mail</span>
                </div>
                <input
                  v-model="form.email"
                  class="w-full pl-10 pr-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="you@college.edu"
                  required
                  type="email"
                />
              </div>
            </div>
            <!-- Department + Semester row -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Department</label>
                <input
                  v-model="form.department"
                  class="w-full px-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="e.g. CS, Business"
                  type="text"
                />
              </div>
              <div>
                <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Semester</label>
                <input
                  v-model.number="form.semester"
                  class="w-full px-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  min="1"
                  max="12"
                  type="number"
                />
              </div>
            </div>
            <!-- Password -->
            <div>
              <label class="block font-headline text-xs font-semibold uppercase tracking-wider text-on-surface-variant mb-1.5">Password</label>
              <div class="relative focus-within:ring-2 focus-within:ring-primary rounded-2xl">
                <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-outline">
                  <span class="material-symbols-outlined text-lg">lock</span>
                </div>
                <input
                  v-model="form.password"
                  class="w-full pl-10 pr-4 py-3 bg-surface-bright border border-surface-container-high rounded-2xl text-sm text-on-surface placeholder:text-outline/70 focus:outline-none focus:border-primary transition-colors"
                  placeholder="At least 8 characters"
                  required
                  minlength="8"
                  type="password"
                />
              </div>
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full mt-2 py-3.5 px-6 rounded-2xl bg-gradient-to-r from-primary to-secondary text-on-primary font-headline font-semibold text-sm shadow-md hover:shadow-lg hover:-translate-y-0.5 active:scale-[0.99] transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              <span>{{ loading ? 'Creating Account...' : 'Create Account' }}</span>
              <span class="material-symbols-outlined text-base">arrow_forward</span>
            </button>
          </form>

          <p class="text-center text-xs text-on-surface-variant mt-6">
            Already have an account?
            <NuxtLink class="font-headline font-semibold text-primary hover:text-primary-dim underline decoration-primary/40 underline-offset-2 transition-colors" to="/login">Log in</NuxtLink>
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = reactive({
  full_name: '',
  email: '',
  username: '',
  department: '',
  semester: 1,
  password: ''
})

const error = ref(null)
const loading = ref(false)

const handleRegister = async () => {
  error.value = null
  loading.value = true

  if (form.password.length < 8) {
    error.value = 'Password must be at least 8 characters long'
    loading.value = false
    return
  }

  try {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(form)
    })
    const data = await res.json()

    if (res.ok) {
      window.location.href = '/dashboard'
    } else {
      error.value = data.error || 'Registration failed. Please try again.'
    }
  } catch (e) {
    error.value = 'Network error. Please check your connection.'
  } finally {
    loading.value = false
  }
}
</script>
