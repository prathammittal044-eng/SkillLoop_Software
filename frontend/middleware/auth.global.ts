export default defineNuxtRouteMiddleware(async (to, from) => {
  // Only execute on client-side navigation
  if (import.meta.server) return

  const publicRoutes = ['/', '/login', '/register']
  const isAuthPage = to.path === '/login' || to.path === '/register'
  const isProtectedPage = !publicRoutes.includes(to.path)

  try {
    const res = await fetch('/api/user/me', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      if (data.user) {
        if (typeof localStorage !== 'undefined') {
          localStorage.setItem('skillloop_auth_active', 'true')
        }
        // If already logged in and visiting login or register, automatically send to dashboard
        if (isAuthPage) {
          const redirect = (to.query.redirect as string) || '/dashboard'
          return navigateTo(redirect)
        }
        return
      }
    }
  } catch (e) {
    // Backend offline or unreachable
  }

  // Not authenticated
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem('skillloop_auth_active')
  }

  if (isProtectedPage) {
    return navigateTo(`/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }
})
