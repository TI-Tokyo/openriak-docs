import fs from 'fs';
import path  from 'path';
import {visit} from 'unist-util-visit';

/**
 * Remark plugin that replaces :::include ./file.md::: with the content of that file.
 */
const pluginIncludeMarkdown = (options) => {
  return async function transformer(tree, file) {
    const includes = [];

    visit(tree, 'paragraph', (node, index, parent) => {
      if (!node.children || node.children.length !== 1) return;
      const child = node.children[0];
      if (child.type !== 'text') return;

      const match = child.value.match(/^:::include\s+(.*?):::$/);
      if (match) {
        const includePath = match[1].trim();
        const sourceDir = path.dirname(file.path);
        const resolvedPath = path.resolve(sourceDir, includePath);

        if (!fs.existsSync(resolvedPath)) {
          throw new Error(`Included file not found: ${resolvedPath}`);
        }

        const includedContent = fs.readFileSync(resolvedPath, 'utf8');

        // Replace current node with the content parsed as Markdown
        includes.push({
          index,
          parent,
          content: includedContent,
        });
      }
    });

    // Dynamically import `fromMarkdown` (remark v15+ way to parse markdown)
    if (includes.length > 0) {
      const { fromMarkdown } = await import('mdast-util-from-markdown');
      const { gfm } = await import('micromark-extension-gfm');
      const { gfmFromMarkdown } = await import('mdast-util-gfm');

      for (const { index, parent, content } of includes) {
        const parsed = fromMarkdown(content, {
          extensions: [gfm()],
          mdastExtensions: [gfmFromMarkdown()],
        });

        // Insert parsed children in place of the :::include node
        parent.children.splice(index, 1, ...parsed.children);
      }
    }
  };
}
/*
const pluginIncludeMarkdown = (context, options) => {
  return {
    name: 'plugin-include-md',
    configureMarkdown(mdOptions) {
      console.log('[include-md] configureMarkdown called'); // Should show
      mdOptions.remarkPlugins = mdOptions.remarkPlugins || [];
      mdOptions.remarkPlugins.push(remarkIncludeMarkdown);
      return mdOptions;
    },
  }; 
};
*/
export default pluginIncludeMarkdown;