import { NavLink } from 'react-router-dom';

function Sidebar() {
  return (
    <aside className="sidebar">
      <ul>
        <li><NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>Dashboard</NavLink></li>
        <li><NavLink to="/customers" className={({ isActive }) => isActive ? 'active' : ''}>Customers</NavLink></li>
      </ul>
    </aside>
  );
}

export default Sidebar;