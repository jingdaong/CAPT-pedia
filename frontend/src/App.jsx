import { useState, useEffect, useContext } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { api } from './api.js'
import { AuthContext } from './auth.js'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Questions from './pages/Questions.jsx'

function ProtectedRoute({ children }) {
  const { director } = useContext(AuthContext)
  if (!director) return <Navigate to="/" replace />
  return children
}

export default function App() {
  // undefined = loading, null = not logged in, object = logged in
  const [director, setDirector] = useState(undefined)

  useEffect(() => {
    api.me()
      .then(setDirector)
      .catch(() => setDirector(null))
  }, [])

  if (director === undefined) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <div className="spinner" />
      </div>
    )
  }

  return (
    <AuthContext.Provider value={{ director, setDirector }}>
      <Routes>
        <Route
          path="/"
          element={director ? <Navigate to="/dashboard" replace /> : <Login />}
        />
        <Route
          path="/dashboard"
          element={<ProtectedRoute><Dashboard /></ProtectedRoute>}
        />
        <Route
          path="/questions"
          element={<ProtectedRoute><Questions /></ProtectedRoute>}
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthContext.Provider>
  )
}
