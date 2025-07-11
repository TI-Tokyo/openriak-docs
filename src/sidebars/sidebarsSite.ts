import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  siteSidebar: [
    {
      type: 'link',
      label: 'Home',
      href: '/', // homepage
    },
    {
      type: 'link',
      label: 'Bing Search',
      href: 'https://www.bing.com', // external link
    },
  ]
};

export default sidebars;
