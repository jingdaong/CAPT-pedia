import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout.jsx'
import Spinner from '../components/Spinner.jsx'
import ReplyModal from '../components/ReplyModal.jsx'
import { api } from '../api.js'
import { useAuth } from '../auth.js'
import { timeAgo } from '../utils.js'

export default function Dashboard() {
  const { director } = useAuth()
  const [questions, setQuestions] = useState([])
  const [committees, setCommittees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [replyTarget, setReplyTarget] = useState(null)

  const firstName = (director?.name || 'Director').split(/\s+/)[0]
  const pendingCount = questions.filter(q => q.status === 'pending').length
  const answeredCount = questions.filter(q => q.status === 'answered').length
  const recentPending = questions.filter(q => q.status === 'pending').slice(0, 5)

  useEffect(() => {
    async function load() {
      setLoading(true)
      try {
        const [qs, cs] = await Promise.all([api.questions(), api.committees()])
        setQuestions(qs)
        setCommittees(cs)
      } catch {
        setError('Failed to load data.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function handleReplied() {
    try {
      const qs = await api.questions()
      setQuestions(qs)
    } catch {
      // silently ignore refresh failure
    }
  }

  return (
    <Layout>
      <div className="header-row">
        <div>
          <h1>Welcome, {firstName}!</h1>
          <p>Here are the latest questions from Telebot users.</p>
        </div>
      </div>

      {error && <p className="alert alert-error">{error}</p>}

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#f57c00' }}>
            {loading ? '—' : pendingCount}
          </div>
          <div className="stat-label">Pending</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#388E3C' }}>
            {loading ? '—' : answeredCount}
          </div>
          <div className="stat-label">Answered</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--primary)' }}>
            {loading ? '—' : questions.length}
          </div>
          <div className="stat-label">Total</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--muted)' }}>
            {loading ? '—' : committees.length}
          </div>
          <div className="stat-label">Committees</div>
        </div>
      </div>

      {/* Recent pending questions */}
      <div className="card">
        <div className="card-header">
          <h2>Pending Questions</h2>
          <Link to="/questions" className="btn btn-secondary">View All</Link>
        </div>

        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '2.5rem' }}>
            <Spinner />
          </div>
        ) : recentPending.length === 0 ? (
          <p style={{ padding: '2rem', textAlign: 'center', color: 'var(--muted)' }}>
            No pending questions — great work! 🎉
          </p>
        ) : (
          <div>
            {recentPending.map((q, i) => (
              <div
                key={q.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'flex-start',
                  gap: '1rem',
                  padding: '1.2rem 1.5rem',
                  borderBottom: i < recentPending.length - 1 ? '1px solid var(--border)' : 'none',
                }}
              >
                <div>
                  <div style={{ fontWeight: 600 }}>{q.question_text}</div>
                  <div className="small" style={{ marginTop: '0.3rem', display: 'flex', gap: '0.6rem', alignItems: 'center' }}>
                    <span className="badge badge-new">{q.committee_name}</span>
                    {timeAgo(q.created_at)}
                  </div>
                </div>
                <button
                  className="btn btn-secondary"
                  style={{ whiteSpace: 'nowrap', minWidth: '80px' }}
                  onClick={() => setReplyTarget(q)}
                >
                  Reply
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <ReplyModal
        question={replyTarget}
        onClose={() => setReplyTarget(null)}
        onReplied={handleReplied}
      />
    </Layout>
  )
}
