import React, { useState, useMemo, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { ConfigTable } from './ConfigTable';

export function ConfigTableLoader({sectionName}) {
  const location = useLocation();
  const [, project, version] = location.pathname.match(/^\/docs\/([^\/]+)\/([0-9]+\.[0-9]+\.[0-9]+)\/.*$/s);

  const [configurationOptions, setConfigurationOptions] = useState(null);
  const configurationOptionsDataPath = `metadata/config-reference/openriak-${project}-${version}.config-reference.default.json`;
  const configurationOptionsURL = useBaseUrl(configurationOptionsDataPath);

  const [relatedPages, setRelatedPages] = useState(null);
  const relatedPagesDataPath = `metadata/config-reference/openriak-${project}-${version}.related-pages.json`;
  const relatedPagesURL = useBaseUrl(relatedPagesDataPath);
  
  // Fetch JSON data from a URL
  useEffect(() => {
    if (!configurationOptions) {
    const fetchData = async () => {
      try {
        //console.log(url);
        const configurationOptionsRes = await fetch(configurationOptionsURL);
        const configurationOptionsJson = await configurationOptionsRes.json();
        //console.log(json);

        if (sectionName) {
          const filteredMappings = Object.fromEntries(
            Object.entries(configurationOptionsJson.mappings).filter(([key, value]) => {
              return (value.docSections && value.docSections.includes(sectionName));
            })
          );
          configurationOptionsJson.mappings = filteredMappings;
        }
        //console.log(json);
        configurationOptionsJson.mappings = Object.fromEntries(
          Object.entries(configurationOptionsJson.mappings)
          .sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
        );

        const relatedPagesRes = await fetch(relatedPagesURL);
        const relatedPagesJson = await relatedPagesRes.json();
        setRelatedPages(relatedPagesJson);
        setConfigurationOptions(configurationOptionsJson);
      } catch (error) {
        console.error('Failed to load configuration reference data:', error);
      }
    };

    fetchData();
  }
  }, []);

  if (!configurationOptions) return <div>Loading...</div>;

  return <ConfigTable configurationOptions={configurationOptions} relatedPages={relatedPages}/>;
}