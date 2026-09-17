import { readdir, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

// The shared shadcn layer owns controls; routes compose it rather than cloning it.
const root = fileURLToPath(new URL('../src', import.meta.url));
const violations = [];
async function check(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      if (file !== path.join(root, 'components', 'ui')) await check(file);
    } else if (file.endsWith('.tsx') && !file.includes('.test.')) {
      const source = await readFile(file, 'utf8');
      for (const [index, line] of source.split('\n').entries()) {
        if (/<(?:button|input|textarea|select|label|details|summary|table|thead|tbody|tfoot|tr|th|td)\b/.test(line)
          || /from\s+["']@radix-ui\//.test(line)) {
          violations.push(`${path.relative(root, file)}:${index + 1}: use the shared ui component layer`);
        }
      }
    }
  }
}
await check(root);
if (violations.length) {
  console.error(violations.join('\n'));
  process.exitCode = 1;
} else console.log('PASS: Owner UI controls use the shared shadcn component layer.');
