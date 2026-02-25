import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts Component - Fetching from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        console.log('Workouts Component - Response status:', response.status);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Raw data received:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching workouts:', error);
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
        <h2>Workout Suggestions</h2>
        <p className="api-endpoint">API Endpoint: {API_URL}</p>
      </div>
      
      {workouts.length === 0 ? (
        <div className="empty-state">
          <p>No workout suggestions found.</p>
        </div>
      ) : (
        <div className="table-container">
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Workout Name</th>
                  <th>Description</th>
                  <th>Exercises</th>
                </tr>
              </thead>
              <tbody>
                {workouts.map((workout) => (
                  <tr key={workout.id}>
                    <td>
                      <strong className="text-primary">{workout.name}</strong>
                    </td>
                    <td>
                      {workout.description ? (
                        <span>{workout.description}</span>
                      ) : (
                        <span className="text-muted">No description</span>
                      )}
                    </td>
                    <td>
                      {workout.exercises && Array.isArray(workout.exercises) && workout.exercises.length > 0 ? (
                        <div>
                          <span className="badge bg-success">{workout.exercises.length} exercises</span>
                          <br />
                          <small className="text-muted">
                            {workout.exercises.map((exercise, idx) => (
                              <div key={idx} className="mt-1">
                                {typeof exercise === 'string' ? exercise : JSON.stringify(exercise)}
                              </div>
                            ))}
                          </small>
                        </div>
                      ) : (
                        <span className="text-muted">No exercises listed</span>
                      )}
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

export default Workouts;
