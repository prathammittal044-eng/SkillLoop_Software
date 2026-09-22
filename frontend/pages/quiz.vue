<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col select-none" :class="{ 'no-copy-quiz': phase === 'quiz' }" @contextmenu="handleContextMenu">
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
          <span class="text-primary font-bold border-b-2 border-primary pb-1 whitespace-nowrap">Quiz</span>
          <NuxtLink to="/leaderboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Leaderboard</NuxtLink>
          <NuxtLink to="/resume" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">Resume</NuxtLink>
        </nav>
      </div>
    </header>

    <!-- ANTI-CHEAT SECURITY TOAST (Copy / Shortcut attempt) -->
    <transition name="slide-fade">
      <div v-if="cheatToast" class="fixed top-20 left-1/2 -translate-x-1/2 z-[100] px-5 py-3 rounded-2xl bg-slate-900/95 text-white border-2 border-red-500 shadow-2xl flex items-center gap-3 backdrop-blur-md animate-pulse">
        <span class="material-symbols-outlined text-red-400 text-2xl">security</span>
        <div>
          <p class="font-headline font-bold text-xs text-red-400">Anti-Cheat Action Blocked</p>
          <p class="text-[11px] text-white/90">{{ cheatToast }}</p>
        </div>
      </div>
    </transition>

    <!-- ANTI-CHEAT FULLSCREEN LOCKDOWN OVERLAY (Window blur / Tab switch / Overlay detected) -->
    <transition name="fade">
      <div v-if="isWindowBlurred && phase === 'quiz' && !autoFailed" class="fixed inset-0 z-[150] bg-slate-950/85 backdrop-blur-xl flex flex-col items-center justify-center p-6 text-center text-white">
        <div class="w-20 h-20 rounded-3xl bg-red-600/20 text-red-500 border border-red-500/40 flex items-center justify-center mb-6 shadow-2xl shadow-red-500/20 animate-bounce">
          <span class="material-symbols-outlined text-4xl">screen_lock_portrait</span>
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/20 text-red-400 text-xs font-bold uppercase tracking-wider mb-3">
          Anti-Cheat Violation Detected
        </div>
        <h2 class="font-headline font-extrabold text-2xl sm:text-3xl mb-3 text-white">Window Focus Lost!</h2>
        <p class="text-sm text-slate-300 max-w-md mb-2 leading-relaxed">
          Another window overlay, alt-tab, or tab switch was detected by the exam proctor.
        </p>
        <p class="text-xs font-bold text-red-400 mb-6 px-3 py-1.5 rounded-xl bg-red-950/60 border border-red-800">
          Strike {{ tabSwitches }} of {{ MAX_TAB_SWITCHES }} allowed. Further violations will immediately auto-fail this quiz.
        </p>
        <button
          @click="dismissFocusWarning"
          class="px-8 py-3.5 rounded-2xl bg-red-600 hover:bg-red-700 text-white font-headline font-bold text-sm shadow-xl shadow-red-600/40 active:scale-95 transition-all flex items-center gap-2"
        >
          <span class="material-symbols-outlined text-lg">verified</span>
          <span>I Understand — Return to Quiz</span>
        </button>
      </div>
    </transition>

    <main class="flex-1 w-full max-w-3xl mx-auto px-4 py-8">

      <!-- AUTO-FAIL Warning Banner -->
      <div v-if="autoFailed" class="mb-6 p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700 flex items-center gap-3">
        <span class="material-symbols-outlined text-2xl">warning</span>
        <div>
          <p class="font-bold">Quiz Auto-Failed</p>
          <p class="text-sm">Too many focus losses or tab switches detected. Submitting test now...</p>
        </div>
      </div>

      <!-- PHASE 1: SELECT SKILL -->
      <div v-if="phase === 'select'" class="space-y-8">
        <div class="text-center space-y-3">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container text-xs font-semibold uppercase tracking-wider">
            <span class="material-symbols-outlined text-sm">verified_user</span>
            Campus Skill Verification
          </div>
          <h1 class="font-display text-3xl sm:text-4xl font-bold text-on-surface tracking-tight">Skill Verification Quiz</h1>
          <p class="text-sm text-on-surface-variant max-w-xl mx-auto">Pass the verification quiz to earn your verified badge and XP. Anti-cheat monitoring and individual question timers are active.</p>
        </div>

        <div v-if="loading" class="text-center text-on-surface-variant py-8">Loading your skills...</div>

        <div v-else-if="teachSkills.length === 0" class="text-center py-8 space-y-4">
          <span class="material-symbols-outlined text-5xl text-on-surface-variant">psychology_alt</span>
          <p class="text-on-surface-variant">You haven't added any skills to teach yet.</p>
          <NuxtLink to="/dashboard" class="px-6 py-3 rounded-xl bg-primary text-on-primary font-semibold inline-block hover:bg-primary-dim transition-colors">Go Add Skills</NuxtLink>
        </div>

        <div v-else class="space-y-6">
          <!-- Skill Selection -->
          <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm">
            <h2 class="font-headline font-bold text-on-surface mb-4">1. Select a Skill to Verify</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                v-for="skill in teachSkills"
                :key="skill.id"
                @click="selectSkill(skill.name)"
                class="p-4 rounded-2xl border-2 text-left transition-all duration-200 hover:shadow-md"
                :class="selectedSkill === skill.name ? 'border-primary bg-primary/5' : 'border-surface-container-high bg-surface-bright hover:border-primary/40'"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <span class="font-headline font-bold text-on-surface block">{{ skill.name }}</span>
                    <span v-if="getVerifiedInfo(skill.name)" class="text-[11px]">
                      <span v-if="getVerifiedInfo(skill.name).decay_status === 'active'" class="text-emerald-700 font-semibold">
                        ● Active • {{ getVerifiedInfo(skill.name).days_remaining }}d left
                      </span>
                      <span v-else-if="getVerifiedInfo(skill.name).decay_status === 'expiring_soon'" class="text-amber-700 font-semibold">
                        ▲ Expiring in {{ getVerifiedInfo(skill.name).days_remaining }}d
                      </span>
                      <span v-else class="text-slate-500 font-semibold">
                        ○ Decayed • Retake to Revive
                      </span>
                    </span>
                  </div>
                  <span v-if="getVerifiedInfo(skill.name)" class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase"
                    :class="getVerifiedInfo(skill.name).is_active ? 'bg-primary/10 text-primary' : 'bg-surface-container text-on-surface-variant'">
                    {{ getVerifiedInfo(skill.name).verified_level }}
                  </span>
                </div>
              </button>
            </div>
          </div>

          <!-- Difficulty Selection -->
          <div v-if="selectedSkill" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm diff-options">
            <h2 class="font-headline font-bold text-on-surface mb-1">2. Choose Difficulty</h2>
            <p class="text-xs text-on-surface-variant mb-4">Higher difficulty = More XP earned</p>
            <div class="space-y-3">
              <button
                v-for="diff in ['beginner', 'intermediate', 'advanced']"
                :key="diff"
                @click="startQuiz(diff)"
                :disabled="loadingQuiz"
                class="w-full p-4 rounded-2xl border-2 border-surface-container-high bg-surface-bright hover:border-primary hover:bg-primary/5 text-left transition-all group flex items-center justify-between disabled:opacity-50"
              >
                <div>
                  <div class="font-headline font-bold text-on-surface capitalize">{{ diff }}</div>
                  <div class="text-xs text-on-surface-variant">
                    <span v-if="diff === 'beginner'">5 questions • Basic concepts • 20s per question</span>
                    <span v-if="diff === 'intermediate'">7 questions • Applied knowledge • 15s per question</span>
                    <span v-if="diff === 'advanced'">7 questions • Expert level • 10s per question</span>
                  </div>
                </div>
                <div class="text-right">
                  <span class="font-bold text-primary text-sm">
                    <span v-if="diff === 'beginner'">+15 XP</span>
                    <span v-if="diff === 'intermediate'">+35 XP</span>
                    <span v-if="diff === 'advanced'">+75 XP</span>
                  </span>
                  <span class="material-symbols-outlined text-sm text-on-surface-variant ml-2 group-hover:text-primary transition-colors">arrow_forward</span>
                </div>
              </button>
            </div>
            <p v-if="loadingQuiz" class="text-center text-primary text-sm mt-4 animate-pulse">Generating anti-cheat verified questions...</p>
          </div>
        </div>

        <!-- History -->
        <div v-if="history.length > 0" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm">
          <h2 class="font-headline font-bold text-on-surface mb-4">Recent Attempts</h2>
          <div class="space-y-3">
            <div v-for="attempt in history.slice(0, 5)" :key="attempt.id" class="flex items-center justify-between p-3 rounded-2xl bg-surface-container-low border border-surface-container">
              <div>
                <p class="font-semibold text-sm text-on-surface">{{ attempt.skill_name }}</p>
                <p class="text-xs text-on-surface-variant capitalize">{{ attempt.difficulty }} • {{ attempt.score }}/{{ attempt.total }} correct</p>
              </div>
              <div class="text-right">
                <span class="text-xs font-bold" :class="attempt.passed ? 'text-green-600' : 'text-red-500'">{{ attempt.passed ? '✓ Passed' : '✗ Failed' }}</span>
                <p class="text-xs text-on-surface-variant">+{{ attempt.xp_earned }} XP</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- PHASE 2: ACTIVE QUIZ -->
      <div v-else-if="phase === 'quiz'" class="space-y-5">

        <!-- Question Navigation Grid Pills -->
        <div class="bg-surface-container-lowest rounded-2xl p-3.5 border border-surface-container shadow-xs flex items-center justify-between gap-2 overflow-x-auto">
          <div class="flex items-center gap-1.5">
            <button
              v-for="(q, idx) in questions"
              :key="idx"
              @click="goToQuestion(idx)"
              class="w-8 h-8 rounded-xl font-headline font-bold text-xs transition-all flex items-center justify-center shrink-0"
              :class="[
                currentQ === idx ? 'ring-2 ring-primary ring-offset-1 font-extrabold' : '',
                userAnswers[idx] !== -1 ? 'bg-primary text-on-primary' : (questionTimesLeft[idx] <= 0 ? 'bg-red-100 text-red-700' : 'bg-surface-container text-on-surface-variant hover:bg-surface-container-high')
              ]"
              :title="`Question ${idx + 1} (${questionTimesLeft[idx]}s remaining)`"
            >
              {{ idx + 1 }}
            </button>
          </div>
          <div class="flex items-center gap-3 text-xs shrink-0 pl-2">
            <span class="text-on-surface-variant flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-primary inline-block"></span> Answered
            </span>
            <span class="text-on-surface-variant flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-red-500 inline-block"></span> Expired
            </span>
          </div>
        </div>

        <!-- Main Question Card -->
        <div class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border-2 border-primary/40 shadow-md ring-4 ring-primary-container/20 relative overflow-hidden">
          <!-- Top Bar: Question Info & Resuming Timer -->
          <div class="flex items-center justify-between mb-5">
            <div>
              <p class="text-xs font-semibold text-primary uppercase tracking-wide font-label">{{ quizSkill }} • {{ quizDifficulty }}</p>
              <h3 class="font-headline font-bold text-on-surface text-base sm:text-lg">Question {{ currentQ + 1 }} of {{ questions.length }}</h3>
            </div>
            
            <!-- Resilient Timer Display (Counts down question's individual time, NEVER resets on back navigation) -->
            <div class="flex items-center gap-2">
              <div
                class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full font-bold text-sm tracking-tight transition-all"
                :class="[
                  questionTimesLeft[currentQ] <= 0 ? 'bg-red-100 text-red-700 border border-red-300' :
                  questionTimesLeft[currentQ] <= 5 ? 'bg-red-100 text-red-700 animate-pulse border border-red-300' :
                  'bg-primary/10 text-primary border border-primary/20'
                ]"
              >
                <span class="material-symbols-outlined text-base">timer</span>
                <span>{{ questionTimesLeft[currentQ] > 0 ? `${questionTimesLeft[currentQ]}s` : 'Time Expired' }}</span>
              </div>
            </div>
          </div>

          <!-- Progress Bar for Current Question Time -->
          <div class="w-full h-2 bg-surface-container rounded-full overflow-hidden mb-6">
            <div
              class="h-full rounded-full transition-all duration-300"
              :class="questionTimesLeft[currentQ] <= 5 ? 'bg-red-500' : 'bg-primary'"
              :style="`width: ${(questionTimesLeft[currentQ] / timePerQuestion) * 100}%`"
            ></div>
          </div>

          <!-- Question Text (Protected from copying/selection) -->
          <h2 class="font-headline font-bold text-on-surface text-lg sm:text-xl mb-6 leading-relaxed select-none">
            {{ currentQuestion.q }}
          </h2>

          <!-- Options -->
          <div class="space-y-3">
            <button
              v-for="(opt, idx) in currentQuestion.shuffledOptions"
              :key="idx"
              @click="selectAnswer(opt.originalIdx)"
              :disabled="questionTimesLeft[currentQ] <= 0 || autoFailed"
              class="w-full text-left p-4 rounded-2xl border-2 text-sm font-medium text-on-surface flex items-center gap-3 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed select-none"
              :class="userAnswers[currentQ] === opt.originalIdx
                ? 'border-primary bg-primary/10 text-primary font-bold shadow-xs'
                : 'border-surface-container-high bg-surface-bright hover:border-primary/50 hover:bg-surface-container-low'"
            >
              <span class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs shrink-0 transition-colors"
                :class="userAnswers[currentQ] === opt.originalIdx ? 'bg-primary text-on-primary' : 'bg-surface-container-high text-on-surface-variant'">
                {{ String.fromCharCode(65 + idx) }}
              </span>
              <span class="flex-1">{{ opt.text }}</span>
              <span v-if="userAnswers[currentQ] === opt.originalIdx" class="material-symbols-outlined text-primary text-lg" style="font-variation-settings: 'FILL' 1;">check_circle</span>
            </button>
          </div>

          <!-- Expired Notice if time runs out for this question -->
          <div v-if="questionTimesLeft[currentQ] <= 0" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-center gap-2">
            <span class="material-symbols-outlined text-sm">alarm_off</span>
            <span>Time expired for Question {{ currentQ + 1 }}. You cannot change this answer anymore.</span>
          </div>

          <!-- Navigation Buttons: Previous / Next / Submit -->
          <div class="flex items-center justify-between mt-8 pt-5 border-t border-surface-container-high">
            <button
              v-if="currentQ > 0"
              @click="goToQuestion(currentQ - 1)"
              class="px-4 py-2.5 rounded-xl border border-outline-variant/60 text-on-surface text-xs font-bold hover:bg-surface-container-low active:scale-95 transition-all flex items-center gap-1.5"
            >
              <span class="material-symbols-outlined text-base">arrow_back</span>
              <span>Previous</span>
            </button>
            <div v-else></div>

            <div class="flex items-center gap-2">
              <button
                v-if="currentQ < questions.length - 1"
                @click="goToQuestion(currentQ + 1)"
                class="px-5 py-2.5 rounded-xl bg-primary text-on-primary text-xs font-bold font-headline flex items-center gap-1.5 hover:bg-primary-dim active:scale-95 transition-all shadow-sm"
              >
                <span>Next Question</span>
                <span class="material-symbols-outlined text-base">arrow_forward</span>
              </button>
              <button
                v-else
                @click="submitQuiz"
                :disabled="isSubmitting"
                class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-primary to-secondary text-on-primary text-xs font-bold font-headline flex items-center gap-2 hover:opacity-95 active:scale-95 transition-all shadow-md disabled:opacity-60 disabled:cursor-not-allowed"
              >
                <span v-if="isSubmitting" class="w-3.5 h-3.5 rounded-full border-2 border-white/40 border-t-white animate-spin inline-block"></span>
                <span>{{ isSubmitting ? 'Submitting Test...' : 'Submit Quiz' }}</span>
                <span v-if="!isSubmitting" class="material-symbols-outlined text-base">task_alt</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Anti-Cheat Status Badge in Footer -->
        <div class="flex items-center justify-between px-2 text-[11px] text-on-surface-variant">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span>Proctor Monitoring: Active</span>
          </div>
          <span class="font-semibold">Copy & Focus Shield Enabled</span>
        </div>
      </div>

      <!-- PHASE 3: RESULTS -->
      <div v-else-if="phase === 'result'" class="result-card space-y-6">
        <div class="bg-surface-container-lowest rounded-3xl p-8 border shadow-xl text-center" :class="result.passed ? 'border-primary/30' : 'border-error/30'">
          <!-- Score Circle -->
          <div class="relative w-32 h-32 mx-auto mb-4">
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
              <path class="text-surface-container-high" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" stroke-width="3.5"></path>
              <path :class="result.passed ? 'text-primary' : 'text-error'" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="currentColor" :stroke-dasharray="`${scorePercent}, 100`" stroke-linecap="round" stroke-width="3.5"></path>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <span class="font-display font-extrabold text-2xl text-on-surface">{{ scorePercent }}%</span>
              <span class="text-[10px] text-on-surface-variant font-semibold">60% to pass</span>
            </div>
          </div>

          <!-- Status -->
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-sm font-bold mb-4" :class="result.passed ? 'bg-green-100 text-green-700 border border-green-200' : 'bg-red-100 text-red-700 border border-red-200'">
            <span class="material-symbols-outlined text-sm">{{ result.passed ? 'task_alt' : 'cancel' }}</span>
            {{ result.passed ? 'Skill Verified! ✨' : 'Not Passed This Time' }}
          </div>

          <h2 class="font-display text-2xl font-bold text-on-surface mb-2">{{ quizSkill }} — {{ quizDifficulty }}</h2>

          <!-- Stats Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 text-left">
            <div class="p-3 rounded-2xl bg-surface-container-low border border-surface-container-high text-center">
              <div class="text-[10px] text-on-surface-variant font-semibold mb-1 uppercase">Correct</div>
              <div class="font-headline font-extrabold text-on-surface text-base">{{ result.effective_correct }}/{{ result.total }}</div>
            </div>
            <div class="p-3 rounded-2xl bg-surface-container-low border border-surface-container-high text-center">
              <div class="text-[10px] text-on-surface-variant font-semibold mb-1 uppercase">XP Earned</div>
              <div class="font-headline font-extrabold text-primary text-base">+{{ result.xp_earned }}</div>
            </div>
            <div class="p-3 rounded-2xl bg-surface-container-low border border-surface-container-high text-center">
              <div class="text-[10px] text-on-surface-variant font-semibold mb-1 uppercase">Penalties</div>
              <div class="font-headline font-extrabold text-secondary text-base">{{ result.tab_switches || 0 }} Strikes</div>
            </div>
            <div class="p-3 rounded-2xl bg-surface-container-low border border-surface-container-high text-center">
              <div class="text-[10px] text-on-surface-variant font-semibold mb-1 uppercase">Badge</div>
              <div class="font-headline font-extrabold text-tertiary text-base capitalize">{{ result.passed ? quizDifficulty : 'None' }}</div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-3 mt-8">
            <NuxtLink to="/dashboard" class="flex-1 py-3 rounded-2xl bg-primary text-on-primary font-headline font-bold text-sm text-center hover:bg-primary-dim active:scale-95 transition-all flex items-center justify-center gap-2">
              <span class="material-symbols-outlined text-base">home</span>
              Back to Dashboard
            </NuxtLink>
            <button @click="resetQuiz" class="flex-1 py-3 rounded-2xl border-2 border-primary text-primary font-headline font-bold text-sm hover:bg-primary/5 active:scale-95 transition-all flex items-center justify-center gap-2">
              <span class="material-symbols-outlined text-base">replay</span>
              Try Another Quiz
            </button>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const phase = ref('select')  // 'select' | 'quiz' | 'result'
