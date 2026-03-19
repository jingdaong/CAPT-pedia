import { useState, useEffect } from 'react'
import Layout from '../components/Layout.jsx'
import Spinner from '../components/Spinner.jsx'
import ReplyModal from '../components/ReplyModal.jsx'
import { api } from '../api.js'
import { timeAgo, formatDate } from '../utils.js'

export default function Questions() {
  const [questions, setQuestions] = useState([])
  const [committees, setCommittees] = useState([])
  const [filter, setFilter] = useState('')
  const [committeeFilter, setCommitteeFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [replyTarget, setReplyTarget] = useState(null)

  async function doLoad(f, c) {
    setLoading(true)
    setError('')
    try {
      const qs = await api.questions(f, c)
      setQuestions(qs)
    } catch {
      setError('Failed to load questions.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    api.committees().then(setCommittees).catch(() => {})
    doLoad('', '')
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  function handleFilterChange(newFilter) {
    setFilter(newFilter)
    doLoad(newFilter, committeeFilter)
  }

  function handleCommitteeChange(e) {
    const val = e.target.value
    setCommitteeFilter(val)
    doLoad(filter, val)
  }

  return (
    <Layout>
      <div className="header-row">
        <div>
          <h1>Questions</h1>
          <p>View and reply to questions from Telebot users.</p>
        </div>
        <button
          className="btn btn-secondary"
          onClick={() => doLoad(filter, committeeFilter)}
          style={{ alignSelf: 'center' }}
        >
          Refresh
        </button>
      </div>

      {error && <p className="alert alert-error">{error}</p>}

      {/* Filters */}
      <div className="card" style={{ padding: '1rem 1.4rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div className="filter-group">
            {[['', 'All'], ['pending', 'Pending'], ['answered', 'Answered']].map(([val, label]) => (
              <button
                key={val}
                className={'filter-btn' + (filter === val ? ' active' : '')}
                onClick={() => handleFilterChange(val)}
              >
                {label}
              </button>
            ))}
          </div>

          <select
            value={committeeFilter}
            onChange={handleCommitteeChange}
            className="filter-select"
          >
            <option value="">All Committees</option>
            {committees.map(c => (
              <option key={c.short_name} value={c.short_name}>{c.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* List */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: '3rem' }}>
          <Spinner size="2rem" />
        </div>
      ) : questions.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--muted)' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>💬</div>
          <p style={{ fontSize: '1.1rem', fontWeight: 600, margin: '0 0 0.4rem' }}>No questions found</p>
          <p className="small" style={{ margin: 0 }}>Check back later or change the filter above.</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1rem' }}>
          {questions.map(q => (
            <QuestionCard key={q.id} question={q} onReply={() => setReplyTarget(q)} />
          ))}
        </div>
      )}

      <ReplyModal
        question={replyTarget}
        onClose={() => setReplyTarget(null)}
        onReplied={() => doLoad(filter, committeeFilter)}
      />
    </Layout>
  )
}

function QuestionCard({ question: q, onReply }) {
  const isPending = q.status === 'pending'

  return (
    <div className={'card question-card' + (isPending ? ' question-card--pending' : '')}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Meta row */}
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', marginBottom: '0.6rem', flexWrap: 'wrap' }}>
            <span style={{ fontFamily: 'monospace', fontSize: '0.78rem', color: 'var(--muted)' }}>
              #{q.id}
            </span>
            <span className="badge badge-new">{q.committee_name}</span>
            <span className={'badge ' + (isPending ? 'badge-pending' : 'badge-answer')}>
              {isPending ? 'Pending' : 'Answered'}
            </span>
          </div>

          {/* Question text */}
          <p style={{ margin: '0 0 0.6rem', fontWeight: 500, lineHeight: 1.55 }}>
            {q.question_text}
          </p>

          {/* Timestamps */}
          <div
            className="small"
            style={{ display: 'flex', gap: '1.2rem', flexWrap: 'wrap' }}
          >
            <span>{timeAgo(q.created_at)}</span>
            {q.answered_by && (
              <span>
                Answered by <strong>{q.answered_by}</strong>
                {' · '}{formatDate(q.answered_at)}
              </span>
            )}
          </div>

          {/* Inline reply preview */}
          {q.reply_text && (
            <div className="reply-preview">
              <div className="reply-preview__label">Reply sent</div>
              <p style={{ margin: 0, lineHeight: 1.55 }}>{q.reply_text}</p>
            </div>
          )}
        </div>

        {isPending && (
          <button
            className="btn btn-primary"
            onClick={onReply}
            style={{ whiteSpace: 'nowrap', flexShrink: 0 }}
          >
            Reply
          </button>
        )}
      </div>
    </div>
  )
}
