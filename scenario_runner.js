const fs = require("fs");
const vm = require("vm");

const appSource = fs.readFileSync("app.js", "utf8");

const noopElement = {
  open: false,
  classList: { toggle() {} },
  dataset: {},
  style: { setProperty() {} },
  addEventListener() {},
  close() {},
  showModal() {},
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
      fillText() {},
      set fillStyle(_value) {},
      set strokeStyle(_value) {},
      set lineWidth(_value) {},
      set lineCap(_value) {},
      set font(_value) {},
      set textAlign(_value) {},
    };
  },
  set innerHTML(_value) {},
  get innerHTML() { return ""; },
  set textContent(_value) {},
  get textContent() { return ""; },
};

const context = {
  console,
  Blob,
  window: {
    clearTimeout() {},
    setTimeout() {},
  },
  URL: { createObjectURL() { return "blob:test"; }, revokeObjectURL() {} },
  navigator: { clipboard: { writeText() {} } },
  requestAnimationFrame() {},
  document: {
    addEventListener() {},
    createElement() { return noopElement; },
    body: { appendChild() {} },
    querySelectorAll() { return []; },
    querySelector() { return noopElement; },
    getElementById() { return noopElement; },
  },
};

vm.createContext(context);
vm.runInContext(appSource, context);
const results = vm.runInContext("lastScenarioResults", context);
const auditIssues = vm.runInContext("auditInteractionCoverage()", context);

const playthroughs = vm.runInContext(`
(() => {
  const scripts = [
    {
      name: "Direct Social Helper",
      expects: [
        ["does not produce a higher profile from social drive alone", (p) => p.band !== "higher"],
        ["novelty/social route is treated as a confound", (p) => p.flags.includes("novelty-confound")],
      ],
      choices: [
        ["mira", 0],
        ["saff", 0],
        ["lio", 1],
        ["nia", 0],
        ["oren", 2],
        ["ribbonstall", 1],
      ],
    },
    {
      name: "Observe Then Join",
      expects: [
        ["social-reading route is at least mixed", (p) => p.band !== "lower"],
        ["social-masking flag present", (p) => p.flags.includes("social-masking")],
      ],
      choices: [
        ["mira", 1],
        ["saff", 2],
        ["lio", 2],
        ["nia", 1],
        ["oren", 1],
        ["tidepool", 0],
      ],
    },
    {
      name: "Quiet Regulation Route",
      expects: [
        ["sensory-regulation flag present", (p) => p.flags.includes("sensory-regulation")],
        ["predictability-support flag present", (p) => p.flags.includes("predictability-support")],
      ],
      choices: [
        ["mossycedar", 0],
        ["fountain", 0],
        ["shell", 1],
        ["mira", 3],
        ["saff", 1],
        ["nia", 2],
        ["workshopwindow", 1],
      ],
    },
    {
      name: "Detailed Systemizer",
      expects: [
        ["focused-interest flag present", (p) => p.flags.includes("focused-interest")],
        ["single-domain focus is not treated as conclusive higher profile", (p) => p.band !== "higher"],
      ],
      choices: [
        ["lanternline", 0],
        ["lio", 0],
        ["oren", 0],
        ["threadbasket", 0],
        ["saff", 0],
        ["tidepool", 0],
      ],
    },
    {
      name: "Novelty Sampler",
      expects: [
        ["novelty confound flag present", (p) => p.flags.includes("novelty-confound")],
        ["novelty-only route has low score", (p) => p.score < 0.18],
      ],
      choices: [
        ["ribbonstall", 1],
        ["lio", 1],
        ["oren", 2],
        ["threadbasket", 1],
        ["workshopwindow", 0],
        ["nia", 0],
      ],
    },
    {
      name: "Story Play Route",
      expects: [
        ["imagination/play domain is sampled", (p) => p.sourceDomains.some((domain) => domain.id === "imagination" && domain.value >= 0.30)],
        ["play alone is not treated as a higher profile", (p) => p.band !== "higher"],
      ],
      choices: [
        ["storylantern", 0],
        ["driftwoodstage", 0],
        ["ribbonstall", 1],
        ["tidepool", 0],
      ],
    },
    {
      name: "Broad Domain Route",
      expects: [
        ["at least four source domains are sampled", (p) => p.sourceDomains.filter((domain) => domain.value >= 0.30).length >= 4],
        ["credibility is not early", (p) => p.credibility !== "Early read"],
      ],
      choices: [
        ["noticeboard", 0],
        ["storycards", 0],
        ["saff", 1],
        ["glassloom", 0],
        ["mira", 2],
        ["lio", 2],
        ["oren", 0],
      ],
    },
  ];

  return scripts.map((script) => {
    model = createModel();
    storyText = "";
    moveTarget = null;
    pendingInteraction = null;
    script.choices.forEach(([id, choiceIndex]) => {
      const object = OBJECTS.find((item) => item.id === id);
      if (!object) throw new Error("Missing object in playthrough: " + id);
      const choice = object.choices[choiceIndex];
      if (!choice) throw new Error("Missing choice " + choiceIndex + " for " + id);
      chooseOption(object, choice);
    });
    const profile = currentProfile();
    const playthrough = {
      name: script.name,
      band: profile.band,
      score: Number(profile.projection.score.toFixed(3)),
      uncertainty: Number(profile.projection.uncertainty.toFixed(3)),
      flags: profile.flags,
      sourceDomains: profile.sourceDomains.map((domain) => ({
        id: domain.id,
        value: Number(domain.value.toFixed(3)),
        level: domain.level,
      })),
      credibility: profile.credibility.label,
      strongestSignals: Object.entries(profile.evidence)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([dim, value]) => [dim, Number(value.toFixed(3))]),
      completed: { ...model.completed },
    };
    playthrough.checks = script.expects.map(([label, predicate]) => ({
      label,
      pass: Boolean(predicate(playthrough)),
    }));
    playthrough.pass = playthrough.checks.every((check) => check.pass);
    return playthrough;
  });
})()
`, context);

