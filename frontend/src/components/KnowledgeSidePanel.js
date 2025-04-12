import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './KnowledgeSidePanel.css';

const KnowledgeSidePanel = ({ activeEntities = [] }) => {
  const [knowledgeData, setKnowledgeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedCategories, setExpandedCategories] = useState({});
  
  useEffect(() => {
    const fetchKnowledgeBase = async () => {
      try {
        setLoading(true);
        console.log("Fetching knowledge base data...");
        const response = await axios.get('/knowledge');
        console.log("Knowledge base data received:", response.data);
        
        // Validate response structure
        if (!response.data || !response.data.entities || !response.data.relationships) {
          console.error("Invalid knowledge base data format:", response.data);
          setError('Invalid knowledge base data format');
          setLoading(false);
          return;
        }
        
        setKnowledgeData(response.data);
        
        // Initialize expanded categories based on active entities
        if (activeEntities.length > 0 && response.data) {
          const newExpanded = {};
          Object.keys(response.data.entities).forEach(category => {
            if (response.data.entities[category].some(entity => 
              activeEntities.includes(entity.toLowerCase())
            )) {
              newExpanded[category] = true;
            }
          });
          setExpandedCategories(newExpanded);
        }
        
        setLoading(false);
      } catch (err) {
        console.error("Error fetching knowledge base:", err);
        setError('Failed to load knowledge base data. ' + (err.response?.data?.detail || err.message));
        setLoading(false);
      }
    };
    
    fetchKnowledgeBase();
  }, [activeEntities]);
  
  const toggleCategory = (category) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };
  
  const formatCategoryName = (name) => {
    return name.replace(/([A-Z])/g, ' $1').trim();
  };
  
  const isEntityActive = (entity) => {
    return activeEntities.some(active => 
      entity.toLowerCase().includes(active.toLowerCase()) || 
      active.toLowerCase().includes(entity.toLowerCase())
    );
  };

  if (loading) {
    return <div className="side-panel-loading">Loading knowledge base...</div>;
  }
  
  if (error) {
    return <div className="side-panel-error">{error}</div>;
  }
  
  return (
    <div className="knowledge-side-panel">
      <div className="panel-header">
        <h3>Knowledge Base</h3>
        <p>Cybersecurity concepts and relationships</p>
      </div>
      
      <div className="panel-content">
        {knowledgeData && Object.keys(knowledgeData.entities).map(category => (
          <div key={category} className="entity-category">
            <div 
              className="category-header" 
              onClick={() => toggleCategory(category)}
            >
              <h4>
                <span className={`toggle-icon ${expandedCategories[category] ? 'expanded' : ''}`}>
                  {expandedCategories[category] ? '▼' : '▶'}
                </span>
                {formatCategoryName(category)}
              </h4>
              <span className="entity-count">{knowledgeData.entities[category].length}</span>
            </div>
            
            {expandedCategories[category] && (
              <ul className="entity-list">
                {knowledgeData.entities[category].map(entity => (
                  <li 
                    key={entity}
                    className={isEntityActive(entity) ? 'active-entity' : ''}
                  >
                    {entity}
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
      
      <div className="panel-footer">
        <h4>Relationships</h4>
        {knowledgeData && activeEntities.length > 0 && (
          <div className="relationships-section">
            {Object.entries(knowledgeData.relationships.MitigatedBy || {})
              .filter(([threat]) => 
                activeEntities.some(active => 
                  threat.toLowerCase().includes(active.toLowerCase()) || 
                  active.toLowerCase().includes(threat.toLowerCase())
                )
              )
              .map(([threat, mitigations]) => (
                <div key={threat} className="relationship-item">
                  <strong>{threat}</strong> is mitigated by:
                  <ul>
                    {mitigations.map(mitigation => (
                      <li key={mitigation}>{mitigation}</li>
                    ))}
                  </ul>
                </div>
              ))
            }
            
            {Object.entries(knowledgeData.relationships.DetectedBy || {})
              .filter(([threat]) => 
                activeEntities.some(active => 
                  threat.toLowerCase().includes(active.toLowerCase()) || 
                  active.toLowerCase().includes(threat.toLowerCase())
                )
              )
              .map(([threat, detectors]) => (
                <div key={threat} className="relationship-item">
                  <strong>{threat}</strong> is detected by:
                  <ul>
                    {detectors.map(detector => (
                      <li key={detector}>{detector}</li>
                    ))}
                  </ul>
                </div>
              ))
            }
            
            {/* Show defenses that mitigate active threats */}
            {activeEntities
              .filter(active => 
                Object.values(knowledgeData.relationships.MitigatedBy || {})
                  .some(mitigations => 
                    mitigations.some(mitigation => 
                      mitigation.toLowerCase().includes(active.toLowerCase()) || 
                      active.toLowerCase().includes(mitigation.toLowerCase())
                    )
                  )
              )
              .map(activeDefense => (
                <div key={activeDefense} className="relationship-item">
                  <strong>{activeDefense}</strong> mitigates:
                  <ul>
                    {Object.entries(knowledgeData.relationships.MitigatedBy || {})
                      .filter(([_, mitigations]) => 
                        mitigations.some(mitigation => 
                          mitigation.toLowerCase().includes(activeDefense.toLowerCase()) || 
                          activeDefense.toLowerCase().includes(mitigation.toLowerCase())
                        )
                      )
                      .map(([threat]) => (
                        <li key={threat}>{threat}</li>
                      ))
                    }
                  </ul>
                </div>
              ))
            }
          </div>
        )}
        
        {(!knowledgeData || activeEntities.length === 0) && (
          <p className="no-relationships">
            No active entities detected in the conversation.
            Ask a question about cybersecurity concepts to see their relationships.
          </p>
        )}
      </div>
    </div>
  );
};

export default KnowledgeSidePanel;