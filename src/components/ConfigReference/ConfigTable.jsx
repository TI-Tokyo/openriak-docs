import './ConfigTable.css';
import React, { useState, useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from '@tanstack/react-table';
import { getDataTypeList, getDefaultValue, getComments, getSees, getAnchorFromName } from '@site/src/components/ConfigReference/Columns'
import { CollapsibleDatatypeSection } from '@site/src/components/ConfigReference/CollapsibleDatatypeSection'

export function ConfigTable({schemaData}) {
  //console.log(schemaData);
  const [globalFilter, setGlobalFilter] = useState('');
  const [columnFilters, setColumnFilters] = useState([]);
  const [sorting, setSorting] = useState([]);
 
  const columns = useMemo(() => [
    {
      header: 'Config Name',
      accessorKey: 'configName',
      cell: info => {
        const configName = info.row.original.configName;
        const settingName = info.row.original.settingName || 'UNKNOWN';
        const anchor = getAnchorFromName(configName);
        return (
          <div>
            <code id={anchor} style={{ fontSize: '1em' }}>{configName}</code><br />
            <i style={{ fontSize: '0.85em', color: '#666' }}>maps to <code>{settingName}</code></i>
          </div>
        );
      },
    },
    {
      accessorFn: row => {return (row ?? '')},
      header: 'Details',
      cell: info => {
        const defaultContents = getDefaultValue(info);
        const datatypeContents = getDataTypeList(info);
        const commentContents = getComments(info);
        const alsoSeeContents = getSees(info);
        //console.log(alsoSeeContents);

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
            {commentContents.length > 0 && 
            <div
              key="valueInfo-comments"
              style={{
                display: 'grid',
                gridTemplateColumns: '120px 1fr',
                alignItems: 'start',
              }}
            >
              <span key="valueInfo-comments-label">Comments:</span>
              <span key="valueInfo-comments-value" style={{ paddingLeft: '1em', borderLeftWidth: '1px', borderLeftStyle: 'dotted', borderLeftColor: '#666' }}>{commentContents}</span>
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
              <span key="valueInfo-hidden-label">Status:</span>
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
    },
/*
    {
      accessorKey: 'comment',
      header: 'Comments',
      cell: info => (info.getValue() || []).map(line => <p>{line}</p>),
    },
*/
  ], []);

  const dataSource = Object.values(schemaData.mappings);

  function doesItemMatch(item, terms) {
    if (typeof item === 'string') {
      for (const term of terms) {
        if (item.toLowerCase().includes(term)) {
          //console.log(item + ' includes ' + term);
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
      for (const [key,value] of Object.entries(item)) {
        if (doesItemMatch(key, terms)) { return true;}
        if (doesItemMatch(value, terms)) { return true;}
      }
    } else {
      return doesItemMatch(JSON.stringify(item), terms);
    }
    return false;
  }  

  const filteredData = useMemo(() => {
    if (!globalFilter) return dataSource;
   
    const searchResults = dataSource.filter(item => {
      return doesItemMatch(item, [globalFilter.trim()])
      });
    //console.log(searchResults);
    return searchResults;
  }, [globalFilter]);

  const table = useReactTable({
    data: filteredData,
    columns,
    state: {
      sorting,
      globalFilter,
      columnFilters,
    },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <>
      <input
        value={globalFilter ?? ''}
        onChange={e => setGlobalFilter(e.target.value)}
        placeholder="🔍 Search..."
        style={{ padding: '0.5rem', width: '100%', marginBottom: '1rem' }}
      />

      <table className="table" style={{ 
        width: '100%', 
        borderCollapse: 'collapse',
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