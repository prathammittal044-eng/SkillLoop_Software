<template>
  <div class="bg-background text-on-surface font-body min-h-screen flex flex-col selection:bg-secondary-container selection:text-on-secondary-container">
    <!-- ==================== 1. TOP NAVIGATION (Pixel-Perfect Match with dashboard.vue) ==================== -->
    <header class="bg-surface-container-low shadow-sm sticky top-0 z-40 print:hidden">
      <div class="flex justify-between items-center w-full px-6 py-3 max-w-7xl mx-auto">
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
            <NuxtLink to="/chat" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1.5 whitespace-nowrap">
              <span class="material-symbols-outlined text-lg">chat</span>
              Chat &amp; Video
            </NuxtLink>
            <NuxtLink to="/quiz" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1 whitespace-nowrap">
              Quiz
            </NuxtLink>
            <NuxtLink to="/leaderboard" class="text-on-surface-variant hover:text-primary transition-colors pb-1 flex items-center gap-1 whitespace-nowrap">
              Leaderboard
            </NuxtLink>
            <span class="text-primary font-bold border-b-2 border-primary pb-1 flex items-center gap-1.5 whitespace-nowrap">
              <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">description</span>
              Resume
            </span>
          </nav>
        </div>

        <div class="flex items-center gap-3 shrink-0">
          <!-- Time Credits Pill (Identical to Dashboard) -->
          <div class="flex items-center gap-1.5 bg-surface-container-lowest px-3 py-1.5 rounded-full border border-secondary-fixed shadow-sm text-sm font-label font-bold text-on-surface whitespace-nowrap shrink-0">
            <span class="material-symbols-outlined text-primary text-lg" style="font-variation-settings: 'FILL' 1;">bolt</span>
            <span>{{ user?.time_credits ?? 5 }} Credits</span>
          </div>

          <!-- Notification Bell (Identical to Dashboard) -->
          <NuxtLink
            to="/dashboard"
            class="relative w-9 h-9 rounded-full bg-surface-container-low border border-surface-container flex items-center justify-center text-on-surface-variant hover:bg-surface-container hover:text-primary transition-colors shrink-0"
            title="Notifications"
          >
            <span class="material-symbols-outlined text-xl">notifications</span>
          </NuxtLink>

          <!-- Avatar (Identical to Dashboard) -->
          <div class="relative w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold text-sm uppercase shadow-sm shrink-0">
            {{ (resume.profile.full_name || user?.full_name || user?.username || 'P').charAt(0) }}
          </div>

          <NuxtLink to="/login" class="text-xs text-on-surface-variant hover:text-error transition-colors font-semibold whitespace-nowrap">
            Logout
          </NuxtLink>
        </div>
      </div>
    </header>

    <!-- ==================== 2. MAIN WORKSPACE = -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-6 md:py-8 space-y-6">

      <!-- Welcome / Status Banner (Matches Dashboard Welcome Banner) -->
      <section class="bg-surface-container-lowest rounded-3xl p-6 sm:p-8 border border-surface-container shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6 relative overflow-hidden print:hidden">
        <div class="relative z-10 space-y-1.5 max-w-2xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-surface-container-low text-primary text-xs font-semibold uppercase tracking-wider font-label mb-1">
            <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            {{ campusNodeLabel }} • Live Portfolio
          </div>
          <h1 class="font-display text-2xl sm:text-3xl font-bold text-on-surface tracking-tight">
            Resume Studio ✨
          </h1>
          <p class="text-on-surface-variant font-body text-sm sm:text-base leading-relaxed">
            Configure your education, verified skills, and project accomplishments into an executive A4 resume.
          </p>
        </div>

        <div class="relative z-10 flex flex-wrap items-center gap-4 shrink-0">
          <div class="bg-surface-container-low px-5 py-3 rounded-2xl border border-secondary-fixed text-right min-w-[130px]">
            <div class="flex items-baseline justify-end gap-1.5">
              <span class="font-display font-extrabold text-2xl text-primary">{{ atsScore }}%</span>
              <span class="text-xs font-semibold text-on-surface-variant">{{ atsStatusLabel }}</span>
            </div>
            <div class="w-32 h-2 bg-surface-container rounded-full overflow-hidden mt-1.5">
              <div class="h-full bg-primary rounded-full transition-all duration-500" :style="`width: ${atsScore}%`"></div>
            </div>
          </div>

          <div class="flex items-center gap-2.5">
            <button
              @click="exportPdf"
              class="px-4 py-2.5 rounded-xl bg-surface-container-lowest text-on-surface hover:text-primary hover:bg-surface-container-low font-headline text-xs font-bold transition-all flex items-center gap-2 border border-surface-container shadow-sm active:scale-95 cursor-pointer whitespace-nowrap"
              title="Download ATS-Friendly PDF"
            >
              <span class="material-symbols-outlined text-lg text-primary">download</span>
              <span>Download PDF</span>
            </button>

            <button
              @click="saveResume"
              :disabled="saving"
              class="px-5 py-2.5 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-sm hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-2 cursor-pointer disabled:opacity-50 whitespace-nowrap"
            >
              <span v-if="saving" class="w-4 h-4 rounded-full border-2 border-on-primary/40 border-t-on-primary animate-spin"></span>
              <span v-else class="material-symbols-outlined text-lg">check</span>
              <span>{{ saving ? 'Saving...' : 'Save Resume' }}</span>
            </button>
          </div>
        </div>
        <div class="absolute -right-16 -top-16 w-48 h-48 bg-secondary-container/30 rounded-full blur-3xl pointer-events-none"></div>
      </section>

      <!-- 2-COLUMN STUDIO WORKBENCH -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

        <!-- ==================== LEFT COLUMN: EDITOR WORKBENCH (5 Cols) ==================== -->
        <div class="lg:col-span-5 flex flex-col gap-4 overflow-y-auto max-h-[calc(100vh-14rem)] pr-1 custom-scroll print:hidden">
          
          <!-- Category Tabs (Consistent Button Style with Dashboard) -->
          <div class="flex items-center gap-2 overflow-x-auto pb-1 text-xs font-headline shrink-0 no-scrollbar">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                activeTab === tab.id
                  ? 'bg-primary text-on-primary font-bold shadow-sm'
                  : 'bg-surface-container-lowest text-on-surface-variant font-semibold hover:text-primary hover:bg-surface-container-low border border-surface-container shadow-xs'
              ]"
              class="px-4 py-2 rounded-xl transition-all flex items-center gap-1.5 shrink-0 cursor-pointer active:scale-95"
            >
              <span class="material-symbols-outlined text-base">{{ tab.icon }}</span>
              <span>{{ tab.label }}</span>
            </button>
          </div>

          <!-- ==================== TAB 1: PROFILE & BIO ==================== -->
          <div v-show="activeTab === 'profile'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center gap-3 pb-3 border-b border-surface-container">
              <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                <span class="material-symbols-outlined text-xl">person</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-base text-on-surface">Personal &amp; Contact Info</h3>
                <p class="text-xs text-on-surface-variant">Binds live to your resume header</p>
              </div>
            </div>

            <div class="space-y-3.5 text-xs sm:text-sm font-body">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Full Name</label>
                  <input
                    v-model="resume.profile.full_name"
                    type="text"
                    placeholder="e.g. Alex Sharma"
                    class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Target Professional Title</label>
                  <input
                    v-model="resume.target_role"
                    type="text"
                    placeholder="e.g. Software Development Engineer"
                    class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Email Address</label>
                  <input
                    v-model="resume.profile.email"
                    type="email"
                    placeholder="e.g. student@university.edu"
                    class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Phone Number</label>
                  <input
                    v-model="resume.profile.phone"
                    type="text"
                    placeholder="e.g. +91 98765 43210"
                    class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">GitHub URL</label>
                  <input
                    v-model="resume.profile.github"
                    type="text"
                    placeholder="github.com/your-username"
                    class="w-full px-3.5 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-xs focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">LinkedIn URL</label>
                  <input
                    v-model="resume.profile.linkedin"
                    type="text"
                    placeholder="linkedin.com/in/your-profile"
                    class="w-full px-3.5 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-xs focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Campus Location</label>
                  <input
                    v-model="resume.profile.location"
                    type="text"
                    placeholder="e.g. New Delhi, India"
                    class="w-full px-3.5 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-xs focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                  />
                </div>
              </div>

              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="block text-xs font-headline font-bold text-on-surface">Executive Summary</label>
                  <button
                    @click="polishWithAi('summary')"
                    :disabled="polishing"
                    type="button"
                    class="text-xs text-primary font-headline font-bold hover:underline flex items-center gap-1 cursor-pointer disabled:opacity-50"
                  >
                    <span class="material-symbols-outlined text-sm">auto_awesome</span>
                    <span>{{ polishing ? 'Polishing...' : 'Polish with AI' }}</span>
                  </button>
                </div>
                <textarea
                  v-model="resume.summary"
                  rows="4"
                  placeholder="Brief summary of your engineering journey, specialties, and campus leadership..."
                  class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all leading-relaxed"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- ==================== TAB 2: EDUCATION & CAMPUS ==================== -->
          <div v-show="activeTab === 'education'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-surface-container">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                  <span class="material-symbols-outlined text-xl">school</span>
                </div>
                <div>
                  <h3 class="font-headline font-bold text-base text-on-surface">Education Details</h3>
                  <p class="text-xs text-on-surface-variant">Configure your college and student status</p>
                </div>
              </div>
              <span class="text-xs font-label font-bold text-primary bg-surface-container-low px-3 py-1 rounded-full border border-secondary-fixed">
                Primary College
              </span>
            </div>

            <div class="space-y-3.5 relative font-body">
              <div>
                <label class="block text-xs font-headline font-bold text-on-surface mb-1">
                  College / University Name <span class="text-primary">*</span>
                </label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-on-surface-variant">
                    <span class="material-symbols-outlined text-lg">apartment</span>
                  </div>
                  <input
                    v-model="eduForm.institution"
                    @focus="showInstDropdown = true"
                    @input="onInstInput"
                    type="text"
                    placeholder="Search college (e.g. ABESIT, IIT, DTU, AKGEC...)"
                    class="w-full pl-10 pr-10 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-body"
                  />
                  <div v-if="eduForm.institution" class="absolute inset-y-0 right-0 pr-3 flex items-center text-primary">
                    <span class="material-symbols-outlined text-lg" style="font-variation-settings: 'FILL' 1;">verified</span>
                  </div>
                </div>

                <!-- Quick Selection Chips -->
                <div class="flex flex-wrap items-center gap-1.5 pt-2">
                  <span class="text-[11px] font-label font-semibold text-on-surface-variant">Quick Pick:</span>
                  <button
                    v-for="chip in popularInstitutions"
                    :key="chip.short"
                    @click="selectInstitution(chip)"
                    type="button"
                    :class="eduForm.institution.includes(chip.short) ? 'bg-primary text-on-primary font-bold shadow-xs' : 'bg-surface-container-low text-on-surface-variant hover:text-primary border border-surface-container font-semibold'"
                    class="px-2.5 py-1 rounded-full text-xs transition-all cursor-pointer"
                  >
                    {{ chip.short }}
                  </button>
                </div>

                <!-- Floating Dropdown -->
                <div
                  v-if="showInstDropdown && (instResults.length > 0 || isSearchingInst || eduForm.institution)"
                  class="absolute left-0 right-0 top-full mt-1.5 bg-surface-container-lowest rounded-2xl border border-secondary-fixed shadow-xl z-50 p-2 space-y-1 max-h-64 overflow-y-auto"
                >
                  <div class="flex items-center justify-between px-2 py-1 text-xs font-label text-on-surface-variant border-b border-surface-container pb-1 mb-1">
                    <span>INSTITUTION MATCHES</span>
                    <button @click="showInstDropdown = false" class="text-on-surface-variant hover:text-primary text-xs">✕ Close</button>
                  </div>

                  <div
                    v-if="eduForm.institution && !instResults.some(r => r.name.toLowerCase() === eduForm.institution.toLowerCase())"
                    @click="selectCustomInst(eduForm.institution)"
                    class="p-2.5 rounded-xl hover:bg-surface-container-low flex items-center gap-2 text-xs font-headline font-bold text-primary cursor-pointer"
                  >
                    <span class="material-symbols-outlined text-sm">add_circle</span>
                    <span>Use custom: &quot;<strong>{{ eduForm.institution }}</strong>&quot;</span>
                  </div>

                  <div
                    v-for="(inst, idx) in instResults"
                    :key="idx"
                    @click="selectInstitution(inst)"
                    class="p-2.5 rounded-xl bg-surface-container-low/60 hover:bg-surface-container border border-surface-container flex items-start gap-3 cursor-pointer transition-colors"
                  >
                    <div class="w-8 h-8 rounded-lg bg-primary text-on-primary flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">
                      {{ inst.short ? inst.short.charAt(0) : 'A' }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center gap-1.5 flex-wrap">
                        <p class="text-xs font-headline font-bold text-on-surface">{{ inst.name }}</p>
                        <span class="px-2 py-0.2 rounded-full text-[10px] font-mono font-bold bg-secondary-container text-on-secondary-container">{{ campusNodeId }}</span>
                      </div>
                      <p class="text-[11px] text-on-surface-variant mt-0.5">{{ inst.location }} <span v-if="inst.affiliation">• {{ inst.affiliation }}</span></p>
                    </div>
                    <span class="material-symbols-outlined text-primary text-lg" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                  </div>
                </div>
              </div>

              <!-- Enrolled Toggle -->
              <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between gap-3">
                <div class="flex items-start gap-3">
                  <input
                    id="enrolled-toggle"
                    type="checkbox"
                    v-model="eduForm.is_current"
                    class="w-4 h-4 text-primary rounded border-outline focus:ring-primary cursor-pointer mt-0.5"
                  />
                  <div>
                    <label for="enrolled-toggle" class="text-xs font-headline font-bold text-on-surface cursor-pointer">
                      I am currently studying / enrolled here
                    </label>
                    <p class="text-[11px] text-on-surface-variant mt-0.5">Students can omit formal degree and display expected graduation.</p>
                  </div>
                </div>
                <span v-if="eduForm.is_current" class="shrink-0 px-2.5 py-1 rounded-full text-xs font-label font-bold bg-secondary-container text-on-secondary-container">
                  Enrolled Student
                </span>
              </div>

              <!-- Degree / Branch -->
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="text-xs font-headline font-bold text-on-surface">Degree / Field of Study</label>
                  <span class="text-[11px] text-on-surface-variant font-body">(Optional for current students)</span>
                </div>
                <input
                  v-model="eduForm.degree"
                  type="text"
                  placeholder="e.g. B.Tech in Computer Science & Engineering"
                  class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                />
              </div>

              <!-- Years -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Start Year</label>
                  <input
                    v-model="eduForm.start_year"
                    type="text"
                    placeholder="2025"
                    class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">
                    {{ eduForm.is_current ? 'Expected Graduation Year' : 'Graduation Year' }}
                  </label>
                  <input
                    v-model="eduForm.end_year"
                    type="text"
                    placeholder="2029"
                    class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                  />
                </div>
              </div>

              <!-- GPA & Coursework -->
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">GPA / Score (Optional)</label>
                  <input
                    v-model="eduForm.grade"
                    type="text"
                    placeholder="8.8 / 10 CGPA"
                    class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-xs font-headline font-bold text-on-surface mb-1">Relevant Coursework</label>
                  <input
                    v-model="eduForm.coursework"
                    type="text"
                    placeholder="Data Structures, OOP (Java), DBMS..."
                    class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-sm focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- ==================== TAB 3: SKILLS & TECHNICALITIES ==================== -->
          <div v-show="activeTab === 'skills'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-5">
            <div class="flex items-center gap-3 pb-3 border-b border-surface-container">
              <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                <span class="material-symbols-outlined text-xl">code</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-base text-on-surface">Technical Competencies</h3>
                <p class="text-xs text-on-surface-variant">Live categorized skills updating instantly on your resume</p>
              </div>
            </div>

            <!-- Languages -->
            <div class="space-y-2.5">
              <div class="flex items-center justify-between">
                <label class="font-headline font-bold text-xs text-on-surface flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-primary"></span>
                  Programming Languages
                </label>
                <span class="text-[11px] font-label text-on-surface-variant">({{ resume.skills.languages.length }} added)</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="(skill, idx) in resume.skills.languages"
                  :key="idx"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-primary border border-secondary-fixed text-xs font-label font-bold shadow-2xs"
                >
                  <span>{{ skill }}</span>
                  <button @click="removeSkillItem('languages', idx)" class="hover:text-error cursor-pointer leading-none font-bold">✕</button>
                </span>
              </div>
              <div class="flex gap-2 pt-1">
                <input
                  v-model="newSkillInput.languages"
                  @keydown.enter.prevent="addSkillItem('languages')"
                  type="text"
                  placeholder="Add language (e.g. Python, Java, C++...)"
                  class="flex-1 px-3.5 py-2 bg-surface-container-low border border-surface-container rounded-xl text-xs text-on-surface focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                />
                <button
                  @click="addSkillItem('languages')"
                  type="button"
                  class="px-4 py-2 bg-primary text-on-primary font-headline text-xs font-bold rounded-xl hover:bg-primary-dim cursor-pointer active:scale-95"
                >
                  Add
                </button>
              </div>
              <div class="flex flex-wrap items-center gap-1">
                <span class="text-[11px] font-label text-on-surface-variant">Quick Pick:</span>
                <button
                  v-for="s in ['Python', 'Java (SE 17/21) ★', 'JavaScript (ES6+)', 'C / C++', 'SQL', 'TypeScript', 'Go', 'Rust']"
                  :key="s"
                  v-show="!resume.skills.languages.includes(s)"
                  @click="quickAddSkill('languages', s)"
                  type="button"
                  class="px-2.5 py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container text-on-surface-variant hover:text-primary text-[11px] font-label font-semibold transition-colors cursor-pointer border border-surface-container"
                >
                  + {{ s }}
                </button>
              </div>
            </div>

            <!-- Web & Frameworks -->
            <div class="space-y-2.5 pt-4 border-t border-surface-container">
              <div class="flex items-center justify-between">
                <label class="font-headline font-bold text-xs text-on-surface flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-secondary"></span>
                  Web &amp; Frameworks
                </label>
                <span class="text-[11px] font-label text-on-surface-variant">({{ resume.skills.frameworks.length }} added)</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="(skill, idx) in resume.skills.frameworks"
                  :key="idx"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-secondary border border-secondary-fixed text-xs font-label font-bold shadow-2xs"
                >
                  <span>{{ skill }}</span>
                  <button @click="removeSkillItem('frameworks', idx)" class="hover:text-error cursor-pointer leading-none font-bold">✕</button>
                </span>
              </div>
              <div class="flex gap-2 pt-1">
                <input
                  v-model="newSkillInput.frameworks"
                  @keydown.enter.prevent="addSkillItem('frameworks')"
                  type="text"
                  placeholder="Add framework (e.g. Vue.js 3, Nuxt 3, Node.js...)"
                  class="flex-1 px-3.5 py-2 bg-surface-container-low border border-surface-container rounded-xl text-xs text-on-surface focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                />
                <button
                  @click="addSkillItem('frameworks')"
                  type="button"
                  class="px-4 py-2 bg-primary text-on-primary font-headline text-xs font-bold rounded-xl hover:bg-primary-dim cursor-pointer active:scale-95"
                >
                  Add
                </button>
              </div>
              <div class="flex flex-wrap items-center gap-1">
                <span class="text-[11px] font-label text-on-surface-variant">Quick Pick:</span>
                <button
                  v-for="s in ['Vue.js 3', 'Nuxt 3', 'Tailwind CSS', 'Node.js', 'RESTful APIs', 'React', 'FastAPI', 'Express']"
                  :key="s"
                  v-show="!resume.skills.frameworks.includes(s)"
                  @click="quickAddSkill('frameworks', s)"
                  type="button"
                  class="px-2.5 py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container text-on-surface-variant hover:text-primary text-[11px] font-label font-semibold transition-colors cursor-pointer border border-surface-container"
                >
                  + {{ s }}
                </button>
              </div>
            </div>

            <!-- Tools & DevOps -->
            <div class="space-y-2.5 pt-4 border-t border-surface-container">
              <div class="flex items-center justify-between">
                <label class="font-headline font-bold text-xs text-on-surface flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-tertiary"></span>
                  Tools &amp; DevOps
                </label>
                <span class="text-[11px] font-label text-on-surface-variant">({{ resume.skills.tools.length }} added)</span>
              </div>
              <div class="flex flex-wrap gap-1.5">
                <span
                  v-for="(skill, idx) in resume.skills.tools"
                  :key="idx"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low text-tertiary border border-surface-container text-xs font-label font-bold shadow-2xs"
                >
                  <span>{{ skill }}</span>
                  <button @click="removeSkillItem('tools', idx)" class="hover:text-error cursor-pointer leading-none font-bold">✕</button>
                </span>
              </div>
              <div class="flex gap-2 pt-1">
                <input
                  v-model="newSkillInput.tools"
                  @keydown.enter.prevent="addSkillItem('tools')"
                  type="text"
                  placeholder="Add tool (e.g. Git, Linux, Docker, Postman...)"
                  class="flex-1 px-3.5 py-2 bg-surface-container-low border border-surface-container rounded-xl text-xs text-on-surface focus:bg-surface-container-lowest focus:border-primary focus:outline-none"
                />
                <button
                  @click="addSkillItem('tools')"
                  type="button"
                  class="px-4 py-2 bg-primary text-on-primary font-headline text-xs font-bold rounded-xl hover:bg-primary-dim cursor-pointer active:scale-95"
                >
                  Add
                </button>
              </div>
              <div class="flex flex-wrap items-center gap-1">
                <span class="text-[11px] font-label text-on-surface-variant">Quick Pick:</span>
                <button
                  v-for="s in ['Git / GitHub', 'Linux (Ubuntu / Arch)', 'Docker Basics', 'Postman', 'Vite', 'Kubernetes', 'AWS']"
                  :key="s"
                  v-show="!resume.skills.tools.includes(s)"
                  @click="quickAddSkill('tools', s)"
                  type="button"
                  class="px-2.5 py-0.5 rounded-full bg-surface-container-low hover:bg-surface-container text-on-surface-variant hover:text-primary text-[11px] font-label font-semibold transition-colors cursor-pointer border border-surface-container"
                >
                  + {{ s }}
                </button>
              </div>
            </div>
          </div>

          <!-- ==================== TAB 4: PROJECTS ==================== -->
          <div v-show="activeTab === 'projects'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-surface-container">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                  <span class="material-symbols-outlined text-xl">rocket_launch</span>
                </div>
                <div>
                  <h3 class="font-headline font-bold text-base text-on-surface">Engineering Projects</h3>
                  <p class="text-xs text-on-surface-variant">Highlight coding builds and repository links</p>
                </div>
              </div>
              <button
                @click="openProjModal()"
                class="px-4 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-sm hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-1.5 cursor-pointer"
              >
                <span class="material-symbols-outlined text-sm">add</span>
                <span>Add Project</span>
              </button>
            </div>

            <div v-if="resume.projects && resume.projects.length > 0" class="space-y-3">
              <div
                v-for="(proj, idx) in resume.projects"
                :key="idx"
                class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-start justify-between gap-3"
              >
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h4 class="font-headline font-bold text-sm text-on-surface">{{ proj.title }}</h4>
                    <span v-if="proj.link" class="text-xs font-mono text-primary flex items-center gap-0.5">
                      <span>[{{ proj.link }}]</span>
                    </span>
                  </div>
                  <p class="text-xs font-mono text-on-surface-variant mt-0.5">{{ proj.year || '2025' }}</p>
                  <p class="text-xs text-on-surface-variant mt-1.5 font-body leading-relaxed">{{ proj.description }}</p>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <button @click="openProjModal(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">edit</span>
                  </button>
                  <button @click="deleteProj(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-error transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">delete</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 border-2 border-dashed border-surface-container rounded-2xl text-on-surface-variant text-xs">
              No projects added yet. Click &quot;Add Project&quot; to highlight your coding repos.
            </div>
          </div>

          <!-- ==================== TAB 5: EXPERIENCE ==================== -->
          <div v-show="activeTab === 'experience'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-surface-container">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                  <span class="material-symbols-outlined text-xl">work</span>
                </div>
                <div>
                  <h3 class="font-headline font-bold text-base text-on-surface">Experience &amp; Internships</h3>
                  <p class="text-xs text-on-surface-variant">Campus roles, internships, and work history</p>
                </div>
              </div>
              <button
                @click="openExpModal()"
                class="px-4 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-sm hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-1.5 cursor-pointer"
              >
                <span class="material-symbols-outlined text-sm">add</span>
                <span>Add Position</span>
              </button>
            </div>

            <div v-if="resume.experiences && resume.experiences.length > 0" class="space-y-3">
              <div
                v-for="(exp, idx) in resume.experiences"
                :key="idx"
                class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-start justify-between gap-3"
              >
                <div>
                  <h4 class="font-headline font-bold text-sm text-on-surface">{{ exp.title }}</h4>
                  <p class="text-xs text-primary font-semibold">{{ exp.company }} <span v-if="exp.location">• {{ exp.location }}</span></p>
                  <p class="text-xs font-mono text-on-surface-variant mt-0.5">{{ exp.start_date }} — {{ exp.end_date || 'Present' }}</p>
                  <p class="text-xs text-on-surface-variant mt-1.5 font-body leading-relaxed">{{ exp.description }}</p>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <button @click="openExpModal(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">edit</span>
                  </button>
                  <button @click="deleteExp(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-error transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">delete</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 border-2 border-dashed border-surface-container rounded-2xl text-on-surface-variant text-xs">
              No work experience added yet. Click &quot;Add Position&quot; to include internships.
            </div>
          </div>

          <!-- ==================== TAB 6: CERTIFICATIONS ==================== -->
          <div v-show="activeTab === 'certifications'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-surface-container">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                  <span class="material-symbols-outlined text-xl">verified</span>
                </div>
                <div>
                  <h3 class="font-headline font-bold text-base text-on-surface">Certificates &amp; Badges</h3>
                  <p class="text-xs text-on-surface-variant">Cloud badges, NPTEL, and external exams</p>
                </div>
              </div>
              <button
                @click="openCertModal()"
                class="px-4 py-2 rounded-xl bg-primary text-on-primary font-headline text-xs font-bold shadow-sm hover:bg-primary-dim active:scale-95 transition-all flex items-center gap-1.5 cursor-pointer"
              >
                <span class="material-symbols-outlined text-sm">add</span>
                <span>Add Cert</span>
              </button>
            </div>

            <div v-if="resume.certifications && resume.certifications.length > 0" class="space-y-3">
              <div
                v-for="(cert, idx) in resume.certifications"
                :key="idx"
                class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-start justify-between gap-3"
              >
                <div>
                  <h4 class="font-headline font-bold text-sm text-on-surface">{{ cert.name }}</h4>
                  <p class="text-xs text-primary font-semibold">{{ cert.issuer }} <span v-if="cert.issue_date">• {{ cert.issue_date }}</span></p>
                </div>
                <div class="flex items-center gap-1 shrink-0">
                  <button @click="openCertModal(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-primary transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">edit</span>
                  </button>
                  <button @click="deleteCert(idx)" class="p-1.5 rounded-lg bg-surface-container-lowest hover:bg-surface-container text-on-surface-variant hover:text-error transition-colors cursor-pointer">
                    <span class="material-symbols-outlined text-base">delete</span>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-8 border-2 border-dashed border-surface-container rounded-2xl text-on-surface-variant text-xs">
              No certifications added yet. Click &quot;Add Cert&quot; to include them.
            </div>
          </div>

          <!-- ==================== TAB 7: PRIVACY & SETTINGS ==================== -->
          <div v-show="activeTab === 'privacy'" class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container shadow-sm space-y-4">
            <div class="flex items-center gap-3 pb-3 border-b border-surface-container">
              <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold">
                <span class="material-symbols-outlined text-xl">tune</span>
              </div>
              <div>
                <h3 class="font-headline font-bold text-base text-on-surface">Privacy &amp; Teaching Display</h3>
                <p class="text-xs text-on-surface-variant">Control your peer mentorship visibility</p>
              </div>
            </div>

            <div class="space-y-4">
              <div class="p-4 rounded-2xl bg-surface-container-low border border-surface-container flex items-center justify-between gap-4">
                <div>
                  <h4 class="font-headline font-bold text-sm text-on-surface">Include Skills I Teach</h4>
                  <p class="text-xs text-on-surface-variant mt-0.5">Showcase your peer tutoring hours and verified subject mastery</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input type="checkbox" v-model="resume.settings.show_teaching_skills" class="sr-only peer" />
                  <div class="w-11 h-6 bg-surface-container rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                </label>
              </div>

              <div>
                <label class="block text-xs font-headline font-bold text-on-surface mb-1">Peer Mentorship Statement</label>
                <textarea
                  v-model="resume.mentorship_desc"
                  rows="3"
                  placeholder="Describe your campus mentorship and peer tutoring contributions..."
                  class="w-full px-4 py-2.5 bg-surface-container-low border border-surface-container rounded-xl text-on-surface text-xs focus:bg-surface-container-lowest focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all font-body leading-relaxed"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- DYNAMIC PEER-TO-PEER NETWORK CARD (Directly below editor) -->
          <div class="bg-surface-container-lowest rounded-3xl p-5 border border-surface-container shadow-sm space-y-3 shrink-0">
            <div class="flex items-start gap-3">
              <div class="w-10 h-10 rounded-2xl bg-surface-container-low text-primary flex items-center justify-center font-bold shrink-0">
                <span class="material-symbols-outlined text-xl">hub</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h4 class="font-headline font-bold text-sm text-on-surface">SkillLoop Network Integration</h4>
                  <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-secondary-container text-on-secondary-container">P2P LEDGER</span>
                </div>
                <p class="text-xs text-on-surface-variant mt-0.5 font-body">
                  Your public resume links cryptographically to your timebank ledger and peer reviews.
                </p>
              </div>
            </div>

            <div class="pt-3 border-t border-surface-container flex items-center justify-between gap-4">
              <span class="text-xs font-headline font-bold text-on-surface">Include Skills I Teach</span>
              <label class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="resume.settings.show_teaching_skills" class="sr-only peer" />
                <div class="w-11 h-6 bg-surface-container rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>

            <div class="flex items-center gap-2 text-xs text-on-surface font-mono bg-surface-container-low px-3 py-2 rounded-xl border border-secondary-fixed">
              <span class="material-symbols-outlined text-primary text-base">verified</span>
              <span>{{ user?.time_credits || 0 }} hrs taught &amp; 5.0★ peer review rating attached</span>
            </div>
          </div>

        </div>

        <!-- ==================== RIGHT COLUMN: LIVE DOCUMENT CANVAS (7 Cols) ==================== -->
        <div class="lg:col-span-7 flex flex-col gap-4 overflow-y-auto max-h-[calc(100vh-14rem)] custom-scroll">
          
          <!-- Canvas Controls Bar -->
          <div class="bg-surface-container-lowest rounded-2xl p-3 px-5 border border-surface-container shadow-xs flex flex-wrap items-center justify-between gap-3 print:hidden">
            <div class="flex items-center gap-2 whitespace-nowrap">
              <span class="w-2.5 h-2.5 rounded-full bg-primary animate-pulse"></span>
              <span class="text-xs font-headline font-bold text-on-surface">Live Preview • A4 Sheet</span>
              <span class="text-[11px] font-mono text-on-surface-variant">| 210 × 297 mm</span>
            </div>

            <!-- Template Switcher (Matches Dashboard pill style) -->
            <div class="flex items-center bg-surface-container-low p-1 rounded-xl text-xs font-headline font-semibold border border-surface-container whitespace-nowrap">
              <button
                @click="resume.settings.template = 'modern'"
                :class="resume.settings.template === 'modern' ? 'bg-surface-container-lowest text-primary font-bold shadow-xs' : 'text-on-surface-variant hover:text-primary'"
                class="px-3 py-1.5 rounded-lg transition-all cursor-pointer whitespace-nowrap"
              >
                Executive Modern
              </button>
              <button
                @click="resume.settings.template = 'ats'"
                :class="resume.settings.template === 'ats' ? 'bg-surface-container-lowest text-primary font-bold shadow-xs' : 'text-on-surface-variant hover:text-primary'"
                class="px-3 py-1.5 rounded-lg transition-all cursor-pointer whitespace-nowrap"
              >
                Classic ATS
              </button>
            </div>

            <!-- Zoom & Action Buttons -->
            <div class="flex items-center gap-2 whitespace-nowrap">
              <div class="flex items-center gap-1 bg-surface-container-low border border-surface-container rounded-xl px-2.5 py-1 text-xs text-on-surface font-mono">
                <button @click="zoomOut" class="hover:text-primary font-bold p-0.5 cursor-pointer">-</button>
                <span class="px-1 text-xs font-bold">{{ zoomLevel }}%</span>
                <button @click="zoomIn" class="hover:text-primary font-bold p-0.5 cursor-pointer">+</button>
              </div>

              <button
                @click="exportPdf"
                class="px-3 py-1.5 rounded-xl bg-surface-container-low text-on-surface hover:text-primary border border-surface-container text-xs font-headline font-bold flex items-center gap-1 cursor-pointer transition-colors whitespace-nowrap"
                title="Download PDF"
              >
                <span class="material-symbols-outlined text-base">download</span>
                <span class="hidden sm:inline">PDF</span>
              </button>

              <button
                @click="saveResume"
                :disabled="saving"
                class="px-3.5 py-1.5 rounded-xl bg-primary text-on-primary text-xs font-headline font-bold flex items-center gap-1 cursor-pointer hover:bg-primary-dim transition-colors whitespace-nowrap disabled:opacity-50"
              >
                <span v-if="saving" class="w-3 h-3 rounded-full border-2 border-on-primary/40 border-t-on-primary animate-spin"></span>
                <span v-else class="material-symbols-outlined text-base">check</span>
                <span>Save</span>
              </button>
            </div>
          </div>

          <!-- Canvas Desk (Soft Lavender Ambient Background, Not Cold Slate!) -->
          <div class="bg-surface-container-low rounded-3xl p-4 sm:p-8 border border-surface-container shadow-inner flex justify-center items-start overflow-x-auto min-h-[920px]">
            
            <!-- ==================== TEMPLATE 1: EXECUTIVE MODERN ==================== -->
            <div
              v-if="resume.settings.template === 'modern'"
              id="resume-a4-sheet"
              :style="{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top center' }"
              class="w-full max-w-[820px] bg-surface-container-lowest rounded-2xl shadow-xl p-8 sm:p-12 relative text-on-surface transition-all duration-200"
            >
              <!-- Top Accent Ribbon -->
              <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-primary via-secondary to-primary-container rounded-t-2xl"></div>

              <!-- Header -->
              <div class="border-b border-surface-container pb-5 mb-5">
                <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2">
                  <div>
                    <h1 class="font-display font-extrabold text-3xl sm:text-4xl text-on-surface tracking-tight">
                      {{ resume.profile.full_name || user?.full_name || user?.username || 'Your Name' }}
                    </h1>
                    <p class="font-headline font-bold text-base sm:text-lg text-primary mt-1">
                      {{ resume.target_role || (user?.department ? `${user.department} Specialist & Peer Mentor` : 'Campus Peer Lead') }}
                    </p>
                  </div>
                  <div class="text-right sm:self-center">
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-surface-container-low border border-secondary-fixed text-primary text-xs font-label font-bold">
                      <span class="w-2 h-2 rounded-full bg-primary"></span>
                      {{ campusNodeLabel }}
                    </span>
                  </div>
                </div>

                <!-- Contact Strip -->
                <div class="flex flex-wrap items-center gap-y-1.5 gap-x-3 mt-3.5 text-xs text-on-surface-variant font-body">
                  <a v-if="resume.profile.email || user?.email" :href="`mailto:${resume.profile.email || user?.email}`" class="flex items-center gap-1 hover:text-primary">
                    <span class="material-symbols-outlined text-[15px]">mail</span>
                    <span>{{ resume.profile.email || user?.email }}</span>
                  </a>
                  <span v-if="(resume.profile.email || user?.email) && resume.profile.phone" class="text-surface-variant">•</span>
                  <span v-if="resume.profile.phone" class="flex items-center gap-1">
                    <span class="material-symbols-outlined text-[15px]">call</span>
                    <span>{{ resume.profile.phone }}</span>
                  </span>
                  <span v-if="resume.profile.github" class="text-surface-variant">•</span>
                  <a v-if="resume.profile.github" :href="`https://${resume.profile.github.replace(/^https?:\/\//, '')}`" target="_blank" class="flex items-center gap-1 hover:text-primary">
                    <span class="material-symbols-outlined text-[15px]">code</span>
                    <span>{{ resume.profile.github }}</span>
                  </a>
                  <span v-if="resume.profile.linkedin" class="text-surface-variant">•</span>
                  <a v-if="resume.profile.linkedin" :href="`https://${resume.profile.linkedin.replace(/^https?:\/\//, '')}`" target="_blank" class="flex items-center gap-1 hover:text-primary">
                    <span class="material-symbols-outlined text-[15px]">link</span>
                    <span>{{ resume.profile.linkedin }}</span>
                  </a>
                  <span v-if="resume.profile.location" class="text-surface-variant">•</span>
                  <span v-if="resume.profile.location" class="flex items-center gap-1 text-on-surface-variant">
                    <span class="material-symbols-outlined text-[15px]">location_on</span>
                    <span>{{ resume.profile.location }}</span>
                  </span>
                </div>
              </div>

              <!-- Summary -->
              <div class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-1.5">Executive Summary</h3>
                <p class="text-xs sm:text-sm text-on-surface leading-relaxed text-justify font-body">
                  {{ resume.summary }}
                </p>
              </div>

              <!-- Verified Competencies Box -->
              <div class="mb-5 p-4 rounded-2xl bg-surface-container-low border border-secondary-fixed relative overflow-hidden">
                <div class="flex flex-wrap items-center justify-between gap-2 border-b border-surface-container pb-2 mb-2.5">
                  <div class="flex items-center gap-1.5 text-primary font-headline font-bold text-xs tracking-wider">
                    <span class="material-symbols-outlined text-base">verified_user</span>
                    <span>SKILLLOOP VERIFIED COMPETENCIES</span>
                  </div>
                  <span class="font-mono text-[10px] text-on-surface-variant bg-surface-container-lowest px-2 py-0.5 rounded-full border border-surface-container">
                    Hash: {{ protocolHash }} • {{ campusNodeLabel }}
                  </span>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                  <!-- Real Verified Skills from DB -->
                  <template v-if="verifications.length > 0">
                    <div 
                      v-for="v in verifications.slice(0, 2)" 
                      :key="v.skill_name"
                      class="bg-surface-container-lowest rounded-xl p-2.5 border border-surface-container shadow-2xs flex items-start gap-2"
                    >
                      <span class="material-symbols-outlined text-primary text-lg shrink-0 mt-0.5" style="font-variation-settings: 'FILL' 1;">
                        {{ v.is_active ? 'verified' : 'history_toggle_off' }}
                      </span>
                      <div class="min-w-0">
                        <p class="text-xs font-headline font-bold text-on-surface capitalize truncate">{{ v.skill_name }}</p>
                        <p class="text-[10px] font-mono text-on-surface-variant">Level: {{ v.verified_level }} • {{ v.activity_type === 'aee_session' ? 'A.E.E. Proof' : 'Quiz Proctored' }}</p>
                        <span 
                          class="inline-block mt-1 px-1.5 py-0.2 rounded-full text-[9px] font-bold"
                          :class="v.is_active ? 'bg-secondary-container text-on-secondary-container' : 'bg-surface-container text-on-surface-variant'"
                        >
                          {{ v.is_active ? `Active (${v.days_remaining}d)` : 'Dormant' }}
                        </span>
                      </div>
                    </div>
                  </template>

                  <!-- Empty state prompt if no verified skills -->
                  <div v-else class="sm:col-span-2 bg-surface-container-lowest rounded-xl p-2.5 border border-dashed border-surface-container flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <span class="material-symbols-outlined text-primary text-base">quiz</span>
                      <p class="text-xs text-on-surface-variant font-body">No skills verified yet. Pass a 15-second benchmark quiz to attach verified credentials here.</p>
                    </div>
                    <NuxtLink to="/quiz" class="px-2.5 py-1 rounded-lg bg-primary text-on-primary text-[10px] font-bold font-headline whitespace-nowrap">Verify Skill</NuxtLink>
                  </div>

                  <!-- Live TimeBank Escrow Card -->
                  <div class="bg-surface-container-lowest rounded-xl p-2.5 border border-surface-container shadow-2xs flex items-start gap-2">
                    <span class="material-symbols-outlined text-primary text-lg shrink-0 mt-0.5" style="font-variation-settings: 'FILL' 1;">schedule</span>
                    <div>
                      <p class="text-xs font-headline font-bold text-on-surface">TimeBank Escrow</p>
                      <p class="text-[10px] font-mono text-on-surface-variant">{{ user?.time_credits ?? 5 }} credits • {{ user?.total_sessions || 0 }} sessions</p>
                      <span class="inline-block mt-1 px-1.5 py-0.2 rounded-full text-[9px] font-bold bg-secondary-container text-on-secondary-container">
                        {{ user?.rating_avg ? `${user.rating_avg}★ Peer Rating` : 'Verified Campus Node' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Education -->
              <div class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Education &amp; Campus Credentials
                </h3>
                <div class="flex items-start justify-between gap-4 font-body">
                  <div>
                    <div class="flex items-center gap-2 flex-wrap">
                      <h4 class="font-headline font-bold text-sm text-on-surface">
                        {{ eduForm.institution || user?.education || 'University / Institution' }}
                      </h4>
                      <span v-if="resume.profile.location" class="px-2 py-0.5 rounded-full text-[10px] font-label font-bold bg-surface-container-low text-primary border border-secondary-fixed">
                        {{ resume.profile.location }}
                      </span>
                    </div>
                    <p class="text-xs font-semibold text-on-surface-variant mt-0.5">
                      <span v-if="eduForm.degree" class="text-on-surface font-bold">{{ eduForm.degree }}</span>
                      <span v-else-if="eduForm.is_current" class="text-primary font-bold">Enrolled Undergraduate Student</span>
                      <span v-if="eduForm.grade"> • <span class="text-primary font-bold">CGPA: {{ eduForm.grade }}</span></span>
                    </p>
                    <p v-if="eduForm.coursework" class="text-[11px] text-on-surface-variant mt-1 leading-relaxed">
                      Relevant Coursework: {{ eduForm.coursework }}
                    </p>
                  </div>
                  <div class="text-right shrink-0">
                    <span class="font-mono text-xs font-bold text-on-surface bg-surface-container-low px-2.5 py-1 rounded-full border border-surface-container">
                      {{ eduForm.start_year || defaultStartYear }} — {{ eduForm.is_current ? 'Present' : (eduForm.end_year || defaultEndYear) }}
                      <span v-if="eduForm.is_current && eduForm.end_year" class="text-on-surface-variant"> (Exp. {{ eduForm.end_year }})</span>
                    </span>
                    <p v-if="eduForm.is_current" class="text-[10px] font-headline font-bold text-primary mt-1">
                      ● Active Student
                    </p>
                  </div>
                </div>
              </div>

              <!-- Technical Competencies -->
              <div class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Technical Competencies
                </h3>
                <div class="space-y-2 text-xs font-body">
                  <div v-if="resume.skills.languages.length > 0" class="flex items-baseline gap-2">
                    <span class="font-headline font-bold text-on-surface w-32 shrink-0">Languages:</span>
                    <div class="flex flex-wrap gap-1.5">
                      <span
                        v-for="(skill, i) in resume.skills.languages"
                        :key="i"
                        class="px-2.5 py-0.5 rounded-full bg-surface-container-low text-primary border border-secondary-fixed font-mono text-[11px] font-semibold"
                      >
                        {{ skill }}
                      </span>
                    </div>
                  </div>

                  <div v-if="resume.skills.frameworks.length > 0" class="flex items-baseline gap-2">
                    <span class="font-headline font-bold text-on-surface w-32 shrink-0">Frameworks:</span>
                    <div class="flex flex-wrap gap-1.5">
                      <span
                        v-for="(skill, i) in resume.skills.frameworks"
                        :key="i"
                        class="px-2.5 py-0.5 rounded-full bg-surface-container-low text-secondary border border-surface-container font-mono text-[11px]"
                      >
                        {{ skill }}
                      </span>
                    </div>
                  </div>

                  <div v-if="resume.skills.tools.length > 0" class="flex items-baseline gap-2">
                    <span class="font-headline font-bold text-on-surface w-32 shrink-0">Tools &amp; DevOps:</span>
                    <div class="flex flex-wrap gap-1.5">
                      <span
                        v-for="(skill, i) in resume.skills.tools"
                        :key="i"
                        class="px-2.5 py-0.5 rounded-full bg-surface-container-low text-tertiary border border-surface-container font-mono text-[11px]"
                      >
                        {{ skill }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Projects -->
              <div v-if="resume.projects && resume.projects.length > 0" class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Engineering Projects
                </h3>
                <div class="space-y-3 font-body">
                  <div v-for="(proj, i) in resume.projects" :key="i" class="space-y-1">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <h4 class="font-headline font-bold text-sm text-on-surface">{{ proj.title }}</h4>
                        <a v-if="proj.link" :href="`https://${proj.link.replace(/^https?:\/\//, '')}`" target="_blank" class="text-xs font-mono text-primary hover:underline flex items-center gap-0.5">
                          <span>[{{ proj.link }}]</span>
                          <span class="material-symbols-outlined text-[13px]">open_in_new</span>
                        </a>
                      </div>
                      <span class="font-mono text-xs text-on-surface-variant">{{ proj.year || '2025' }}</span>
                    </div>
                    <p class="text-xs text-on-surface-variant leading-relaxed">{{ proj.description }}</p>
                  </div>
                </div>
              </div>

              <!-- Experience -->
              <div v-if="resume.experiences && resume.experiences.length > 0" class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Work Experience
                </h3>
                <div class="space-y-3 font-body">
                  <div v-for="(exp, i) in resume.experiences" :key="i" class="space-y-1">
                    <div class="flex items-center justify-between">
                      <div>
                        <h4 class="font-headline font-bold text-sm text-on-surface">{{ exp.title }}</h4>
                        <p class="text-xs text-primary font-semibold">{{ exp.company }} <span v-if="exp.location">• {{ exp.location }}</span></p>
                      </div>
                      <span class="font-mono text-xs text-on-surface-variant">{{ exp.start_date }} — {{ exp.end_date || 'Present' }}</span>
                    </div>
                    <p class="text-xs text-on-surface-variant leading-relaxed">{{ exp.description }}</p>
                  </div>
                </div>
              </div>

              <!-- Certifications -->
              <div v-if="resume.certifications && resume.certifications.length > 0" class="mb-5">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Certifications
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                  <div v-for="(cert, i) in resume.certifications" :key="i" class="p-2.5 rounded-xl bg-surface-container-low border border-surface-container">
                    <p class="font-headline font-bold text-on-surface">{{ cert.name }}</p>
                    <p class="text-[11px] text-primary mt-0.5">{{ cert.issuer }} <span v-if="cert.issue_date">• {{ cert.issue_date }}</span></p>
                  </div>
                </div>
              </div>

              <!-- Mentorship -->
              <div v-if="resume.settings.show_teaching_skills">
                <h3 class="font-headline font-bold text-xs uppercase tracking-wider text-on-surface-variant mb-2 border-b border-surface-container pb-1">
                  Campus Leadership &amp; Peer Mentorship
                </h3>
                <div class="font-body">
                  <div class="flex items-baseline justify-between">
                    <h4 class="font-headline font-bold text-sm text-on-surface">
                      Campus Peer Mentor in {{ teaches.length > 0 ? teaches.slice(0, 2).join(' & ') : (user?.department || 'Peer Skills') }}
                    </h4>
                    <span class="font-mono text-xs text-on-surface-variant">SkillLoop {{ campusNodeId }} ({{ (eduForm.institution || user?.department || 'Campus').split(' ')[0] }})</span>
                  </div>
                  <p class="text-xs text-on-surface-variant font-medium mt-0.5 leading-relaxed">
                    {{ resume.mentorship_desc || 'Conducted 10+ hours of 1-on-1 peer code reviews, debugging sessions, and algorithm walkthroughs with 100% positive learner evaluations and zero disputes.' }}
                  </p>
                  <div v-if="teaches.length > 0" class="flex items-center gap-1.5 mt-2 flex-wrap">
                    <span class="text-xs text-on-surface-variant font-semibold">Verified teaching skills:</span>
                    <span v-for="t in teaches" :key="t" class="px-2.5 py-0.5 rounded-full text-[11px] font-bold"
                      :class="getSkillVerif(t)?.is_active ? 'bg-secondary-container text-on-secondary-container' : 'bg-surface-container text-on-surface-variant/70'">
                      {{ t }}
                      <span v-if="getSkillVerif(t)?.is_active" class="text-[9px] text-emerald-700 ml-1">✓ Active ({{ getSkillVerif(t)?.days_remaining }}d)</span>
                      <span v-else-if="getSkillVerif(t)?.decay_status === 'decayed'" class="text-[9px] text-slate-500 ml-1">(Dormant)</span>
                    </span>
                  </div>
                </div>
              </div>

              <!-- Footprint -->
              <div class="mt-8 pt-3 border-t border-surface-container flex items-center justify-between text-[10px] font-mono text-on-surface-variant">
                <span>SkillLoop Cryptographic Signature Attached • Verified Campus Registry</span>
                <span>Document ID: {{ documentId }}</span>
              </div>
            </div>

            <!-- ==================== TEMPLATE 2: CLASSIC ATS ==================== -->
            <div
              v-else
              id="resume-a4-sheet"
              :style="{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top center' }"
              class="w-full max-w-[820px] bg-white rounded-xl shadow-xl p-8 sm:p-12 relative text-slate-900 font-sans transition-all duration-200"
            >
              <!-- ATS Header -->
              <div class="text-center border-b-2 border-slate-900 pb-4 mb-4">
                <h1 class="font-serif font-bold text-2xl sm:text-3xl text-slate-950 uppercase tracking-wide">
                  {{ resume.profile.full_name || user?.full_name || user?.username || 'Your Name' }}
                </h1>
                <p class="text-sm font-semibold text-slate-800 mt-1">
                  {{ resume.target_role || (user?.department ? user.department + ' Student' : 'Undergraduate Student') }}
                </p>
                <div class="flex items-center justify-center gap-3 text-xs text-slate-600 mt-2 flex-wrap font-sans">
                  <span v-if="resume.profile.email || user?.email">{{ resume.profile.email || user?.email }}</span>
                  <span>|</span>
                  <span v-if="resume.profile.phone">{{ resume.profile.phone }}</span>
                  <span>|</span>
                  <span v-if="resume.profile.location">{{ resume.profile.location }}</span>
                  <span>|</span>
                  <span v-if="resume.profile.linkedin">{{ resume.profile.linkedin }}</span>
                </div>
              </div>

              <div class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Summary
                </h3>
                <p class="text-xs text-slate-800 leading-relaxed text-justify">
                  {{ resume.summary }}
                </p>
              </div>

              <div class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Education
                </h3>
                <div class="flex justify-between items-baseline text-xs">
                  <div>
                    <span class="font-bold text-slate-900">{{ eduForm.institution || user?.education || 'University / Institution' }}</span>
                    <span v-if="eduForm.degree"> — {{ eduForm.degree }}</span>
                    <span v-else-if="eduForm.is_current" class="italic"> (Enrolled Student)</span>
                    <span v-if="eduForm.grade"> (CGPA: {{ eduForm.grade }})</span>
                  </div>
                  <span class="text-slate-600 font-mono">
                    {{ eduForm.start_year || defaultStartYear }} – {{ eduForm.is_current ? 'Present' : (eduForm.end_year || defaultEndYear) }}
                  </span>
                </div>
                <p v-if="eduForm.coursework" class="text-[11px] text-slate-600 mt-0.5">
                  Relevant Coursework: {{ eduForm.coursework }}
                </p>
              </div>

              <div class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Technical Skills
                </h3>
                <div class="text-xs space-y-1">
                  <p v-if="resume.skills.languages.length > 0">
                    <span class="font-bold">Languages:</span> {{ resume.skills.languages.join(', ') }}
                  </p>
                  <p v-if="resume.skills.frameworks.length > 0">
                    <span class="font-bold">Frameworks &amp; Web:</span> {{ resume.skills.frameworks.join(', ') }}
                  </p>
                  <p v-if="resume.skills.tools.length > 0">
                    <span class="font-bold">Tools &amp; Platforms:</span> {{ resume.skills.tools.join(', ') }}
                  </p>
                </div>
              </div>

              <div v-if="resume.projects && resume.projects.length > 0" class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Projects
                </h3>
                <div class="space-y-2 text-xs">
                  <div v-for="(p, i) in resume.projects" :key="i">
                    <div class="flex justify-between font-bold">
                      <span>{{ p.title }} <span v-if="p.link" class="font-normal text-slate-600">({{ p.link }})</span></span>
                      <span class="font-normal text-slate-600">{{ p.year }}</span>
                    </div>
                    <p class="text-slate-700 mt-0.5">{{ p.description }}</p>
                  </div>
                </div>
              </div>

              <div v-if="resume.experiences && resume.experiences.length > 0" class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Experience
                </h3>
                <div class="space-y-2 text-xs">
                  <div v-for="(e, i) in resume.experiences" :key="i">
                    <div class="flex justify-between font-bold">
                      <span>{{ e.title }} — {{ e.company }}</span>
                      <span class="font-normal text-slate-600">{{ e.start_date }} – {{ e.end_date || 'Present' }}</span>
                    </div>
                    <p class="text-slate-700 mt-0.5">{{ e.description }}</p>
                  </div>
                </div>
              </div>

              <div v-if="resume.settings.show_teaching_skills" class="mb-4">
                <h3 class="font-serif font-bold text-xs uppercase tracking-wider text-slate-900 border-b border-slate-300 pb-0.5 mb-1">
                  Campus Leadership &amp; Peer Mentorship
                </h3>
                <p class="text-xs text-slate-800">
                  {{ resume.mentorship_desc || ('Campus Peer Mentor on SkillLoop Protocol' + (teaches.length > 0 ? (' in ' + teaches.join(', ')) : '') + '. Conducted verified peer reviews and technical mentoring.') }}
                </p>
              </div>
            </div>

          </div>
        </div>

      </div>
    </main>

    <!-- ==================== EXPERIENCE MODAL ==================== -->
    <div v-if="expModal.open" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container max-w-lg w-full space-y-4 shadow-2xl text-on-surface">
        <div class="flex items-center justify-between border-b border-surface-container pb-3">
          <h3 class="font-headline font-bold text-base text-on-surface">
            {{ expModal.isEdit ? 'Edit Experience' : 'Add Experience' }}
          </h3>
          <button @click="expModal.open = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">✕</button>
        </div>
        <div class="space-y-3 text-xs sm:text-sm font-body">
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Job Title *</label>
            <input v-model="expModal.form.title" type="text" placeholder="e.g. Frontend Developer Intern" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Company / Organization *</label>
            <input v-model="expModal.form.company" type="text" placeholder="e.g. TechCorp Labs" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-headline font-bold text-on-surface mb-1">Start Date</label>
              <input v-model="expModal.form.start_date" type="text" placeholder="e.g. May 2024" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
            </div>
            <div>
              <label class="block text-xs font-headline font-bold text-on-surface mb-1">End Date</label>
              <input v-model="expModal.form.end_date" type="text" placeholder="e.g. Aug 2024 or Present" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
            </div>
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Description &amp; Impact</label>
            <textarea v-model="expModal.form.description" rows="3" placeholder="Key responsibilities and engineering achievements..." class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface"></textarea>
          </div>
        </div>
        <div class="flex items-center justify-end gap-2 pt-3 border-t border-surface-container">
          <button @click="expModal.open = false" class="px-4 py-2 rounded-xl bg-surface-container-low text-xs font-headline font-semibold text-on-surface-variant cursor-pointer">Cancel</button>
          <button @click="saveExpModal" class="px-5 py-2 rounded-xl bg-primary text-on-primary text-xs font-headline font-bold hover:bg-primary-dim cursor-pointer">Save Position</button>
        </div>
      </div>
    </div>

    <!-- ==================== PROJECT MODAL ==================== -->
    <div v-if="projModal.open" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container max-w-lg w-full space-y-4 shadow-2xl text-on-surface">
        <div class="flex items-center justify-between border-b border-surface-container pb-3">
          <h3 class="font-headline font-bold text-base text-on-surface">
            {{ projModal.isEdit ? 'Edit Project' : 'Add Project' }}
          </h3>
          <button @click="projModal.open = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">✕</button>
        </div>
        <div class="space-y-3 text-xs sm:text-sm font-body">
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Project Name *</label>
            <input v-model="projModal.form.title" type="text" placeholder="e.g. Decentralized Task Protocol" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Repository / Live Link</label>
            <input v-model="projModal.form.link" type="text" placeholder="e.g. github.com/username/project" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Year</label>
            <input v-model="projModal.form.year" type="text" placeholder="e.g. 2025" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Description &amp; Highlights</label>
            <textarea v-model="projModal.form.description" rows="3" placeholder="Key tech stack used, problem solved, and architecture..." class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface"></textarea>
          </div>
        </div>
        <div class="flex items-center justify-end gap-2 pt-3 border-t border-surface-container">
          <button @click="projModal.open = false" class="px-4 py-2 rounded-xl bg-surface-container-low text-xs font-headline font-semibold text-on-surface-variant cursor-pointer">Cancel</button>
          <button @click="saveProjModal" class="px-5 py-2 rounded-xl bg-primary text-on-primary text-xs font-headline font-bold hover:bg-primary-dim cursor-pointer">Save Project</button>
        </div>
      </div>
    </div>

    <!-- ==================== CERTIFICATION MODAL ==================== -->
    <div v-if="certModal.open" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
      <div class="bg-surface-container-lowest rounded-3xl p-6 border border-surface-container max-w-lg w-full space-y-4 shadow-2xl text-on-surface">
        <div class="flex items-center justify-between border-b border-surface-container pb-3">
          <h3 class="font-headline font-bold text-base text-on-surface">
            {{ certModal.isEdit ? 'Edit Certification' : 'Add Certification' }}
          </h3>
          <button @click="certModal.open = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">✕</button>
        </div>
        <div class="space-y-3 text-xs sm:text-sm font-body">
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Certificate Name *</label>
            <input v-model="certModal.form.name" type="text" placeholder="e.g. AWS Certified Solutions Architect" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Issuing Organization *</label>
            <input v-model="certModal.form.issuer" type="text" placeholder="e.g. Amazon Web Services, Coursera" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
          <div>
            <label class="block text-xs font-headline font-bold text-on-surface mb-1">Issue Date</label>
            <input v-model="certModal.form.issue_date" type="text" placeholder="e.g. Jun 2024" class="w-full px-4 py-2 bg-surface-container-low border border-surface-container rounded-xl text-on-surface" />
          </div>
        </div>
        <div class="flex items-center justify-end gap-2 pt-3 border-t border-surface-container">
          <button @click="certModal.open = false" class="px-4 py-2 rounded-xl bg-surface-container-low text-xs font-headline font-semibold text-on-surface-variant cursor-pointer">Cancel</button>
          <button @click="saveCertModal" class="px-5 py-2 rounded-xl bg-primary text-on-primary text-xs font-headline font-bold hover:bg-primary-dim cursor-pointer">Save Certificate</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'

const user = ref(null)
const teaches = ref([])
const verifications = ref([])
const activeTab = ref('education')
const saving = ref(false)
const polishing = ref(false)
const zoomLevel = ref(100)

const currentYear = new Date().getFullYear()

const defaultStartYear = computed(() => {
  const sem = user.value?.semester || 1
  const yearsBack = Math.max(0, Math.floor((sem - 1) / 2))
  return String(currentYear - yearsBack)
})

const defaultEndYear = computed(() => {
  return String(parseInt(defaultStartYear.value) + 4)
})

const campusNodeId = computed(() => {
  return `Node #${String(user.value?.id || 1).padStart(3, '0')}`
})

const campusNodeLabel = computed(() => {
  const inst = (eduForm.institution || user.value?.education || user.value?.department || 'Campus').split(' ')[0]
  return `${inst} ${campusNodeId.value}`
})

const documentId = computed(() => {
  return `SL-RES-${currentYear}-${String(user.value?.id || 1).padStart(5, '0')}`
})

const protocolHash = computed(() => {
  const uid = user.value?.id || 1
  const hex = ((uid * 2654435761) >>> 0).toString(16).padStart(8, '0')
  return `0x${hex}...4a${String(uid).slice(-2).padStart(2, '0')}`
})

// Dynamic ATS Completeness Score (0 - 100%)
const atsScore = computed(() => {
  let score = 0
  // Profile (25 pts)
  if (resume.profile.full_name) score += 10
  if (resume.profile.email) score += 10
  if (resume.profile.phone || resume.profile.location || resume.profile.github) score += 5
  // Role & Summary (20 pts)
  if (resume.target_role) score += 10
  if (resume.summary && resume.summary.length > 30) score += 10
  // Education (20 pts)
  if (eduForm.institution) score += 10
  if (eduForm.degree || eduForm.is_current) score += 10
  // Skills (15 pts)
  const totalSkills = (resume.skills.languages?.length || 0) + (resume.skills.frameworks?.length || 0) + (resume.skills.tools?.length || 0)
  if (totalSkills >= 5) score += 15
  else if (totalSkills >= 2) score += 8
  // Projects / Experience (10 pts)
  if ((resume.projects?.length || 0) > 0 || (resume.experiences?.length || 0) > 0) score += 10
  // Verifications / Certs (10 pts)
  if ((verifications.value?.length || 0) > 0 || (resume.certifications?.length || 0) > 0) score += 10
  return Math.min(100, Math.max(10, score))
})

const atsStatusLabel = computed(() => {
  if (atsScore.value >= 80) return 'ATS Ready'
  if (atsScore.value >= 50) return 'In Progress'
  return 'Draft'
})

const tabs = [
  { id: 'profile', label: 'Profile & Contact', icon: 'person' },
  { id: 'education', label: 'Education & Campus', icon: 'school' },
  { id: 'skills', label: 'Skills & Tech', icon: 'code' },
  { id: 'projects', label: 'Projects', icon: 'rocket_launch' },
  { id: 'experience', label: 'Experience', icon: 'work' },
  { id: 'certifications', label: 'Certifications', icon: 'verified' },
  { id: 'privacy', label: 'Teaching & Settings', icon: 'tune' }
]

const popularInstitutions = [
  { name: 'ABES Institute of Technology (ABESIT)', short: 'ABESIT', location: 'Ghaziabad, Uttar Pradesh' },
  { name: 'ABES Engineering College (ABES EC)', short: 'ABES EC', location: 'Ghaziabad, Uttar Pradesh' },
  { name: 'Ajay Kumar Garg Engineering College (AKGEC)', short: 'AKGEC', location: 'Ghaziabad, Uttar Pradesh' },
  { name: 'KIET Group of Institutions (KIET)', short: 'KIET', location: 'Ghaziabad, Uttar Pradesh' },
  { name: 'Delhi Technological University (DTU / DCE)', short: 'DTU', location: 'New Delhi, Delhi' },
  { name: 'Indian Institute of Technology Delhi (IIT Delhi)', short: 'IIT Delhi', location: 'New Delhi, Delhi' }
]

// Education inline reactive form
const eduForm = reactive({
  institution: '',
  degree: '',
  is_current: true,
  start_year: '',
  end_year: '',
  grade: '',
  coursework: ''
})

// Autocomplete State
const showInstDropdown = ref(false)
const isSearchingInst = ref(false)
const instResults = ref([])
let instSearchTimer = null

const onInstInput = () => {
  showInstDropdown.value = true
  if (instSearchTimer) clearTimeout(instSearchTimer)
  instSearchTimer = setTimeout(() => {
    searchInstitutions(eduForm.institution || '')
  }, 180)
}

const searchInstitutions = async (query = '') => {
  isSearchingInst.value = true
  try {
    const res = await fetch(`/api/institutions/search?q=${encodeURIComponent(query)}`)
    if (res.ok) {
      const data = await res.json()
      instResults.value = data.results || []
    }
  } catch (err) {
    console.error('Error searching institutions:', err)
  } finally {
    isSearchingInst.value = false
  }
}

const selectInstitution = (inst) => {
  eduForm.institution = inst.name
  showInstDropdown.value = false
}

const selectCustomInst = (name) => {
  eduForm.institution = name.trim()
  showInstDropdown.value = false
}

// Full Resume State with Categorized Skills & Profile (clean initial state, populated dynamically from DB)
const resume = reactive({
  profile: {
    full_name: '',
    email: '',
    phone: '',
    github: '',
    linkedin: '',
    location: ''
  },
  target_role: '',
  summary: '',
  skills: {
    languages: [],
    frameworks: [],
    tools: []
  },
  experiences: [],
  education: [],
  certifications: [],
  projects: [],
  mentorship_desc: '',
  settings: {
    show_teaching_skills: true,
    template: 'modern'
  }
})

// Skills Handlers
const newSkillInput = reactive({ languages: '', frameworks: '', tools: '' })

const addSkillItem = (category) => {
  const val = newSkillInput[category].trim()
  if (val && !resume.skills[category].includes(val)) {
    resume.skills[category].push(val)
    newSkillInput[category] = ''
  }
}

const quickAddSkill = (category, name) => {
  if (name && !resume.skills[category].includes(name)) {
    resume.skills[category].push(name)
  }
}

const removeSkillItem = (category, idx) => {
  resume.skills[category].splice(idx, 1)
}

// Modals State
const expModal = reactive({ open: false, isEdit: false, index: -1, form: { title: '', company: '', location: '', start_date: '', end_date: '', description: '' } })
const projModal = reactive({ open: false, isEdit: false, index: -1, form: { title: '', link: '', year: '2025', description: '' } })
const certModal = reactive({ open: false, isEdit: false, index: -1, form: { name: '', issuer: '', issue_date: '' } })

// Zoom controls
const zoomIn = () => { if (zoomLevel.value < 130) zoomLevel.value += 10 }
const zoomOut = () => { if (zoomLevel.value > 70) zoomLevel.value -= 10 }

// Experience Handlers
const openExpModal = (idx = -1) => {
  if (idx >= 0 && resume.experiences[idx]) {
    expModal.isEdit = true
    expModal.index = idx
    expModal.form = { ...resume.experiences[idx] }
  } else {
    expModal.isEdit = false
    expModal.index = -1
    expModal.form = { title: '', company: '', location: resume.profile.location || '', start_date: '', end_date: '', description: '' }
  }
  expModal.open = true
}

const saveExpModal = () => {
  if (!expModal.form.title || !expModal.form.company) {
    alert('Title and company are required.')
    return
  }
  if (expModal.isEdit && expModal.index >= 0) {
    resume.experiences[expModal.index] = { ...expModal.form }
  } else {
    resume.experiences.push({ ...expModal.form, id: Date.now() })
  }
  expModal.open = false
}

const deleteExp = (idx) => {
  if (confirm('Delete this experience?')) resume.experiences.splice(idx, 1)
}

// Project Handlers
const openProjModal = (idx = -1) => {
  if (idx >= 0 && resume.projects[idx]) {
    projModal.isEdit = true
    projModal.index = idx
    projModal.form = { ...resume.projects[idx] }
  } else {
    projModal.isEdit = false
    projModal.index = -1
    projModal.form = { title: '', link: '', year: String(currentYear), description: '' }
  }
  projModal.open = true
}

const saveProjModal = () => {
  if (!projModal.form.title) {
    alert('Project title is required.')
    return
  }
  if (projModal.isEdit && projModal.index >= 0) {
    resume.projects[projModal.index] = { ...projModal.form }
  } else {
    resume.projects.push({ ...projModal.form, id: Date.now() })
  }
  projModal.open = false
}

const deleteProj = (idx) => {
  if (confirm('Delete this project?')) resume.projects.splice(idx, 1)
}

// Certification Handlers
const openCertModal = (idx = -1) => {
  if (idx >= 0 && resume.certifications[idx]) {
    certModal.isEdit = true
    certModal.index = idx
    certModal.form = { ...resume.certifications[idx] }
  } else {
    certModal.isEdit = false
    certModal.index = -1
    certModal.form = { name: '', issuer: '', issue_date: String(currentYear) }
  }
  certModal.open = true
}

const saveCertModal = () => {
  if (!certModal.form.name || !certModal.form.issuer) {
    alert('Certificate name and issuer are required.')
    return
  }
  if (certModal.isEdit && certModal.index >= 0) {
    resume.certifications[certModal.index] = { ...certModal.form }
  } else {
    resume.certifications.push({ ...certModal.form, id: Date.now() })
  }
  certModal.open = false
}

const deleteCert = (idx) => {
  if (confirm('Delete this certification?')) resume.certifications.splice(idx, 1)
}

const getSkillVerif = (name) => {
  if (!name || !verifications.value) return null
  return verifications.value.find(v => v.skill_name?.toLowerCase() === name.toLowerCase())
}

// Fetch Resume Data from Backend
const fetchCurrentUser = async () => {
  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const d = await res.json()
      user.value = d.user
      if (user.value) {
        if (!resume.profile.full_name && user.value.full_name) resume.profile.full_name = user.value.full_name
        if (!resume.profile.email && user.value.email) resume.profile.email = user.value.email
      }
    }
  } catch (e) {
    console.error('Error loading user me:', e)
  }
}

const populateDefaultsFromUser = () => {
  if (!user.value) return

  if (!resume.profile.full_name) {
    resume.profile.full_name = user.value.full_name || user.value.username || ''
  }
  if (!resume.profile.email) {
    resume.profile.email = user.value.email || ''
  }
  if (!resume.profile.github && user.value.github) {
    resume.profile.github = user.value.github
  }
  if (!resume.profile.linkedin && user.value.linkedin) {
    resume.profile.linkedin = user.value.linkedin
  }
  if (!resume.profile.location) {
    resume.profile.location = user.value.education ? `${user.value.education.split(' ')[0]} Campus` : 'Campus Node'
  }
  if (!resume.target_role) {
    resume.target_role = user.value.department ? `${user.value.department} Specialist & Peer Mentor` : 'Campus Peer Lead'
  }
  if (!resume.summary) {
    if (user.value.bio) {
      resume.summary = user.value.bio
    } else {
      resume.summary = `Driven undergraduate in ${user.value.department || 'Engineering'} at ${user.value.education || 'campus'} with verified competencies on the SkillLoop peer exchange network. Passionate about practical problem-solving, collaborative peer teaching, and developing real-world software applications.`
    }
  }

  // Education defaults
  if (!eduForm.institution) {
    eduForm.institution = user.value.education || (popularInstitutions[0]?.name || 'University Campus')
  }
  if (!eduForm.degree) {
    eduForm.degree = user.value.department ? `B.Tech in ${user.value.department}` : 'Bachelor of Technology'
  }
  if (!eduForm.start_year) {
    eduForm.start_year = defaultStartYear.value
  }
  if (!eduForm.end_year) {
    eduForm.end_year = defaultEndYear.value
  }
  if (!eduForm.grade && user.value.semester) {
    eduForm.grade = 'Semester ' + user.value.semester
  }

  // Populate skills from teaches & learns if empty
  if (resume.skills.languages.length === 0 && teaches.value.length > 0) {
    resume.skills.languages = [...teaches.value.slice(0, 4)]
  }
  if (resume.skills.languages.length === 0) {
    resume.skills.languages = ['Python', 'JavaScript', 'SQL']
  }
  if (resume.skills.frameworks.length === 0 && user.value.department) {
    resume.skills.frameworks = [user.value.department, 'Git', 'Agile Peer Review']
  }

  // Add default project if empty
  if (resume.projects.length === 0) {
    resume.projects = [
      {
        title: 'SkillLoop — Campus Peer Learning & Escrow Protocol',
        link: 'github.com/skillloop-p2p',
        year: String(currentYear),
        description: 'Collaborative peer-to-peer exchange platform enabling university students to trade skill sessions using proof-of-work validation and time-banking escrow.'
      }
    ]
  }

  if (!resume.mentorship_desc) {
    const teachingList = teaches.value.length > 0 ? teaches.value.slice(0, 2).join(' & ') : (user.value.department || 'core coursework')
    resume.mentorship_desc = `Conducted verified 1-on-1 peer reviews, code walkthroughs, and tutoring sessions in ${teachingList} with positive learner evaluations on the SkillLoop campus protocol.`
  }
}

const fetchResume = async () => {
  try {
    const res = await fetch('/api/resume', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      user.value = data.user || null
      teaches.value = data.teaches || []
      verifications.value = data.verifications || []
      
      const r = data.resume || {}
      if (r.target_role) resume.target_role = r.target_role
      if (r.summary) resume.summary = r.summary
      if (Array.isArray(r.experiences) && r.experiences.length > 0) resume.experiences = r.experiences
      if (Array.isArray(r.projects) && r.projects.length > 0) resume.projects = r.projects
      if (Array.isArray(r.certifications) && r.certifications.length > 0) resume.certifications = r.certifications
      
      if (r.custom_skills) {
        if (typeof r.custom_skills === 'object' && !Array.isArray(r.custom_skills)) {
          if (Array.isArray(r.custom_skills.languages) && r.custom_skills.languages.length > 0) resume.skills.languages = r.custom_skills.languages
          if (Array.isArray(r.custom_skills.frameworks) && r.custom_skills.frameworks.length > 0) resume.skills.frameworks = r.custom_skills.frameworks
          if (Array.isArray(r.custom_skills.tools) && r.custom_skills.tools.length > 0) resume.skills.tools = r.custom_skills.tools
        }
      }

      if (r.settings) {
        resume.settings = { ...resume.settings, ...r.settings }
        if (r.settings.profile) Object.assign(resume.profile, r.settings.profile)
        if (r.settings.mentorship_desc) resume.mentorship_desc = r.settings.mentorship_desc
      }

      if (Array.isArray(r.education) && r.education.length > 0) {
        resume.education = r.education
        Object.assign(eduForm, r.education[0])
      }

      // Populate any missing fields dynamically from authenticated user
      populateDefaultsFromUser()
    }
  } catch (err) {
    console.error('Error fetching resume:', err)
  }
}

// Save Resume Data to Backend
const saveResume = async () => {
  saving.value = true
  try {
    if (eduForm.institution) {
      resume.education = [{ ...eduForm }]
    }

    const payload = {
      target_role: resume.target_role,
      summary: resume.summary,
      experiences: resume.experiences,
      education: resume.education,
      certifications: resume.certifications,
      projects: resume.projects,
      custom_skills: resume.skills,
      settings: {
        ...resume.settings,
        profile: resume.profile,
        mentorship_desc: resume.mentorship_desc
      }
    }

    const res = await fetch('/api/resume', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(payload)
    })
    if (res.ok) {
      // Saved
    }
  } catch (err) {
    console.error('Error saving resume:', err)
  } finally {
    saving.value = false
  }
}

// AI Polish
const polishWithAi = async (field = 'summary') => {
  polishing.value = true
  try {
    const textToPolish = field === 'summary' ? resume.summary : ''
    const res = await fetch('/api/resume/ai-polish', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        target_role: resume.target_role,
        field: field,
        content: textToPolish
      })
    })
    if (res.ok) {
      const data = await res.json()
      if (data.polished) {
        resume.summary = data.polished
      }
    }
  } catch (err) {
    console.error('Error polishing with AI:', err)
  } finally {
    polishing.value = false
  }
}

// 1-Click PDF Export
const exportPdf = () => {
  window.print()
}

onMounted(async () => {
  await fetchCurrentUser()
  await fetchResume()
})
</script>

<style>
.custom-scroll::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background: #efe3ff;
  border-radius: 9999px;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
  background: #dbc9ff;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

@media print {
  body {
    background: #ffffff !important;
    color: #0f172a !important;
  }
  header, .print\:hidden, button {
    display: none !important;
  }
  main {
    display: block !important;
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }
  .lg\:col-span-5 {
    display: none !important;
  }
  .lg\:col-span-7 {
    display: block !important;
    width: 100% !important;
    max-height: none !important;
    overflow: visible !important;
  }
  #resume-a4-sheet {
    box-shadow: none !important;
    border: none !important;
    transform: none !important;
    width: 100% !important;
    max-width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
  }
}
</style>
