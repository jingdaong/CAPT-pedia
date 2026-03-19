import Sidebar from './Sidebar.jsx'

export default function Layout({ children }) {
  return (
    <div className="portal">
      <div className="layout container">
        <Sidebar />
        <main className="portal-main" role="main">
          {children}
        </main>
      </div>
    </div>
  )
}
