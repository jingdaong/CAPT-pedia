import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api.js'
import { useAuth } from '../auth.js'

export default function Login() {
  const { setDirector } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [code, setCode] = useState('')
  const [step, setStep] = useState('email') // 'email' | 'otp'
  const [loading, setLoading] = useState(false)
  const [info, setInfo] = useState('')
  const [error, setError] = useState('')

  async function handleRequestCode(e) {
    e.preventDefault()
    setError('')
    setInfo('')
    setLoading(true)
    try {
      await api.requestCode(email.trim().toLowerCase())
      setStep('otp')
      setInfo('Verification code sent — check your inbox.')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleVerifyCode(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await api.verifyCode(email.trim().toLowerCase(), code.trim())
      setDirector(user)
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleResend() {
    setError('')
    setInfo('')
    setLoading(true)
    try {
      await api.requestCode(email.trim().toLowerCase())
      setInfo('A new code has been sent.')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function goBack() {
    setStep('email')
    setCode('')
    setError('')
    setInfo('')
  }

  return (
    <div className="login-screen">
      <div className="login-card" role="main">
        <h1>CAPT-pedia</h1>
        <p>Directors Portal — answer questions from your Telebot users.</p>

        {step === 'email' ? (
          <form onSubmit={handleRequestCode} style={{ display: 'grid', gap: '1.25rem' }}>
            <div className="form-row">
              <label htmlFor="login-email">NUS Email</label>
              <input
                id="login-email"
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="e1234567@u.nus.edu"
                required
                autoComplete="email"
                autoFocus
              />
            </div>
            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? 'Sending…' : 'Send Verification Code'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyCode} style={{ display: 'grid', gap: '1.25rem' }}>
            <p style={{ margin: 0, color: 'rgba(255,255,255,0.75)', fontSize: '0.9rem' }}>
              Code sent to <strong style={{ color: 'white' }}>{email}</strong>
            </p>
            <div className="form-row">
              <label htmlFor="login-code">Verification Code</label>
              <input
                id="login-code"
                type="text"
                inputMode="numeric"
                maxLength={8}
                value={code}
                onChange={e => setCode(e.target.value)}
                placeholder="Enter code from your email"
                required
                autoFocus
              />
            </div>
            <button className="login-btn" type="submit" disabled={loading}>
              {loading ? 'Verifying…' : 'Verify & Sign In'}
            </button>
            <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem' }}>
              <button type="button" className="link-btn" onClick={handleResend} disabled={loading}>
                Resend code
              </button>
              <button type="button" className="link-btn" onClick={goBack}>
                Use a different email
              </button>
            </div>
          </form>
        )}

        {info && <p className="form-message success" style={{ marginTop: '1rem' }}>{info}</p>}
        {error && <p className="form-message error" style={{ marginTop: '1rem' }}>{error}</p>}

        <p style={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.35)', marginTop: '2rem', textAlign: 'center' }}>
          Access restricted to NUS email domains.
        </p>
      </div>
    </div>
  )
}
