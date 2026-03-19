import { useState, useEffect } from 'react'
import { api } from '../api.js'

export default function ReplyModal({ question, onClose, onReplied }) {
  const [replyText, setReplyText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (question) {
      setReplyText('')
      setError('')
    }
  }, [question])

  // Close on Escape
  useEffect(() => {
    function onKey(e) {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])

  async function handleSubmit(e) {
    e.preventDefault()
    const text = replyText.trim()
    if (!text) {
      setError('Reply cannot be empty.')
      return
    }
    setLoading(true)
    setError('')
    try {
      await api.reply(question.id, text)
      onReplied()
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (!question) return null

  return (
    <div
      className="modal-backdrop"
      onClick={e => { if (e.target === e.currentTarget) onClose() }}
    >
      <div className="modal-content" role="dialog" aria-modal="true">
        <div className="modal-header">
          <div>
            <h2 style={{ margin: 0 }}>
              Reply{' '}
              <span style={{ color: 'var(--primary)', fontFamily: 'monospace', fontSize: '0.9rem' }}>
                #{question.id}
              </span>
            </h2>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.9rem', color: 'var(--muted)' }}>
              {question.committee_name}
            </p>
          </div>
          <button className="modal-close" onClick={onClose} aria-label="Close modal">
            ×
          </button>
        </div>

        <div className="modal-body">
          <div className="question-quote">
            "{question.question_text}"
          </div>

          <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1rem' }}>
            <div className="form-row">
              <label htmlFor="modal-reply">Your Reply</label>
              <textarea
                id="modal-reply"
                rows={5}
                value={replyText}
                onChange={e => setReplyText(e.target.value)}
                placeholder="Type your reply here…"
                required
                autoFocus
                style={{ resize: 'vertical' }}
              />
            </div>

            {error && <p className="form-message error">{error}</p>}

            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end' }}>
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Sending…' : 'Send Reply'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
