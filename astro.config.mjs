import mdx from '@astrojs/mdx';
import { defineConfig } from 'astro/config';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://beneggers.com',
  integrations: [mdx(), sitemap()],
  build: {
    inlineStylesheets: 'always',
  },
  server: {
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
  },
});
