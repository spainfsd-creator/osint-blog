import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'OSINT Blog',
  tagline: 'Investigacion, herramientas y metodologias OSINT en espanol',
  favicon: 'img/favicon.svg',

  future: {
    v4: true,
  },

  url: 'https://spainfsd-creator.github.io',
  baseUrl: '/osint-blog/',

  organizationName: 'spainfsd-creator',
  projectName: 'osint-blog',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'es',
    locales: ['es'],
  },

  presets: [
    [
      'classic',
      {
        docs: false,
        blog: {
          routeBasePath: '/',
          showReadingTime: true,
          postsPerPage: 10,
          blogSidebarCount: 'ALL',
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    announcementBar: {
      id: 'ai-publishing-experiment',
      content:
        '<strong>Experimento con IA:</strong> los artículos se generan automáticamente y se publican sin revisión humana. <a href="/osint-blog/ai-experiment">Más información y limitaciones</a>.',
      backgroundColor: '#ccfbf1',
      textColor: '#073b36',
      isCloseable: false,
    },
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'OSINT Blog',
      logo: {
        alt: 'OSINT Blog',
        src: 'img/logo-light.svg',
        srcDark: 'img/logo.svg',
      },
      items: [
        {to: '/', label: 'Blog', position: 'left'},
        {to: '/tags', label: 'Tags', position: 'left'},
        {to: '/ai-experiment', label: 'Experimento IA', position: 'left'},
        {
          href: 'https://github.com/spainfsd-creator/osint-blog',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'OSINT Blog',
        src: 'img/logo-light.svg',
        srcDark: 'img/logo.svg',
        width: 40,
        height: 40,
      },
      links: [
        {
          title: 'Contenido',
          items: [
            {
              label: 'Todas las entradas',
              to: '/',
            },
            {
              label: 'Tags',
              to: '/tags',
            },
          ],
        },
        {
          title: 'Feeds',
          items: [
            {
              label: 'RSS',
              href: 'https://spainfsd-creator.github.io/osint-blog/rss.xml',
            },
            {
              label: 'Atom',
              href: 'https://spainfsd-creator.github.io/osint-blog/atom.xml',
            },
          ],
        },
        {
          title: 'Mas',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/spainfsd-creator/osint-blog',
            },
            {
              label: 'Autor',
              href: 'https://github.com/spainfsd-creator',
            },
            {
              label: 'Experimento de publicación con IA',
              to: '/ai-experiment',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} OSINT Blog · Inteligencia de fuentes abiertas, con metodo y responsabilidad.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
