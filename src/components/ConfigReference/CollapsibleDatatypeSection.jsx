import React, { useState, useRef, useEffect } from 'react';
import './ClampedSection.css';

export function CollapsibleDatatypeSection({ datatypeContents }) {
  const [expanded, setExpanded] = useState(false);
  const [showControls, setShowControls] = useState(false);
  const contentRef = useRef(null);

  useEffect(() => {
    if (contentRef.current) {
      const lineHeight = parseFloat(getComputedStyle(contentRef.current).lineHeight) || 24;
      const maxLines = 4;
      const maxHeight = lineHeight * maxLines;
      if (contentRef.current.scrollHeight > maxHeight) {
        setShowControls(true);
      }
    }
  }, []);

  return (
    <div className="datatype-section">
      <div
        className={`clamp-wrapper ${expanded ? 'expanded' : ''}`}
        ref={contentRef}
      >
        {datatypeContents}
        {!expanded && showControls && <div className="fade-overlay" />}
      </div>
      {showControls && (
        <button className="expand-button" onClick={() => setExpanded(!expanded)}>
          {expanded ? 'Show less' : 'Show more'}
        </button>
      )}
    </div>
  );
}
