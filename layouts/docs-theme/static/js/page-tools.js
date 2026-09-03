(() => {
  'use strict';

  const writeClipboard = async (value) => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const field = document.createElement('textarea');
    field.value = value;
    field.setAttribute('readonly', '');
    field.style.position = 'fixed';
    field.style.opacity = '0';
    document.body.append(field);
    field.select();
    try {
      if (!document.execCommand('copy')) throw new Error('Copy command was rejected');
    } finally {
      field.remove();
    }
  };

  const parseJsonSource = (element) => {
    try { return JSON.parse(element?.textContent || '""'); } catch (_) { return ''; }
  };

  document.querySelectorAll('.heading-permalink').forEach((link) => {
    link.addEventListener('click', async (event) => {
      event.preventDefault();
      const marker = link.querySelector('span');
      const originalLabel = link.getAttribute('aria-label') || 'Copy link to this section';
      try {
        await writeClipboard(new URL(link.getAttribute('href'), window.location.href).href);
        link.setAttribute('aria-label', 'Section URL copied');
        link.title = 'Section URL copied';
        if (marker) marker.textContent = '✓';
      } catch (_) {
        link.setAttribute('aria-label', 'Could not copy section URL');
        link.title = 'Could not copy section URL';
      }
      window.setTimeout(() => {
        link.setAttribute('aria-label', originalLabel);
        link.title = originalLabel;
        if (marker) marker.textContent = '#';
      }, 1400);
    });
  });

  const pageTools = document.querySelector('[data-doc-page-tools]');
  if (pageTools) {
    const issueLinks = [...pageTools.querySelectorAll('[data-report-documentation]')];
    const feedbackStatus = pageTools.querySelector('[data-feedback-status]');
    const feedbackFollowUp = pageTools.querySelector('[data-feedback-follow-up]');
    const voteButtons = [...pageTools.querySelectorAll('[data-feedback-vote]')];
    const storageKey = `openriak-docs-feedback:${pageTools.dataset.pagePath}`;
    const twoWeeks = 14 * 24 * 60 * 60 * 1000;

    const selectedOs = () => {
      const id = document.documentElement.dataset.selectedOs || '';
      const label = document.querySelector('[data-os-trigger] .picker-label')?.textContent?.trim() || id;
      return { id, label };
    };
    const pageUrl = (includeOs = false) => {
      const url = new URL(window.location.href);
      url.searchParams.delete('highlight');
      url.searchParams.delete('os');
      const os = selectedOs();
      if (includeOs && os.id) url.searchParams.set('os', os.id);
      return url;
    };
    const issueUrl = () => {
      const url = new URL(pageTools.dataset.issueBase);
      if (/\/issues\/?$/.test(url.pathname)) url.pathname = `${url.pathname.replace(/\/$/, '')}/new`;
      const os = selectedOs();
      const section = window.location.hash ? decodeURIComponent(window.location.hash.slice(1)) : 'Not specified';
      const body = [
        '## Documentation problem',
        '',
        `- Page: ${pageTools.dataset.pageTitle}`,
        `- URL: ${pageUrl(true).href}`,
        `- Product: ${pageTools.dataset.productName}`,
        `- Version: ${pageTools.dataset.productVersion}`,
        `- Operating system: ${os.label || 'Not selected'}${os.id && os.label !== os.id ? ` (${os.id})` : ''}`,
        `- Section: ${section}`,
        '',
        '## What is missing or incorrect?',
        '',
        '<!-- Please describe the problem. -->',
        '',
        '## Suggested improvement',
        '',
        '<!-- If you have a suggestion, please add it here. -->'
      ].join('\n');
      url.searchParams.set('title', `Documentation problem: ${pageTools.dataset.pageTitle}`);
      url.searchParams.set('body', body);
      return url.href;
    };
    const updateIssueLinks = () => issueLinks.forEach((link) => { link.href = issueUrl(); });
    updateIssueLinks();
    issueLinks.forEach((link) => {
      link.addEventListener('focus', updateIssueLinks);
      link.addEventListener('pointerdown', updateIssueLinks);
    });
    new MutationObserver(updateIssueLinks).observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-selected-os']
    });

    const readVote = () => {
      try {
        const stored = JSON.parse(localStorage.getItem(storageKey) || 'null');
        if (!stored || stored.expiresAt <= Date.now() || !['yes', 'no'].includes(stored.vote)) {
          localStorage.removeItem(storageKey);
          return '';
        }
        return stored.vote;
      } catch (_) { return ''; }
    };
    const renderVote = (vote, changed = false) => {
      voteButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.feedbackVote === vote)));
      feedbackFollowUp.hidden = vote !== 'no';
      feedbackStatus.textContent = vote
        ? `You answered ${vote === 'yes' ? 'Yes' : 'No'}.${changed ? ' Your updated answer has been saved.' : ' You can change your answer.'}`
        : '';
    };
    const trackVote = (vote) => {
      const endpoint = new URL(pageTools.dataset.feedbackEndpoint, window.location.origin);
      const os = selectedOs();
      endpoint.searchParams.set('vote', vote);
      endpoint.searchParams.set('page', pageTools.dataset.pagePath);
      endpoint.searchParams.set('product', pageTools.dataset.productName);
      endpoint.searchParams.set('version', pageTools.dataset.productVersion);
      if (os.id) endpoint.searchParams.set('os', os.id);
      endpoint.searchParams.set('_', String(Date.now()));
      fetch(endpoint, { method: 'GET', cache: 'no-store', credentials: 'omit', keepalive: true }).catch(() => {});
    };
    let currentVote = readVote();
    renderVote(currentVote);
    voteButtons.forEach((button) => button.addEventListener('click', () => {
      const vote = button.dataset.feedbackVote;
      if (vote === currentVote) return;
      currentVote = vote;
      try { localStorage.setItem(storageKey, JSON.stringify({ vote, expiresAt: Date.now() + twoWeeks })); } catch (_) {}
      trackVote(vote);
      renderVote(vote, true);
    }));

    const markdownButton = pageTools.querySelector('[data-copy-page-markdown]');
    const markdownSource = parseJsonSource(pageTools.querySelector('[data-page-markdown-source]'));
    markdownButton?.addEventListener('click', async () => {
      const label = markdownButton.querySelector('span');
      try {
        await writeClipboard(markdownSource);
        label.textContent = 'Copied Markdown';
      } catch (_) {
        label.textContent = 'Copy failed';
      }
      window.setTimeout(() => { label.textContent = 'Copy page as Markdown'; }, 1600);
    });
  }

  const shellTokens = (line) => line.match(/(?:[^\s"'\\]+|\\.|"(?:\\.|[^"])*"|'[^']*')+/g) || [];
  const shellCommentIndex = (line) => {
    let quote = '';
    let escaped = false;
    for (let index = 0; index < line.length; index += 1) {
      const character = line[index];
      if (escaped) {
        escaped = false;
        continue;
      }
      if (character === '\\' && quote !== "'") {
        escaped = true;
        continue;
      }
      if (quote) {
        if (character === quote) quote = '';
        continue;
      }
      if (character === '"' || character === "'") {
        quote = character;
        continue;
      }
      if (character === '#' && (index === 0 || /\s/.test(line[index - 1]))) return index;
    }
    return -1;
  };
  const splitShellCommands = (value) => {
    const lines = [];
    value.split('\n').forEach((line) => {
      if (!line.trim()) {
        lines.push(line);
        return;
      }
      const indentation = line.match(/^\s*/)?.[0] || '';
      const commentIndex = shellCommentIndex(line);
      const comment = commentIndex >= 0 ? line.slice(commentIndex) : '';
      const command = commentIndex >= 0 ? line.slice(0, commentIndex).trimEnd() : line;
      const tokens = shellTokens(command.trim());
      const firstOption = tokens.findIndex((token) => /^--?[A-Za-z]/.test(token));
      if (firstOption < 1) {
        lines.push(line);
        return;
      }
      const groups = [];
      tokens.slice(firstOption).forEach((token) => {
        if (/^--?[A-Za-z]/.test(token)) groups.push([token]);
        else groups[groups.length - 1].push(token);
      });
      const prefix = `${indentation}${tokens.slice(0, firstOption).join(' ')}`;
      lines.push(`${prefix} \\`);
      groups.forEach((group, groupIndex) => {
        const lastGroup = groupIndex === groups.length - 1;
        lines.push(`${indentation}    ${group.join(' ')}${lastGroup && comment ? ` ${comment}` : ''}${lastGroup ? '' : ' \\'}`);
      });
    });
    return { source: lines.join('\n'), lineNumbers: lines.map((_, index) => String(index + 1)) };
  };
  const renderCodeLines = (code, source, lineNumbers = source.split('\n').map((_, index) => String(index + 1))) => {
    let lines = [...code.children].filter((child) => child.tagName === 'SPAN');
    if (lines.length !== lineNumbers.length) {
      code.replaceChildren();
      lines = source.split('\n').map((line) => {
        const span = document.createElement('span');
        span.textContent = line.length ? line : '\u00a0';
        code.append(span);
        return span;
      });
    }
    lines.forEach((line, index) => {
      line.classList.add('doc-code-line');
      line.dataset.lineNumber = lineNumbers[index] || '';
      if (!line.querySelector(':scope > .doc-code-line-content')) {
        const content = document.createElement('span');
        content.className = 'doc-code-line-content';
        while (line.firstChild) content.append(line.firstChild);
        line.append(content);
      }
    });
  };
  const appendShellToken = (content, value, className = '') => {
    if (!value) return;
    if (!className) {
      content.append(document.createTextNode(value));
      return;
    }
    const token = document.createElement('span');
    token.className = className;
    token.textContent = value;
    content.append(token);
  };
  const shellKeywords = new Set(['case', 'do', 'done', 'elif', 'else', 'esac', 'fi', 'for', 'function', 'if', 'in', 'select', 'then', 'time', 'until', 'while']);
  const highlightShellLine = (content, value) => {
    content.replaceChildren();
    if (!value.length) {
      content.textContent = '\u00a0';
      return;
    }
    const commentIndex = shellCommentIndex(value);
    const command = commentIndex >= 0 ? value.slice(0, commentIndex) : value;
    let index = 0;
    let commandWord = true;
    while (index < command.length) {
      const character = command[index];
      if (/\s/.test(character)) {
        const end = command.slice(index).search(/\S/);
        const next = end < 0 ? command.length : index + end;
        appendShellToken(content, command.slice(index, next));
        index = next;
        continue;
      }
      if (character === "'" || character === '"' || character === '`') {
        const quote = character;
        let end = index + 1;
        while (end < command.length) {
          if (command[end] === '\\' && quote !== "'") {
            end += 2;
            continue;
          }
          if (command[end++] === quote) break;
        }
        appendShellToken(content, command.slice(index, end), quote === "'" ? 's1' : quote === '`' ? 'sb' : 's2');
        index = end;
        commandWord = false;
        continue;
      }
      const variable = command.slice(index).match(/^\$(?:\{[^}]+\}|[A-Za-z_][A-Za-z0-9_]*|[?#@*!$0-9-])/);
      if (variable) {
        appendShellToken(content, variable[0], 'nv');
        index += variable[0].length;
        continue;
      }
      const operator = command.slice(index).match(/^(?:&&|\|\||>>|<<|[|;&<>])/);
      if (operator) {
        appendShellToken(content, operator[0], 'o');
        index += operator[0].length;
        commandWord = true;
        continue;
      }
      const end = command.slice(index).search(/[\s'"`$|;&<>]/);
      const next = end < 0 ? command.length : index + end;
      const word = command.slice(index, next);
      let className = '';
      if (shellKeywords.has(word)) className = 'k';
      else if (/^[A-Za-z_][A-Za-z0-9_]*=/.test(word)) className = 'nv';
      else if (commandWord && !word.startsWith('-') && word !== '\\') className = 'nb';
      appendShellToken(content, word, className);
      if (!/^[A-Za-z_][A-Za-z0-9_]*=/.test(word) && word !== '\\') commandWord = false;
      index = next;
    }
    if (commentIndex >= 0) appendShellToken(content, value.slice(commentIndex), 'c1 doc-code-shell-comment');
  };
  const highlightShellCode = (code, source) => {
    const sourceLines = source.split('\n');
    [...code.querySelectorAll('.doc-code-line')].forEach((line, index) => {
      const value = sourceLines[index] || '';
      const content = line.querySelector(':scope > .doc-code-line-content') || line;
      highlightShellLine(content, value);
    });
  };

  const codeOptionsStorageKey = 'openriak-docs-code-options-v1';
  const codeAnchorStorageKey = 'openriak-docs-code-anchor-v1';
  const codeControllers = [];
  const codeControllersByLanguage = new Map();
  let codeOptions = {};
  let lastInteractedBlock = null;
  try {
    codeOptions = JSON.parse(window.localStorage.getItem(codeOptionsStorageKey) || '{}') || {};
  } catch (_) {
    codeOptions = {};
  }
  const preserveCodeBlockPosition = (block, update) => {
    const top = block.getBoundingClientRect().top;
    update();
    const nextTop = block.getBoundingClientRect().top;
    if (nextTop !== top) window.scrollBy(0, nextTop - top);
  };
  const nearestVisibleCodeBlock = () => {
    const visible = codeControllers.filter(({ block }) => {
      const bounds = block.getBoundingClientRect();
      return bounds.bottom > 0 && bounds.top < window.innerHeight;
    });
    if (!visible.length) return null;
    if (lastInteractedBlock && visible.some(({ block }) => block === lastInteractedBlock)) return lastInteractedBlock;
    return visible.sort((left, right) => Math.abs(left.block.getBoundingClientRect().top) - Math.abs(right.block.getBoundingClientRect().top))[0].block;
  };
  const storeCodeOptions = () => {
    try {
      window.localStorage.setItem(codeOptionsStorageKey, JSON.stringify(codeOptions));
    } catch (_) {
      // Display preferences still work for the current page when storage is unavailable.
    }
  };
  const syncCodeOption = (controller, option, enabled) => {
    lastInteractedBlock = controller.block;
    preserveCodeBlockPosition(controller.block, () => {
      (codeControllersByLanguage.get(controller.language) || [controller]).forEach((item) => item.applyOption(option, enabled));
    });
    codeOptions[controller.language] = { ...(codeOptions[controller.language] || {}), [option]: enabled };
    storeCodeOptions();
  };

  document.querySelectorAll('[data-code-block]').forEach((block, index) => {
    const language = (block.dataset.codeLanguage || 'text').toLowerCase();
    const source = parseJsonSource(block.querySelector('[data-code-source]'));
    const copyButton = block.querySelector('[data-code-copy]');
    const lineButton = block.querySelector('[data-code-lines]');
    const wrapButton = block.querySelector('[data-code-wrap]');
    const shellWrapButton = block.querySelector('[data-code-shell-wrap]');
    const downloadButton = block.querySelector('[data-code-download]');
    const highlighted = block.querySelector('[data-code-highlight]');
    const highlightedCode = highlighted?.querySelector('code');
    const shellView = block.querySelector('[data-code-shell-view]');
    const shellCode = shellView?.querySelector('code');
    const shellWrapped = shellWrapButton ? splitShellCommands(source) : null;
    const setLineNumberWidth = (lineCount) => block.style.setProperty('--code-line-number-digits', String(Math.max(1, String(lineCount).length)));
    const activeCodeSource = () => block.classList.contains('is-shell-wrapped') && shellWrapped ? shellWrapped.source : source;
    setLineNumberWidth(source.split('\n').length);
    if (highlightedCode) renderCodeLines(highlightedCode, source);
    if (shellCode && shellWrapped) {
      renderCodeLines(shellCode, shellWrapped.source, shellWrapped.lineNumbers);
      highlightShellCode(shellCode, shellWrapped.source);
    }
    const applyOption = (option, enabled) => {
      if (option === 'lineNumbers') {
        block.classList.toggle('has-line-numbers', enabled);
        lineButton?.setAttribute('aria-checked', String(enabled));
      } else if (option === 'wrap') {
        block.classList.toggle('is-wrapped', enabled);
        wrapButton?.setAttribute('aria-pressed', String(enabled));
      } else if (option === 'shellWrap' && shellWrapButton && shellWrapped) {
        block.classList.toggle('is-shell-wrapped', enabled);
        shellWrapButton.setAttribute('aria-pressed', String(enabled));
        highlighted.hidden = enabled;
        shellView.hidden = !enabled;
        setLineNumberWidth(enabled ? shellWrapped.lineNumbers.length : source.split('\n').length);
      }
    };
    const controller = { block, language, applyOption };
    codeControllers.push(controller);
    if (!codeControllersByLanguage.has(language)) codeControllersByLanguage.set(language, []);
    codeControllersByLanguage.get(language).push(controller);
    const savedOptions = codeOptions[language] || {};
    applyOption('lineNumbers', savedOptions.lineNumbers === true);
    applyOption('wrap', savedOptions.wrap === true);
    applyOption('shellWrap', savedOptions.shellWrap === true);

    copyButton?.addEventListener('click', async () => {
      const label = copyButton.querySelector('span');
      try {
        await writeClipboard(activeCodeSource());
        label.textContent = 'Copied';
      } catch (_) {
        label.textContent = 'Failed';
      }
      window.setTimeout(() => { label.textContent = 'Copy'; }, 1400);
    });
    lineButton?.addEventListener('click', () => {
      syncCodeOption(controller, 'lineNumbers', !block.classList.contains('has-line-numbers'));
    });
    wrapButton?.addEventListener('click', () => {
      syncCodeOption(controller, 'wrap', !block.classList.contains('is-wrapped'));
    });
    shellWrapButton?.addEventListener('click', () => {
      syncCodeOption(controller, 'shellWrap', !block.classList.contains('is-shell-wrapped'));
    });
    downloadButton?.addEventListener('click', () => {
      const generatedStem = [
        block.dataset.codeProduct || 'documentation',
        block.dataset.codeVersion,
        block.dataset.codePage || 'page',
        block.dataset.codePartialName || String(index + 1)
      ].filter(Boolean).join('-');
      const filename = `${block.dataset.codeFilename || generatedStem}.${block.dataset.codeExtension || 'txt'}`;
      const downloadSource = activeCodeSource();
      const url = URL.createObjectURL(new Blob([downloadSource], { type: 'text/plain;charset=utf-8' }));
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.append(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  });

  window.addEventListener('storage', (event) => {
    if (event.key !== codeOptionsStorageKey) return;
    try {
      codeOptions = JSON.parse(event.newValue || '{}') || {};
    } catch (_) {
      return;
    }
    const anchor = nearestVisibleCodeBlock();
    const applyStoredOptions = () => codeControllers.forEach((controller) => {
      const options = codeOptions[controller.language] || {};
      controller.applyOption('lineNumbers', options.lineNumbers === true);
      controller.applyOption('wrap', options.wrap === true);
      controller.applyOption('shellWrap', options.shellWrap === true);
    });
    if (anchor) preserveCodeBlockPosition(anchor, applyStoredOptions);
    else applyStoredOptions();
  });
  window.addEventListener('pagehide', () => {
    const block = nearestVisibleCodeBlock();
    if (!block) return;
    try {
      window.sessionStorage.setItem(codeAnchorStorageKey, JSON.stringify({
        path: window.location.pathname,
        index: codeControllers.findIndex((controller) => controller.block === block),
        top: block.getBoundingClientRect().top
      }));
    } catch (_) {
      // Native scroll restoration remains available when session storage is unavailable.
    }
  });
  window.addEventListener('pageshow', () => {
    let anchor;
    try {
      anchor = JSON.parse(window.sessionStorage.getItem(codeAnchorStorageKey) || 'null');
      window.sessionStorage.removeItem(codeAnchorStorageKey);
    } catch (_) {
      return;
    }
    if (!anchor || anchor.path !== window.location.pathname || !codeControllers[anchor.index]) return;
    window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
      const block = codeControllers[anchor.index].block;
      window.scrollBy(0, block.getBoundingClientRect().top - anchor.top);
    }));
  });
})();
