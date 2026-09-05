#!/usr/bin/env node
/**
 * CLI Runner for prompt-capability-optimizer
 * Author: Mahmoud Abdelhameid <Develper.net@gmail.com>
 * LinkedIn: https://www.linkedin.com/in/mahmoud-abdelhameid-dev/
 */

const path = require('path');
const { spawnSync } = require('child_process');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);

// Check if python is available
const pyCmd = process.platform === 'win32' ? 'python' : 'python3';
const checkPy = spawnSync(pyCmd, ['--version'], { encoding: 'utf-8' });

if (checkPy.error || checkPy.status !== 0) {
  console.log(`=== Prompt Capability Optimizer ===`);
  console.log(`Author: Mahmoud Abdelhameid (https://www.linkedin.com/in/mahmoud-abdelhameid-dev/)`);
  console.log(`Skill Location: ${path.join(PACKAGE_ROOT, 'SKILL.md')}`);
  console.log(`Notice: Python runtime is required for the full optimizer engine CLI.`);
  console.log(`To use this skill with Claude/Cursor/Gemini, point your agent to: ${PACKAGE_ROOT}`);
  process.exit(0);
}

// Transparently run python engine
const proc = spawnSync(pyCmd, ['-m', 'prompt_capability_optimizer', ...args], {
  cwd: PACKAGE_ROOT,
  stdio: 'inherit'
});

process.exit(proc.status || 0);
