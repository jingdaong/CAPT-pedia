async function apiFetch(url, options = {}) {
  const { suppressAuthError = false, ...fetchOptions } = options
  const response = await fetch(url, { credentials: 'include', ...fetchOptions })

  if (response.status === 401) {
    const err = new Error('Not authenticated')
    err.status = 401
    throw err
  }

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    const err = new Error(data.detail || `Request failed (${response.status})`)
    err.status = response.status
    throw err
  }

  return response.json()
}

export const api = {
  me: () => apiFetch('/api/me'),

  requestCode: (email) =>
    apiFetch('/auth/request-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
    }),

  verifyCode: (email, code) =>
    apiFetch('/auth/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, code }),
    }),

  logout: () =>
    fetch('/auth/logout', { method: 'POST', credentials: 'include' }),

  questions: (filter, committee) => {
    const params = new URLSearchParams()
    if (filter) params.set('filter', filter)
    if (committee) params.set('committee', committee)
    const qs = params.toString()
    return apiFetch('/api/questions' + (qs ? '?' + qs : ''))
  },

  reply: (questionId, replyText) =>
    apiFetch(`/api/questions/${questionId}/reply`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reply_text: replyText }),
    }),

  committees: () => apiFetch('/api/committees'),
}
