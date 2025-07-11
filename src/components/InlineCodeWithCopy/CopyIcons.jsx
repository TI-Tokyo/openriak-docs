import React from 'react';

export function CopyIcon(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      width="1em"
      height="1em"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  );
}

export function CopiedIcon(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      width="1em"
      height="1em"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}
