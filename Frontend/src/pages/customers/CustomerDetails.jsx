/* eslint-disable react-hooks/set-state-in-effect */
/* eslint-disable no-unused-vars */
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { customerApi } from '../../services/customerApi';
import Loading from '../../components/Loading';
import ErrorMessage from '../../components/ErrorMessage';
import ConfirmDialog from '../../components/ConfirmDialog';

function CustomerList() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteId, setDeleteId] = useState(null);
  const [showConfirm, setShowConfirm] = useState(false);

  const loadCustomers = async (query = '') => {
    try {
      setLoading(true);
      setError('');
      let response;
      if (query.trim()) {
        response = await customerApi.search(query);
      } else {
        response = await customerApi.getAll();
      }
      setCustomers(response.data);
    } catch (err) {
      setError('Failed to load customers.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomers();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    loadCustomers(searchTerm);
  };

  const handleDelete = async () => {
    if (!deleteId) return;
    try {
      await customerApi.delete(deleteId);
      setCustomers(customers.filter(c => c.id !== deleteId));
      setShowConfirm(false);
    } catch (err) {
      setError('Failed to delete customer.');
    }
  };

  if (loading) return <Loading />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <div className="list-header">
        <h2>Customers</h2>
        <Link to="/customers/new" className="btn btn-primary">+ New Customer</Link>
      </div>
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search by name, email, phone..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Search</button>
        <button type="button" onClick={() => { setSearchTerm(''); loadCustomers(); }}>Clear</button>
      </form>
      {customers.length === 0 ? (
        <div className="empty-state">No customers found.</div>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map(c => (
              <tr key={c.id}>
                <td>{c.id}</td>
                <td>{c.firstName} {c.lastName}</td>
                <td>{c.email}</td>
                <td>{c.phone}</td>
                <td>
                  <Link to={`/customers/${c.id}`} className="btn btn-sm">View</Link>
                  <Link to={`/customers/${c.id}/edit`} className="btn btn-sm btn-edit">Edit</Link>
                  <Link to={`/customers/${c.id}/ai`} className="btn btn-sm btn-ai">AI</Link>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => { setDeleteId(c.id); setShowConfirm(true); }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <ConfirmDialog
        isOpen={showConfirm}
        onConfirm={handleDelete}
        onCancel={() => setShowConfirm(false)}
        title="Delete Customer"
        message="Are you sure you want to delete this customer? This action cannot be undone."
      />
    </div>
  );
}

export default CustomerList;