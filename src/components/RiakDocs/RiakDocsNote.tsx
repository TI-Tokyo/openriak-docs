import React from 'react';

export default function RiakDocsNote({title, children}) {
  return (
    <div className="blocknote">
        {title && <div className="blocknote__title">{title}</div>}
        {children}
    </div>);
}
