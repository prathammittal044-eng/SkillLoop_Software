export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Proxy API, Socket.IO, and uploads to the Hugging Face Spaces backend
    if (
      url.pathname.startsWith('/api/') ||
      url.pathname.startsWith('/socket.io/') ||
      url.pathname.startsWith('/uploads/')
    ) {
      const backendUrl = env.API_BASE_URL || 'https://zoggy-skillloop-backend.hf.space';
      const target = new URL(url.pathname + url.search, backendUrl);

      const headers = new Headers(request.headers);
      headers.set('host', target.host);
      const clientIp = request.headers.get('cf-connecting-ip');
      if (clientIp) {
        headers.set('x-forwarded-for', clientIp);
      }
      headers.set('x-forwarded-proto', url.protocol.replace(':', ''));

      return fetch(new Request(target.toString(), {
        method: request.method,
        headers,
        body: request.body,
        redirect: 'follow',
        duplex: 'half'
      }));
    }

    // Serve static assets from Cloudflare edge
    return env.ASSETS.fetch(request);
  }
};
