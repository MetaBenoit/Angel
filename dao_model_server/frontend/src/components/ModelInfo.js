import React, { useState, useEffect } from 'react';
import { chatAPI } from '../services/api';

const ModelInfo = () => {
  const [modelStatus, setModelStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchModelStatus = async () => {
    try {
      setLoading(true);
      const status = await chatAPI.getModelStatus();
      setModelStatus(status);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReloadModel = async () => {
    try {
      setLoading(true);
      await chatAPI.reloadModel();
      await fetchModelStatus();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModelStatus();
    const interval = setInterval(fetchModelStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'ready':
      case 'healthy':
        return '#10b981';
      case 'loading':
        return '#f59e0b';
      default:
        return '#ef4444';
    }
  };

  if (loading && !modelStatus) {
    return (
      <div className="info-card">
        <h3>Loading model status...</h3>
      </div>
    );
  }

  if (error) {
    return (
      <div className="info-card error">
        <h3>Error loading model status</h3>
        <p>{error}</p>
        <button onClick={fetchModelStatus} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="model-info">
      <div className="info-card">
        <h3>🚀 Professional Dao Model</h3>
        <div className="metric">
          <span>Status:</span>
          <span 
            className="metric-value" 
            style={{color: getStatusColor(modelStatus?.status)}}
          >
            {modelStatus?.status || 'Unknown'}
          </span>
        </div>
        <div className="metric">
          <span>Model:</span>
          <span className="metric-value">dao_ires_lifestyle</span>
        </div>
        <div className="metric">
          <span>Architecture:</span>
          <span className="metric-value">Professional Angel</span>
        </div>
        <button onClick={handleReloadModel} className="reload-button" disabled={loading}>
          {loading ? 'Reloading...' : 'Reload Model'}
        </button>
      </div>
    </div>
  );
};

export default ModelInfo;