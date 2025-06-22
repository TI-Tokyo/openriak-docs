// src/components/SomeOtherComponent.tsx
import React from 'react';
import { useOSSelection } from '@site/src/components/OSSelection/OSSelectionContext';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function ChosenOS() {
  const { selected } = useOSSelection();

  return <span className='chosenOS'><img src={useBaseUrl(selected.smallLogo)} alt={selected.displayName} style={{height: "0.8em"}} /> {selected.displayName}</span>;
}
