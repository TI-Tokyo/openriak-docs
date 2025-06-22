import React from 'react';
import { marked } from 'marked';
import sanitizeHtml from 'sanitize-html';
import parse from 'html-react-parser';
import InlineCodeWithCopy from '../InlineCodeWithCopy/InlineCodeWithCopy';

type MarkdownRendererProps = {
     markdown: string;
};

export default function MarkdownRenderer({ markdown }: MarkdownRendererProps) {
//    const withCodeCopy = markdown;
    //const withCodeCopy = markdown.replace(/(^|[^`])`([^`\n]+?)`([^`]|$)/g, "$1<InlineCodeWithCopy>$2</InlineCodeWithCopy>$3");
    const withCodeCopy = markdown.replace(/(^|[^`])`([^`\n]+?)`([^`]|$)/g, (match, before, code, after) => {
        return `${before}<InlineCodeWithCopy>${code}</InlineCodeWithCopy>${after}`;
    });
    const dirtyHtml = marked(withCodeCopy);
    const safeHtml = sanitizeHtml(dirtyHtml.toString(), {
        allowedAttributes: {
            '*': ['href', 'src', 'alt', 'title'], // explicitly omit sidebarPath
        },
        allowedTags: sanitizeHtml.defaults.allowedTags.concat([ 'InlineCodeWithCopy' ]),
        parser: {
            lowerCaseTags: false,
            lowerCaseAttributeNames: false
        },
        transformTags: {
            'inlinecodewithcopy': 'InlineCodeWithCopy',
        }
    });

    const options = {
        replace: (domNode) => {
            if (domNode.name === 'InlineCodeWithCopy' || domNode.name === 'inlinecodewithcopy') {
                return <InlineCodeWithCopy>{domNode.children[0].data}</InlineCodeWithCopy>;
            }
        },
    };

    const rendered = parse(safeHtml, options);
    return <>{rendered}</>;
}
