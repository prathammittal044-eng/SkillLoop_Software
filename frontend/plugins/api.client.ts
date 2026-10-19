export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const apiBase = (config.public?.apiBase || '').toString().trim()
  if (!apiBase) return

  const normalizedBase = apiBase.replace(/\/$/, '')

  if (typeof window !== 'undefined' && window.fetch) {
    const originalFetch = window.fetch
    window.fetch = function (input: RequestInfo | URL, init?: RequestInit) {
      if (typeof input === 'string') {
        if (input.startsWith('/api/') || input.startsWith('/uploads/')) {
          input = `${normalizedBase}${input}`
          init = { ...init, credentials: init?.credentials || 'include' }
        }
      } else if (input instanceof URL) {
        if (input.pathname.startsWith('/api/') || input.pathname.startsWith('/uploads/')) {
          input = new URL(input.pathname + input.search, normalizedBase)
          init = { ...init, credentials: init?.credentials || 'include' }
        }
      }
      return originalFetch.call(this, input, init)
    }
  }
})
