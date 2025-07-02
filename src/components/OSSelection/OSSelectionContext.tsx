import { createContext, useContext, useEffect, useState } from 'react';
import osOptions from '@site/src/metadata/os/os.json';

type OSSelectionContextType = {
  selected: any; // Or a more specific type for your icons
  setSelected: React.Dispatch<React.SetStateAction<any>>;
};

const OSSelectionContext = createContext<OSSelectionContextType | null>(null);

export const OSSelectionProvider = ({ children }) => {
  //console.log("Doing OSSelectionProvider");
  const [selected, setSelected] = useState(null);
  if (!selected) {
    setSelected(osOptions[0]);
  }
  // Load selection from localStorage after mount
  useEffect(() => {
    const stored = localStorage?.getItem('osSelection') ?? '';
    if (stored) {
      setSelected(JSON.parse(stored))
    } else {
      setSelected(osOptions[0])
    }
  }, []);

  // Save selection to localStorage when it changes
  useEffect(() => {
    if (localStorage && selected !== null) {
      localStorage.setItem('osSelection', JSON.stringify(selected));
    }
  }, [selected]);
  //console.log("Returning useOSSelection");

  return (
    <OSSelectionContext.Provider value={{ selected, setSelected }}>
      {children}
    </OSSelectionContext.Provider>
  );
};

export const useOSSelection = (): OSSelectionContextType => {
  const context = useContext(OSSelectionContext);
  if (!context) {
    throw new Error('useOSSelection must be used within an OSSelectionProvider');
  }
  return context;
};