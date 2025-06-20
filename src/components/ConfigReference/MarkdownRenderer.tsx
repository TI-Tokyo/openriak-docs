import React from 'react';
import { marked } from 'marked';
import sanitizeHtml from 'sanitize-html';

type MarkdownRendererProps = {
     markdown: string;
};

export default function MarkdownRenderer({ markdown }: MarkdownRendererProps) {
    const dirtyHtml = marked(markdown);
    const safeHtml = sanitizeHtml(dirtyHtml.toString(), {
        allowedAttributes: {
            '*': ['href', 'src', 'alt', 'title'], // explicitly omit sidebarPath
        },
    });

    return <div dangerouslySetInnerHTML={{ __html: safeHtml }} />;
}
