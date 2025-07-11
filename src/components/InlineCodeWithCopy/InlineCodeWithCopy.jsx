import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './inlineCodeWithCopy.module.css';
import { CopyIcon, CopiedIcon } from './CopyIcons';

export default function InlineCodeWithCopy({ children }) {
  const [copied, setCopied] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(children);
      setCopied(true);
      setTimeout(() => setFadeOut(true), 500);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Copy failed', err);
    }
  };

  return (
    <span className={styles.wrapper}>
      <code className={styles.code}>{children}</code>
      <button
        type="button"
        className={clsx('clean-btn', styles.copyButton)}
        onClick={handleCopy}
        aria-label={copied ? 'Copied!' : 'Copy code'}
      >
        {copied ? <CopiedIcon className={styles.iconCopied} /> : <CopyIcon className={styles.icon} />}
      </button>
    </span>
  );
}
