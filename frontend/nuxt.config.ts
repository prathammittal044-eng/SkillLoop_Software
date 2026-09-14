// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  srcDir: '.',
  vite: {
    server: {
      allowedHosts: true
    }
  },
  devtools: { enabled: true },
  app: {
    head: {
      title: 'SkillLoop | Exchange Skills, Not Just Contacts',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap' }
      ],
      script: [
        { src: 'https://cdn.tailwindcss.com?plugins=forms,container-queries' },
        { innerHTML: 'tailwind.config = { darkMode: \"class\", theme: { extend: { \"colors\": { \"primary-container\": \"#9e93ff\", \"outline-variant\": \"#b5a6d5\", \"on-surface\": \"#34284f\", \"on-error\": \"#ffefef\", \"tertiary-fixed\": \"#ff8bc3\", \"on-secondary\": \"#f8f0ff\", \"on-secondary-container\": \"#53319a\", \"secondary\": \"#6847af\", \"secondary-dim\": \"#5b3aa3\", \"on-tertiary\": \"#ffeff3\", \"surface-container-high\": \"#eaddff\", \"primary-fixed-dim\": \"#8f83ff\", \"surface-tint\": \"#543ce0\", \"primary-fixed\": \"#9e93ff\", \"on-error-container\": \"#510017\", \"surface-container-low\": \"#f6edff\", \"on-secondary-fixed\": \"#3f1985\", \"surface-container-lowest\": \"#ffffff\", \"primary-dim\": \"#482cd4\", \"primary\": \"#543ce0\", \"on-tertiary-fixed-variant\": \"#6e1048\", \"surface\": \"#fbf4ff\", \"on-tertiary-fixed\": \"#360021\", \"outline\": \"#7d709b\", \"on-primary-fixed\": \"#000000\", \"on-secondary-fixed-variant\": \"#5c3ba4\", \"tertiary\": \"#99366c\", \"surface-container\": \"#efe3ff\", \"tertiary-dim\": \"#8b2a5f\", \"on-primary-fixed-variant\": \"#250094\", \"surface-bright\": \"#fbf4ff\", \"inverse-on-surface\": \"#a496c4\", \"inverse-surface\": \"#12062c\", \"on-tertiary-container\": \"#62023f\", \"on-surface-variant\": \"#62557f\", \"secondary-fixed-dim\": \"#ceb9ff\", \"surface-variant\": \"#e5d6ff\", \"surface-container-highest\": \"#e5d6ff\", \"background\": \"#fbf4ff\", \"tertiary-fixed-dim\": \"#f07db6\", \"secondary-fixed\": \"#dbc9ff\", \"inverse-primary\": \"#8c7fff\", \"secondary-container\": \"#dbc9ff\", \"error\": \"#b41340\", \"tertiary-container\": \"#ff8bc3\", \"error-dim\": \"#a70138\", \"on-primary\": \"#f5f0ff\", \"on-background\": \"#34284f\", \"surface-dim\": \"#ddccff\", \"error-container\": \"#f74b6d\", \"on-primary-container\": \"#1d007a\" }, \"borderRadius\": { \"DEFAULT\": \"0.25rem\", \"lg\": \"0.5rem\", \"xl\": \"0.75rem\", \"full\": \"9999px\" }, \"fontFamily\": { \"headline\": [\"Plus Jakarta Sans\"], \"display\": [\"Plus Jakarta Sans\"], \"body\": [\"Inter\"], \"label\": [\"Public Sans\"] } }, }, }' }
      ]
    }
  },
  routeRules: {
    '/api/**': { proxy: 'http://127.0.0.1:5000/api/**' },
    '/socket.io/**': {
      proxy: {
        to: 'http://127.0.0.1:5000/socket.io/**',
        ws: true
      }
    }
  }
})
