import React, { useState, useMemo } from 'react';
import { getDefaultValueFromItem } from '@site/src/components/ConfigReference/Columns'
import InlineCodeWithCopy from "@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy";
import { useResource } from './ConfigReferenceContext';
import { ConfigReferenceProvider } from './ConfigReferenceContext';

export function ConfigDefaultValue({name}) {
  const { configurationOptions, extras, loading, error } = useResource();

  if (!configurationOptions) {
    return <>Loading...</>
  }

  const defValue = getDefaultValueFromItem(configurationOptions.mappings[name]);
  return <>{defValue}</>
}