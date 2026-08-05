#!/usr/bin/env node
// Sync the version across package.json and .codex-plugin/plugin.json.
// Usage: node scripts/set-version.mjs <version>
import { readFileSync, writeFileSync } from 'node:fs';

const version = process.argv[2];
if (!version || !/^\d+\.\d+\.\d+/.test(version)) {
  console.error('usage: set-version <semver>');
  process.exit(1);
}

for (const file of ['package.json', '.codex-plugin/plugin.json']) {
  const obj = JSON.parse(readFileSync(file, 'utf8'));
  obj.version = version;
  writeFileSync(file, JSON.stringify(obj, null, 2) + '\n');
  console.log(`${file} -> ${version}`);
}
