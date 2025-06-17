// src/components/LogOnRender.tsx
import React, { useEffect } from 'react';

export default function LogOnRender() {
  useEffect(() => {
    console.error("🔥 MDX Component rendered");
  }, []);
  return null;
}
