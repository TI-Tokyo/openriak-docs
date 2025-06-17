import React, { useState, useMemo, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { ConfigTable } from './ConfigTable';

export function ConfigTableLoader() {
  const location = useLocation();
  const [schemaData, setSchemaData] = useState(null);
  const [, project, version] = location.pathname.match(/^\/docs\/([^\/]+)\/([0-9]+\.[0-9]+\.[0-9]+)\/.*$/s);
  const schemaDataPath = `cached-data/schemas/${project}/${version}/openriak-${project}-${version}.default.schema.json`;
  const url = useBaseUrl(schemaDataPath);
  
  // Fetch JSON data from a URL
  useEffect(() => {
    if (!schemaData) {
    const fetchData = async () => {
      try {
        //console.log(url);
        const res = await fetch(url); // relative to site root
        const json = await res.json();
        //console.log(json);
        setSchemaData(json);
      } catch (error) {
        console.error('Failed to load configuration reference data:', error);
      }
    };

    fetchData();
  }
  }, []);

  if (!schemaData) return <div>Loading...</div>;

  return <ConfigTable schemaData={schemaData} />;
}