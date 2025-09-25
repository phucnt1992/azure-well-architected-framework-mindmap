// @ts-check
import starlight from '@astrojs/starlight';
import { defineConfig } from 'astro/config';
import starlightFullViewMode from 'starlight-fullview-mode'
import { remarkDiagram } from './plugins/remark-diagram.js';

// https://astro.build/config
export default defineConfig({
  integrations: [starlight({
    title: '🗺️ Azure Mind Mapping',
    social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/phucnt1992/azure-well-architected-framework-mindmap' }],
    credits: true,
    plugins: [starlightFullViewMode()],
    customCss: [
      './src/styles/custom.css'
    ],
    sidebar: [
      {
        label: 'Well-architected Framework',
        autogenerate: { directory: 'waf' },
      },
      {
        label: 'Azure',
        autogenerate: { directory: 'azure' },
      },
    ],
    components: {
      Footer: './src/components/Footer/Footer.astro'
    }
  })],
  markdown: {
    remarkPlugins: [remarkDiagram],
  },
});