const reliabilityBatch = vm.runInContext(`
(() => {
  const pairs = [
    {
      name: "social-reading order stability",
      a: [["noticeboard", 0], ["mira", 1], ["nia", 1], ["saff", 2]],
      b: [["saff", 2], ["nia", 1], ["noticeboard", 0], ["mira", 1]],
    },
    {
      name: "pattern-maker order stability",
      a: [["glassloom", 1], ["threadbasket", 0], ["lio", 0], ["oren", 0]],
      b: [["oren", 0], ["lio", 0], ["glassloom", 1], ["threadbasket", 0]],
    },
    {
      name: "story-play order stability",
      a: [["storylantern", 0], ["storycards", 0], ["driftwoodstage", 0]],
      b: [["driftwoodstage", 0], ["storycards", 0], ["storylantern", 0]],
    },
  ];

  function runChoices(choices) {
    model = createModel();
    storyText = "";
    moveTarget = null;
    pendingInteraction = null;
    choices.forEach(([id, choiceIndex]) => {
      const object = OBJECTS.find((item) => item.id === id);
      if (!object) throw new Error("Missing object in reliability route: " + id);
      const choice = object.choices[choiceIndex];
      if (!choice) throw new Error("Missing choice " + choiceIndex + " for " + id);
      chooseOption(object, choice);
    });
    const profile = currentProfile();
    return {
      band: profile.band,
      score: Number(profile.projection.score.toFixed(3)),
      domains: Object.fromEntries(profile.sourceDomains.map((domain) => [domain.id, Number(domain.value.toFixed(3))])),
      flags: profile.flags,
    };
  }

  function domainDistance(a, b) {
    return Object.keys(a.domains).reduce((sum, id) => sum + Math.abs(a.domains[id] - b.domains[id]), 0) / Object.keys(a.domains).length;
  }

  return pairs.map((pair) => {
    const a = runChoices(pair.a);
    const b = runChoices(pair.b);
    const distance = Number(domainDistance(a, b).toFixed(3));
    const checks = [
      { label: "band stable", pass: a.band === b.band },
      { label: "domain profile stable", pass: distance <= 0.16 },
    ];
    return { name: pair.name, a, b, distance, checks, pass: checks.every((check) => check.pass) };
  });
})()
`, context);

