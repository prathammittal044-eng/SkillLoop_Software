<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col">

    <!-- Top Navigation (shared across all pages) -->
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
            <NuxtLink to="/dashboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5">
              <span class="material-symbols-outlined text-lg">space_dashboard</span>
              Dashboard
            </NuxtLink>
            <NuxtLink to="/chat" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">
              <span class="material-symbols-outlined text-lg">chat</span>
              Chat & Video
            </NuxtLink>
            <NuxtLink to="/quiz" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Quiz</NuxtLink>
            <NuxtLink to="/leaderboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Leaderboard</NuxtLink>
            <NuxtLink to="/resume" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">Resume</NuxtLink>
            <span class="text-primary font-bold border-b-2 border-primary pb-1 flex items-center gap-1">
              <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">person</span>
              Profile
            </span>
          </nav>
        </div>
        <div class="flex items-center gap-3">
          <div v-if="me" class="relative w-9 h-9 rounded-full text-on-primary flex items-center justify-center font-bold text-sm uppercase shadow-sm cursor-pointer" :style="avatarStyle(me)">
            <img v-if="me.profile_picture" :src="me.profile_picture" class="w-full h-full rounded-full object-cover" />
            <span v-else>{{ (me.full_name || me.username || 'U').charAt(0) }}</span>
          </div>
          <button @click="logout" class="text-xs text-on-surface-variant hover:text-error transition-colors font-semibold">Logout</button>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center space-y-3">
        <div class="w-12 h-12 rounded-full border-4 border-primary/30 border-t-primary animate-spin mx-auto"></div>
        <p class="text-on-surface-variant text-sm">Loading profile...</p>
      </div>
    </div>

    <!-- Profile Not Found -->
    <div v-else-if="notFound" class="flex-1 flex items-center justify-center">
      <div class="text-center space-y-4">
        <span class="material-symbols-outlined text-6xl text-on-surface-variant">person_off</span>
        <p class="font-headline font-bold text-xl">User not found</p>
        <NuxtLink to="/dashboard" class="px-6 py-3 rounded-xl bg-primary text-on-primary font-semibold inline-block">Back to Dashboard</NuxtLink>
      </div>
    </div>

    <!-- Main Profile Content -->
    <main v-else-if="profile" class="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 py-8 space-y-5">

      <!-- Profile Card -->
      <div class="bg-surface-container-lowest rounded-3xl overflow-hidden border border-surface-container shadow-sm">

        <!-- Banner -->
        <div class="relative h-44 overflow-hidden rounded-t-3xl" :style="bannerStyle">
          <!-- Banner Image -->
          <img v-if="profile.banner_image" :src="profile.banner_image" class="w-full h-full object-cover" />

          <!-- Visible "Change Banner" button (own profile only) -->
          <label v-if="isOwnProfile" class="absolute top-3 right-3 flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/60 hover:bg-black/80 text-white text-xs font-semibold cursor-pointer shadow-md transition-all z-20 backdrop-blur-sm">
            <span class="material-symbols-outlined text-base">photo_camera</span>
            <span>Change Banner</span>
            <input type="file" accept="image/*" class="hidden" @change="uploadBanner" :disabled="uploadingBanner" />
          </label>

          <!-- Uploading spinner -->
          <div v-if="uploadingBanner" class="absolute inset-0 flex items-center justify-center bg-black/40 z-30">
            <div class="w-8 h-8 rounded-full border-4 border-white/30 border-t-white animate-spin"></div>
          </div>
        </div>

        <!-- Avatar + Name Row -->
        <div class="px-6 pb-6 relative">
          <!-- Avatar -->
          <div class="relative -mt-12 mb-3 w-fit">
            <div class="w-24 h-24 rounded-full border-4 border-surface-container-lowest shadow-lg overflow-hidden flex items-center justify-center font-bold text-3xl text-on-primary bg-primary"
                 :style="avatarStyle(profile)">
              <img v-if="profile.profile_picture" :src="profile.profile_picture" class="w-full h-full object-cover" />
              <span v-else>{{ (profile.full_name || profile.username || 'U').charAt(0) }}</span>
            </div>
            <!-- Upload avatar button (own profile) -->
            <label v-if="isOwnProfile" class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center cursor-pointer shadow-md hover:bg-primary-dim transition-all z-20 ring-2 ring-surface-container-lowest" title="Upload profile picture">
              <span class="material-symbols-outlined text-base">photo_camera</span>
              <input type="file" accept="image/*" class="hidden" @change="uploadAvatar" :disabled="uploadingAvatar" />
            </label>
            <div v-if="uploadingAvatar" class="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center z-30">
              <div class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            </div>
          </div>

          <!-- Name, Headline, Action Buttons Row -->
          <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
            <div>
              <h1 class="font-display text-2xl font-bold text-on-surface">{{ profile.full_name || profile.username }}</h1>
              <p class="text-on-surface-variant text-sm mt-0.5">@{{ profile.username }}</p>
              <p v-if="profile.headline" class="text-on-surface text-sm mt-1 font-medium">{{ profile.headline }}</p>
            </div>

            <!-- OWN PROFILE: Edit button -->
            <div v-if="isOwnProfile" class="flex gap-2 shrink-0">
              <button v-if="!editMode" @click="startEdit"
                class="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-on-primary font-semibold text-sm hover:bg-primary-dim transition-colors shadow-sm">
                <span class="material-symbols-outlined text-base">edit</span>
                Edit Profile
              </button>
              <template v-else>
                <button @click="saveProfile" :disabled="savingProfile"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-on-primary font-semibold text-sm hover:bg-primary-dim transition-colors shadow-sm disabled:opacity-60">
                  <span class="material-symbols-outlined text-base">{{ savingProfile ? 'hourglass_empty' : 'save' }}</span>
                  {{ savingProfile ? 'Saving...' : 'Save Changes' }}
                </button>
                <button @click="cancelEdit" class="px-4 py-2 rounded-xl border border-outline-variant text-on-surface-variant text-sm font-semibold hover:bg-surface-container transition-colors">
                  Cancel
                </button>
              </template>
            </div>

            <!-- PEER PROFILE: Connect / Book / Message -->
            <div v-else class="flex flex-col gap-2 shrink-0 sm:items-end">
              <div class="flex gap-2">
                <button @click="sendConnect"
                  :disabled="connStatus !== null"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl font-semibold text-sm transition-colors shadow-sm"
                  :class="connStatus ? 'bg-surface-container text-on-surface-variant cursor-default' : 'bg-primary text-on-primary hover:bg-primary-dim'">
                  <span class="material-symbols-outlined text-base">{{ connStatus?.status === 'accepted' ? 'how_to_reg' : connStatus ? 'pending' : 'person_add' }}</span>
                  {{ connStatus?.status === 'accepted' ? 'Connected' : connStatus ? 'Pending' : 'Connect' }}
                </button>
                <button @click="goBookSession" class="flex items-center gap-2 px-4 py-2 rounded-xl border-2 border-primary text-primary font-semibold text-sm hover:bg-primary/10 transition-colors">
                  <span class="material-symbols-outlined text-base">calendar_add_on</span>
                  Book Session
                </button>
              </div>
              <NuxtLink :to="`/chat?peer=${profile.username}`" class="text-sm text-primary font-semibold flex items-center gap-1 hover:underline">
                <span class="material-symbols-outlined text-base">send</span>
                Send Message
              </NuxtLink>
            </div>
          </div>

          <!-- Stats Row -->
          <div class="flex flex-wrap gap-2 mt-4">
            <div class="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded-full text-sm font-semibold text-on-surface">
              <span class="material-symbols-outlined text-primary text-base" style="font-variation-settings: 'FILL' 1;">bolt</span>
              {{ profile.xp || 0 }} XP
            </div>
            <div class="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded-full text-sm font-semibold text-on-surface">
              <span class="material-symbols-outlined text-secondary text-base" style="font-variation-settings: 'FILL' 1;">school</span>
              {{ profile.total_sessions || 0 }} Sessions
            </div>
            <div class="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded-full text-sm font-semibold text-on-surface">
              <span class="material-symbols-outlined text-amber-500 text-base" style="font-variation-settings: 'FILL' 1;">star</span>
              {{ profile.rating_avg ? profile.rating_avg.toFixed(1) : '—' }} Rating
              <span v-if="profile.rating_count" class="text-on-surface-variant text-xs">({{ profile.rating_count }})</span>
            </div>
            <div class="flex items-center gap-1.5 bg-surface-container px-3 py-1.5 rounded-full text-sm font-semibold text-on-surface">
              <span class="material-symbols-outlined text-tertiary text-base" style="font-variation-settings: 'FILL' 1;">timer</span>
              {{ formatTime(profile.total_teaching_seconds) }} Taught
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Form (own profile only, when editing) -->
      <div v-if="isOwnProfile && editMode" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6 space-y-5">
        <h2 class="font-headline font-bold text-lg text-on-surface">Edit Profile</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Full Name</label>
            <input v-model="editForm.full_name" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Headline</label>
            <input v-model="editForm.headline" placeholder="e.g. Full Stack Dev | 3rd Sem CSE @ GGSIPU" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Department</label>
            <input v-model="editForm.department" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Semester</label>
            <input v-model="editForm.semester" type="number" min="1" max="8" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Graduation Year</label>
            <input v-model="editForm.graduation_year" type="number" min="2024" max="2035" placeholder="e.g. 2027" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">Institution</label>
            <input v-model="editForm.education" placeholder="e.g. GGSIPU, Delhi" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">About Me / Bio</label>
            <textarea v-model="editForm.bio" rows="3" maxlength="500" placeholder="Tell peers about yourself, your goals, and what you love building..." class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"></textarea>
            <p class="text-xs text-on-surface-variant text-right mt-0.5">{{ (editForm.bio || '').length }}/500</p>
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">
              <span class="material-symbols-outlined text-sm align-middle">code</span> GitHub URL
            </label>
            <input v-model="editForm.github_url" placeholder="https://github.com/yourname" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">
              <span class="material-symbols-outlined text-sm align-middle">work</span> LinkedIn URL
            </label>
            <input v-model="editForm.linkedin_url" placeholder="https://linkedin.com/in/yourname" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
          <div class="sm:col-span-2">
            <label class="block text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-1">
              <span class="material-symbols-outlined text-sm align-middle">link</span> Portfolio / Website URL
            </label>
            <input v-model="editForm.portfolio_url" placeholder="https://yourportfolio.dev" class="w-full rounded-xl border border-outline-variant bg-surface-container-low px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:ring-2 focus:ring-primary/40" />
          </div>
        </div>
        <p v-if="saveError" class="text-error text-sm font-medium">{{ saveError }}</p>
      </div>

      <!-- About Me (view mode) -->
      <div v-if="!editMode && profile.bio" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-2">About Me</h2>
        <p class="text-on-surface-variant text-sm leading-relaxed">{{ profile.bio }}</p>
      </div>

      <!-- Academic Info (view mode) -->
      <div v-if="!editMode && (profile.education || profile.department || profile.graduation_year)" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-3">Academic Info</h2>
        <dl class="grid grid-cols-2 sm:grid-cols-4 gap-y-3 text-sm">
          <div v-if="profile.department">
            <dt class="text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Department</dt>
            <dd class="text-on-surface font-medium mt-0.5">{{ profile.department }}</dd>
          </div>
          <div v-if="profile.semester">
            <dt class="text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Semester</dt>
            <dd class="text-on-surface font-medium mt-0.5">{{ profile.semester }}</dd>
          </div>
          <div v-if="profile.education">
            <dt class="text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Institution</dt>
            <dd class="text-on-surface font-medium mt-0.5">{{ profile.education }}</dd>
          </div>
          <div v-if="profile.graduation_year">
            <dt class="text-xs font-semibold text-on-surface-variant uppercase tracking-wide">Graduation</dt>
            <dd class="text-on-surface font-medium mt-0.5">{{ profile.graduation_year }}</dd>
          </div>
        </dl>
      </div>

      <!-- Skills I Teach -->
      <div v-if="(profile.teaches || []).length" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-3">Skills I Teach</h2>
        <div class="flex flex-wrap gap-2">
          <span v-for="skill in profile.teaches" :key="skill"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-semibold"
            :class="isVerified(skill) ? 'bg-primary text-on-primary' : 'bg-primary/15 text-primary'">
            <span v-if="isVerified(skill)" class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">verified</span>
            {{ skill }}
            <span v-if="isVerified(skill)" class="text-xs opacity-80 ml-0.5">· {{ getVerifiedLevel(skill) }}</span>
          </span>
        </div>
      </div>

      <!-- Skills I Want to Learn -->
      <div v-if="(profile.learns || []).length" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-3">Skills I Want to Learn</h2>
        <div class="flex flex-wrap gap-2">
          <span v-for="skill in profile.learns" :key="skill"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-outline-variant text-on-surface-variant text-sm font-semibold hover:border-primary hover:text-primary transition-colors">
            {{ skill }}
          </span>
        </div>
      </div>

      <!-- Links -->
      <div v-if="profile.github_url || profile.linkedin_url || profile.portfolio_url"
        class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-3">Links</h2>
        <div class="space-y-2.5">
          <a v-if="profile.github_url" :href="profile.github_url" target="_blank" rel="noopener"
            class="flex items-center gap-3 text-sm text-on-surface hover:text-primary transition-colors group">
            <div class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center group-hover:bg-primary/10 transition-colors">
              <span class="material-symbols-outlined text-base">code</span>
            </div>
            <span class="font-medium">{{ profile.github_url.replace('https://', '') }}</span>
            <span class="material-symbols-outlined text-sm text-on-surface-variant">open_in_new</span>
          </a>
          <a v-if="profile.linkedin_url" :href="profile.linkedin_url" target="_blank" rel="noopener"
            class="flex items-center gap-3 text-sm text-on-surface hover:text-primary transition-colors group">
            <div class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center group-hover:bg-primary/10 transition-colors">
              <span class="material-symbols-outlined text-base">work</span>
            </div>
            <span class="font-medium">{{ profile.linkedin_url.replace('https://', '') }}</span>
            <span class="material-symbols-outlined text-sm text-on-surface-variant">open_in_new</span>
          </a>
          <a v-if="profile.portfolio_url" :href="profile.portfolio_url" target="_blank" rel="noopener"
            class="flex items-center gap-3 text-sm text-on-surface hover:text-primary transition-colors group">
            <div class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center group-hover:bg-primary/10 transition-colors">
              <span class="material-symbols-outlined text-base">link</span>
            </div>
            <span class="font-medium">{{ profile.portfolio_url.replace('https://', '') }}</span>
            <span class="material-symbols-outlined text-sm text-on-surface-variant">open_in_new</span>
          </a>
        </div>
      </div>

      <!-- Reviews -->
      <div v-if="(profile.reviews || []).length" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6">
        <h2 class="font-headline font-semibold text-base text-on-surface mb-4">
          Reviews from Peers
          <span class="ml-2 text-sm font-normal text-on-surface-variant">({{ profile.reviews.length }})</span>
        </h2>
        <div class="space-y-3">
          <div v-for="review in profile.reviews" :key="review.created_at"
            class="flex gap-4 p-4 rounded-2xl bg-surface-container">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm text-on-primary shrink-0"
                 :style="{ background: review.reviewer_color || '#543ce0' }">
              {{ (review.reviewer_name || review.reviewer_username || '?').charAt(0) }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <span class="font-semibold text-sm text-on-surface">{{ review.reviewer_name || review.reviewer_username }}</span>
                <div class="flex items-center gap-0.5">
                  <span v-for="i in 5" :key="i" class="material-symbols-outlined text-base"
                    :style="{ color: i <= review.rating ? '#f59e0b' : '#d1d5db' }"
                    style="font-variation-settings: 'FILL' 1;">star</span>
                </div>
              </div>
              <p v-if="review.comment" class="text-on-surface-variant text-sm mt-1 leading-relaxed">{{ review.comment }}</p>
              <p class="text-xs text-on-surface-variant mt-1 opacity-60">
                {{ review.role === 'learner_rating_teacher' ? 'As student' : 'As teacher' }} ·
                {{ new Date(review.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty state for reviews -->
      <div v-else-if="!loading" class="bg-surface-container-lowest rounded-3xl border border-surface-container shadow-sm p-6 text-center">
        <span class="material-symbols-outlined text-4xl text-on-surface-variant opacity-40">rate_review</span>
        <p class="text-on-surface-variant text-sm mt-2">No reviews yet. Complete sessions to earn reviews!</p>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const me = ref(null)
const profile = ref(null)
const loading = ref(true)
const notFound = ref(false)
const editMode = ref(false)
const savingProfile = ref(false)
const saveError = ref(null)
const uploadingAvatar = ref(false)
const uploadingBanner = ref(false)

const editForm = ref({
  full_name: '',
  headline: '',
  department: '',
  semester: '',
  education: '',
  graduation_year: '',
  bio: '',
  github_url: '',
  linkedin_url: '',
  portfolio_url: ''
})

// Are we viewing our own profile?
const targetUsername = computed(() => route.query.u || null)
const isOwnProfile = computed(() => !targetUsername.value || (me.value && me.value.username === targetUsername.value))

const connStatus = computed(() => profile.value?.connection_status || null)

const bannerGradients = [
  'linear-gradient(135deg, #543ce0 0%, #99366c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
]

const bannerStyle = computed(() => {
  if (profile.value?.banner_image) return {}
  const idx = profile.value ? (profile.value.id || 0) % bannerGradients.length : 0
  return { background: bannerGradients[idx] }
})

function avatarStyle(user) {
  if (!user) return {}
  if (user.profile_picture) return {}
  return { background: user.avatar_color || '#543ce0' }
}

function formatTime(seconds) {
  if (!seconds) return '0m'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  if (h > 0) return `${h}h ${m}m`
  return `${m}m`
}

function isVerified(skillName) {
  return (profile.value?.verified_skills || []).some(v =>
    v.skill_name.toLowerCase() === skillName.toLowerCase()
  )
}

function getVerifiedLevel(skillName) {
  const v = (profile.value?.verified_skills || []).find(v =>
    v.skill_name.toLowerCase() === skillName.toLowerCase()
  )
  return v ? v.verified_level : ''
}

async function fetchMe() {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      me.value = data.user
    }
  } catch {}
}

async function fetchProfile() {
  const username = targetUsername.value || me.value?.username
  if (!username) { notFound.value = true; loading.value = false; return }

  try {
    const res = await fetch(`/api/user/${username}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      profile.value = data.profile
    } else {
      notFound.value = true
    }
  } catch {
    notFound.value = true
  } finally {
    loading.value = false
  }
}

function startEdit() {
  const p = profile.value
  editForm.value = {
    full_name: p.full_name || '',
    headline: p.headline || '',
    department: p.department || '',
    semester: p.semester || '',
    education: p.education || '',
    graduation_year: p.graduation_year || '',
    bio: p.bio || '',
    github_url: p.github_url || '',
    linkedin_url: p.linkedin_url || '',
    portfolio_url: p.portfolio_url || ''
  }
  editMode.value = true
  saveError.value = null
}

function cancelEdit() {
  editMode.value = false
  saveError.value = null
}

async function saveProfile() {
  savingProfile.value = true
  saveError.value = null
  try {
    const res = await fetch('/api/user/me', {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm.value)
    })
    if (res.ok) {
      // Refresh profile data
      Object.assign(profile.value, editForm.value)
      editMode.value = false
    } else {
      const data = await res.json()
      saveError.value = data.error || 'Failed to save. Please try again.'
    }
  } catch {
    saveError.value = 'Network error. Please try again.'
  } finally {
    savingProfile.value = false
  }
}

async function uploadAvatar(event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploadingAvatar.value = true
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await fetch('/api/user/upload-avatar', { method: 'POST', credentials: 'include', body: form })
    const data = await res.json()
    if (res.ok) {
      profile.value.profile_picture = data.url + '?t=' + Date.now()
      if (me.value) me.value.profile_picture = profile.value.profile_picture
    } else {
      alert(data.error || 'Failed to upload profile picture.')
    }
  } catch (e) {
    alert('Network error while uploading profile picture. Is the server running?')
  } finally {
    uploadingAvatar.value = false
    event.target.value = ''
  }
}

async function uploadBanner(event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploadingBanner.value = true
  const form = new FormData()
  form.append('file', file)
  try {
    const res = await fetch('/api/user/upload-banner', { method: 'POST', credentials: 'include', body: form })
    const data = await res.json()
    if (res.ok) {
      profile.value.banner_image = data.url + '?t=' + Date.now()
    } else {
      alert(data.error || 'Failed to upload banner image.')
    }
  } catch (e) {
    alert('Network error while uploading banner. Is the server running?')
  } finally {
    uploadingBanner.value = false
    event.target.value = ''
  }
}


async function sendConnect() {
  if (!profile.value || connStatus.value) return
  try {
    const res = await fetch('/api/connect', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ receiver_username: profile.value.username })
    })
    if (res.ok) {
      profile.value.connection_status = { status: 'pending', i_sent: true }
    }
  } catch {}
}

function goBookSession() {
  router.push(`/dashboard?book=${profile.value.username}`)
}

async function logout() {
  try { await fetch('/api/logout', { method: 'POST', credentials: 'include' }) } catch {}
  if (typeof localStorage !== 'undefined') localStorage.removeItem('skillloop_auth_active')
  window.location.href = '/login'
}

onMounted(async () => {
  await fetchMe()
  await fetchProfile()
})
</script>
