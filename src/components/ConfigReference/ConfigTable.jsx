import React, { useState, useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from '@tanstack/react-table';
import { getDataTypeList, getDefaultValue, getComments, getSees, getAnchorFromName } from '@site/src/components/ConfigReference/Columns'
import InlineCodeWithCopy from "@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy";
import { useResource } from './ConfigReferenceContext';
import SetStateLink from './SetStateLink';
import DebouncedInput from './DebouncedInput';

export function ConfigTable(sectionName, configNamePattern) {
  const { configurationOptions, extras, loading, error } = useResource();
  const [globalFilter, setGlobalFilter] = useState('');
  const [columnFilters, setColumnFilters] = useState([]);
  const [sorting, setSorting] = useState([]);
  const columns = useMemo(() => [
    {
      header: 'Config Name',
      accessorKey: 'configName',
      cell: info => {
        const configName = info.row.original.configName;
        const settingName = info.row.original.settingName || '';
        const anchor = getAnchorFromName(configName);
        return (
          <div id={anchor} >
            <InlineCodeWithCopy style={{ fontSize: '1em' }}>{configName}</InlineCodeWithCopy><br />
            {settingName && <i style={{ fontSize: '0.85em', color: '#666' }}>maps to <InlineCodeWithCopy>{settingName}</InlineCodeWithCopy></i>}
          </div>
        );
      },
    },
    {
      accessorFn: row => { return (row ?? '') },
      header: 'Details',
      cell: info => {
        const { configurationOptions, extras, loading, error } = useResource();
        const defaultContents = getDefaultValue(info);
        const datatypeContents = getDataTypeList(info);
        const commentContents = getComments(info);
        const alsoSeeContents = getSees(info, extras);

        return (
          <div key="valueInfo" style={{ display: 'grid', rowGap: '0.5rem' }}>
            <div
              key="valueInfo-default"
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
              key="valueInfo-datatypes"
              style={{
                display: 'grid',
                gridTemplateColumns: '120px 1fr',
                alignItems: 'start',
              }}
            >
              <span key="valueInfo-datatypes-label">Valid datatype:</span>
              <span key="valueInfo-datatypes-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{datatypeContents}</span>
            </div>
            {commentContents &&
              <div
                key="valueInfo-comments"
                style={{
                  display: 'grid',
                  gridTemplateColumns: '120px 1fr',
                  alignItems: 'start',
                }}
              >
                <span key="valueInfo-comments-label">Comments:</span>
                <span key="valueInfo-comments-value" className="comments-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{commentContents}</span>
              </div>}
            {alsoSeeContents.length > 0 &&
              <div
                key="valueInfo-alsosees"
                style={{
                  display: 'grid',
                  gridTemplateColumns: '120px 1fr',
                  alignItems: 'start',
                }}
              >
                <span key="valueInfo-alsosees-label">Also see:</span>
                <span key="valueInfo-alsosees-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{alsoSeeContents}</span>
              </div>}
            <div
              key="hidden-hidden"
              style={{
                display: 'grid',
                gridTemplateColumns: '120px 1fr', // adjust 150px as needed
                alignItems: 'start',
              }}
            >
              <span key="valueInfo-hidden-label">Location:</span>
              {!info.getValue().properties?.hidden &&
                <span key="valueInfo-hidden-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>In <i>riak.conf</i>.</span>
              }
              {info.getValue().properties?.hidden &&
                <span key="valueInfo-hidden-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>Not in <i>riak.conf</i> but can be added.</span>
              }
            </div>
          </div>
        )
      },
    }
  ], []);

  function doesItemMatch(item, terms) {
    if (typeof item === 'string') {
      for (const term of terms) {
        if (item.toLowerCase().includes(term)) {
          return true;
        }
      }
    } else if (Array.isArray(item)) {
      for (const subItem of item) {
        if (doesItemMatch(subItem, terms)) {
          return true;
        }
      }
    } else if (typeof item == 'object') {
      for (const [key, value] of Object.entries(item)) {
        if (doesItemMatch(key, terms)) { return true; }
        if (doesItemMatch(value, terms)) { return true; }
      }
    } else {
      return doesItemMatch(JSON.stringify(item), terms);
    }
    return false;
  }

  const [recentFilters, setRecentFilters] = useState(getSavedRecentFilters());

  function removeFromRecentFilters(removeItem) {
    if (!removeItem.trim()) return;

    // Remove duplicates and add to front
    const updated = [...recentFilters.filter(item => item !== removeItem)];

    // Keep only the last 10
    const trimmed = updated.slice(0, 10);

    localStorage.setItem('recentConfigFilters', JSON.stringify(trimmed));
    setRecentFilters(trimmed);
  }

  function saveToRecentFilters(input) {
    if (!input.trim()) return;

    // Remove duplicates and add to front
    const updated = [input, ...recentFilters.filter(item => item !== input)];

    // Keep only the last 10
    const trimmed = updated.slice(0, 10);

    localStorage.setItem('recentConfigFilters', JSON.stringify(trimmed));
    setRecentFilters(trimmed);
  }

  function getSavedRecentFilters() {
    const stored = localStorage.getItem('recentConfigFilters');
    return stored ? JSON.parse(stored) : [];
  }

  const filteredData = useMemo(() => {
    if (!configurationOptions || !configurationOptions.mappings) return;
    const dataSource = Object.values(configurationOptions.mappings)
    if (!globalFilter) return dataSource;

    saveToRecentFilters(globalFilter);

    const searchResults = dataSource.filter(item => {
      return doesItemMatch(item, [globalFilter.trim().toLowerCase()])
    });
    return searchResults;
  }, [globalFilter, configurationOptions]);

  const table = useReactTable({
    data: filteredData,
    columns,
    state: {
      sorting,//: [{ id: 'configName', desc: false }],
      globalFilter,
      columnFilters,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  if (loading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;
  if (!table.getRowModel().rows) return <p>Loading table…</p>;

  //setRecentFilters(getSavedRecentFilters());
  
  const recentFiltersOutput = [];
  if (recentFilters.length > 0) {
    recentFiltersOutput.push(<span key="recentFilterLabel">Recently used filters:</span>);
    recentFilters.map((item, index) => {
      recentFiltersOutput.push(<SetStateLink key={'recentFilter-'+index} className="recentFilterLink" linkText={item} setValue={item} setMethod={setGlobalFilter} />);
      recentFiltersOutput.push(<a key={'clearRecentFilter-'+index} className="clearRecentFilter" href="#" onClick={(e) => { e.preventDefault(); removeFromRecentFilters(item);}}>❌</a>);
    });
  } else {
    recentFiltersOutput.push(<React.Fragment key="noRecentFiltersLabel">There are no recently used filters.</React.Fragment>);
  }

  return (
    <>
      <DebouncedInput
        value={globalFilter ?? ''}
        onChange={setGlobalFilter}
        placeholder="🔍 Search..."
        style={{ padding: '0.5rem', width: '100%', marginBottom: '0.125rem' }}
        delay="500"
      />
      <div className="recentFilters" style={{ paddingLeft: '1rem', marginBottom: '0.5rem' }}>{recentFiltersOutput}</div>
      <table className="table" style={{
        width: '100%',
        borderCollapse: 'collapse',
        borderWidth: '0.125rem'
      }}>
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th key={header.id} style={{ textAlign: 'left', padding: '0.5rem' }}>
                  <div
                    onClick={header.column.getToggleSortingHandler()}
                    style={{ cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                    {header.column.getIsSorted() === 'asc' ? ' 🔼' : header.column.getIsSorted() === 'desc' ? ' 🔽' : ''}
                  </div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.length === 0 ? (
            <tr><td colSpan={columns.length}>No matching results.</td></tr>
          ) : (
            table.getRowModel().rows.map(row => (
              <tr key={row.id}>
                {row.getVisibleCells().map(cell => (
                  <td key={cell.id} style={{ padding: '0.5rem', borderTop: '1px solid #ddd' }}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))
          )}
        </tbody>
      </table>
    </>
  );
}