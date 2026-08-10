#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const GUIDE_ROOT = path.resolve(
  process.env.MAA_EVIDENCE_GUIDE_ROOT ?? path.join(SCRIPT_DIR, ".."),
);
const UPSTREAM_SKILL = path.join("skills", "maa-evidence", "SKILL.md");

function parseArgs(argv) {
  const roots = [];
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] !== "--root" || !argv[index + 1]) {
      throw new Error("Usage: find-maa-evidence-skill.mjs [--root PATH ...]");
    }
    roots.push(path.resolve(argv[index + 1]));
    index += 1;
  }
  return roots;
}

function canonical(candidate) {
  try {
    return fs.realpathSync.native(candidate);
  } catch {
    return path.resolve(candidate);
  }
}

function isFile(candidate) {
  try {
    return fs.statSync(candidate).isFile();
  } catch {
    return false;
  }
}

function addCandidate(list, seen, candidate, source, precedence) {
  const resolved = canonical(candidate);
  const key = process.platform === "win32" ? resolved.toLowerCase() : resolved;
  if (seen.has(key)) return;
  seen.add(key);
  list.push({ path: resolved, source, precedence });
}

function ancestors(start) {
  const result = [];
  let current = path.resolve(start);
  while (true) {
    result.push(current);
    const parent = path.dirname(current);
    if (parent === current) return result;
    current = parent;
  }
}

function packageInfo(candidate) {
  const packageJson = path.join(candidate, "package.json");
  if (!isFile(packageJson)) return undefined;
  try {
    const metadata = JSON.parse(fs.readFileSync(packageJson, "utf8"));
    if (metadata.name !== "maa-evidence-kit") return undefined;
    return { root: canonical(candidate), version: metadata.version ?? null };
  } catch {
    return undefined;
  }
}

function packageManagerRoot(command) {
  try {
    const executable = process.platform === "win32" ? `${command}.cmd` : command;
    return execFileSync(executable, ["root", "-g"], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
      timeout: 5000,
    }).trim();
  } catch {
    return undefined;
  }
}

function skillFromExplicitRoot(root) {
  const candidates = [
    root,
    path.join(root, "SKILL.md"),
    path.join(root, "maa-evidence", "SKILL.md"),
    path.join(root, UPSTREAM_SKILL),
  ];
  return candidates.find((candidate) => isFile(candidate));
}

function isUpstreamSkill(candidate) {
  if (!isFile(candidate)) return false;
  if (canonical(candidate).startsWith(`${canonical(GUIDE_ROOT)}${path.sep}`)) return false;
  const head = fs.readFileSync(candidate, "utf8").slice(0, 4096);
  return /^---\r?\n[\s\S]*?^name:\s*["']?maa-evidence["']?\s*$/m.test(head);
}

function main() {
  const explicitRoots = parseArgs(process.argv.slice(2));
  const skillCandidates = [];
  const packageCandidates = [];
  const seenSkills = new Set();
  const seenPackages = new Set();

  for (const root of explicitRoots) {
    if (packageInfo(root)) {
      addCandidate(packageCandidates, seenPackages, root, "explicit-package", 0);
    } else {
      const skill = skillFromExplicitRoot(root);
      if (skill) addCandidate(skillCandidates, seenSkills, skill, "explicit", 0);
      const packageRoot = path.dirname(root);
      if (packageInfo(packageRoot)) addCandidate(packageCandidates, seenPackages, packageRoot, "explicit-package", 0);
    }
  }

  const home = os.homedir();
  const projectRoots = ancestors(process.cwd());
  const skillRoots = [];
  for (const root of projectRoots) {
    skillRoots.push(path.join(root, ".codex", "skills"), path.join(root, ".agents", "skills"), path.join(root, ".claude", "skills"));
  }
  if (process.env.CODEX_HOME) skillRoots.push(path.join(process.env.CODEX_HOME, "skills"));
  skillRoots.push(path.join(home, ".codex", "skills"), path.join(home, ".agents", "skills"), path.join(home, ".claude", "skills"));

  for (const root of skillRoots) {
    addCandidate(skillCandidates, seenSkills, path.join(root, "maa-evidence", "SKILL.md"), "installed-skill", 1);
  }

  for (const root of projectRoots) {
    addCandidate(packageCandidates, seenPackages, path.join(root, "node_modules", "maa-evidence-kit"), "project-package", 2);
  }
  for (const manager of ["npm", "pnpm"]) {
    const root = packageManagerRoot(manager);
    if (root) addCandidate(packageCandidates, seenPackages, path.join(root, "maa-evidence-kit"), `${manager}-global-package`, 3);
  }

  skillCandidates.sort((left, right) => left.precedence - right.precedence);
  for (const candidate of skillCandidates) {
    if (isUpstreamSkill(candidate.path)) {
      console.log(JSON.stringify({ status: "found", source: candidate.source, skillPath: candidate.path, packageRoot: null, packageVersion: null }, null, 2));
      return;
    }
  }

  packageCandidates.sort((left, right) => left.precedence - right.precedence);
  let packageWithoutSkill;
  for (const candidate of packageCandidates) {
    const info = packageInfo(candidate.path);
    if (!info) continue;
    const skillPath = path.join(info.root, UPSTREAM_SKILL);
    if (isUpstreamSkill(skillPath)) {
      console.log(JSON.stringify({ status: "found", source: candidate.source, skillPath, packageRoot: info.root, packageVersion: info.version }, null, 2));
      return;
    }
    packageWithoutSkill ??= { candidate, info };
  }

  if (packageWithoutSkill) {
    console.log(JSON.stringify({ status: "package-without-skill", source: packageWithoutSkill.candidate.source, skillPath: null, packageRoot: packageWithoutSkill.info.root, packageVersion: packageWithoutSkill.info.version }, null, 2));
    return;
  }

  console.log(JSON.stringify({ status: "not-found", source: null, skillPath: null, packageRoot: null, packageVersion: null }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
