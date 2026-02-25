import React, { useState, useEffect } from 'react';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Teams Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Teams Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams Component - Processed data:', teamsData);
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error fetching teams:', error);
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
        <h2>Teams</h2>
        <p className="api-endpoint">API Endpoint: {API_URL}</p>
      </div>
      
      {teams.length === 0 ? (
        <div className="empty-state">
          <p>No teams found.</p>
        </div>
      ) : (
        <div className="table-container">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Team Name</th>
                  <th>Members Count</th>
                  <th>Team Members</th>
                </tr>
              </thead>
              <tbody>
                {teams.map((team) => {
                  // Extract usernames from member objects
                  const memberUsernames = team.members && Array.isArray(team.members)
                    ? team.members.map(member => 
                        typeof member === 'object' ? member.username : member
                      ).filter(Boolean)
                    : [];
                  
                  return (
                    <tr key={team.id}>
                      <td>
                        <strong className="text-primary">{team.name}</strong>
                      </td>
                      <td>
                        {memberUsernames.length > 0 ? (
                          <span className="badge bg-info text-dark">{memberUsernames.length} members</span>
                        ) : (
                          <span className="badge bg-light text-dark">0 members</span>
                        )}
                      </td>
                      <td>
                        {memberUsernames.length > 0 ? (
                          <small className="text-muted">{memberUsernames.join(', ')}</small>
                        ) : (
                          <span className="text-muted">No members</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default Teams;
