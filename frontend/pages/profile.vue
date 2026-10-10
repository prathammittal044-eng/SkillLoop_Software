<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col selection:bg-primary/20">

    <!-- Top Navigation (Pixel-Perfect with Dashboard & Chat) -->
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
            <NuxtLink to="/dashboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5">
              <span class="material-symbols-outlined text-lg">space_dashboard</span>
              Dashboard
            </NuxtLink>
            <NuxtLink to="/chat" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1">
              <span class="material-symbols-outlined text-lg">chat</span>
              Chat &amp; Video
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
        <div class="flex items-center gap-1.5 sm:gap-3 shrink-0">
          <div v-if="me" class="flex items-center gap-1 bg-surface-container-lowest px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-full border border-secondary-fixed shadow-sm text-xs sm:text-sm font-label font-bold text-on-surface whitespace-nowrap shrink-0">
            <span class="material-symbols-outlined text-primary text-base sm:text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
            <span>{{ me.time_credits || 0 }} <span class="hidden sm:inline">Credits</span><span class="sm:hidden">cr</span></span>
          </div>

          <NuxtLink to="/profile" class="relative w-8 sm:w-9 h-8 sm:h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-xs sm:text-sm uppercase shadow-sm overflow-hidden hover:ring-2 hover:ring-primary/40 transition-all shrink-0" title="My Profile">
            <img v-if="me?.profile_picture" :src="me.profile_picture" class="w-full h-full object-cover" />
            <span v-else>{{ (me?.full_name || me?.username || 'U').charAt(0) }}</span>
          </NuxtLink>
          <button @click="logout" class="hidden sm:inline text-xs text-on-surface-variant hover:text-error transition-colors font-semibold">Logout</button>
        </div>
      </div>
    </header>

    <!-- Loading State -->
    <div v-if="loading" class="flex-1 flex items-center justify-center">
      <div class="text-center space-y-3">
        <div class="w-12 h-12 rounded-full border-4 border-primary/30 border-t-primary animate-spin mx-auto"></div>
        <p class="text-on-surface-variant text-sm font-medium">Loading profile...</p>
      </div>
    </div>

    <!-- User Not Found -->
    <div v-else-if="notFound" class="flex-1 flex items-center justify-center p-6">
      <div class="text-center space-y-4 max-w-sm bg-white p-8 rounded-3xl border border-surface-container shadow-sm">
        <div class="w-16 h-16 rounded-2xl bg-error/10 text-error flex items-center justify-center mx-auto">
          <span class="material-symbols-outlined text-3xl">person_off</span>
        </div>
        <h2 class="font-headline font-bold text-xl text-on-surface">Student Not Found</h2>
        <p class="text-on-surface-variant text-xs leading-relaxed">The username "@{{ targetUsername }}" does not exist or may have been removed.</p>
        <NuxtLink to="/dashboard" class="px-6 py-2.5 rounded-xl bg-primary text-on-primary font-semibold text-sm inline-block shadow-sm hover:bg-primary-dim transition-all">Back to Dashboard</NuxtLink>
      </div>
    </div>

    <!-- Main Profile Workspace (Matches Mockup Perfectly) -->
    <main v-else-if="profile" class="flex-1 w-full max-w-5xl mx-auto px-4 sm:px-6 py-8 space-y-6">

      <!-- ==================== 1. HERO PROFILE CARD ==================== -->
      <div class="bg-white rounded-3xl overflow-hidden border border-surface-container shadow-sm">

        <!-- Top Banner (~180px) -->
        <div class="relative h-44 sm:h-52 overflow-hidden" :style="bannerStyle">
          <img v-if="profile.banner_image" :src="profile.banner_image" class="w-full h-full object-cover" />

          <!-- Banner Action Controls (Own Profile) -->
          <div v-if="isOwnProfile" class="absolute top-4 right-4 flex items-center gap-2 z-20">
            <!-- Edit Profile Quick Button (Mockup style) -->
            <button
              @click="openEditModal"
              class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-white/95 hover:bg-white text-on-surface text-xs font-bold shadow-md backdrop-blur-md transition-all active:scale-95"
            >
              <span class="material-symbols-outlined text-base text-primary">edit</span>
              <span>Edit</span>
            </button>

            <!-- Change Banner Photo Button -->
            <label class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/60 hover:bg-black/80 text-white text-xs font-semibold cursor-pointer shadow-md backdrop-blur-md transition-all active:scale-95" title="Upload cover banner">
              <span class="material-symbols-outlined text-base">photo_camera</span>
              <span class="hidden sm:inline">Change Banner</span>
              <input type="file" accept="image/*" class="hidden" @change="uploadBanner" :disabled="uploadingBanner" />
            </label>
          </div>

          <!-- Uploading Spinner for Banner -->
          <div v-if="uploadingBanner" class="absolute inset-0 flex items-center justify-center bg-black/50 z-30">
            <div class="w-8 h-8 rounded-full border-4 border-white/30 border-t-white animate-spin"></div>
          </div>
        </div>

        <!-- Avatar, Identity & Header Actions -->
        <div class="px-6 sm:px-8 pb-7 relative">

          <!-- Overlapping Circular Avatar (80px - 96px) -->
          <div class="relative -mt-12 sm:-mt-14 mb-4 w-fit">
            <div
              class="w-24 h-24 sm:w-28 sm:h-28 rounded-full border-4 border-white shadow-lg overflow-hidden flex items-center justify-center font-bold text-3xl sm:text-4xl text-on-primary bg-primary relative"
              :style="avatarStyle(profile)"
            >
              <img v-if="profile.profile_picture" :src="profile.profile_picture" class="w-full h-full object-cover" />
              <span v-else>{{ (profile.full_name || profile.username || 'U').charAt(0) }}</span>
            </div>

            <!-- Upload Avatar Camera Pill (Own Profile) -->
            <label
              v-if="isOwnProfile"
              class="absolute bottom-1 right-1 w-8 h-8 rounded-full bg-primary text-on-primary flex items-center justify-center cursor-pointer shadow-md hover:bg-primary-dim transition-all z-20 ring-2 ring-white hover:scale-105 active:scale-95"
              title="Upload profile picture"
            >
              <span class="material-symbols-outlined text-base">photo_camera</span>
              <input type="file" accept="image/*" class="hidden" @change="uploadAvatar" :disabled="uploadingAvatar" />
            </label>

            <!-- Uploading Spinner for Avatar -->
            <div v-if="uploadingAvatar" class="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center z-30">
              <div class="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            </div>
          </div>

          <!-- Name, Headline & Action Buttons Row -->
          <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-5">
            <div>
              <div class="flex items-center gap-2.5 flex-wrap">
                <h1 class="font-display text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight">
                  {{ profile.full_name || profile.username }}
                </h1>
                <span class="text-xs px-2.5 py-0.5 rounded-full bg-surface-container font-mono text-on-surface-variant font-semibold">
                  @{{ profile.username }}
                </span>
              </div>

              <!-- Headline / Tagline -->
              <p class="text-sm sm:text-base font-medium text-on-surface-variant mt-1 max-w-2xl leading-snug">
                {{ profile.headline || (profile.department ? `${profile.department} Student • Sem ${profile.semester || 1}` : 'SkillLoop Campus Learner') }}
              </p>
            </div>

            <!-- ACTION BUTTONS (Right Side) -->
            <!-- Case A: PEER PROFILE VIEW -->
            <div v-if="!isOwnProfile" class="flex flex-col sm:items-end gap-2.5 shrink-0">
              <div class="flex items-center gap-2.5 flex-wrap">
                <!-- Connect Button -->
                <button
                  @click="sendConnect"
                  :disabled="connStatus !== null"
                  class="flex items-center gap-2 px-6 py-2.5 rounded-xl font-headline font-bold text-sm transition-all shadow-xs active:scale-95"
                  :class="connStatus?.status === 'accepted' ? 'bg-emerald-100 text-emerald-800 cursor-default' : (connStatus ? 'bg-surface-container text-on-surface-variant cursor-default' : 'bg-primary text-on-primary hover:bg-primary-dim')"
                >
                  <span class="material-symbols-outlined text-lg">{{ connStatus?.status === 'accepted' ? 'how_to_reg' : connStatus ? 'hourglass_top' : 'person_add' }}</span>
                  <span>{{ connStatus?.status === 'accepted' ? 'Connected' : connStatus ? 'Pending' : 'Connect' }}</span>
                </button>

                <!-- Book Session Button -->
                <button
                  @click="goBookSession"
                  class="flex items-center gap-2 px-5 py-2.5 rounded-xl border-2 border-primary text-primary hover:bg-primary/5 font-headline font-bold text-sm transition-all active:scale-95 shadow-xs"
                >
                  <span class="material-symbols-outlined text-lg">calendar_add_on</span>
                  <span>Book Session</span>
                </button>
              </div>

              <!-- Send Message Link -->
              <NuxtLink
                :to="`/chat?user=${profile.username}`"
                class="inline-flex items-center gap-1.5 text-xs font-bold text-primary hover:underline group pt-0.5"
              >
                <span>Send Message</span>
                <span class="material-symbols-outlined text-sm group-hover:translate-x-0.5 transition-transform">send</span>
              </NuxtLink>
            </div>

            <!-- Case B: MY OWN PROFILE VIEW -->
            <div v-else class="flex items-center gap-2.5 shrink-0">
              <button
                @click="openEditModal"
                class="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-bold text-sm shadow-xs hover:bg-primary-dim transition-all active:scale-95"
              >
                <span class="material-symbols-outlined text-lg">edit</span>
                <span>Edit Profile</span>
              </button>
              <button
                @click="copyProfileLink"
                class="flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-outline-variant text-on-surface hover:bg-surface-container-low font-headline font-semibold text-sm transition-all active:scale-95"
                title="Copy shareable link"
              >
                <span class="material-symbols-outlined text-lg text-primary">{{ linkCopied ? 'check' : 'share' }}</span>
                <span>{{ linkCopied ? 'Copied!' : 'Share' }}</span>
              </button>
            </div>
          </div>

          <!-- Stats Row (4 Pill Chips from Mockup) -->
          <div class="flex flex-wrap items-center gap-2.5 mt-6 pt-5 border-t border-surface-container">
            <!-- 1. XP -->
            <div class="flex items-center gap-2 bg-surface-container-low px-4 py-2 rounded-2xl border border-surface-container text-xs font-bold text-on-surface shadow-xs">
              <span class="material-symbols-outlined text-primary text-base" style="font-variation-settings: 'FILL' 1;">bolt</span>
              <span>{{ profile.xp || 0 }} XP</span>
            </div>

            <!-- 2. Sessions -->
            <div class="flex items-center gap-2 bg-surface-container-low px-4 py-2 rounded-2xl border border-surface-container text-xs font-bold text-on-surface shadow-xs">
              <span class="material-symbols-outlined text-secondary text-base" style="font-variation-settings: 'FILL' 1;">school</span>
              <span>{{ profile.total_sessions || 0 }} Sessions</span>
            </div>

            <!-- 3. Rating -->
            <div class="flex items-center gap-2 bg-surface-container-low px-4 py-2 rounded-2xl border border-surface-container text-xs font-bold text-on-surface shadow-xs">
              <span class="material-symbols-outlined text-amber-500 text-base" style="font-variation-settings: 'FILL' 1;">star</span>
              <span>{{ profile.rating_avg ? profile.rating_avg.toFixed(1) : '5.0' }} Rating</span>
              <span v-if="profile.rating_count" class="text-on-surface-variant font-normal">({{ profile.rating_count }})</span>
            </div>

            <!-- 4. Teaching Time -->
            <div class="flex items-center gap-2 bg-surface-container-low px-4 py-2 rounded-2xl border border-surface-container text-xs font-bold text-on-surface shadow-xs">
              <span class="material-symbols-outlined text-tertiary text-base" style="font-variation-settings: 'FILL' 1;">timer</span>
              <span>{{ formatTime(profile.total_teaching_seconds) }} Taught</span>
            </div>
          </div>

        </div>
      </div>


      <!-- ==================== 2. TWO-COLUMN WORKSPACE (MOCKUP ACCURATE) ==================== -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

        <!-- ─── LEFT COLUMN (7 Cols: About Me, Skills, Links) ─── -->
        <div class="lg:col-span-7 space-y-6">

          <!-- About Me Card -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-3">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-xl">person</span>
                <span>About Me</span>
              </h2>
              <button v-if="isOwnProfile && !profile.bio" @click="openEditModal" class="text-xs font-bold text-primary hover:underline">
                + Add Bio
              </button>
            </div>
            <p v-if="profile.bio" class="text-on-surface-variant text-sm leading-relaxed whitespace-pre-line">
              {{ profile.bio }}
            </p>
            <p v-else class="text-on-surface-variant/70 text-sm italic">
              {{ isOwnProfile ? 'Tell peers about your interests, what you study, and what you love building.' : 'This student hasn\'t added a bio yet.' }}
            </p>
          </div>

          <!-- Skills I Teach Card -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-xl">psychology</span>
                <span>Skills I Teach</span>
              </h2>
              <span v-if="(profile.teaches || []).length" class="text-xs font-bold text-on-surface-variant px-2 py-0.5 rounded-full bg-surface-container">
                {{ profile.teaches.length }}
              </span>
            </div>

            <div v-if="(profile.teaches || []).length" class="flex flex-wrap gap-2.5">
              <div
                v-for="skill in profile.teaches"
                :key="skill"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-full font-headline font-bold text-xs shadow-xs transition-all"
                :class="isVerified(skill) ? 'bg-primary text-on-primary' : 'bg-primary/10 text-primary border border-primary/20'"
              >
                <span v-if="isVerified(skill)" class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">verified</span>
                <span>{{ skill }}</span>
                <span v-if="isVerified(skill)" class="px-1.5 py-0.2 rounded-full bg-white/20 text-[10px] uppercase font-mono tracking-wider">
                  {{ getVerifiedLevel(skill) }}
                </span>
              </div>
            </div>
            <p v-else class="text-on-surface-variant/70 text-sm italic">
              No teaching skills listed yet.
            </p>
          </div>

          <!-- Skills I Want to Learn Card -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-secondary text-xl">school</span>
                <span>Skills I Want to Learn</span>
              </h2>
              <span v-if="(profile.learns || []).length" class="text-xs font-bold text-on-surface-variant px-2 py-0.5 rounded-full bg-surface-container">
                {{ profile.learns.length }}
              </span>
            </div>

            <div v-if="(profile.learns || []).length" class="flex flex-wrap gap-2.5">
              <span
                v-for="skill in profile.learns"
                :key="skill"
                class="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border-2 border-outline-variant/60 text-on-surface font-headline font-semibold text-xs hover:border-primary hover:text-primary transition-colors bg-white shadow-xs"
              >
                {{ skill }}
              </span>
            </div>
            <p v-else class="text-on-surface-variant/70 text-sm italic">
              No learning goals listed yet.
            </p>
          </div>

          <!-- Links Card (GitHub, LinkedIn, Portfolio from Mockup) -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-3.5">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-xl">link</span>
                <span>Links &amp; Profiles</span>
              </h2>
              <button v-if="isOwnProfile" @click="openEditModal" class="text-xs font-bold text-primary hover:underline">
                Edit Links
              </button>
            </div>

            <div class="space-y-2.5">
              <!-- GitHub Link -->
              <a
                v-if="profile.github_url"
                :href="formatUrl(profile.github_url)"
                target="_blank"
                rel="noopener"
                class="flex items-center justify-between p-3 rounded-2xl bg-surface-container-low hover:bg-surface-container border border-surface-container/60 transition-all group"
              >
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-8 h-8 rounded-xl bg-surface-container-lowest text-on-surface flex items-center justify-center shrink-0 shadow-xs group-hover:text-primary transition-colors">
                    <span class="material-symbols-outlined text-lg">code</span>
                  </div>
                  <div class="min-w-0">
                    <p class="font-headline font-bold text-xs text-on-surface">GitHub</p>
                    <p class="text-[11px] text-on-surface-variant truncate font-mono">{{ cleanUrl(profile.github_url) }}</p>
                  </div>
                </div>
                <span class="material-symbols-outlined text-sm text-on-surface-variant group-hover:text-primary transition-colors">open_in_new</span>
              </a>

              <!-- LinkedIn Link -->
              <a
                v-if="profile.linkedin_url"
                :href="formatUrl(profile.linkedin_url)"
                target="_blank"
                rel="noopener"
                class="flex items-center justify-between p-3 rounded-2xl bg-surface-container-low hover:bg-surface-container border border-surface-container/60 transition-all group"
              >
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-8 h-8 rounded-xl bg-surface-container-lowest text-primary flex items-center justify-center shrink-0 shadow-xs">
                    <span class="material-symbols-outlined text-lg">work</span>
                  </div>
                  <div class="min-w-0">
                    <p class="font-headline font-bold text-xs text-on-surface">LinkedIn</p>
                    <p class="text-[11px] text-on-surface-variant truncate font-mono">{{ cleanUrl(profile.linkedin_url) }}</p>
                  </div>
                </div>
                <span class="material-symbols-outlined text-sm text-on-surface-variant group-hover:text-primary transition-colors">open_in_new</span>
              </a>

              <!-- Portfolio Link -->
              <a
                v-if="profile.portfolio_url"
                :href="formatUrl(profile.portfolio_url)"
                target="_blank"
                rel="noopener"
                class="flex items-center justify-between p-3 rounded-2xl bg-surface-container-low hover:bg-surface-container border border-surface-container/60 transition-all group"
              >
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-8 h-8 rounded-xl bg-surface-container-lowest text-tertiary flex items-center justify-center shrink-0 shadow-xs">
                    <span class="material-symbols-outlined text-lg">public</span>
                  </div>
                  <div class="min-w-0">
                    <p class="font-headline font-bold text-xs text-on-surface">Portfolio / Website</p>
                    <p class="text-[11px] text-on-surface-variant truncate font-mono">{{ cleanUrl(profile.portfolio_url) }}</p>
                  </div>
                </div>
                <span class="material-symbols-outlined text-sm text-on-surface-variant group-hover:text-primary transition-colors">open_in_new</span>
              </a>

              <!-- Empty links state -->
              <div v-if="!profile.github_url && !profile.linkedin_url && !profile.portfolio_url" class="p-4 rounded-2xl bg-surface-container-low/60 border border-dashed border-surface-container text-center">
                <p class="text-xs text-on-surface-variant/70 italic">No social links added yet.</p>
              </div>
            </div>
          </div>

        </div>


        <!-- ─── RIGHT COLUMN (5 Cols: Academic Info, Reviews) ─── -->
        <div class="lg:col-span-5 space-y-6">

          <!-- Academic Info Card (From Mockup) -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-primary text-xl">school</span>
                <span>Academic Info</span>
              </h2>
              <button v-if="isOwnProfile" @click="openEditModal" class="text-xs font-bold text-primary hover:underline">
                Edit
              </button>
            </div>

            <div class="space-y-3 text-xs">
              <!-- Department -->
              <div class="flex items-center justify-between py-2 border-b border-surface-container-low">
                <span class="font-headline font-semibold text-on-surface-variant">Department</span>
                <span class="font-bold text-on-surface font-headline">{{ profile.department || 'Not specified' }}</span>
              </div>

              <!-- Semester -->
              <div class="flex items-center justify-between py-2 border-b border-surface-container-low">
                <span class="font-headline font-semibold text-on-surface-variant">Semester</span>
                <span class="font-bold text-on-surface font-headline">{{ profile.semester ? `Semester ${profile.semester}` : 'Semester 1' }}</span>
              </div>

              <!-- Institution / College -->
              <div class="flex items-center justify-between py-2 border-b border-surface-container-low">
                <span class="font-headline font-semibold text-on-surface-variant">Institution</span>
                <span class="font-bold text-on-surface font-headline truncate max-w-[180px] text-right">{{ profile.education || 'GGSIPU' }}</span>
              </div>

              <!-- Graduation Year -->
              <div class="flex items-center justify-between py-2">
                <span class="font-headline font-semibold text-on-surface-variant">Graduation</span>
                <span class="font-bold text-on-surface font-headline">{{ profile.graduation_year || '2027' }}</span>
              </div>
            </div>
          </div>

          <!-- Reviews from Peers Card (From Mockup) -->
          <div class="bg-white rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between">
              <h2 class="font-headline font-bold text-base text-on-surface flex items-center gap-2">
                <span class="material-symbols-outlined text-amber-500 text-xl" style="font-variation-settings: 'FILL' 1;">star</span>
                <span>Reviews from Peers</span>
              </h2>
              <span v-if="(profile.reviews || []).length" class="text-xs font-bold text-on-surface-variant px-2.5 py-0.5 rounded-full bg-surface-container">
                {{ profile.reviews.length }}
              </span>
            </div>

            <!-- Review Cards List -->
            <div v-if="(profile.reviews || []).length" class="space-y-3.5">
              <div
                v-for="r in profile.reviews"
                :key="r.created_at"
                class="p-4 rounded-2xl bg-surface-container-low border border-surface-container/70 space-y-2 hover:border-primary/30 transition-all"
              >
                <!-- Reviewer header + Stars -->
                <div class="flex items-center justify-between gap-2">
                  <NuxtLink :to="'/profile?u=' + r.reviewer_username" class="flex items-center gap-2 min-w-0 hover:text-primary transition-colors">
                    <div
                      class="w-7 h-7 rounded-lg text-white font-bold text-xs flex items-center justify-center uppercase shrink-0 shadow-xs"
                      :style="{ background: r.reviewer_color || '#543ce0' }"
                    >
                      {{ (r.reviewer_name || r.reviewer_username || '?').charAt(0) }}
                    </div>
                    <span class="font-headline font-bold text-xs text-on-surface truncate">
                      {{ r.reviewer_name || r.reviewer_username }}
                    </span>
                  </NuxtLink>

                  <!-- 5 Star Icons -->
                  <div class="flex items-center text-amber-500 shrink-0">
                    <span v-for="i in 5" :key="i" class="material-symbols-outlined text-sm" :class="i <= r.rating ? 'opacity-100' : 'text-gray-300'" style="font-variation-settings: 'FILL' 1;">
                      star
                    </span>
                  </div>
                </div>

                <!-- Comment text -->
                <p v-if="r.comment" class="text-xs text-on-surface-variant leading-relaxed">
                  "{{ r.comment }}"
                </p>

                <!-- Role badge and date -->
                <div class="flex items-center justify-between text-[10px] text-on-surface-variant/70 pt-1 border-t border-surface-container/50">
                  <span>{{ r.role === 'learner_rating_teacher' ? 'As Teacher' : 'As Learner' }}</span>
                  <span>{{ formatDate(r.created_at) }}</span>
                </div>
              </div>
            </div>

            <!-- Empty Reviews State -->
            <div v-else class="p-6 rounded-2xl bg-surface-container-low/60 border border-dashed border-surface-container text-center space-y-1">
              <span class="material-symbols-outlined text-3xl text-on-surface-variant/50">rate_review</span>
              <p class="font-headline font-semibold text-xs text-on-surface">No reviews yet</p>
              <p class="text-[11px] text-on-surface-variant/70">Complete skill exchange calls to earn peer ratings!</p>
            </div>
          </div>

        </div>

      </div>

    </main>


    <!-- ==================== 3. EDIT PROFILE MODAL ==================== -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto"
      @click.self="closeEditModal"
    >
      <div class="bg-white rounded-3xl max-w-2xl w-full border border-surface-container shadow-2xl overflow-hidden my-8 animate-in fade-in zoom-in-95 duration-150">

        <!-- Modal Header -->
        <div class="p-5 sm:p-6 border-b border-surface-container flex items-center justify-between bg-surface-container-low/50">
          <div class="flex items-center gap-2.5">
            <div class="w-10 h-10 rounded-2xl bg-primary/10 text-primary flex items-center justify-center">
              <span class="material-symbols-outlined text-xl">edit_note</span>
            </div>
            <div>
              <h3 class="font-headline font-bold text-lg text-on-surface">Edit Profile Details</h3>
              <p class="text-xs text-on-surface-variant">Update your public student profile and links</p>
            </div>
          </div>
          <button @click="closeEditModal" class="w-8 h-8 rounded-full hover:bg-surface-container text-on-surface-variant flex items-center justify-center transition-colors">
            <span class="material-symbols-outlined text-xl">close</span>
          </button>
        </div>

        <!-- Modal Form Fields -->
        <div class="p-5 sm:p-6 space-y-4 max-h-[70vh] overflow-y-auto">
          <!-- Full Name -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Full Name</label>
            <input
              v-model="editForm.full_name"
              type="text"
              class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary font-body"
              placeholder="e.g. Pratham Mittal"
            />
          </div>

          <!-- Headline / Tagline -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Headline / Tagline</label>
            <input
              v-model="editForm.headline"
              type="text"
              class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary font-body"
              placeholder="e.g. Full Stack Dev | 3rd Sem CSE @ GGSIPU"
            />
          </div>

          <!-- Academic 2x2 Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Department / Branch</label>
              <input
                v-model="editForm.department"
                type="text"
                class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g. CSE / IT / ECE"
              />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Semester</label>
              <input
                v-model="editForm.semester"
                type="number"
                min="1"
                max="8"
                class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g. 3"
              />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Institution / College</label>
              <input
                v-model="editForm.education"
                type="text"
                class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g. GGSIPU, Delhi"
              />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">Graduation Year</label>
              <input
                v-model="editForm.graduation_year"
                type="number"
                min="2024"
                max="2035"
                class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g. 2027"
              />
            </div>
          </div>

          <!-- Bio / About Me -->
          <div>
            <label class="block text-xs font-bold uppercase tracking-wider text-on-surface-variant mb-1 font-label">About Me / Bio</label>
            <textarea
              v-model="editForm.bio"
              rows="3"
              maxlength="600"
              class="w-full px-4 py-2.5 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-sm focus:outline-none focus:ring-2 focus:ring-primary font-body resize-none"
              placeholder="Tell peers what you're passionate about, projects you've built, and what you hope to learn..."
            ></textarea>
            <p class="text-[11px] text-on-surface-variant text-right">{{ (editForm.bio || '').length }} / 600</p>
          </div>

          <!-- Social Links -->
          <div class="space-y-3 pt-2 border-t border-surface-container-low">
            <h4 class="text-xs font-bold uppercase tracking-wider text-on-surface-variant font-label">Links</h4>
            <div>
              <label class="block text-[11px] font-semibold text-on-surface mb-1">GitHub URL</label>
              <input
                v-model="editForm.github_url"
                type="text"
                class="w-full px-4 py-2 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-xs font-mono focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://github.com/your-username"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-on-surface mb-1">LinkedIn URL</label>
              <input
                v-model="editForm.linkedin_url"
                type="text"
                class="w-full px-4 py-2 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-xs font-mono focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://linkedin.com/in/your-username"
              />
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-on-surface mb-1">Portfolio / Personal Website</label>
              <input
                v-model="editForm.portfolio_url"
                type="text"
                class="w-full px-4 py-2 rounded-xl border border-surface-container bg-surface-container-low/40 text-on-surface text-xs font-mono focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="https://yourportfolio.dev"
              />
            </div>
          </div>
        </div>

        <!-- Modal Actions -->
        <div class="p-5 sm:p-6 border-t border-surface-container bg-surface-container-low/40 flex items-center justify-end gap-3">
          <button
            @click="closeEditModal"
            class="px-5 py-2.5 rounded-xl border border-outline-variant text-on-surface font-headline font-semibold text-xs hover:bg-surface-container transition-all"
          >
            Cancel
          </button>
          <button
            @click="saveProfile"
            :disabled="isSaving"
            class="px-6 py-2.5 rounded-xl bg-primary text-on-primary font-headline font-bold text-xs shadow-xs hover:bg-primary-dim transition-all active:scale-95 disabled:opacity-60 flex items-center gap-1.5"
          >
            <span v-if="isSaving" class="w-3.5 h-3.5 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
            <span>{{ isSaving ? 'Saving...' : 'Save Changes' }}</span>
          </button>
        </div>

      </div>
    </div>

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
const showEditModal = ref(false)
const isSaving = ref(false)
const uploadingAvatar = ref(false)
const uploadingBanner = ref(false)
const linkCopied = ref(false)

