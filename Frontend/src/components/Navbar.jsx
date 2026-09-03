import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="container navbar-content">
        <Link to="/" className="navbar-brand">🚗 VSM</Link>
        <div className="navbar-links">
          <Link to="/">Dashboard</Link>
          <Link to="/customers">Customers</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;