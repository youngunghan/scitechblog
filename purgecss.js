import { promises as fs } from 'fs';
import { PurgeCSS } from 'purgecss';

const DIST_PATH = '_sass/vendors';
const output = `${DIST_PATH}/_bootstrap.scss`;

const config = {
  content: ['_includes/**/*.html', '_layouts/**/*.html', '_javascript/**/*.js'],
  css: ['node_modules/bootstrap/dist/css/bootstrap.min.css'],
  keyframes: true,
  variables: true,
  // The `safelist` should be changed appropriately for future development
  safelist: {
    standard: [/^collaps/, /^w-/, 'shadow', 'border', 'kbd'],
    greedy: [/^col-/, /tooltip/]
  }
};

async function main() {
  await fs.rm(DIST_PATH, { recursive: true, force: true });
  await fs.mkdir(DIST_PATH, { recursive: true });
  const result = await new PurgeCSS().purge(config);
  await fs.writeFile(output, result[0].css);
}

main().catch((err) => {
  console.error('Error during PurgeCSS process:', err);
  process.exitCode = 1;
});