const editForm = ref({
  full_name: '',
  headline: '',
  department: '',
  semester: 1,
  education: '',
  graduation_year: 2027,
  bio: '',
  github_url: '',
  linkedin_url: '',
  portfolio_url: ''
})

// Determine target user
const targetUsername = computed(() => {
  const u = route.query.u || route.query.username
  return typeof u === 'string' ? u.trim().replace(/^@/, '') : null
})

const isOwnProfile = computed(() => {
  if (!targetUsername.value) return true
  if (me.value && me.value.username.toLowerCase() === targetUsername.value.toLowerCase()) return true
  return false
})

const connStatus = computed(() => profile.value?.connection_status || null)

// Gradient presets
const bannerGradients = [
  'linear-gradient(135deg, #543ce0 0%, #99366c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
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

function formatDate(isoStr) {
  if (!isoStr) return ''
  try {
    const d = new Date(isoStr)
    return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })
  } catch {
    return ''
  }
}

function cleanUrl(url) {
  if (!url) return ''
  return url.replace(/^https?:\/\//i, '').replace(/^www\./i, '')
}

function formatUrl(url) {
  if (!url) return '#'
  if (/^https?:\/\//i.test(url)) return url
  return `https://${url}`
}

function isVerified(skillName) {
  return (profile.value?.verified_skills || []).some(
    v => v.skill_name.toLowerCase() === skillName.toLowerCase()
  )
}

function getVerifiedLevel(skillName) {
  const v = (profile.value?.verified_skills || []).find(
    v => v.skill_name.toLowerCase() === skillName.toLowerCase()
  )
  return v ? v.verified_level : ''
}

// Fetch current user
async function fetchMe() {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      me.value = data.user
    }
  } catch {}
}

