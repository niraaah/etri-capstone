import { Link, NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-inner">
          <Link to="/search" className="app-brand">
            <span className="app-brand-mark" aria-hidden="true">
              📄
            </span>
            리서치 리포트
          </Link>
          <nav className="app-nav">
            <NavLink
              to="/search"
              className={({ isActive }) => `app-nav-link${isActive ? " active" : ""}`}
            >
              논문 검색
            </NavLink>
            <NavLink
              to="/reports"
              className={({ isActive }) => `app-nav-link${isActive ? " active" : ""}`}
              end
            >
              저장된 리포트
            </NavLink>
          </nav>
        </div>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  );
}
