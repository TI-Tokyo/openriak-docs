// src/components/SidebarIconDropdown.js
import React from 'react';
import osOptions from '@site/src/metadata/os/os.json';
import { useOSSelection } from '@site/src/components/OSSelection/OSSelectionContext';

export default function SidebarOSDropdown() {
  const { selected, setSelected } = useOSSelection();

  const handleChange = (e) => {
    const chosen = osOptions.find(opt => opt.displayName === e.target.value);
    setSelected(chosen);
  };

  return (
    <div style={{ padding: '0.5rem' }}>
      <label style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>Select OS:</label>
      <select
        style={{ marginTop: '0.25rem', width: '100%' }}
        value={selected?.displayName ?? ''}
        onChange={handleChange}
      >
        {osOptions.map(opt => (
          <option key={opt.displayName} value={opt.displayName}>
            {opt.smallLogo} {opt.displayName}
          </option>
        ))}
      </select>
    </div>
  );
}
