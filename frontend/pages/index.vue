<template>
<div class="bg-background text-on-surface font-body min-h-screen flex flex-col relative overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar (Shared Component) -->
<header class="sticky top-0 w-full z-50 bg-surface-bright border-b border-surface-container-high shadow-sm">
<div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
<!-- Brand Logo -->
<NuxtLink class="flex items-center gap-2.5 font-display text-2xl font-bold tracking-tight text-primary transition-all duration-200 active:scale-95" to="/login">
<span class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center text-on-primary shadow-sm">
<span class="material-symbols-outlined text-2xl" data-icon="all_inclusive">all_inclusive</span>
</span>
<span>SkillLoop</span>
</NuxtLink>
<!-- Navigation Links -->
<nav class="hidden md:flex items-center gap-8 font-headline text-base font-semibold">
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" to="/">Explore</NuxtLink>
<NuxtLink class="text-primary font-semibold hover:text-primary transition-colors duration-200" to="/">How It Works</NuxtLink>
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" to="/">Features</NuxtLink>
</nav>
<!-- Trailing Action Buttons -->
<div class="flex items-center gap-3">
<NuxtLink class="px-5 py-2.5 rounded-xl font-headline text-sm font-semibold text-primary border border-outline-variant hover:bg-surface-container transition-all duration-200 active:scale-95" to="/login">
          Login
        </NuxtLink>
<NuxtLink class="px-5 py-2.5 rounded-xl font-headline text-sm font-semibold bg-primary text-on-primary shadow-sm hover:bg-primary-dim transition-all duration-200 active:scale-95 flex items-center gap-1.5" to="/register">
<span>Get Started</span>
<span class="material-symbols-outlined text-base" data-icon="arrow_forward">arrow_forward</span>
</NuxtLink>
</div>
</div>
</header>
<!-- Hero Section -->
<main>
<section class="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28">
<!-- Ambient light background circles -->
<div class="absolute -top-24 right-1/4 w-96 h-96 bg-secondary-fixed/40 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div class="absolute top-1/2 left-0 w-80 h-80 bg-surface-container-high/60 rounded-full blur-3xl pointer-events-none -z-10"></div>
<div class="max-w-7xl mx-auto px-6">
<div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
<!-- Text Content -->
<div class="lg:col-span-7 flex flex-col items-start space-y-6">
<!-- Campus Badge -->
<div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-surface-container border border-surface-container-high text-primary font-label text-xs font-semibold tracking-wide">
<span>⚡</span>
<span>Campus Peer-to-Peer Learning Network</span>
</div>
<!-- Headline -->
<h1 class="font-headline text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-on-background leading-[1.12]">
              Trade what you know. <br class="hidden sm:inline"/>
<span class="text-primary underline decoration-secondary-container decoration-wavy decoration-2">Learn what you love.</span>
</h1>
<!-- Subtitle -->
<p class="font-body text-base sm:text-lg text-on-surface-variant max-w-xl leading-relaxed">
              SkillLoop connects verified university students to swap skills 1-on-1. No cash, no awkward tutor rates — just pure knowledge exchange.
            </p>
<!-- Call to Actions -->
<div class="flex flex-wrap items-center gap-4 pt-2 w-full sm:w-auto">
<NuxtLink class="w-full sm:w-auto inline-flex justify-center items-center gap-2 px-7 py-3.5 rounded-xl font-headline text-base font-bold bg-primary text-on-primary shadow-md hover:bg-primary-dim transition-all duration-200 active:scale-95" to="/register">
<span>Get Started</span>
<span class="material-symbols-outlined text-lg" data-icon="arrow_forward">arrow_forward</span>
</NuxtLink>
<NuxtLink class="w-full sm:w-auto inline-flex justify-center items-center px-7 py-3.5 rounded-xl font-headline text-base font-semibold border-2 border-outline-variant text-on-surface hover:bg-surface-container-low transition-all duration-200 active:scale-95" to="/login">
                Login
              </NuxtLink>