const teachSkills = ref([])
const verifiedSkills = ref([])
const history = ref([])
const loading = ref(true)
const loadingQuiz = ref(false)
const selectedSkill = ref(null)

const questions = ref([])
const shuffledQuestions = ref([])
const quizSkill = ref('')
const quizDifficulty = ref('')
const currentQ = ref(0)
const userAnswers = ref([])
const timePerQuestion = ref(20)

// ─── Result & Submission State ───────────────────────────────────────────────
const result = ref({})
const isSubmitting = ref(false)
const quizSource = ref('ai')

const scorePercent = computed(() => {
  if (!result.value || !result.value.total) return 0
  return Math.round(((result.value.effective_correct || 0) / result.value.total) * 100)
})

// ─── Individual Question Timer State (Persistent Memory) ─────────────────────
// Each question has its own allocated time; navigating does NOT reset it!
const questionTimesLeft = ref([])
let timerInterval = null

// ─── Anti-Cheat & Focus Loss State ───────────────────────────────────────────
const MAX_TAB_SWITCHES = 3
const tabSwitches = ref(0)
const isWindowBlurred = ref(false)
const autoFailed = ref(false)
const cheatToast = ref(null)
let toastTimeout = null

const shuffleArray = (arr) => {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

const buildShuffled = (rawQuestions) => {
  return rawQuestions.map(q => {
    const optObjs = q.options.map((text, originalIdx) => ({ text, originalIdx }))
    return { ...q, shuffledOptions: shuffleArray(optObjs) }
  })
}

const currentQuestion = computed(() => shuffledQuestions.value[currentQ.value] || { q: '', shuffledOptions: [] })

const fetchInitialData = async () => {
  try {
    const [resSkills, resVerified, resHistory] = await Promise.all([
      fetch('/api/skills', { credentials: 'include' }).catch(() => null),
      fetch('/api/quiz/verified', { credentials: 'include' }).catch(() => null),
      fetch('/api/quiz/history', { credentials: 'include' }).catch(() => null)
    ])
    if (resSkills?.ok)  { const d = await resSkills.json();  teachSkills.value = d.teaches || [] }
    if (resVerified?.ok){ const d = await resVerified.json();verifiedSkills.value = d.verified || [] }
    if (resHistory?.ok) { const d = await resHistory.json(); history.value = d.history || [] }
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

onMounted(() => {
  fetchInitialData()
  document.addEventListener('visibilitychange', handleVisibilityChange)
  window.addEventListener('blur', handleWindowBlur)
  window.addEventListener('keydown', handleKeydown)
  document.addEventListener('copy', handleCopyAttempt)
  document.addEventListener('cut', handleCopyAttempt)
  document.addEventListener('paste', handleCopyAttempt)
})

onUnmounted(() => {
  clearInterval(timerInterval)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  window.removeEventListener('blur', handleWindowBlur)
  window.removeEventListener('keydown', handleKeydown)
  document.removeEventListener('copy', handleCopyAttempt)
  document.removeEventListener('cut', handleCopyAttempt)
  document.removeEventListener('paste', handleCopyAttempt)
})

// ─── Anti-Cheat Copy & Shortcut Blockers ─────────────────────────────────────
const triggerCheatToast = (msg) => {
  cheatToast.value = msg
  clearTimeout(toastTimeout)
  toastTimeout = setTimeout(() => { cheatToast.value = null }, 3500)
}

const handleContextMenu = (e) => {
  if (phase.value === 'quiz') {
    e.preventDefault()
    triggerCheatToast("Right-click context menu is disabled during verification.")
  }
}

const handleCopyAttempt = (e) => {
  if (phase.value === 'quiz') {
    e.preventDefault()
    triggerCheatToast("Copying or cutting text is blocked by anti-cheat proctor.")
  }
}

const handleKeydown = (e) => {
  if (phase.value !== 'quiz') return
  const key = e.key.toLowerCase()
  // Block Ctrl+C, Ctrl+X, Ctrl+A, Ctrl+U, Ctrl+V
  if ((e.ctrlKey || e.metaKey) && ['c', 'x', 'a', 'u', 'v'].includes(key)) {
    e.preventDefault()
    triggerCheatToast(`Keyboard shortcut Ctrl+${key.toUpperCase()} is strictly prohibited.`)
  }
  // Block F12 and Ctrl+Shift+I / Ctrl+Shift+J (DevTools)
  if (e.key === 'F12' || ((e.ctrlKey || e.metaKey) && e.shiftKey && ['i', 'j', 'c'].includes(key))) {
    e.preventDefault()
    triggerCheatToast("Developer inspection tools are disabled during verification.")
  }
}

// ─── Anti-Cheat Focus & Overlay Detection ────────────────────────────────────
const handleVisibilityChange = () => {
  if (phase.value !== 'quiz' || autoFailed.value) return
  if (document.hidden) {
    triggerFocusLoss()
  }
}

const handleWindowBlur = () => {
  if (phase.value !== 'quiz' || autoFailed.value) return
  triggerFocusLoss()
}

const triggerFocusLoss = () => {
  if (isWindowBlurred.value) return // already flagged
  isWindowBlurred.value = true
  tabSwitches.value++
  pauseTimer()

  if (tabSwitches.value > MAX_TAB_SWITCHES) {
    autoFailed.value = true
    triggerCheatToast("Maximum anti-cheat strikes exceeded! Submitting quiz...")
    setTimeout(() => submitQuiz(), 1800)
  }
}

const dismissFocusWarning = () => {
  isWindowBlurred.value = false
  // Resume the timer on the current question
  if (!autoFailed.value && phase.value === 'quiz') {
    startActiveQuestionTimer()
  }
}

const getVerifiedStatus = (skillName) => {
  const info = verifiedSkills.value.find(v => v.skill_name?.toLowerCase() === skillName?.toLowerCase())
  return info ? info.verified_level : 'unverified'
}

const getVerifiedInfo = (skillName) => {
  if (!skillName) return null
  return verifiedSkills.value.find(v => v.skill_name?.toLowerCase() === skillName?.toLowerCase())
}

const selectSkill = (skillName) => { selectedSkill.value = skillName }

const startQuiz = async (difficulty) => {
  if (!selectedSkill.value) return
  loadingQuiz.value = true
  try {
    const res = await fetch('/api/quiz/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ skill_name: selectedSkill.value, difficulty })
    })
    if (res.ok) {
      const data = await res.json()
      questions.value = data.questions
      shuffledQuestions.value = buildShuffled(data.questions)
      quizSkill.value = data.skill
      quizDifficulty.value = data.difficulty
      quizSource.value = data.source || 'local'
      timePerQuestion.value = data.time_per_question || 20
      
      // Initialize persistent remaining time for EACH question separately!
      questionTimesLeft.value = new Array(data.questions.length).fill(timePerQuestion.value)
      userAnswers.value = new Array(data.questions.length).fill(-1)
      
      currentQ.value = 0
      tabSwitches.value = 0
      autoFailed.value = false
      isWindowBlurred.value = false
      phase.value = 'quiz'

      // Start timer for question 0
      startActiveQuestionTimer()
    } else {
      const errData = await res.json().catch(() => ({}))
      alert(errData.error || `Failed to generate quiz (status ${res.status}). Please try again.`)
    }
  } catch(e) {
    console.error(e)
    alert('Network error while generating quiz. Is the backend running?')
  } finally {
    loadingQuiz.value = false
  }
}

// ─── Resilient Individual Question Timer ─────────────────────────────────────
const startActiveQuestionTimer = () => {
  clearInterval(timerInterval)
  
  // If time already expired on this question, don't tick
  if (questionTimesLeft.value[currentQ.value] <= 0) return

  timerInterval = setInterval(() => {
    if (isWindowBlurred.value) return // pause while security modal is active
    
    if (questionTimesLeft.value[currentQ.value] > 0) {
      questionTimesLeft.value[currentQ.value]--
    }

    // Time expired on this specific question
    if (questionTimesLeft.value[currentQ.value] <= 0) {
      clearInterval(timerInterval)
      // Check if all questions are completed or expired
      const allDone = questionTimesLeft.value.every((t, i) => t <= 0 || userAnswers.value[i] !== -1)
      if (allDone) {
        submitQuiz()
      } else {
        // Auto-advance to next available unanswered question
        autoAdvanceToAvailable()
      }
    }
  }, 1000)
}

const pauseTimer = () => {
  clearInterval(timerInterval)
}

// Navigation between questions (Previous / Next / Question Pills)
// This preserves the exact remaining time on every question and NEVER resets to 20!
const goToQuestion = (targetIdx) => {
  if (targetIdx < 0 || targetIdx >= questions.value.length) return
  pauseTimer()
  currentQ.value = targetIdx
  startActiveQuestionTimer()
}

const autoAdvanceToAvailable = () => {
  // Find next question that still has time left
  let nextIdx = -1
  for (let i = currentQ.value + 1; i < questions.value.length; i++) {
    if (questionTimesLeft.value[i] > 0 && userAnswers.value[i] === -1) {
      nextIdx = i
      break
    }
  }
  // Wrap around if needed
  if (nextIdx === -1) {
    for (let i = 0; i < currentQ.value; i++) {
      if (questionTimesLeft.value[i] > 0 && userAnswers.value[i] === -1) {
        nextIdx = i
        break
      }
    }
  }

  if (nextIdx !== -1) {
    goToQuestion(nextIdx)
  }
}

const selectAnswer = (originalIdx) => {
  if (autoFailed.value || questionTimesLeft.value[currentQ.value] <= 0) return
  userAnswers.value[currentQ.value] = originalIdx
}

const submitQuiz = async () => {
  if (isSubmitting.value) return
  isSubmitting.value = true
  pauseTimer()
  try {
    const res = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        answers: userAnswers.value,
        tab_switches: tabSwitches.value,
        auto_failed: autoFailed.value
      })
    })
    if (res.ok) {
      result.value = await res.json()
      phase.value = 'result'
      fetchInitialData()
    } else {
      const d = await res.json().catch(() => ({}))
      // Fallback: check recent history in case the quiz attempt was already recorded
      const histRes = await fetch('/api/quiz/history', { credentials: 'include' })
      if (histRes.ok) {
        const histData = await histRes.json()
        if (histData.history && histData.history.length > 0) {
          const top = histData.history[0]
          result.value = {
            effective_correct: top.score,
            total: top.total,
            passed: Boolean(top.passed),
            xp_earned: top.xp_earned,
            tab_switches: top.tab_switches
          }
          phase.value = 'result'
          fetchInitialData()
          return
        }
      }
      alert(d.error || 'Failed to submit quiz. Please try again.')
    }
  } catch (e) {
    console.error('Submit quiz error:', e)
    alert('Network error while submitting quiz.')
  } finally {
    isSubmitting.value = false
  }
}

const resetQuiz = () => {
  pauseTimer()
  phase.value = 'select'
  selectedSkill.value = null
  questions.value = []
  shuffledQuestions.value = []
  userAnswers.value = []
  questionTimesLeft.value = []
  currentQ.value = 0
  result.value = {}
  tabSwitches.value = 0
  autoFailed.value = false
  isWindowBlurred.value = false
  quizSource.value = 'local'
}
</script>

<style scoped>
.no-copy-quiz {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translate(-50%, -20px);
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
