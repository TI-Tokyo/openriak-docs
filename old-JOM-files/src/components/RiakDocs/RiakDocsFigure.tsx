import React from 'react';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function RiakDocsNote({id, url, children}) {
  const safeUrl = useBaseUrl(url);
  return (
    <figure id={id} style={{textAlign: 'center'}}>
      <img src={safeUrl} alt={id} />
      <figcaption>{children}</figcaption>
    </figure>
  );
}
