import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from './src/themes/preset-openriak';
import pluginIncludeMarkdown from './src/remark/include-md';
import type { DeepPartial, Overwrite } from 'utility-types';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'OpenRiak Docs',
  tagline: 'For when your data gets Big',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://www.openriak.org/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/docs',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'openriak', // Usually your GitHub org/user name.
  projectName: 'openriak-docs', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  customFields: {
    configReference: {
      fallbackVersion: "3.2.5"
    }
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
/*
          {
            from: '/kv/latest/',
            to: '/kv/',
          },
*/
        ],
        createRedirects: (path) => {
          // Match all /kv/latest/* paths
          if (path.startsWith('/kv/latest/')) {
            return [path.replace('/kv/latest', '/kv')];
          }
          return [];
        },
      },
    ],
  ],

  presets: [
    [
      'preset-openriak',
      {
        kv: {
          id: "kv",
          path: "content/kv",
          routeBasePath: "kv",
          sidebarPath: require.resolve('./src/sidebars/sidebarsKV.ts'),
          editUrl:
            'https://github.com/openriak/openriak-docs/tree/develop/kv/',
          lastVersion: 'current',
          versions: {
            current: {
              label: 'The last 3.2 release aka 3.2.5',
            }
          },
          remarkPlugins: [pluginIncludeMarkdown]
        },
        cs: {
          id: "cs",
          path: "content/cs",
          routeBasePath: "cs",
          sidebarPath: require.resolve('./src/sidebars/sidebarsCS.ts'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/openriak/openriak-docs/tree/develop/cs/',
          lastVersion: 'current',
          versions: {
            current: {
              label: '3.0.1',
              path: '3.0.1'
            }
          }
        },
        ts: {
          id: "ts",
          path: "content/ts",
          routeBasePath: "ts",
          sidebarPath: require.resolve('./src/sidebars/sidebarsTS.ts'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/openriak/openriak-docs/tree/develop/ts/',
          lastVersion: 'current',
          versions: {
            current: {
              label: '3.0.0',
              path: '3.0.0',
            }
          }
        },
        community: {
          id: "community",
          path: "content/community",
          routeBasePath: "community"
        },
        blog: {
          id: "blog",
          path: "content/blog",
          routeBasePath: "blog",
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/openriak/openriak-docs/tree/develop/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ]
  ],

  themeConfig: {
    // Replace with your project's social card
    codeBlock: {
      showCopyButton: true,
    },
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: '/Docs',
      logo: {
        alt: 'OpenRiak',
        src: 'img/openriak-logo.svg',
      },
      items: [
        {
          type: 'docsVersionDropdown',
          position: 'right',
          dropdownActiveClassDisabled: true, // optional
          docsPluginId: 'kv',
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          dropdownActiveClassDisabled: true, // optional
          docsPluginId: 'cs',
        },
        {
          type: 'docsVersionDropdown',
          position: 'right',
          dropdownActiveClassDisabled: true, // optional
          docsPluginId: 'ts',
        },
        { to: '/kv/latest/intro', label: 'KV', position: 'left' },
        { to: '/cs/latest/intro', label: 'CS', position: 'left' },
        { to: '/ts/latest/intro', label: 'TS', position: 'left' },
        { to: '/community', label: 'Community', position: 'left' },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/openriak/openriak-docs',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'OpenRiak KV',
              to: '/kv/latest/intro',
            },
            {
              label: 'OpenRiak CS',
              to: '/cs/latest/intro',
            },
            {
              label: 'OpenRiak TS',
              to: '/ts/latest/intro',
            },
          ],
        },
        {
          title: 'Source',
          items: [
            {
              label: 'OpenRiak',
              to: 'https://github.com/OpenRiak',
            },
            {
              label: 'OpenRiak KV',
              to: 'https://github.com/OpenRiak/riak_kv',
            },
            {
              label: 'TicTac AAE',
              to: 'https://github.com/OpenRiak/kv_index_tictactree',
            },
            {
              label: 'Riak Erlang Client',
              to: 'https://github.com/OpenRiak/riak-erlang-client',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/openriak',
            },
            {
              label: 'Slack',
              href: 'https://the-eef.slack.com/app_redirect?channel=open-riak',
            },
            {
              label: 'X',
              href: 'https://x.com/OpenRiak',
            },
            {
              label: 'BlueSky',
              href: 'https://bsky.app/profile/openriak.com',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/openriak/openriak-docs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} OpenRiak. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: [
        'bash',
        'elixir',
        'erlang',
        'ini',
        'java',
        'javascript',
        'powershell',
        'protobuf',
        'regex',
        'rust',
      ]
    }
  } satisfies Preset.ThemeConfig,
};

export default config;