const simulationBatch = vm.runInContext(`
(() => {
  const ACTIONS = {
    directJoin: { social_drive: 0.08, sensory_accumulation: 0.03 },
    askChildren: { social_drive: 0.07, sensory_accumulation: 0.03 },
    directSignup: { social_drive: 0.09, novelty_breadth: 0.03 },
    readRoom: { social_prediction_uncertainty: 0.05, social_monitoring_cost: 0.06 },
    waitForTurn: { social_prediction_uncertainty: 0.04, social_monitoring_cost: 0.05 },
    helperObserve: { social_monitoring_cost: 0.07, masking_adaptation: 0.04 },
    socialBridge: { masking_adaptation: 0.06, social_monitoring_cost: 0.04, ambiguity_avoidance: 0.02 },
    holdAssignedJob: { ambiguity_avoidance: 0.05, regulation_dependency: 0.03, social_monitoring_cost: 0.02 },
    askRule: { ambiguity_avoidance: 0.06, social_monitoring_cost: 0.03 },
    askSchedule: { ambiguity_avoidance: 0.05, regulation_dependency: 0.05 },
    quietEdge: { regulation_dependency: 0.07, sensory_accumulation: 0.04 },
    recoverySpot: { regulation_dependency: 0.08, sensory_accumulation: 0.02 },
    comfortObject: { regulation_dependency: 0.06, ambiguity_avoidance: 0.02 },
    patternSort: { systemizing_structure: 0.08, focused_loop_depth: 0.06 },
    fineTune: { focused_loop_depth: 0.09, systemizing_structure: 0.05, context_switch_friction: 0.03 },
    repeatOneArea: { focused_loop_depth: 0.08, context_switch_friction: 0.04 },
    simpleReadablePlan: { systemizing_structure: 0.06, ambiguity_avoidance: 0.04 },
    sampleNovel: { novelty_breadth: 0.08, social_drive: 0.02 },
    broadExplore: { novelty_breadth: 0.10 },
    brightChoice: { novelty_breadth: 0.07 },
    unstructuredPlay: { novelty_breadth: 0.10, social_drive: 0.03 },
    storyPlay: { imagination_play: 0.10, novelty_breadth: 0.02 },
    symbolicMaking: { imagination_play: 0.08, systemizing_structure: 0.02 },
    cardStory: { imagination_play: 0.11, novelty_breadth: 0.02 },
    cardSort: { systemizing_structure: 0.06, ambiguity_avoidance: 0.04 },
    glassRows: { systemizing_structure: 0.09, focused_loop_depth: 0.05 },
    glassLoop: { focused_loop_depth: 0.10, context_switch_friction: 0.04, systemizing_structure: 0.04 },
    glassSample: { novelty_breadth: 0.09 },
    tolerateNoise: { sensory_accumulation: 0.08, social_drive: 0.03 },
  };

  const simPlayers = [
    {
      name: "Baseline Wanderer",
      actions: ["directJoin", "sampleNovel", "broadExplore", "brightChoice"],
      expects: [
        ["does not produce higher profile", (p) => p.band !== "higher"],
        ["score remains low", (p) => p.score < 0.18],
      ],
    },
    {
      name: "Social Butterfly",
      actions: ["directJoin", "askChildren", "directSignup", "directJoin", "unstructuredPlay", "brightChoice"],
      expects: [
        ["social drive alone is not treated as ASD evidence", (p) => !p.flags.includes("social-masking")],
        ["does not produce higher profile", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Social Reader",
      actions: ["readRoom", "waitForTurn", "helperObserve", "socialBridge", "holdAssignedJob", "readRoom"],
      expects: [
        ["social-masking flag present", (p) => p.flags.includes("social-masking")],
        ["profile is at least mixed", (p) => p.band !== "lower"],
      ],
    },
    {
      name: "Quiet Planner",
      actions: ["quietEdge", "recoverySpot", "askSchedule", "holdAssignedJob", "comfortObject", "quietEdge"],
      expects: [
        ["sensory-regulation flag present", (p) => p.flags.includes("sensory-regulation")],
        ["predictability-support flag present", (p) => p.flags.includes("predictability-support")],
        ["sensory plus predictability alone is not higher", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Pattern Maker",
      actions: ["patternSort", "fineTune", "patternSort", "repeatOneArea", "fineTune"],
      expects: [
        ["focused-interest flag present", (p) => p.flags.includes("focused-interest")],
        ["single-family focus is not higher", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Pattern And Regulation",
      actions: ["patternSort", "fineTune", "quietEdge", "askSchedule", "recoverySpot", "simpleReadablePlan"],
      expects: [
        ["focused-interest flag present", (p) => p.flags.includes("focused-interest")],
        ["sensory-regulation flag present", (p) => p.flags.includes("sensory-regulation")],
        ["profile is at least mixed", (p) => p.band !== "lower"],
        ["profile is not higher without social/camouflaging evidence", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Masking High Load",
      actions: ["socialBridge", "readRoom", "socialBridge", "tolerateNoise", "recoverySpot", "quietEdge", "askSchedule"],
      expects: [
        ["social-masking flag present", (p) => p.flags.includes("social-masking")],
        ["sensory-regulation flag present", (p) => p.flags.includes("sensory-regulation")],
        ["profile is higher", (p) => p.band === "higher"],
      ],
    },
    {
      name: "Novelty Explorer",
      actions: ["sampleNovel", "broadExplore", "brightChoice", "unstructuredPlay", "sampleNovel"],
      expects: [
        ["novelty confound flag present", (p) => p.flags.includes("novelty-confound")],
        ["novelty route stays low score", (p) => p.score < 0.18],
      ],
    },
    {
      name: "Imaginative Maker",
      actions: ["storyPlay", "symbolicMaking", "cardStory", "storyPlay", "brightChoice"],
      expects: [
        ["imagination/play domain is sampled", (p) => p.sourceDomains.some((domain) => domain.id === "imagination" && domain.value >= 0.30)],
        ["imagination alone stays non-diagnostic", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Broad Source Coverage",
      actions: ["helperObserve", "socialBridge", "quietEdge", "recoverySpot", "cardStory", "glassRows", "glassLoop", "askSchedule"],
      expects: [
        ["at least four domains sampled", (p) => p.sourceDomains.filter((domain) => domain.value >= 0.30).length >= 4],
        ["credibility is broader", (p) => p.credibility === "Broader read"],
        ["profile can be higher when several core domains align", (p) => p.band === "higher"],
      ],
    },
    {
      name: "Novelty And Play Confound",
      actions: ["brightChoice", "glassSample", "sampleNovel", "broadExplore", "cardStory"],
      expects: [
        ["imagination/play sampled separately from novelty", (p) => p.sourceDomains.some((domain) => domain.id === "imagination" && domain.value >= 0.30)],
        ["novelty confound remains visible", (p) => p.flags.includes("novelty-confound")],
        ["route is not higher", (p) => p.band !== "higher"],
      ],
    },
    {
      name: "Rule Seeker",
      actions: ["askRule", "holdAssignedJob", "askSchedule", "simpleReadablePlan", "askRule"],
      expects: [
        ["predictability-support flag present", (p) => p.flags.includes("predictability-support")],
        ["profile is at least mixed", (p) => p.band !== "lower"],
      ],
    },
    {
      name: "Mixed Low Evidence",
      actions: ["directJoin", "patternSort", "sampleNovel", "quietEdge"],
      expects: [
        ["brief mixed sample is not higher", (p) => p.band !== "higher"],
        ["brief mixed sample is not a clean profile", (p) => p.score < 0.22],
      ],
    },
    {
      name: "All Core Families",
      actions: ["readRoom", "socialBridge", "waitForTurn", "quietEdge", "recoverySpot", "askSchedule", "patternSort", "fineTune", "simpleReadablePlan"],
      expects: [
        ["social-masking flag present", (p) => p.flags.includes("social-masking")],
        ["sensory-regulation flag present", (p) => p.flags.includes("sensory-regulation")],
        ["focused-interest flag present", (p) => p.flags.includes("focused-interest")],
        ["profile is higher", (p) => p.band === "higher"],
      ],
    },
    {
      name: "Direct With Sensory Load",
      actions: ["directJoin", "tolerateNoise", "directJoin", "askChildren", "recoverySpot"],
      expects: [
        ["does not infer social masking from directness", (p) => !p.flags.includes("social-masking")],
        ["does not produce higher profile", (p) => p.band !== "higher"],
      ],
    },
  ];

  function runActions(actions) {
    model = createModel();
    model.simulatedEventCount = actions.length;
    actions.forEach((actionName) => {
      const delta = ACTIONS[actionName];
      if (!delta) throw new Error("Missing simulation action: " + actionName);
      applyDelta(model.evidence, delta);
    });
    const profile = currentProfile();
    const result = {
      band: profile.band,
      score: Number(profile.projection.score.toFixed(3)),
      uncertainty: Number(profile.projection.uncertainty.toFixed(3)),
      flags: profile.flags,
      strongestSignals: Object.entries(profile.evidence)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([dim, value]) => [dim, Number(value.toFixed(3))]),
      families: Object.fromEntries(Object.entries(profile.projection.families)
        .map(([name, value]) => [name, Number(value.toFixed(3))])),
      sourceDomains: profile.sourceDomains.map((domain) => ({
        id: domain.id,
        value: Number(domain.value.toFixed(3)),
        level: domain.level,
      })),
      credibility: profile.credibility.label,
    };
    return result;
  }

  return simPlayers.map((script) => {
    const result = { name: script.name, ...runActions(script.actions) };
    result.checks = script.expects.map(([label, predicate]) => ({
      label,
      pass: Boolean(predicate(result)),
    }));
    result.pass = result.checks.every((check) => check.pass);
    return result;
  });
})()
`, context);

console.log(JSON.stringify({
  auditIssues,
  passed: results.filter((result) => result.pass).length,
  total: results.length,
  results: results.map((result) => ({
    name: result.name,
    pass: result.pass,
    band: result.profile.band,
    score: Number(result.profile.projection.score.toFixed(3)),
    uncertainty: Number(result.profile.projection.uncertainty.toFixed(3)),
    flags: result.profile.flags,
      checks: result.checks,
    })),
  playthroughs,
  reliabilityBatch,
  simulationBatch,
}, null, 2));

if (results.some((result) => !result.pass)) {
  process.exitCode = 1;
}
if (playthroughs.some((result) => !result.pass)) {
  process.exitCode = 1;
}
if (reliabilityBatch.some((result) => !result.pass)) {
  process.exitCode = 1;
}
if (simulationBatch.some((result) => !result.pass)) {
  process.exitCode = 1;
}
if (auditIssues.length) {
  process.exitCode = 1;
}
