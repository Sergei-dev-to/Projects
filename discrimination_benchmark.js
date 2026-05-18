#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const vm = require("node:vm");

const count = Number(process.argv[2] || 1000);
const outputPath = process.argv[3] || "DISCRIMINATION_BENCHMARK.md";
const seed = Number(process.argv[4] || 739391);

function makeRng(initialSeed) {
  let state = initialSeed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

const rng = makeRng(seed);

function rand(min = 0, max = 1) {
  return min + (max - min) * rng();
}

function pick(list) {
  return list[Math.floor(rand(0, list.length))];
}

function shuffled(list) {
  const copy = [...list];
  for (let i = copy.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand(0, i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy;
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function fixed(value) {
  return Number(value.toFixed(3));
}

const archetypes = [
  {
    id: "asd-female-core",
    label: "ASD female-presentation core",
    expectedPrimary: "asdAligned",
    routeMin: 6,
    routeMax: 9,
    choices: [["mira", 2], ["saff", 1], ["lio", 2], ["oren", 0], ["glassloom", 0], ["noticeboard", 0], ["mossycedar", 0], ["threadbasket", 0]],
  },
  {
    id: "asd-extroverted",
    label: "Extroverted ASD-like mixed route",
    expectedPrimary: "asdAligned",
    routeMin: 6,
    routeMax: 9,
    choices: [["mira", 0], ["nia", 0], ["saff", 1], ["fountain", 2], ["lio", 2], ["oren", 0], ["glassloom", 1], ["noticeboard", 0]],
  },
  {
    id: "safety-stress",
    label: "Anxiety/trauma-like safety seeker",
    expectedPrimary: "safetyStressOverlap",
    routeMin: 5,
    routeMax: 8,
    choices: [["mira", 3], ["saff", 2], ["fountain", 0], ["fountain", 1], ["mossycedar", 0], ["mossycedar", 1], ["nia", 2], ["workshopwindow", 1], ["shell", 1]],
  },
  {
    id: "social-anxiety-only",
    label: "Social anxiety / people-reading only",
    expectedPrimary: "safetyStressOverlap",
    routeMin: 4,
    routeMax: 7,
    choices: [["mira", 1], ["noticeboard", 0], ["nia", 1], ["lio", 2], ["oren", 1], ["saff", 2]],
  },
  {
    id: "novelty-attention",
    label: "ADHD-like novelty explorer",
    expectedPrimary: "noveltyAttentionOverlap",
    routeMin: 5,
    routeMax: 9,
    choices: [["ribbonstall", 1], ["lio", 1], ["oren", 2], ["threadbasket", 1], ["workshopwindow", 0], ["driftwoodstage", 3], ["storycards", 3], ["glassloom", 2], ["nia", 0]],
  },
  {
    id: "sensory-fatigue",
    label: "Migraine/fatigue sensory-only route",
    expectedPrimary: "safetyStressOverlap",
    expectedAsdMax: 0.45,
    routeMin: 4,
    routeMax: 7,
    choices: [["saff", 1], ["fountain", 0], ["shell", 1], ["mossycedar", 0], ["tidepool", 1]],
  },
  {
    id: "completionist",
    label: "Completionist / puzzle-structure route",
    expectedAsdMax: 0.50,
    routeMin: 5,
    routeMax: 8,
    choices: [["glassloom", 1], ["threadbasket", 0], ["lio", 0], ["oren", 0], ["lanternline", 0], ["storycards", 2], ["driftwoodstage", 2]],
  },
  {
    id: "typical-cozy",
    label: "Typical cozy-game helper",
    expectedAsdMax: 0.38,
    expectedPrimary: "noveltyAttentionOverlap",
    routeMin: 4,
    routeMax: 7,
    choices: [["mira", 0], ["lio", 1], ["oren", 2], ["nia", 0], ["ribbonstall", 1], ["threadbasket", 1]],
  },
];

const allChoices = archetypes.flatMap((archetype) => archetype.choices);

function routeFor(archetype) {
  const length = Math.floor(rand(archetype.routeMin, archetype.routeMax + 1));
  const preferred = shuffled(archetype.choices);
  const route = [];
  while (route.length < length && preferred.length) {
    route.push(preferred.shift());
  }
  while (route.length < length) {
    const source = rng() < 0.70 ? archetype.choices : allChoices;
    route.push(pick(source));
  }
  return route;
}

const noopElement = {
  open: false,
  hidden: false,
  classList: { add() {}, remove() {}, toggle() {} },
  dataset: {},
  style: { setProperty() {} },
  addEventListener() {},
  setAttribute() {},
  close() {},
  showModal() {},
  appendChild() {},
  remove() {},
  click() {},
  querySelector() { return noopElement; },
  querySelectorAll() { return []; },
  getBoundingClientRect() { return { left: 0, top: 0, width: 960, height: 600 }; },
  getContext() {
    return {
      clearRect() {},
      fillRect() {},
      beginPath() {},
      moveTo() {},
      lineTo() {},
      arcTo() {},
      closePath() {},
      fill() {},
      stroke() {},
      arc() {},
      ellipse() {},
      fillText() {},
      measureText(text) { return { width: String(text).length * 7 }; },
      createRadialGradient() { return { addColorStop() {} }; },
      createLinearGradient() { return { addColorStop() {} }; },
      save() {},
      restore() {},
      set fillStyle(_value) {},
      set strokeStyle(_value) {},
      set lineWidth(_value) {},
      set lineCap(_value) {},
      set font(_value) {},
      set textAlign(_value) {},
      set shadowColor(_value) {},
      set shadowBlur(_value) {},
      set shadowOffsetY(_value) {},
    };
  },
  set innerHTML(_value) {},
  get innerHTML() { return ""; },
  set textContent(_value) {},
  get textContent() { return ""; },
  set value(_value) {},
  get value() { return ""; },
};

const appSource = fs.readFileSync("app.js", "utf8");
const context = {
  console,
  Blob,
  window: { clearTimeout() {}, setTimeout() {} },
  URL: { createObjectURL() { return "blob:test"; }, revokeObjectURL() {} },
  navigator: { clipboard: { writeText() {} } },
  requestAnimationFrame() {},
  generatedCases: Array.from({ length: count }, (_, index) => {
    const archetype = archetypes[index % archetypes.length];
    return { archetype, route: routeFor(archetype) };
  }),
  document: {
    addEventListener() {},
    createElement() { return noopElement; },
    body: { appendChild() {}, classList: { add() {}, remove() {} } },
    querySelectorAll() { return []; },
    querySelector() { return noopElement; },
    getElementById() { return noopElement; },
  },
};

vm.createContext(context);
vm.runInContext(appSource, context);

const records = vm.runInContext(`
generatedCases.map(({ archetype, route }) => {
  model = createModel();
  storyText = "";
  moveTarget = null;
  pendingInteraction = null;
  route.forEach(([id, choiceIndex]) => {
    const object = OBJECTS.find((item) => item.id === id);
    if (!object) throw new Error("Missing object: " + id);
    const choice = object.choices[choiceIndex];
    if (!choice) throw new Error("Missing choice " + choiceIndex + " for " + id);
    chooseOption(object, choice);
  });
  const record = assessmentRecord();
  const channels = record.interpretationChannels;
  return {
    archetypeId: archetype.id,
    archetypeLabel: archetype.label,
    expectedPrimary: archetype.expectedPrimary || null,
    expectedAsdMax: archetype.expectedAsdMax ?? null,
    route,
    topChannel: channels[0]?.id || null,
    asdScore: channels.find((channel) => channel.id === "asdAligned")?.score || 0,
    safetyScore: channels.find((channel) => channel.id === "safetyStressOverlap")?.score || 0,
    noveltyScore: channels.find((channel) => channel.id === "noveltyAttentionOverlap")?.score || 0,
    band: record.projection.band,
    score: record.projection.score,
  };
})
`, context);

const byArchetype = new Map();
records.forEach((record) => {
  if (!byArchetype.has(record.archetypeId)) byArchetype.set(record.archetypeId, []);
  byArchetype.get(record.archetypeId).push(record);
});

const rows = [...byArchetype.entries()].map(([id, group]) => {
  const archetype = archetypes.find((item) => item.id === id);
  const expected = archetype.expectedPrimary || `ASD <= ${archetype.expectedAsdMax}`;
  const primaryPasses = archetype.expectedPrimary
    ? group.filter((record) => record.topChannel === archetype.expectedPrimary).length
    : group.length;
  const asdCapPasses = archetype.expectedAsdMax == null
    ? group.length
    : group.filter((record) => record.asdScore <= archetype.expectedAsdMax).length;
  const passCount = group.filter((record) => {
    const primaryOk = archetype.expectedPrimary ? record.topChannel === archetype.expectedPrimary : true;
    const asdOk = archetype.expectedAsdMax == null ? true : record.asdScore <= archetype.expectedAsdMax;
    return primaryOk && asdOk;
  }).length;
  const topCounts = group.reduce((acc, record) => {
    acc[record.topChannel] = (acc[record.topChannel] || 0) + 1;
    return acc;
  }, {});
  return {
    id,
    label: archetype.label,
    expected,
    n: group.length,
    passRate: passCount / group.length,
    primaryRate: primaryPasses / group.length,
    asdCapRate: asdCapPasses / group.length,
    asdMean: mean(group.map((record) => record.asdScore)),
    safetyMean: mean(group.map((record) => record.safetyScore)),
    noveltyMean: mean(group.map((record) => record.noveltyScore)),
    topCounts,
  };
});

const overall = mean(rows.map((row) => row.passRate));

const markdown = [
  "# Lantern Tide Discrimination Benchmark",
  "",
  `Generated by \`node discrimination_benchmark.js ${count}\`.`,
  "",
  "Synthetic routes are hand-designed stress tests for scoring behavior. They are not validation data.",
  "",
  `- Records: ${records.length}`,
  `- Seed: ${seed}`,
  `- Mean archetype pass rate: ${(overall * 100).toFixed(1)}%`,
  "",
  "| Archetype | Expected | Pass | ASD mean | Safety/stress mean | Novelty/attention mean | Top channel counts |",
  "|---|---|---:|---:|---:|---:|---|",
  ...rows.map((row) => (
    `| ${row.label} | ${row.expected} | ${(row.passRate * 100).toFixed(1)}% | ${fixed(row.asdMean)} | ${fixed(row.safetyMean)} | ${fixed(row.noveltyMean)} | ${Object.entries(row.topCounts).map(([key, value]) => `${key}: ${value}`).join(", ")} |`
  )),
  "",
  "## Interpretation",
  "",
  "- A good result is not perfect separation. These are overlapping behavioral patterns by design.",
  "- ASD-like archetypes should usually top out on the autism-aligned channel.",
  "- Safety/stress and sensory-only archetypes should not become high-confidence ASD reads by themselves.",
  "- Novelty/attention archetypes should mostly be pulled away from the ASD channel.",
  "",
].join("\n");

fs.writeFileSync(outputPath, markdown);

console.log(JSON.stringify({
  outputPath,
  records: records.length,
  seed,
  meanPassRate: Number(overall.toFixed(4)),
  rows: rows.map((row) => ({
    id: row.id,
    passRate: Number(row.passRate.toFixed(4)),
    asdMean: fixed(row.asdMean),
    safetyMean: fixed(row.safetyMean),
    noveltyMean: fixed(row.noveltyMean),
    topCounts: row.topCounts,
  })),
}, null, 2));
