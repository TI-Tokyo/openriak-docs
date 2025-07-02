import React, { createContext, useContext, useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useOSSelection } from '../OSSelection/OSSelectionContext';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import semver from 'semver';

const ConfigReferenceContext = createContext(null);

export interface LinkInfo {
  url: string;
  text: string;
}

export interface ConfigEntry {
  pattern: string;
  since?: string;
  until?: string;
  relatedPages: string[];
}

export interface Extras {
  links: Record<string, LinkInfo>;
  configs: ConfigEntry[];
}

export const ConfigReferenceProvider = ({ sectionName ='', configNamePattern = '', children }) => {
  const { selected } = useOSSelection();
  const os = selected?.openriakType ?? 'default';
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [configurationOptions, setConfigurationOptions] = useState(null);
  const [extras, setExtras] = useState(null);
  const {siteConfig} = useDocusaurusContext();

  const location = useLocation();

//  const locationMatch = location.pathname?.match(/^\/docs\/([^\/]+)\/([0-9]+\.[0-9]+\.[0-9]+)\/.*$/s);
  const locationMatch = location.pathname?.match(/^\/docs\/([^\/]+)(\/(([0-9]+\.[0-9]+\.[0-9]+)\/?)?.*)?$/s);
  const project = locationMatch?.[1] ?? '';
  var version = locationMatch?.[4] ?? '';

  if (!project) {
    throw new Error("No project could be found from the current location.");
  }
  
  //console.log(siteConfig.customFields);

  if (!siteConfig.customFields) {
    throw new Error("'customFields' is missing.");
  }

  if (!siteConfig.customFields.versionPicker) {
    throw new Error("'customFields.versionPicker' is missing.");
  }

  if (!siteConfig.customFields.versionPicker[project]) {
    throw new Error(`'customFields.versionPicker.$project' is missing.`);
  }

  const activeProjectConfig = siteConfig.customFields.versionPicker[project];
  const currentVersion = activeProjectConfig["current"] ?? '';

  if (!version) {
    //console.log(`Using fallback version for project "${project}".`)
    version = currentVersion ?? '';
  }

  if (!version) {
    throw new Error(`No version could be found from the current location or from 'customFields.versionPicker.${project}.current'.`);
  }

  //console.log(`Loading configuration reference data for project "${project}" version "${version}".`)

  const configurationOptionsDataPath = `metadata/config-reference/openriak-${project}-${version}.config-reference.${os}.json`;
  const configurationOptionsURL = useBaseUrl(configurationOptionsDataPath);

  const extrasDataPath = `metadata/config-reference/openriak-${project}.extras.json`;
  const extrasURL = useBaseUrl(extrasDataPath);

  useEffect(() => {
    let active = true;

    const fetchData = async () => {
      try {
        //console.log("Fetching data for tables...");
        //console.log(`Fetch ${configurationOptionsURL}...`);
        const configurationOptionsRes = await fetch(configurationOptionsURL);
        if (!configurationOptionsRes.ok) throw new Error(`HTTP ${configurationOptionsRes.status}`);
        const configurationOptionsJson = await configurationOptionsRes.json();

        if (!configurationOptionsJson || !configurationOptionsJson.mappings) {
          console.log(configurationOptionsJson);
          throw new Error("configurationOptionsJson was not loaded properly.");
        }

        if (configNamePattern && configurationOptionsJson?.mappings) {
          const filteredMappings = Object.fromEntries(
            Object.entries(configurationOptionsJson.mappings).filter(([key, value]) => {
              return (key.match(configNamePattern));
            })
          );
          configurationOptionsJson.mappings = filteredMappings;
        }

        if (sectionName && configurationOptionsJson?.mappings) {
          const filteredMappings = Object.fromEntries(
            Object.entries(configurationOptionsJson.mappings).filter(([key, value]) => {
              return (value['docSections'] && value['docSections'].includes(sectionName));
            })
          );
          configurationOptionsJson.mappings = filteredMappings;
        }
        //console.log(json);
        if (configurationOptionsJson?.mappings) {
          configurationOptionsJson.mappings = Object.fromEntries(
            Object.entries(configurationOptionsJson.mappings)
              .sort(([keyA], [keyB]) => keyA.localeCompare(keyB))
          );
        }

        //console.log(`Fetch ${extrasURL}...`);
        const extrasRes = await fetch(extrasURL);
        if (!extrasRes.ok) throw new Error(`HTTP ${extrasRes.status}`);
        const extrasJson : Extras = await extrasRes.json();

        //console.log(extrasJson);
        const filteredConfigs = extrasJson.configs.filter((item, index) => {
            try {
              //console.log(item);
              if (item["since"] && !semver.gte(version, item.since)) {
                //console.log(`Removing as since ${item.since} but version ${version}`)
                return false;
              }
              if (item["until"] && !semver.lte(version, item.until)) {
                //console.log(`Removing as until ${item.until} but version ${version}`)
                return false;
              }
              //console.log(`Keeping version ${version} (since: ${item["since"] || 'none'}, until: ${item["until"] || 'none'})`)
              return true;
            } catch (err) {
              console.error(`Error filtering item ${index}:`, err, item);
              return false;
            }
          });

        extrasJson.configs = filteredConfigs;
        //console.log(extrasJson);

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