</div>
<!-- Trust proof micro-copy -->
<div class="flex items-center gap-2 text-on-surface-variant font-label text-xs sm:text-sm pt-2">
<span class="text-primary font-semibold">✓</span>
<span>100% Free for college students • Verified .edu network</span>
</div>
<!-- Quick skill tag pills -->
<div class="flex flex-wrap items-center gap-2 pt-3">
<span class="text-xs font-medium text-on-surface-variant">Popular this week:</span>
<span class="px-2.5 py-1 bg-surface-container rounded-lg text-xs font-medium text-on-surface">Python 🐍</span>
<span class="px-2.5 py-1 bg-surface-container rounded-lg text-xs font-medium text-on-surface">UI/UX Design 🎨</span>
<span class="px-2.5 py-1 bg-surface-container rounded-lg text-xs font-medium text-on-surface">Acoustic Guitar 🎸</span>
<span class="px-2.5 py-1 bg-surface-container rounded-lg text-xs font-medium text-on-surface">Organic Chem 🧪</span>
</div>
</div>
<!-- Hero Graphic Card / Visual Composition -->
<div class="lg:col-span-5 flex justify-center lg:justify-end">
<div class="relative w-full max-w-md">
<!-- Decorative subtle background glow card -->
<div class="absolute -inset-2 bg-gradient-to-r from-primary-fixed to-secondary-container rounded-3xl opacity-50 blur-lg"></div>
<!-- Main Card Container -->
<div class="relative bg-surface-container-lowest rounded-3xl p-4 sm:p-6 border border-surface-container-high shadow-lg transition-transform duration-300 hover:-translate-y-1">
<!-- Floating top pill in the card -->
<div class="flex items-center justify-between pb-4 mb-3 border-b border-surface-container-low">
<div class="flex items-center gap-2">
<span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
<span class="font-headline text-xs font-bold text-on-surface">Active Session Match</span>
</div>
<span class="font-label text-xs px-2.5 py-1 bg-surface-container text-primary font-semibold rounded-full">1 : 1 Trade</span>
</div>
<!-- Verified Image Anchor -->
<div class="w-full aspect-square rounded-2xl overflow-hidden bg-surface-container-low flex items-center justify-center p-2">
<img alt="SkillLoop Hero Illustration" class="w-full h-full object-contain drop-shadow-sm rounded-xl" src="https://lh3.googleusercontent.com/aida/AEtjO1XsYgfPhrbDNtNwt1K60iM5L0_n9Cxg0NplnZ8X6s8adQGe8lXXjLGgtN7-1oQIG6Lk6UxKu9-bakbcQN9ssYRj-Qro5jhJFEnGDgABEqnHcqDsUucelWXPDx2rc2bKLfYXqwdQY4iApVb2TPYOw1Or5ILUU-q5_bn7A3Ziv8x5r9FsVUayfQjrLfwf-Nbi3ZKoYSlxHIsbMxmHQSnmlpobKxBMmFg3wCMbz5VnvQ6adGL43K2v46UVkBVA"/>
</div>
<!-- Card footer live ticker preview -->
<div class="mt-4 pt-3 border-t border-surface-container-low flex items-center justify-between font-label text-xs text-on-surface-variant">
<div class="flex items-center gap-1.5">
<span class="material-symbols-outlined text-base text-primary" data-icon="sync_alt">sync_alt</span>
<span>1 hr Python for 1 hr Figma</span>
</div>
<span class="font-semibold text-primary font-headline">+100 XP</span>
</div>
</div>
</div>
</div>
</div>
</div>
</section>
<!-- Social proof / campus community banner -->
<section class="border-y border-surface-container-high bg-surface-container-low py-10">
<div class="max-w-7xl mx-auto px-6">
<div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center divide-y md:divide-y-0 md:divide-x divide-surface-container-high">
<div class="pt-4 md:pt-0">
<div class="font-display text-3xl sm:text-4xl font-extrabold text-primary">45+</div>
<div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Campus Nodes</div>
<p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Active at top universities nationwide</p>
</div>
<div class="pt-4 md:pt-0">
<div class="font-display text-3xl sm:text-4xl font-extrabold text-primary">2,400+</div>
<div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Hours Swapped</div>
<p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Zero student tuition or tutoring fees spent</p>
</div>
<div class="pt-4 md:pt-0">
<div class="font-display text-3xl sm:text-4xl font-extrabold text-primary">4.9 ★</div>
<div class="font-headline text-sm font-semibold text-on-surface-variant mt-1">Average Peer Rating</div>
<p class="font-body text-xs text-on-surface-variant/80 mt-0.5">Verified feedback on every session</p>
</div>
</div>
</div>
</section>
<!-- Feature Cards Section: How SkillLoop Works -->
<section class="py-20 md:py-28 bg-surface-bright" id="how-it-works">
<div class="max-w-7xl mx-auto px-6">
<!-- Header -->
<div class="text-center max-w-2xl mx-auto mb-16">
<div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container font-label text-xs font-semibold mb-3">
<span class="material-symbols-outlined text-sm" data-icon="auto_awesome">auto_awesome</span>
<span>Simple &amp; Free Process</span>
</div>
<h2 class="font-headline text-3xl sm:text-4xl font-extrabold text-on-background tracking-tight">
            How SkillLoop Works
          </h2>
<p class="font-body text-base text-on-surface-variant mt-3">
            Level up your skillset in three easy steps
          </p>
</div>
<!-- 3 Bento-Style Modern Feature Cards -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
<!-- Card 1 -->
<div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-sm hover:shadow-md hover:border-primary-fixed transition-all duration-300 flex flex-col justify-between">
<div>
<div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-on-primary transition-colors duration-300 mb-6">
<span class="material-symbols-outlined text-3xl" data-icon="swap_horiz">swap_horiz</span>
</div>
<div class="inline-block px-2.5 py-1 bg-surface-container text-primary rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                Peer Exchange
              </div>
<h3 class="font-headline text-xl font-bold text-on-background mb-3">
                1. Exchange Skills
              </h3>
