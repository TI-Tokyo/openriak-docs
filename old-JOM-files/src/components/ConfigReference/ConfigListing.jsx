import React, { useState, useMemo } from 'react';
import {
  flexRender,
} from '@tanstack/react-table';
import { getDataTypeListFromItem, getDefaultValueFromItem, getCommentsFromItem, getSeesFromItem, getAnchorFromName } from '@site/src/components/ConfigReference/Columns'
import InlineCodeWithCopy from "@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy";
import { useResource } from './ConfigReferenceContext';

export function ConfigListing(sectionName, configNamePattern) {
  const { configurationOptions, extras, loading, error } = useResource();

  if (loading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!configurationOptions || !configurationOptions.mappings)  return <p>Nothing to show.</p>;

  const outputResults = [];
  Object.values(configurationOptions.mappings).map((configSetting, index) => {
    const settingResults = [];
    
    // name
    const configName = configSetting.configName;
    const settingName = configSetting.settingName || '';
    const anchor = getAnchorFromName(configName);
    settingResults.push(
      <div className="config-name" key={'setting'+index} style={{marginTop: '1em'}}>
        <InlineCodeWithCopy key={'name'+index} id={anchor}>{configName}</InlineCodeWithCopy>
      </div>);

    const defaultContents = getDefaultValueFromItem(configSetting);
    const datatypeContents = getDataTypeListFromItem(configSetting);
    //const alsoSeeContents = getSeesFromItem(configSetting, extras);
    const hidden = configSetting.properties?.hidden ?? '';
    const commentContents = getCommentsFromItem(configSetting);

    settingResults.push(
      <div key="config-properties" style={{ display: 'grid', rowGap: '0.5rem', paddingLeft: '2em' }}>
        <div
          key="config-mapsto"
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr', // adjust 150px as needed
            alignItems: 'start',
          }}
        >
          <span key="valueInfo-default-label">Maps to:</span>
          <span key="valueInfo-default-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}><InlineCodeWithCopy>{settingName}</InlineCodeWithCopy></span>
        </div>

        <div
          key="config-default"
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr', // adjust 150px as needed
            alignItems: 'start',
          }}
        >
          <span key="valueInfo-default-label">Default value:</span>
          <span key="valueInfo-default-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{defaultContents}</span>
        </div>

        <div
          key="config-datatypes"
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr',
            alignItems: 'start',
          }}
        >
          <span key="config-datatypes-label">Valid datatype:</span>
          <span className="config-datatypes-value" key="config-datatypes-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{datatypeContents}</span>
        </div>

        <div
          key="config-hidden"
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr', // adjust 150px as needed
            alignItems: 'start',
          }}
        >
          <span key="config-hidden-label">Location:</span>
          {!hidden &&
            <span key="config-hidden-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>In <i>riak.conf</i>.</span>
          }
          {hidden &&
            <span key="config-hidden-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>Not in <i>riak.conf</i> but can be added.</span>
          }
        </div>
        {commentContents && <div
          key="config-comments"
          style={{
            display: 'grid',
            gridTemplateColumns: '120px 1fr',
            alignItems: 'start',
          }}
        >
          <span key="config-comments-label">Comments:</span>
          <span className="config-comments-value comments-value" key="config-comments-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{commentContents}</span>
        </div>}
      </div>
    )

    outputResults.push(<div className="configListingItem" key={'setting'+index}>{settingResults}</div>)
  });

  return <div className="configListings">{outputResults}</div>
}