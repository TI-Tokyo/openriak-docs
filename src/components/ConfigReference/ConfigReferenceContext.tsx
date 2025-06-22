// src/context/ResourceContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useOSSelection } from '../OSSelection/OSSelectionContext';

const ConfigReferenceContext = createContext(null);

export const ConfigReferenceProvider = ({ sectionName, configNamePattern, children }) => {
    const { selected } = useOSSelection();
    const os = selected?.openriakType ?? 'default';
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [configurationOptions, setConfigurationOptions] = useState(null);
    const [extras, setExtras] = useState(null);

    const location = useLocation();
    const [, project, version] = location.pathname.match(/^\/docs\/([^\/]+)\/([0-9]+\.[0-9]+\.[0-9]+)\/.*$/s);

    const configurationOptionsDataPath = `metadata/config-reference/openriak-${project}-${version}.config-reference.${os}.json`;
    const configurationOptionsURL = useBaseUrl(configurationOptionsDataPath);

    const extrasDataPath = `metadata/config-reference/openriak-${project}-${version}.extras.json`;
    const extrasURL = useBaseUrl(extrasDataPath);

    useEffect(() => {
        let active = true;

        const fetchData = async () => {
            try {
                //console.log("Fetching data for tables...");
                //console.log(`Fetch ${configurationOptionsDataPath}...`);
                const configurationOptionsRes = await fetch(configurationOptionsURL);
                if (!configurationOptionsRes.ok) throw new Error(`HTTP ${configurationOptionsRes.status}`);
                const configurationOptionsJson = await configurationOptionsRes.json();

                if (configNamePattern) {
                const filteredMappings = Object.fromEntries(
                    Object.entries(configurationOptionsJson.mappings).filter(([key, value]) => {
                    return (key.match(configNamePattern));
                    })
                );
                configurationOptionsJson.mappings = filteredMappings;
                }
                
                if (sectionName) {
                const filteredMappings = Object.fromEntries(
                    Object.entries(configurationOptionsJson.mappings).filter(([key, value]) => {
                    return (value['docSections'] && value['docSections'].includes(sectionName));
                    })
                );
                configurationOptionsJson.mappings = filteredMappings;
                }
                //console.log(json);
                configurationOptionsJson.mappings = Object.fromEntries(
                    Object.entries(configurationOptionsJson.mappings)
                        .sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
                );
            
                const extrasRes = await fetch(extrasURL);
                if (!extrasRes.ok) throw new Error(`HTTP ${extrasRes.status}`);
                const extrasJson = await extrasRes.json();
                if (active) {
                    setExtras(extrasJson);
                    setConfigurationOptions(configurationOptionsJson);
                    setLoading(false);
                }
            } catch (err) {
                if (active) {
                    setError(err);
                    setLoading(false);
                }
            }
        };

        fetchData();
        return () => {
            active = false;
        };
    }, [selected]);
    return (
        <ConfigReferenceContext.Provider value={{ configurationOptions, extras, loading, error }}>
        {children}
        </ConfigReferenceContext.Provider>
    );
};

export const useResource = () => useContext(ConfigReferenceContext);