<p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Swap an hour of your Python mastery for an hour of guitar or design. Knowledge is currency.
              </p>
</div>
<div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-primary">
<span>Time Banking Protocol</span>
<span class="material-symbols-outlined text-sm" data-icon="arrow_forward">arrow_forward</span>
</div>
</div>
<!-- Card 2 -->
<div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-sm hover:shadow-md hover:border-primary-fixed transition-all duration-300 flex flex-col justify-between">
<div>
<div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-secondary group-hover:bg-secondary group-hover:text-on-secondary transition-colors duration-300 mb-6">
<span class="material-symbols-outlined text-3xl" data-icon="military_tech">military_tech</span>
</div>
<div class="inline-block px-2.5 py-1 bg-secondary-container text-on-secondary-container rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                XP &amp; Reputation
              </div>
<h3 class="font-headline text-xl font-bold text-on-background mb-3">
                2. Gain XP
              </h3>
<p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Build your campus reputation with every peer session. Level up and unlock peer mentor accolades.
              </p>
</div>
<div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-secondary">
<span>Dynamic Leaderboards</span>
<span class="material-symbols-outlined text-sm" data-icon="arrow_forward">arrow_forward</span>
</div>
</div>
<!-- Card 3 -->
<div class="group relative bg-surface-container-lowest rounded-3xl p-8 border border-surface-container-high shadow-sm hover:shadow-md hover:border-primary-fixed transition-all duration-300 flex flex-col justify-between">
<div>
<div class="w-14 h-14 rounded-2xl bg-surface-container flex items-center justify-center text-tertiary group-hover:bg-tertiary group-hover:text-on-tertiary transition-colors duration-300 mb-6">
<span class="material-symbols-outlined text-3xl" data-icon="verified">verified</span>
</div>
<div class="inline-block px-2.5 py-1 bg-surface-variant text-on-surface rounded-md font-label text-xs font-bold uppercase tracking-wide mb-3">
                Resume Endorsements
              </div>
<h3 class="font-headline text-xl font-bold text-on-background mb-3">
                3. Get Verified
              </h3>
<p class="font-body text-sm text-on-surface-variant leading-relaxed">
                Validate your skills with peer endorsements and export a cryptographically verified ledger for your resume.
              </p>
</div>
<div class="mt-8 pt-4 border-t border-surface-container-low flex items-center gap-2 text-xs font-semibold text-tertiary">
<span>Exportable Credential</span>
<span class="material-symbols-outlined text-sm" data-icon="arrow_forward">arrow_forward</span>
</div>
</div>
</div>
</div>
</section>
<!-- Campus Call to Action Strip -->
<section class="max-w-7xl mx-auto px-6 pb-20">
<div class="bg-gradient-to-r from-primary via-primary-dim to-secondary rounded-3xl p-8 sm:p-12 text-on-primary flex flex-col md:flex-row items-center justify-between gap-8 shadow-md">
<div class="max-w-xl text-center md:text-left">
<span class="px-3 py-1 bg-surface-container-lowest/20 rounded-full font-label text-xs font-medium uppercase tracking-wider text-on-primary">Join Your Campus Network</span>
<h3 class="font-headline text-2xl sm:text-3xl font-extrabold mt-3 mb-2">Ready to swap skills with peers?</h3>
<p class="font-body text-sm text-on-primary/90">Sign in with your university .edu address and find a learning match in under 5 minutes.</p>
</div>
<div class="flex-shrink-0">
<NuxtLink class="px-8 py-4 rounded-xl bg-surface-container-lowest text-primary font-headline text-base font-bold shadow hover:bg-surface-bright transition-all duration-200 active:scale-95 inline-flex items-center gap-2" to="/register">
<span>Find a Partner</span>
<span class="material-symbols-outlined text-lg" data-icon="school">school</span>
</NuxtLink>
</div>
</div>
</section>
</main>
<!-- Footer (Shared Component) -->
<footer class="w-full bg-surface-container-lowest border-t border-surface-container-high">
<div class="max-w-7xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-6 font-body text-sm">
<!-- Brand & Copyright -->
<div class="flex flex-col sm:flex-row items-center gap-3 sm:gap-6 text-center sm:text-left">
<NuxtLink class="font-display text-xl font-bold text-primary flex items-center gap-1.5" to="/login">
<span class="material-symbols-outlined text-xl" data-icon="all_inclusive">all_inclusive</span>
<span>SkillLoop</span>
</NuxtLink>
<span class="text-on-surface-variant font-body">© 2025 SkillLoop. Built for campus peer learning.</span>
</div>
<!-- Footer Links -->
<nav class="flex flex-wrap items-center justify-center gap-6 font-medium">
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" to="/">Explore</NuxtLink>
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" to="/">How It Works</NuxtLink>
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" to="/">Features</NuxtLink>
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" href="#privacy">Privacy</NuxtLink>
<NuxtLink class="text-on-surface-variant hover:text-primary transition-colors duration-200" href="#terms">Terms</NuxtLink>
</nav>
</div>
</footer>
</div>
</template>

<script setup>
</script>

