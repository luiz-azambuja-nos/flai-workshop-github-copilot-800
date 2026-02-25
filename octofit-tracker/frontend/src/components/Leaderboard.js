import React, { useState, useEffect } from 'react';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;

  useEffect(() => {
    console.log('Leaderboard Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Leaderboard Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard Component - Processed data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return (
    <div className="container mt-4">
      <div className="loading-spinner">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  );
  
  if (error) return (
    <div className="container mt-4">
      <div className="error-message">
        <strong>Error:</strong> {error}
      </div>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="component-header">
        <h2>Leaderboard</h2>
        <p className="api-endpoint">API Endpoint: {API_URL}</p>
      </div>
      
      {leaderboard.length === 0 ? (
        <div className="empty-state">
          <p>No leaderboard data found.</p>
        </div>
      ) : (
        <div className="table-container">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>User</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((entry, index) => (
                  <tr key={entry.id || index}>
                    <td>
                      {index === 0 ? (
                        <span className="badge bg-warning text-dark">🏆 1st</span>
                      ) : index === 1 ? (
                        <span className="badge bg-secondary">🥈 2nd</span>
                      ) : index === 2 ? (
                        <span className="badge bg-info text-dark">🥉 3rd</span>
                      ) : (
                        <span className="badge bg-light text-dark">{index + 1}</span>
                      )}
                    </td>
                    <td>
                      <strong>
                        {entry.user_name || 
                         (typeof entry.user === 'object' ? entry.user.username : entry.user) || 
                         'Unknown User'}
                      </strong>
                    </td>
                    <td>
                      <span className="badge bg-success">{entry.score || 0} points</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
