/* eslint-disable no-unused-vars */
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { customerAI, customerApi } from '../../services/customerApi';
import Loading from '../../components/Loading';
import ErrorMessage from '../../components/ErrorMessage';

function CustomerAI() {
  const { id } = useParams();
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [question, setQuestion] = useState('');
  const [aiError, setAiError] = useState('');
  const [mode, setMode] = useState('summary'); // 'summary' or 'ask'

  useEffect(() => {
    const load = async () => {
      try {
        const res = await customerApi.getById(id);
        setCustomer(res.data);
      } catch (err) {
        setAiError('Could not load customer.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [id]);

  const generateSummary = async () => {
    setAiLoading(true);
    setAiError('');
    try {
      const res = await customerAI.summary(parseInt(id), { question: '' });
      setSummary(res.data.summary);
    } catch (err) {
      setAiError('AI service error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setAiLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) return;
    setAiLoading(true);
    setAiError('');
    try {
      const res = await customerAI.ask(parseInt(id), question);
      setSummary(res.data.summary);
    } catch (err) {
      setAiError('AI error: ' + (err.response?.data?.detail || err.message));
    } finally {
      setAiLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (!customer) return <div>Customer not found.</div>;

  return (
    <div>
      <h2>AI Assistant – {customer.firstName} {customer.lastName}</h2>
      <div className="ai-controls">
        <button 
          className={`btn ${mode === 'summary' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => { setMode('summary'); setSummary(''); setAiError(''); }}
        >
          Summary
        </button>
        <button 
          className={`btn ${mode === 'ask' ? 'btn-primary' : 'btn-secondary'}`}
          onClick={() => { setMode('ask'); setSummary(''); setAiError(''); }}
        >
          Ask Question
        </button>
      </div>

      {mode === 'summary' && (
        <div>
          <p>Click below to generate a comprehensive AI summary for this customer.</p>
          <button onClick={generateSummary} disabled={aiLoading} className="btn btn-primary">
            {aiLoading ? 'Generating...' : 'Generate Summary'}
          </button>
        </div>
      )}

      {mode === 'ask' && (
        <div className="ask-section">
          <div className="form-group">
            <label>Your Question</label>
            <input 
              type="text" 
              value={question} 
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What maintenance is due for this customer?"
            />
          </div>
          <button onClick={askQuestion} disabled={aiLoading || !question.trim()} className="btn btn-primary">
            {aiLoading ? 'Thinking...' : 'Ask'}
          </button>
        </div>
      )}

      {aiLoading && <Loading />}
      {aiError && <ErrorMessage message={aiError} />}
      {summary && (
        <div className="ai-response">
          <h3>AI Response</h3>
          <div className="response-content">{summary}</div>
        </div>
      )}

      <div className="actions">
        <Link to={`/customers/${id}`} className="btn btn-secondary">Back to Customer</Link>
        <Link to="/customers" className="btn btn-secondary">All Customers</Link>
      </div>
    </div>
  );
}

export default CustomerAI;