// Fetch target profile
async function fetchProfile() {
  loading.value = true
  notFound.value = false
  const username = targetUsername.value || me.value?.username

  if (!username) {
    notFound.value = true
    loading.value = false
    return
  }

  try {
    const res = await fetch(`/api/user/${encodeURIComponent(username)}`, { credentials: 'include' })
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

function openEditModal() {
  if (!profile.value) return
  editForm.value = {
    full_name: profile.value.full_name || '',
    headline: profile.value.headline || '',
    department: profile.value.department || '',
    semester: profile.value.semester || 1,
    education: profile.value.education || '',
    graduation_year: profile.value.graduation_year || 2027,
    bio: profile.value.bio || '',
    github_url: profile.value.github_url || '',
    linkedin_url: profile.value.linkedin_url || '',
    portfolio_url: profile.value.portfolio_url || ''
  }
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function saveProfile() {
  isSaving.value = true
  try {
    const res = await fetch('/api/user/me', {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm.value)
    })
    if (res.ok) {
      Object.assign(profile.value, editForm.value)
      if (me.value) Object.assign(me.value, editForm.value)
      showEditModal.value = false
    } else {
      const err = await res.json()
      alert(err.error || 'Failed to update profile.')
    }
  } catch {
    alert('Network error while saving profile.')
  } finally {
    isSaving.value = false
  }
}

async function uploadAvatar(event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploadingAvatar.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('/api/user/upload-avatar', {
      method: 'POST',
      credentials: 'include',
      body: formData
    })
    const data = await res.json()
    if (res.ok) {
      const updatedUrl = data.url + '?t=' + Date.now()
      profile.value.profile_picture = updatedUrl
      if (me.value) me.value.profile_picture = updatedUrl
    } else {
      alert(data.error || 'Failed to upload profile picture.')
    }
  } catch {
    alert('Failed to upload picture. Check server connection.')
  } finally {
    uploadingAvatar.value = false
    event.target.value = ''
  }
}

async function uploadBanner(event) {
  const file = event.target.files?.[0]
  if (!file) return
  uploadingBanner.value = true
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch('/api/user/upload-banner', {
      method: 'POST',
      credentials: 'include',
      body: formData
    })
    const data = await res.json()
    if (res.ok) {
      const updatedUrl = data.url + '?t=' + Date.now()
      profile.value.banner_image = updatedUrl
    } else {
      alert(data.error || 'Failed to upload banner image.')
    }
  } catch {
    alert('Failed to upload banner. Check server connection.')
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
    } else {
      const err = await res.json()
      alert(err.error || 'Could not send connection request.')
    }
  } catch {}
}

function goBookSession() {
  router.push(`/dashboard?book=${encodeURIComponent(profile.value.username)}`)
}

function copyProfileLink() {
  if (typeof window === 'undefined') return
  const url = `${window.location.origin}/profile?u=${profile.value.username}`
  navigator.clipboard.writeText(url).then(() => {
    linkCopied.value = true
    setTimeout(() => { linkCopied.value = false }, 2500)
  })
}

async function logout() {
  try {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' })
  } catch {}
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('skillloop_auth_active')
  }
  window.location.href = '/login'
}

onMounted(async () => {
  await fetchMe()
  await fetchProfile()
})
</script>
