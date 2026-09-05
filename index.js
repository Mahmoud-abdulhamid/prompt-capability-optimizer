/**
 * Prompt Capability Optimizer
 * ===========================
 * Production-grade agent meta-skill for autonomous capability discovery & prompt engineering.
 * 
 * Author: Mahmoud Abdelhameid <Develper.net@gmail.com>
 * LinkedIn: https://www.linkedin.com/in/mahmoud-abdelhameid-dev/
 * License: MIT
 */

const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

const PACKAGE_ROOT = __dirname;
const SKILL_MD_PATH = path.join(PACKAGE_ROOT, 'SKILL.md');

function getSkillPath() {
  return SKILL_MD_PATH;
}

function getSkillContent() {
  return fs.readFileSync(SKILL_MD_PATH, 'utf-8');
}

function getPackageMetadata() {
  const pkg = JSON.parse(fs.readFileSync(path.join(PACKAGE_ROOT, 'package.json'), 'utf-8'));
  return {
    name: pkg.name,
    version: pkg.version,
    author: pkg.author,
    description: pkg.description,
    repository: pkg.repository.url
  };
}

function runOptimizer(args = []) {
  // Attempt python execution
  const pyCmd = process.platform === 'win32' ? 'python' : 'python3';
  const res = spawnSync(pyCmd, ['-m', 'prompt_capability_optimizer', ...args], {
    cwd: PACKAGE_ROOT,
    stdio: 'inherit'
  });
  return res.status;
}

module.exports = {
  PACKAGE_ROOT,
  SKILL_MD_PATH,
  getSkillPath,
  getSkillContent,
  getPackageMetadata,
  runOptimizer
};
