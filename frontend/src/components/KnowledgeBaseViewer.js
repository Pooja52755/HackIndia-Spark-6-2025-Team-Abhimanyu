import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './KnowledgeBaseViewer.css';

const KnowledgeBaseViewer = () => {
  const [knowledgeData, setKnowledgeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [selectedRelationship, setSelectedRelationship] = useState(null);
  const [view, setView] = useState('categories'); // 'categories', 'entities', 'relationships'
  
  useEffect(() => {
    const fetchKnowledgeBase = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/knowledge');
        setKnowledgeData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load knowledge base data');
        setLoading(false);
        console.error('Error fetching knowledge base:', err);
      }
    };
    
    fetchKnowledgeBase();
  }, []);
  
  if (loading) {
    return <div className="knowledge-loading">Loading knowledge base...</div>;
  }
  
  if (error) {
    return <div className="knowledge-error">{error}</div>;
  }
  
  const handleCategorySelect = (category) => {
    setSelectedEntity(category);
    setView('entities');
  };
  
  const handleBackToCategories = () => {
    setSelectedEntity(null);
    setSelectedRelationship(null);
    setView('categories');
  };
  
  const handleEntitySelect = (entity) => {
    setSelectedRelationship(entity);
    setView('relationships');
  };
  
  const renderCategoriesView = () => {
    return (
      <div className="knowledge-categories">
        <h3>Cybersecurity Knowledge Categories</h3>
        <div className="category-grid">
          {knowledgeData && Object.keys(knowledgeData.entities).map(category => (
            <div 
              key={category} 
              className="category-card"
              onClick={() => handleCategorySelect(category)}
            >
              <h4>{formatCategoryName(category)}</h4>
              <p>{knowledgeData.entities[category].length} items</p>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  const renderEntitiesView = () => {
    if (!selectedEntity || !knowledgeData) return null;
    
    return (
      <div className="knowledge-entities">
        <button className="back-button" onClick={handleBackToCategories}>
          &larr; Back to Categories
        </button>
        <h3>{formatCategoryName(selectedEntity)}</h3>
        <div className="entity-list">
          {knowledgeData.entities[selectedEntity].map(entity => (
            <div 
              key={entity} 
              className="entity-item"
              onClick={() => handleEntitySelect(entity)}
            >
              <h4>{entity}</h4>
              {isInRelationships(entity) && (
                <span className="has-relationships">Has relationships</span>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  const renderRelationshipsView = () => {
    if (!selectedRelationship || !knowledgeData) return null;
    
    return (
      <div className="knowledge-relationships">
        <button className="back-button" onClick={() => {
          setSelectedRelationship(null);
          setView('entities');
        }}>
          &larr; Back to {formatCategoryName(selectedEntity)}
        </button>
        <h3>Relationships for {selectedRelationship}</h3>
        
        {/* MitigatedBy relationships */}
        {knowledgeData.relationships.MitigatedBy && 
         knowledgeData.relationships.MitigatedBy[selectedRelationship] && (
          <div className="relationship-section">
            <h4>Mitigated By</h4>
            <ul className="relationship-list">
              {knowledgeData.relationships.MitigatedBy[selectedRelationship].map(item => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        )}
        
        {/* DetectedBy relationships */}
        {knowledgeData.relationships.DetectedBy && 
         knowledgeData.relationships.DetectedBy[selectedRelationship] && (
          <div className="relationship-section">
            <h4>Detected By</h4>
            <ul className="relationship-list">
              {knowledgeData.relationships.DetectedBy[selectedRelationship].map(item => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        )}
        
        {/* Check if this entity mitigates any threats */}
        {Object.entries(knowledgeData.relationships.MitigatedBy || {}).filter(
          ([threat, mitigations]) => mitigations.includes(selectedRelationship)
        ).length > 0 && (
          <div className="relationship-section">
            <h4>Mitigates Threats</h4>
            <ul className="relationship-list">
              {Object.entries(knowledgeData.relationships.MitigatedBy || {})
                .filter(([threat, mitigations]) => mitigations.includes(selectedRelationship))
                .map(([threat]) => (
                  <li key={threat}>{threat}</li>
                ))
              }
            </ul>
          </div>
        )}
        
        {/* Check if this entity detects any threats */}
        {Object.entries(knowledgeData.relationships.DetectedBy || {}).filter(
          ([threat, detectors]) => detectors.includes(selectedRelationship)
        ).length > 0 && (
          <div className="relationship-section">
            <h4>Detects Threats</h4>
            <ul className="relationship-list">
              {Object.entries(knowledgeData.relationships.DetectedBy || {})
                .filter(([threat, detectors]) => detectors.includes(selectedRelationship))
                .map(([threat]) => (
                  <li key={threat}>{threat}</li>
                ))
              }
            </ul>
          </div>
        )}
        
        {/* If no relationships found */}
        {!hasAnyRelationships(selectedRelationship) && (
          <p className="no-relationships">No specific relationships found for this entity in the knowledge base.</p>
        )}
      </div>
    );
  };
  
  // Helper functions
  const formatCategoryName = (name) => {
    // Convert camelCase or PascalCase to spaced words
    return name.replace(/([A-Z])/g, ' $1').trim();
  };
  
  const isInRelationships = (entity) => {
    if (!knowledgeData) return false;
    
    // Check if entity is in MitigatedBy
    if (knowledgeData.relationships.MitigatedBy && 
        (knowledgeData.relationships.MitigatedBy[entity] || 
         Object.values(knowledgeData.relationships.MitigatedBy).some(
           mitigations => mitigations.includes(entity)
         ))) {
      return true;
    }
    
    // Check if entity is in DetectedBy
    if (knowledgeData.relationships.DetectedBy && 
        (knowledgeData.relationships.DetectedBy[entity] || 
         Object.values(knowledgeData.relationships.DetectedBy).some(
           detectors => detectors.includes(entity)
         ))) {
      return true;
    }
    
    return false;
  };
  
  const hasAnyRelationships = (entity) => {
    if (!knowledgeData) return false;
    
    // Check if entity has any relationships
    if (knowledgeData.relationships.MitigatedBy && knowledgeData.relationships.MitigatedBy[entity]) {
      return true;
    }
    
    if (knowledgeData.relationships.DetectedBy && knowledgeData.relationships.DetectedBy[entity]) {
      return true;
    }
    
    // Check if entity is used in any relationships
    if (Object.values(knowledgeData.relationships.MitigatedBy || {}).some(
      mitigations => mitigations.includes(entity)
    )) {
      return true;
    }
    
    if (Object.values(knowledgeData.relationships.DetectedBy || {}).some(
      detectors => detectors.includes(entity)
    )) {
      return true;
    }
    
    return false;
  };
  
  // Render the appropriate view
  return (
    <div className="knowledge-base-container">
      <div className="knowledge-header">
        <h2>Cybersecurity Knowledge Base</h2>
        <p>Explore entities and their relationships in our cybersecurity knowledge base</p>
      </div>
      
      {view === 'categories' && renderCategoriesView()}
      {view === 'entities' && renderEntitiesView()}
      {view === 'relationships' && renderRelationshipsView()}
    </div>
  );
};

export default KnowledgeBaseViewer;