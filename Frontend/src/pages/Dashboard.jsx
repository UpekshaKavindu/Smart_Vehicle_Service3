function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <p>Welcome to Vehicle Service Management System</p>
      <div className="stats">
        <div className="stat-card">Customers: 0</div>
        <div className="stat-card">Vehicles: 0</div>
        <div className="stat-card">Bookings: 0</div>
        <div className="stat-card">Service Records: 0</div>
      </div>
    </div>
  );
}

export default Dashboard;