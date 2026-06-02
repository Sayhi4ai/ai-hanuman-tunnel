export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const target = env.RUNTIME_URL + url.pathname + url.search;

    return fetch(target, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
  }
};
