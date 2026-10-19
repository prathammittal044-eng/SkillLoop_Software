export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    if (
      url.pathname.startsWith('/api/') ||
      url.pathname.startsWith('/socket.io/') ||
      url.pathname.startsWith('/uploads/')
    ) {
      const backendBase = (env.API_BASE_URL || 'https://zoggy-skillloop-backend.hf.space').replace(/\/+$/, '')
      const targetUrl = new URL(url.pathname + url.search, backendBase)

      const headers = new Headers(request.headers)
      headers.set('Host', targetUrl.host)
      headers.set('Origin', backendBase)

      const init = {
        method: request.method,
        headers,
        redirect: 'manual'
      }
      if (request.method !== 'GET' && request.method !== 'HEAD') {
        init.body = request.body
      }

      const response = await fetch(targetUrl.toString(), init)
      const resHeaders = new Headers(response.headers)
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: resHeaders
      })
    }
    return env.ASSETS.fetch(request)
  }
}
