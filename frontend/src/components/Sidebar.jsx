import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth.js'
import { api } from '../api.js'

const NAV_ITEMS = [
  { path: '/dashboard', icon: '📊', label: 'Dashboard' },
  { path: '/questions', icon: '💬', label: 'My Questions' },
]

export default function Sidebar() {
  const location = useLocation()
  const navigate = useNavigate()
  const { director, setDirector } = useAuth()

  const name = director?.name || 'Director'
  const email = director?.email || ''
  const initials = name
    .split(/\s+/)
    .slice(0, 2)
    .map(w => w[0]?.toUpperCase() ?? '')
    .join('')

  async function handleLogout() {
    await api.logout()
    setDirector(null)
    navigate('/')
  }

  return (
    <aside className="sidebar" aria-label="Navigation">
      <div className="sidebar-header">
        <div className="sidebar-avatar" aria-hidden="true">{initials}</div>
        <div>
          <h3>{name}</h3>
          <p className="small">Committee Director</p>
        </div>
      </div>

      <ul className="sidebar-nav" role="menu">
        {NAV_ITEMS.map(item => (
          <li key={item.path}>
            <Link
              to={item.path}
              role="menuitem"
              className={location.pathname === item.path ? 'active' : ''}
            >
              <span className="icon">{item.icon}</span>
              {item.label}
            </Link>
          </li>
        ))}
      </ul>

      <div className="sidebar-footer">
        <div className="small">
          Logged in as<br />
          <strong>{email}</strong>
        </div>
        <button
          className="btn btn-secondary"
          style={{ width: '100%', marginTop: '1rem' }}
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>
    </aside>
  )
}
