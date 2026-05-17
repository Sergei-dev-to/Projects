const EVIDENCE_DIMS = [
  "social_prediction_uncertainty",
  "social_monitoring_cost",
  "masking_adaptation",
  "sensory_accumulation",
  "regulation_dependency",
  "context_switch_friction",
  "focused_loop_depth",
  "systemizing_structure",
  "ambiguity_avoidance",
  "novelty_breadth",
  "social_drive",
];

const STATE_DIMS = ["social_energy", "sensory_load", "regulation_need", "focus_lock", "safety_feeling"];
const WORLD_WIDTH = 960;
const WORLD_HEIGHT = 600;
const DIALOGUE_REVEAL = {
  charsPerStep: 1,
  stepMs: 38,
  punctuationPauseMs: 120,
};

const ASD_WEIGHTS = {
  social_prediction_uncertainty: 0.12,
  social_monitoring_cost: 0.13,
  masking_adaptation: 0.12,
  sensory_accumulation: 0.13,
  regulation_dependency: 0.12,
  context_switch_friction: 0.10,
  focused_loop_depth: 0.12,
  systemizing_structure: 0.10,
  ambiguity_avoidance: 0.06,
};

const QUESTS = {
  lantern: "Find lantern oil for Mira",
  shells: "Help Lio with tide shells",
  display: "Prepare Oren's tide-glass display",
};

const QUEST_TARGETS = {
  lantern: "Mira in the Market Square",
  shells: "Lio on the Beach Path",
  display: "Oren in the Workshop",
};

const QUEST_DETAILS = {
  lantern: {
    title: "Lantern oil list",
    lead: "Mira",
    place: "Mira in the Market Square",
    waiting: "Market Square",
    open: "Mira is sorting lantern oil near the ribbons.",
    done: "Mira has the oil list.",
  },
  shells: {
    title: "Shell path",
    lead: "Lio",
    place: "Lio on the Beach Path",
    waiting: "Beach Path",
    open: "Lio is arranging tide shells by the beach.",
    done: "The shell path is ready.",
  },
  display: {
    title: "Tide-glass display",
    lead: "Oren",
    place: "Oren in the Workshop",
    waiting: "Workshop",
    open: "Oren is working with tide-glass in the workshop.",
    done: "Oren's display is ready.",
  },
};

const VILLAGE_THREADS = [
  { id: "mira", quest: "lantern", title: "Mira", open: QUEST_DETAILS.lantern.open, changed: QUEST_DETAILS.lantern.done },
  { id: "saff", title: "Saff", open: "Saff is testing festival bells in the square." },
  { id: "fountain", flag: "fountain", title: "Garden fountain", open: "The fountain is quiet under the bamboo shade.", changed: "The fountain is a known quiet place." },
  { id: "lio", quest: "shells", title: "Lio", open: QUEST_DETAILS.shells.open, changed: QUEST_DETAILS.shells.done },
  { id: "nia", title: "Nia", open: "Nia is searching the tide pools for a moon charm." },
  { id: "oren", quest: "display", title: "Oren", open: QUEST_DETAILS.display.open, changed: QUEST_DETAILS.display.done },
  { id: "ribbonstall", title: "Ribbon stall", open: "Ribbons flutter at the quieter edge of the square." },
  { id: "tidepool", title: "Tide pool", open: "Small ripples move shell fragments by the beach path." },
];

const ROLE_LABELS = {
  quest: "preparation",
  villager: "villager",
  item: "item",
  comfort: "comfort spot",
};

const WORLD_NOTE_BY_MEMORY = {
  saff_counted: "Saff can tap the bell pattern quietly before ringing it.",
  saff_awning: "Saff gives a warning before ringing the bells again.",
  saff_schedule: "Saff shows how many bell patterns are left.",
  nia_direct: "Nia found the moon charm near the shell baskets.",
  nia_observe: "The still patch of tide-pool water marked where the charm had fallen.",
  nia_support: "Nia's baskets are lined up so the search area stays clear.",
  ribbonstall_ribbons: "The ribbon stall has a quieter corner where supplies are easy to see.",
  ribbonstall_bright: "A bright ribbon is tied where the wind can catch it.",
  ribbonstall_leave: "The ribbon bundles are still soft and neatly tied.",
  lanternline_fix: "One lantern line in the square is hanging evenly now.",
  lanternline_watch: "The twisting lantern marks the wind from the workshop path.",
  mossycedar_rest: "The cedar shade in the garden is a reliable quiet spot.",
  mossycedar_listen: "The cedar shade softens the square into a far-away hum.",
  tidepool_watch: "The tide pool by the beach path marks the water's rhythm.",
  tidepool_touch: "The tide pool is a quick cold reset near the beach path.",
  workshopwindow_light: "The workshop window shows which glass pieces glow at dusk.",
  workshopwindow_stepback: "The workshop window is a good place to see the whole table at once.",
  shell_kept: "The smooth shell is in your pouch.",
  shell_placed: "The smooth shell rests on the fountain edge.",
  shell_left: "The smooth shell is still tucked in the moss.",
  fountain_deep: "The garden fountain can quiet the market noise for a while.",
  fountain_brief: "A short stop at the fountain helps reset the morning.",
  fountain_bells: "From the fountain, the bells become a distant pattern.",
  threadbasket_sorted: "The loose blue thread in the workshop has been wound back into a ring.",
  threadbasket_picked: "A sea-green thread scrap is in your pouch.",
  threadbasket_left: "Oren's thread basket is back where it was.",
};

const WORLD_NOTE_BY_FLAG = {
  mira_low_pressure: "Mira leaves a quieter route open for checking festival supplies.",
  saff_soft_bells: "Saff tests the bells with a pause signal before each bright ring.",
  lio_beach_context: "Lio uses what you noticed on the beach to make the shell path clearer.",
  nia_wide_search: "Nia widens the charm search after your route through the village.",
  oren_return_table: "Oren keeps the tide-glass table set for careful return visits.",
  oren_window_sampling: "Oren leaves a few glass pieces by the window for light testing.",
};

const PLACES = {
  plaza: {
    name: "Market Square",
    description: "The square is warm, busy, and full of lantern chatter.",
  },
  grove: {
    name: "Quiet Garden",
    description: "Bamboo shade, soft moss, and a small fountain muffle the market square.",
  },
  workshop: {
    name: "Tide-Glass Workshop",
    description: "Shelves of colored glass, thread, shells, and careful little labels line the tables.",
  },
  beach: {
    name: "Beach Path",
    description: "The tide is low, the sand is bright, and Lio has left shell baskets near the driftwood.",
  },
};

const OBJECTS = [
  {
    id: "mira",
    type: "npc",
    role: "quest",
    name: "Mira",
    place: "plaza",
    x: 250,
    y: 190,
    color: "#c86247",
    radius: 22,
    prompt: "Talk to Mira",
    text: "Mira balances a stack of lantern ribbons and an oil card with three blank marks. \"Could you help me find out which lanterns still need oil? The group by the fountain probably knows.\"",
    choices: [
      {
        text: "Walk to the fountain group and ask who still needs oil.",
        result: "You walk into the fountain circle and ask about the lantern oil. Mira gives you a grateful wave from across the square.",
        complete: "lantern",
        evidence: { social_drive: 0.18, sensory_accumulation: 0.08 },
        state: { social_energy: -0.08, sensory_load: 0.12 },
      },
      {
        text: "Wait by the ribbons until someone starts naming lanterns.",
        result: "You stay by the ribbon stall until someone starts naming lanterns aloud, then step in with the oil question.",
        complete: "lantern",
        evidence: { social_prediction_uncertainty: 0.10, social_monitoring_cost: 0.10, social_drive: 0.07 },
        state: { social_energy: -0.06, sensory_load: 0.09 },
      },
      {
        text: "Ask Mira to come with you for the first question.",
        result: "Mira smiles and walks beside you. The group answers quickly once she helps open the first question.",
        complete: "lantern",
        evidence: { masking_adaptation: 0.08, social_monitoring_cost: 0.08, ambiguity_avoidance: 0.04 },
        state: { social_energy: -0.05, sensory_load: 0.07, safety_feeling: 0.04 },
      },
      {
        text: "Check the quieter side stall for the oil card.",
        result: "You step out of the crowd and check the side stall. A spare oil card shows exactly which lanterns still need filling.",
        complete: "lantern",
        evidence: { ambiguity_avoidance: 0.04, regulation_dependency: 0.03 },
        state: { social_energy: 0.02, sensory_load: -0.02, safety_feeling: 0.03 },
      },
    ],
  },
  {
    id: "saff",
    type: "npc",
    role: "villager",
    name: "Saff",
    place: "plaza",
    x: 430,
    y: 260,
    color: "#b78e43",
    radius: 20,
    prompt: "Talk to Saff",
    text: "Saff tests the festival bells. The bright notes bounce off the stone walls.",
    followup: {
      counted: "Saff taps the bell frame twice instead of ringing it. \"I saved the pattern we counted. Want the quiet version?\"",
      awning: "Saff points to the awning before touching the bells. \"Warning first this time.\"",
      schedule: "Saff grins and holds up two fingers. \"Two patterns left, then quiet.\"",
    },
    choices: [
      {
        text: "Tap the bell rhythm on the railing.",
        result: "You count the bell pattern with Saff. The ringing is bright, but the sequence starts to make sense.",
        memory: "counted",
        evidence: { sensory_accumulation: 0.12, systemizing_structure: 0.08 },
        state: { sensory_load: 0.16, focus_lock: 0.05 },
      },
      {
        text: "Step under the cloth awning before the next ring.",
        result: "The awning takes the edge off the bells. Saff nods when you return.",
        memory: "awning",
        evidence: { regulation_dependency: 0.08, sensory_accumulation: 0.06 },
        state: { sensory_load: -0.08, safety_feeling: 0.06 },
      },
      {
        text: "Ask Saff to show a pause sign before ringing again.",
        result: "Saff shows you a small hand sign before the last pattern. The pause is visible before the next ring.",
        memory: "schedule",
        evidence: { ambiguity_avoidance: 0.05, regulation_dependency: 0.05 },
        state: { safety_feeling: 0.04 },
      },
    ],
  },
  {
    id: "lio",
    type: "npc",
    role: "quest",
    name: "Lio",
    place: "beach",
    x: 720,
    y: 455,
    color: "#6a9bb8",
    radius: 19,
    prompt: "Talk to Lio",
    text: "Lio has three baskets and a serious expression. \"The shells are for the lantern path, but I can't decide how to sort them.\"",
    choices: [
      {
        text: "Build a pale-to-dark shell path toward the water.",
        result: "Lio gasps when the shell path turns into a tide gradient.",
        complete: "shells",
        evidence: { systemizing_structure: 0.13, focused_loop_depth: 0.08 },
        state: { focus_lock: 0.08, safety_feeling: 0.04 },
      },
      {
        text: "Slip shiny shells between the plain ones.",
        result: "The path looks lively and beachy. Lio declares it bright enough for Lantern Tide.",
        complete: "shells",
        evidence: { novelty_breadth: 0.07 },
        state: { focus_lock: -0.03 },
      },
      {
        text: "Ask Lio to stand at the far end and check the path.",
        result: "Lio points from the far end, and together you make the shell path easy to follow.",
        complete: "shells",
        evidence: { social_monitoring_cost: 0.05, ambiguity_avoidance: 0.04, systemizing_structure: 0.05 },
        state: { social_energy: -0.02 },
      },
    ],
  },
  {
    id: "nia",
    type: "npc",
    role: "villager",
    name: "Nia",
    place: "beach",
    x: 610,
    y: 470,
    color: "#9b73b5",
    radius: 18,
    prompt: "Talk to Nia",
    text: "Nia is searching the tide pools while two children run circles around the baskets. \"I dropped a moon charm somewhere shiny.\"",
    followup: {
      direct: "Nia holds up the moon charm. \"You jumped in fast. The children are still impressed.\"",
      observe: "Nia crouches beside the tide pool. \"You noticed the glitter caught near the still water. I would have missed that.\"",
      support: "Nia points to a neat line of baskets. \"Clear jobs made the search calmer for everyone.\"",
    },
    choices: [
      {
        text: "Step into the search and ask the children what flashed.",
        result: "You step into the noisy search and ask the children for clues. Nia finds the charm near the basket they kept circling.",
        memory: "direct",
        evidence: { social_drive: 0.12, sensory_accumulation: 0.08 },
        state: { social_energy: -0.06, sensory_load: 0.08 },
      },
      {
        text: "Wait for the tide pool to settle, then check the still patch.",
        result: "You wait until the tide-pool reflections settle. The moon charm flashes once under a flat stone.",
        memory: "observe",
        evidence: { social_monitoring_cost: 0.07, social_prediction_uncertainty: 0.06, focused_loop_depth: 0.04 },
        state: { sensory_load: 0.03, focus_lock: 0.04 },
      },
      {
        text: "Keep the shell baskets in one clear line while Nia searches.",
        result: "You keep the baskets in one clear line. With the search area steadier, the missing charm turns up quickly.",
        memory: "support",
        evidence: { ambiguity_avoidance: 0.06, regulation_dependency: 0.05, social_monitoring_cost: 0.04 },
        state: { safety_feeling: 0.06, social_energy: -0.02 },
      },
    ],
  },
  {
    id: "oren",
    type: "npc",
    role: "quest",
    name: "Oren",
    place: "workshop",
    x: 670,
    y: 185,
    color: "#4d67a9",
    radius: 21,
    prompt: "Talk to Oren",
    text: "Oren gestures to a table of colored tide-glass pieces. \"If the display has a clear order, people will know which row to follow.\"",
    choices: [
      {
        text: "Sort the blue glass from pale to dark, then by shape.",
        result: "Oren relaxes as the glass pieces finally have a clear order.",
        complete: "display",
        evidence: { systemizing_structure: 0.16, focused_loop_depth: 0.11, context_switch_friction: 0.03 },
        state: { focus_lock: 0.14 },
      },
      {
        text: "Ask Oren to sketch where the pieces were before moving them.",
        result: "Oren sketches where the pieces were, and the table comes together without guesswork.",
        complete: "display",
        evidence: { ambiguity_avoidance: 0.06, social_monitoring_cost: 0.05 },
        state: { safety_feeling: 0.04 },
      },
      {
        text: "Try a few layouts in the window light.",
        result: "After a few quick layouts at the window, one display catches the light just right.",
        complete: "display",
        evidence: { novelty_breadth: 0.12, systemizing_structure: 0.04 },
        state: { focus_lock: -0.02 },
      },
      {
        text: "Keep tuning the uneven tray until the spacing settles.",
        result: "You keep returning to the same tray until the spacing settles.",
        complete: "display",
        evidence: { focused_loop_depth: 0.16, systemizing_structure: 0.10, context_switch_friction: 0.08 },
        state: { focus_lock: 0.18, social_energy: -0.03 },
      },
    ],
  },
  {
    id: "shell",
    type: "object",
    role: "item",
    name: "Smooth Shell",
    place: "grove",
    x: 385,
    y: 430,
    color: "#f0f0df",
    radius: 15,
    prompt: "Pick up shell",
    text: "A smooth shell rests beside the fountain. It fits neatly in your palm.",
    followup: {
      placed: "The smooth shell is still on the fountain edge, easy to find without keeping it in your pocket.",
      left: "The smooth shell is still beside the fountain, half-hidden in the moss.",
    },
    choices: [
      {
        text: "Slip the smooth shell into your pocket.",
        result: "The smooth shell rests in your pocket, giving your hand a steady place to land.",
        memory: "kept",
        evidence: { regulation_dependency: 0.08, ambiguity_avoidance: 0.03 },
        state: { safety_feeling: 0.09, sensory_load: -0.04 },
      },
      {
        text: "Place the shell on the fountain edge.",
        result: "The shell waits on the fountain edge, visible without being something you have to carry.",
        memory: "placed",
        evidence: { regulation_dependency: 0.05, ambiguity_avoidance: 0.04 },
        state: { safety_feeling: 0.06 },
      },
      {
        text: "Leave the shell tucked in the moss.",
        result: "You leave the shell by the fountain for someone else to find.",
        memory: "left",
        evidence: {},
        state: {},
      },
    ],
  },
  {
    id: "fountain",
    type: "object",
    role: "comfort",
    name: "Garden Fountain",
    place: "grove",
    x: 300,
    y: 350,
    color: "#477c63",
    radius: 28,
    prompt: "Rest by fountain",
    text: "The fountain breaks the village noise into a steady hush.",
    followup: {
      deep: "The fountain is still steady. The market sounds thinner from here.",
      brief: "The fountain is still a good place for one quiet breath before moving again.",
      bells: "From the fountain, Saff's bells arrive as a faint pattern instead of a sharp sound.",
    },
    choices: [
      {
        text: "Stay with the water until the market fades back.",
        result: "The fountain hushes the square into the background. It is easier to think about where to go next.",
        memory: "deep",
        evidence: { regulation_dependency: 0.10 },
        state: { social_energy: 0.10, sensory_load: -0.14, safety_feeling: 0.10 },
      },
      {
        text: "Touch the water once and head back.",
        result: "You use the fountain noise like a bookmark, then choose your next stop.",
        memory: "brief",
        evidence: { ambiguity_avoidance: 0.03 },
        state: { sensory_load: -0.05, safety_feeling: 0.04 },
      },
      {
        text: "Listen for the bell pattern from the fountain.",
        result: "From the fountain, the bells are distant enough to become a pattern instead of a jolt.",
        memory: "bells",
        evidence: { sensory_accumulation: 0.05, systemizing_structure: 0.05, regulation_dependency: 0.04 },
        state: { sensory_load: -0.06, focus_lock: 0.04 },
      },
    ],
  },
  {
    id: "threadbasket",
    type: "object",
    role: "item",
    name: "Thread Basket",
    place: "workshop",
    x: 770,
    y: 225,
    color: "#d88f65",
    radius: 16,
    prompt: "Inspect thread basket",
    text: "A basket of dyed thread sits under Oren's window. Some colors are tangled together; some are wound into perfect little rings.",
    followup: {
      sorted: "The blue thread ring is still neat in the basket.",
      picked: "The basket looks a little less green now, and the scrap in your pouch catches the light.",
      left: "The thread basket is still exactly where Oren left it.",
    },
    choices: [
      {
        text: "Wind the loose blue thread into a ring.",
        result: "The thread basket becomes easier to read at a glance.",
        memory: "sorted",
        evidence: { systemizing_structure: 0.08, focused_loop_depth: 0.08 },
        state: { focus_lock: 0.08 },
      },
      {
        text: "Take the sea-green scrap that catches the light.",
        result: "You pocket a sea-green thread that catches the light, then leave the basket lively and imperfect.",
        memory: "picked",
        evidence: { novelty_breadth: 0.08 },
        state: { focus_lock: -0.02, safety_feeling: 0.02 },
      },
      {
        text: "Put the basket back exactly where it was.",
        result: "You leave Oren's basket untouched. The workshop stays exactly as he arranged it.",
        memory: "left",
        evidence: { ambiguity_avoidance: 0.04, context_switch_friction: 0.03 },
        state: { safety_feeling: 0.03 },
      },
    ],
  },
  {
    id: "ribbonstall",
    type: "object",
    role: "item",
    name: "Ribbon Stall",
    place: "plaza",
    x: 170,
    y: 235,
    color: "#d77b55",
    radius: 17,
    prompt: "look through ribbons",
    text: "A stall of lantern ribbons flutters at the quieter edge of the square. The ribbon ends are soft from many hands choosing colors.",
    followup: {
      ribbons: "The ribbon stall still has a calm corner and a few colors moving in the breeze.",
      bright: "The bright ribbon you chose is tied to the stall post.",
      leave: "The ribbon bundles are still sorted by someone else's careful hands.",
    },
    choices: [
      {
        text: "Make a three-color ribbon pattern.",
        result: "You tie your three-color pattern to the front post so people can copy it.",
        memory: "ribbons",
        evidence: { systemizing_structure: 0.06, ambiguity_avoidance: 0.03 },
        state: { focus_lock: 0.04, safety_feeling: 0.03 },
      },
      {
        text: "Tie the brightest ribbon where the wind catches it.",
        result: "The bright ribbon snaps in the breeze and adds color to the stall.",
        memory: "bright",
        evidence: { novelty_breadth: 0.07 },
        state: { safety_feeling: 0.03 },
      },
      {
        text: "Feel the ribbon ends, then leave the bundles as they are.",
        result: "The ribbon texture is soft and grounding. You leave the bundles as they are.",
        memory: "leave",
        evidence: { regulation_dependency: 0.04 },
        state: { sensory_load: -0.03, safety_feeling: 0.04 },
      },
    ],
  },
  {
    id: "lanternline",
    type: "object",
    role: "item",
    name: "Lantern Line",
    place: "plaza",
    x: 355,
    y: 150,
    color: "#d8a753",
    radius: 16,
    prompt: "check lantern line",
    text: "A short line of paper lanterns hangs above the stall. One lantern keeps twisting sideways.",
    followup: {
      fix: "The lantern line hangs evenly now.",
      watch: "You know the lantern only twists when the wind comes from the workshop path.",
    },
    choices: [
      {
        text: "Straighten the twisted lantern until the row sits even.",
        result: "The lantern line settles into an even row over the stall.",
        memory: "fix",
        evidence: { focused_loop_depth: 0.06, systemizing_structure: 0.05 },
        state: { focus_lock: 0.05 },
      },
      {
        text: "Watch the gusts before touching the lantern.",
        result: "You notice the wind from the workshop path is what keeps turning the lantern.",
        memory: "watch",
        evidence: { focused_loop_depth: 0.04, systemizing_structure: 0.04, sensory_accumulation: 0.02 },
        state: { sensory_load: 0.02, focus_lock: 0.03 },
      },
    ],
  },
  {
    id: "mossycedar",
    type: "object",
    role: "comfort",
    name: "Mossy Cedar",
    place: "grove",
    x: 185,
    y: 390,
    color: "#8fb09b",
    radius: 20,
    prompt: "stand under cedar",
    text: "A cedar tree leans over the garden path. Its shade is cool, and the moss muffles footsteps.",
    followup: {
      rest: "The cedar shade is still cool and quiet.",
      listen: "From under the cedar, the square sounds like a far-away hum.",
    },
    choices: [
      {
        text: "Stay in the cedar shade until the square softens.",
        result: "The cedar shade cools your face while the square sound drops behind the leaves.",
        memory: "rest",
        evidence: { regulation_dependency: 0.08 },
        state: { sensory_load: -0.10, safety_feeling: 0.08 },
      },
      {
        text: "Listen from the cedar before choosing a path.",
        result: "From under the cedar, the square becomes a softer hum and the paths are easier to choose between.",
        memory: "listen",
        evidence: { ambiguity_avoidance: 0.04, regulation_dependency: 0.03 },
        state: { safety_feeling: 0.05 },
      },
    ],
  },
  {
    id: "tidepool",
    type: "object",
    role: "item",
    name: "Tide Pool",
    place: "beach",
    x: 650,
    y: 520,
    color: "#69a8bd",
    radius: 16,
    prompt: "look into tide pool",
    text: "A tide pool flashes with small ripples. Shell fragments move when the water pulls back.",
    followup: {
      watch: "The tide pool still shows the water's rhythm.",
      touch: "The tide pool is cool where your fingers touched it.",
    },
    choices: [
      {
        text: "Count three ripples before reaching in.",
        result: "After the third ripple, you can see which shell fragments are moving and which are settled.",
        memory: "watch",
        evidence: { focused_loop_depth: 0.05, systemizing_structure: 0.04 },
        state: { focus_lock: 0.04, sensory_load: -0.02 },
      },
      {
        text: "Touch the cold water once.",
        result: "The cold water is quick and bright, and the chill stays on your fingers.",
        memory: "touch",
        evidence: { regulation_dependency: 0.05 },
        state: { sensory_load: -0.04, safety_feeling: 0.03 },
      },
    ],
  },
  {
    id: "workshopwindow",
    type: "object",
    role: "item",
    name: "Workshop Window",
    place: "workshop",
    x: 625,
    y: 160,
    color: "#f1f1e8",
    radius: 15,
    prompt: "check the light",
    text: "The workshop window throws a bright rectangle across the table. Glass pieces change color when they cross it.",
    followup: {
      light: "The window light still shows which pieces glow warmest.",
      stepback: "From the window, the whole table is easier to see at once.",
    },
    choices: [
      {
        text: "Slide one glass piece through the window light.",
        result: "The glass warms from blue to green as it crosses the window light.",
        memory: "light",
        evidence: { novelty_breadth: 0.04, focused_loop_depth: 0.04 },
        state: { focus_lock: 0.04 },
      },
      {
        text: "Step back until the whole table fits in view.",
        result: "From the window, the messy table becomes one picture instead of many small demands.",
        memory: "stepback",
        evidence: { ambiguity_avoidance: 0.04, regulation_dependency: 0.03 },
        state: { sensory_load: -0.03, safety_feeling: 0.04 },
      },
    ],
  },
];

const ZONES = [
  { id: "plaza", label: "Market Square", x: 90, y: 80, w: 430, h: 250, color: "#ead7c7" },
  { id: "grove", label: "Quiet Garden", x: 135, y: 325, w: 355, h: 220, color: "#d9e7d7" },
  { id: "workshop", label: "Workshop", x: 560, y: 80, w: 320, h: 230, color: "#d9def0" },
  { id: "beach", label: "Beach Path", x: 555, y: 345, w: 320, h: 175, color: "#efe5c9" },
];

const initialState = {
  social_energy: 0.75,
  sensory_load: 0.10,
  regulation_need: 0.10,
  focus_lock: 0.10,
  safety_feeling: 0.75,
};

let model = createModel();
let player = startingPlayer();
let keys = new Set();
let nearest = null;
let actionTarget = null;
let moveTarget = null;
let pendingInteraction = null;
let playerHasMoved = false;
let arrivalDismissed = true;
let lastScenarioResults = [];
let frame = 0;
let storyText = "The market is already moving. Lanterns sway, shells glint, bells ring, and quiet paths branch away from the square.";
let camera = { x: 0, y: 0, scale: 1 };
let cameraLookOffset = { x: 0, y: 0 };
let mapDrag = null;
let suppressNextCanvasClick = false;
let dialogueRevealTimer = null;
let activeDialogueText = "";
let dialogueFullyRevealed = true;
let soundEnabled = false;
let soundVolume = 0.7;
let audioContext = null;
let lastDialogueBlipAt = 0;
let soundPopoverTimer = null;

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

function createModel() {
  return {
    state: { ...initialState },
    evidence: Object.fromEntries(EVIDENCE_DIMS.map((dim) => [dim, 0])),
    events: [],
    completed: {},
    relationships: {},
    pouch: {},
    objectState: {},
    worldFlags: {},
    traces: createTraceState(),
  };
}

function createTraceState() {
  return {
    zoneTicks: Object.fromEntries(Object.keys(PLACES).map((place) => [place, 0])),
    zoneEntries: { plaza: 1 },
    transitions: [],
    lastPlace: "plaza",
    nearTicks: {},
    observedBeforeInteraction: {},
    observedThenEngaged: {},
    objectInteractions: {},
    systemInteractions: {},
    placeInteractions: {},
    comfortAfterLoad: 0,
    quietReturnAfterLoad: 0,
    lastInteractionSystem: null,
  };
}

function clamp(value, min = 0, max = 1) {
  return Math.max(min, Math.min(max, value));
}

function titleize(key) {
  return key.split("_").map((word) => word.charAt(0).toUpperCase() + word.slice(1)).join(" ");
}

function applyDelta(target, delta, scale = 1) {
  Object.entries(delta || {}).forEach(([key, value]) => {
    target[key] = clamp((target[key] ?? 0) + value * scale);
  });
}

function recalcDerivedStateFor(targetModel) {
  targetModel.state.regulation_need = clamp(
    0.62 * targetModel.state.sensory_load +
      0.28 * (1 - targetModel.state.social_energy) +
      0.10 * Math.max(0, targetModel.state.focus_lock - 0.55)
  );
}

function currentPlace() {
  return ZONES.find((zone) => pointInRect(player, zone))?.id || "plaza";
}

function pointInRect(point, rect) {
  return point.x >= rect.x && point.x <= rect.x + rect.w && point.y >= rect.y && point.y <= rect.y + rect.h;
}

function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

function compactInputMode() {
  return window.matchMedia("(max-width: 640px)").matches;
}

function interactionRange() {
  return compactInputMode() ? 104 : 72;
}

function tapExtraRadius() {
  return compactInputMode() ? 38 : 18;
}

function approachStopDistance() {
  return compactInputMode() ? 66 : 54;
}

function resizeCanvasToDisplaySize() {
  const rect = canvas.getBoundingClientRect();
  const width = Math.max(320, Math.round(rect.width));
  const height = Math.max(240, Math.round(rect.height));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
}

function updateCamera() {
  const screenW = canvas.width;
  const screenH = canvas.height;
  const compact = compactInputMode();
  let viewW = compact ? 560 : WORLD_WIDTH;
  let viewH = viewW * (screenH / screenW);

  if (!compact || viewH > WORLD_HEIGHT) {
    viewH = WORLD_HEIGHT;
    viewW = viewH * (screenW / screenH);
  }

  viewW = Math.min(WORLD_WIDTH, viewW);
  viewH = Math.min(WORLD_HEIGHT, viewH);

  const focusX = compact ? player.x - viewW * 0.33 + cameraLookOffset.x : 0;
  const focusY = compact ? player.y - viewH * 0.48 + cameraLookOffset.y : 0;
  camera = {
    x: clamp(focusX, 0, WORLD_WIDTH - viewW),
    y: clamp(focusY, 0, WORLD_HEIGHT - viewH),
    scale: Math.min(screenW / viewW, screenH / viewH),
  };
}

function screenToWorld(screenX, screenY) {
  return {
    x: camera.x + screenX / camera.scale,
    y: camera.y + screenY / camera.scale,
  };
}

function resetCameraLookOffset() {
  cameraLookOffset = { x: 0, y: 0 };
}

function startingPlayer() {
  return { x: 110, y: 165, speed: 2.8 };
}

function updateNearest() {
  nearest = OBJECTS
    .filter((object) => model.objectState[object.id] !== "removed")
    .map((object) => ({ object, dist: distance(player, object) }))
    .filter(({ dist }) => dist < interactionRange())
    .sort((a, b) => a.dist - b.dist)[0]?.object || null;

  const hint = document.getElementById("interactionHint");
  const actionButton = document.getElementById("actionButton");
  actionButton.hidden = true;
  actionTarget = null;
  if (nearest && (playerHasMoved || hasPlayerHistory())) {
    const completedQuest = completedQuestForObject(nearest);
    const roleLabel = ROLE_LABELS[nearest.role] || nearest.type;
    if (completedQuest) {
      hint.textContent = `${nearest.name} has a follow-up. ${nextGoalText()}`;
    } else if (model.relationships[nearest.id] && nearest.followup) {
      hint.textContent = `Click ${nearest.name} for a follow-up conversation.`;
    } else {
      hint.textContent = `Click ${nearest.name} to ${nearest.prompt}. (${roleLabel})`;
    }
    actionButton.textContent = actionLabelFor(nearest);
    actionTarget = nearest;
    actionButton.hidden = false;
  } else if (moveTarget) {
    hint.textContent = "Walking. Click a person or object to interact.";
  } else {
    hint.textContent = idleHintText();
  }
}

function actionLabelFor(object) {
  if (object.type === "npc") return `Talk with ${object.name}`;
  if (object.role === "comfort") return `Visit ${object.name}`;
  return `Inspect ${object.name}`;
}

function dismissArrival() {
  arrivalDismissed = true;
  const arrivalCard = document.getElementById("arrivalCard");
  if (arrivalCard) arrivalCard.hidden = true;
}

function hasPlayerHistory() {
  return model.events.length > 0 ||
    Object.keys(model.completed).length > 0 ||
    Object.keys(model.relationships).length > 0 ||
    Object.keys(model.pouch).length > 0 ||
    Object.keys(model.worldFlags).length > 0;
}

function idleHintText() {
  if (Object.keys(QUESTS).every((key) => model.completed[key])) {
    return "The village is ready. Wander, revisit people, rest, or finish the morning.";
  }
  const place = currentPlace();
  if (!hasPlayerHistory()) {
    return compactInputMode()
      ? "Tap to walk. Drag sideways to look around. Mira is nearby, or follow anything else that catches your eye."
      : "Click anywhere to walk. Mira is nearby, or follow anything else that catches your eye.";
  }
  if (place === "plaza") return "Market Square is busy. Try a quieter path, the beach, the workshop, or someone nearby.";
  if (place === "grove") return "The garden is quiet. Rest by the fountain, look around, or head back toward the village.";
  if (place === "beach") return "The beach path has people and small things to notice. Click what catches your eye.";
  if (place === "workshop") return "The workshop has displays, materials, and people who may want company.";
  return "Wander toward a person, object, or place that catches your eye.";
}

function step() {
  frame += 1;
  resizeCanvasToDisplaySize();
  updateCamera();
  const hadPlayerMoved = playerHasMoved;
  let dx = 0;
  let dy = 0;
  if (keys.has("ArrowLeft") || keys.has("a")) dx -= 1;
  if (keys.has("ArrowRight") || keys.has("d")) dx += 1;
  if (keys.has("ArrowUp") || keys.has("w")) dy -= 1;
  if (keys.has("ArrowDown") || keys.has("s")) dy += 1;

  if (dx || dy) {
    playerHasMoved = true;
    moveTarget = null;
    pendingInteraction = null;
    const len = Math.hypot(dx, dy);
    player.x = clamp(player.x + (dx / len) * player.speed, 36, WORLD_WIDTH - 36);
    player.y = clamp(player.y + (dy / len) * player.speed, 44, WORLD_HEIGHT - 38);
    applyAmbientPlaceTelemetry();
  } else if (moveTarget) {
    playerHasMoved = true;
    const dist = distance(player, moveTarget);
    if (dist <= player.speed + 1) {
      player.x = moveTarget.x;
      player.y = moveTarget.y;
      moveTarget = null;
      if (pendingInteraction) {
        const object = OBJECTS.find((item) => item.id === pendingInteraction);
        pendingInteraction = null;
        if (object) openInteraction(object);
      }
    } else {
      player.x += ((moveTarget.x - player.x) / dist) * player.speed;
      player.y += ((moveTarget.y - player.y) / dist) * player.speed;
      applyAmbientPlaceTelemetry();
    }
  }

  if (!hadPlayerMoved && playerHasMoved) {
    renderHud();
  }
  trackRouteTelemetry();
  updateNearest();
  draw();
  requestAnimationFrame(step);
}

let ambientTick = 0;
let routeTick = 0;
function applyAmbientPlaceTelemetry() {
  ambientTick += 1;
  if (ambientTick % 24 !== 0) return;
  const place = currentPlace();
  if (place === "plaza") {
    applyDelta(model.state, { sensory_load: 0.012, social_energy: -0.006 });
    applyDelta(model.evidence, { sensory_accumulation: 0.004 });
  }
  if (place === "grove") {
    applyDelta(model.state, { sensory_load: -0.014, safety_feeling: 0.008 });
  }
  if (place === "workshop") {
    applyDelta(model.state, { focus_lock: 0.006 });
  }
  recalcDerivedStateFor(model);
  renderHud();
}

function trackRouteTelemetry() {
  if (!arrivalDismissed || !model.traces) return;
  routeTick += 1;
  if (routeTick % 30 !== 0) return;

  const trace = model.traces;
  const place = currentPlace();
  trace.zoneTicks[place] = (trace.zoneTicks[place] || 0) + 1;

  if (trace.lastPlace !== place) {
    trace.transitions.push({ from: trace.lastPlace, to: place });
    trace.transitions = trace.transitions.slice(-24);
    trace.zoneEntries[place] = (trace.zoneEntries[place] || 0) + 1;
    if (place === "grove" && model.state.sensory_load >= 0.20) {
      trace.quietReturnAfterLoad += 1;
    }
    trace.lastPlace = place;
  }

  if (nearest && nearest.type === "npc" && !model.relationships[nearest.id] && !completedQuestForObject(nearest)) {
    trace.nearTicks[nearest.id] = (trace.nearTicks[nearest.id] || 0) + 1;
    if (trace.nearTicks[nearest.id] >= 3) {
      trace.observedBeforeInteraction[nearest.id] = true;
    }
  }
}

function draw() {
  updateCamera();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const pulse = Math.sin(frame / 160) * 0.5 + 0.5;
  ctx.fillStyle = `rgb(${222 + pulse * 3}, ${231 + pulse * 2}, ${216 + pulse * 4})`;
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.setTransform(camera.scale, 0, 0, camera.scale, -camera.x * camera.scale, -camera.y * camera.scale);

  drawTerrain();

  drawAmbientBackdrop();
  drawVillagePaths();
  drawScenery();
  drawFestivalChanges();

  OBJECTS.forEach((object) => {
    if (model.objectState[object.id] === "removed") return;
    drawObjectAura(object);
    const completed = object.choices.some((choice) => choice.complete && model.completed[choice.complete]);
    const remembered = Boolean(model.relationships[object.id] || model.worldFlags[object.id]);
    const bob = object.type === "npc" ? Math.sin(frame / 38 + object.x * 0.03) * 1.5 : 0;
    if (object.type === "npc") {
      drawVillager(object, object.x, object.y + bob, completed, remembered);
    } else {
      drawWorldObject(object, completed, remembered);
    }
    if (nearest?.id === object.id) {
      drawNameplate(object.name, object.x, object.y + object.radius + 18);
    }
    if (completed || remembered) {
      ctx.beginPath();
      ctx.strokeStyle = completed ? "#477c63" : "rgba(45, 103, 118, 0.72)";
      ctx.lineWidth = completed ? 4 : 3;
      ctx.arc(object.x, object.y, object.radius + 7, 0, Math.PI * 2);
      ctx.stroke();
      drawStatusBadge(object, completed);
    }
    ctx.textAlign = "start";
  });

  if (moveTarget) {
    ctx.beginPath();
    ctx.strokeStyle = "rgba(23,25,28,0.55)";
    ctx.lineWidth = 3;
    ctx.arc(moveTarget.x, moveTarget.y, 10, 0, Math.PI * 2);
    ctx.stroke();
  }

  drawPlayer();
  ctx.setTransform(1, 0, 0, 1, 0, 0);
}

function drawStatusBadge(object, completed) {
  const x = object.x + object.radius + 7;
  const y = object.y - object.radius - 7;
  ctx.fillStyle = completed ? "rgba(71, 124, 99, 0.94)" : "rgba(45, 103, 118, 0.92)";
  ctx.beginPath();
  ctx.arc(x, y, 9, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "rgba(255, 253, 247, 0.95)";
  ctx.lineWidth = 2;
  ctx.lineCap = "round";
  ctx.beginPath();
  if (completed) {
    ctx.moveTo(x - 4, y);
    ctx.lineTo(x - 1, y + 4);
    ctx.lineTo(x + 5, y - 4);
  } else {
    ctx.moveTo(x - 3, y);
    ctx.lineTo(x + 3, y);
    ctx.moveTo(x, y - 3);
    ctx.lineTo(x, y + 3);
  }
  ctx.stroke();
}

function drawFestivalChanges() {
  if (model.completed.lantern) {
    drawLanternGlow(212, 126);
    drawLanternGlow(460, 115);
    drawLanternGlow(595, 110);
    ctx.fillStyle = "rgba(242, 197, 107, 0.85)";
    roundRect(232, 222, 42, 14, 6);
    ctx.fill();
  }
  if (model.completed.shells) {
    for (let i = 0; i < 8; i += 1) {
      ctx.beginPath();
      ctx.fillStyle = i % 2 === 0 ? "rgba(106, 155, 184, 0.86)" : "rgba(240, 240, 223, 0.92)";
      ctx.arc(590 + i * 24, 504 + Math.sin(i) * 8, 7, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = "rgba(255, 253, 247, 0.72)";
      ctx.lineWidth = 2;
      ctx.stroke();
    }
  }
  if (model.completed.display) {
    const gems = [
      [628, 164, "#6a9bb8"],
      [648, 164, "#4d67a9"],
      [668, 164, "#9b73b5"],
      [628, 183, "#d8a753"],
      [648, 183, "#d88f65"],
      [668, 183, "#477c63"],
    ];
    gems.forEach(([x, y, color]) => {
      ctx.fillStyle = color;
      roundRect(x, y, 12, 12, 3);
      ctx.fill();
    });
  }
  if (Object.keys(QUESTS).every((key) => model.completed[key])) {
    ctx.fillStyle = "rgba(242, 197, 107, 0.32)";
    roundRect(115, 92, 338, 52, 18);
    ctx.fill();
  }
  drawMemoryChanges();
}

function drawMemoryChanges() {
  if (model.worldFlags.mira_low_pressure) {
    drawSmallSign("side path", 250, 154, "#2d6776");
  }
  if (model.relationships.saff === "counted") {
    drawSmallSign("tap tap", 432, 232, "#d8a753");
  }
  if (model.relationships.saff === "awning") {
    drawAwningShade(392, 286);
  }
  if (model.relationships.saff === "schedule") {
    drawSmallSign("2 left", 448, 228, "#d8a753");
  }
  if (model.worldFlags.saff_soft_bells) {
    drawSmallSign("pause", 394, 250, "#2d6776");
  }
  if (model.relationships.nia) {
    drawMoonCharm(594, 492);
  }
  if (model.worldFlags.nia_wide_search) {
    drawSmallSign("search", 602, 446, "#9b73b5");
  }
  if (model.worldFlags.lio_beach_context) {
    drawSmallSign("tide clue", 714, 426, "#6a9bb8");
  }
  if (model.relationships.ribbonstall === "ribbons") {
    drawRibbonPennants(155, 198, ["#c86247", "#d8a753", "#4d67a9"]);
  }
  if (model.relationships.ribbonstall === "bright") {
    drawRibbonPennants(176, 198, ["#f1a36f"]);
  }
  if (model.relationships.lanternline === "fix") {
    drawSmallSign("even", 378, 130, "#d8a753");
  }
  if (model.relationships.lanternline === "watch") {
    drawWindSwirl(420, 136);
  }
  if (model.relationships.tidepool === "watch") {
    drawSmallSign("3 ripples", 622, 526, "#6a9bb8");
  }
  if (model.relationships.workshopwindow === "light") {
    drawLightBeam(635, 178);
  }
  if (model.worldFlags.oren_return_table) {
    drawSmallSign("return", 684, 158, "#4d67a9");
  }
  if (model.relationships.threadbasket === "sorted") {
    drawThreadRing(762, 218, "#4d67a9");
  }
  if (model.pouch.thread) {
    drawThreadRing(748, 218, "#477c63");
  }
  if (model.worldFlags.shell === "noticed" || model.relationships.shell === "placed") {
    drawShellObject(315, 336, 10);
  }
}

function drawTerrain() {
  drawTerrainPatch(90, 78, 440, 260, 26, "rgba(234, 215, 199, 0.82)", [
    [126, 102], [505, 86], [532, 235], [492, 330], [150, 326], [88, 285],
  ]);
  drawTerrainPatch(130, 318, 370, 240, 28, "rgba(217, 231, 215, 0.82)", [
    [158, 338], [455, 320], [512, 392], [486, 552], [156, 548], [115, 430],
  ]);
  drawTerrainPatch(548, 80, 348, 245, 30, "rgba(217, 222, 240, 0.84)", [
    [578, 92], [856, 82], [910, 148], [880, 306], [612, 326], [540, 250],
  ]);
  drawTerrainPatch(535, 355, 355, 180, 30, "rgba(239, 229, 201, 0.9)", [
    [565, 370], [850, 360], [900, 430], [870, 540], [575, 525], [520, 455],
  ]);
  drawSignpost("Market", 118, 100);
  drawSignpost("Garden", 164, 337);
  drawSignpost("Workshop", 588, 100);
  drawSignpost("Beach", 585, 365);
}

function drawTerrainPatch(x, y, w, h, r, color, points) {
  ctx.fillStyle = color;
  ctx.beginPath();
  points.forEach(([px, py], index) => {
    if (index === 0) ctx.moveTo(px, py);
    else {
      const [prevX, prevY] = points[index - 1];
      ctx.quadraticCurveTo((prevX + px) / 2, (prevY + py) / 2, px, py);
    }
  });
  const [firstX, firstY] = points[0];
  const [lastX, lastY] = points[points.length - 1];
  ctx.quadraticCurveTo((lastX + firstX) / 2, (lastY + firstY) / 2, firstX, firstY);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = "rgba(255, 253, 247, 0.34)";
  ctx.lineWidth = 3;
  ctx.stroke();
}

function drawSignpost(text, x, y) {
  ctx.fillStyle = "rgba(92, 70, 47, 0.38)";
  roundRect(x - 3, y + 10, 6, 26, 2);
  ctx.fill();
  ctx.fillStyle = "rgba(255, 253, 247, 0.78)";
  roundRect(x - 7, y - 4, 74, 24, 7);
  ctx.fill();
  ctx.fillStyle = "rgba(23, 25, 28, 0.58)";
  ctx.font = "800 12px sans-serif";
  ctx.fillText(text, x + 6, y + 12);
}

function drawVillagePaths() {
  drawCurvedPath([[118, 166], [235, 185], [370, 206], [520, 190], [635, 190], [725, 212]]);
  drawCurvedPath([[312, 296], [322, 342], [310, 382], [250, 440], [195, 500]]);
  drawCurvedPath([[470, 430], [548, 430], [625, 440], [720, 480], [852, 496]]);
  drawCurvedPath([[668, 315], [675, 355], [690, 405], [720, 480]]);
}

function drawCurvedPath(points) {
  ctx.strokeStyle = "rgba(151, 126, 92, 0.26)";
  ctx.lineWidth = 20;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.beginPath();
  points.forEach(([x, y], index) => {
    if (index === 0) ctx.moveTo(x, y);
    else {
      const [prevX, prevY] = points[index - 1];
      ctx.quadraticCurveTo(prevX, prevY, (prevX + x) / 2, (prevY + y) / 2);
    }
  });
  ctx.stroke();
  ctx.strokeStyle = "rgba(255, 253, 247, 0.22)";
  ctx.lineWidth = 7;
  ctx.stroke();
}

function drawLanternGlow(x, y) {
  const glow = 0.28 + (Math.sin(frame / 30 + x * 0.02) + 1) * 0.08;
  ctx.fillStyle = `rgba(242, 197, 107, ${glow})`;
  ctx.beginPath();
  ctx.arc(x, y + 7, 22, 0, Math.PI * 2);
  ctx.fill();
}

function drawSmallSign(text, x, y, color) {
  ctx.fillStyle = "rgba(255, 253, 247, 0.86)";
  roundRect(x - 22, y - 12, 48, 22, 6);
  ctx.fill();
  ctx.fillStyle = color;
  ctx.font = "800 10px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(text, x + 2, y + 3);
  ctx.textAlign = "start";
}

function drawAwningShade(x, y) {
  ctx.fillStyle = "rgba(255, 253, 247, 0.42)";
  roundRect(x - 44, y - 18, 88, 28, 8);
  ctx.fill();
  ctx.fillStyle = "rgba(45, 103, 118, 0.22)";
  for (let i = 0; i < 4; i += 1) {
    roundRect(x - 38 + i * 18, y - 18, 9, 28, 4);
    ctx.fill();
  }
}

function drawMoonCharm(x, y) {
  ctx.fillStyle = "rgba(255, 253, 247, 0.92)";
  ctx.beginPath();
  ctx.arc(x, y, 9, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(106, 155, 184, 0.88)";
  ctx.beginPath();
  ctx.arc(x + 4, y - 2, 8, 0, Math.PI * 2);
  ctx.fill();
}

function drawRibbonPennants(x, y, colors) {
  colors.forEach((color, index) => {
    const px = x + index * 18;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(px, y);
    ctx.lineTo(px + 12, y + Math.sin(frame / 18 + index) * 3);
    ctx.lineTo(px + 6, y + 20);
    ctx.closePath();
    ctx.fill();
  });
}

function drawWindSwirl(x, y) {
  ctx.strokeStyle = "rgba(45, 103, 118, 0.34)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  for (let i = 0; i < 24; i += 1) {
    const a = i / 3 + frame / 55;
    const r = i * 0.8;
    const px = x + Math.cos(a) * r;
    const py = y + Math.sin(a) * r * 0.55;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();
}

function drawLightBeam(x, y) {
  ctx.fillStyle = "rgba(242, 197, 107, 0.22)";
  ctx.beginPath();
  ctx.moveTo(x, y);
  ctx.lineTo(x + 88, y + 70);
  ctx.lineTo(x + 36, y + 86);
  ctx.lineTo(x - 22, y + 16);
  ctx.closePath();
  ctx.fill();
}

function drawThreadRing(x, y, color) {
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.ellipse(x, y, 10, 7, 0.4, 0, Math.PI * 2);
  ctx.stroke();
}

function drawAmbientBackdrop() {
  drawLeafDrift();
  drawBellMotes();
  drawFountainRipples(300, 350);
}

function drawScenery() {
  drawWorkshopBuilding(598, 132);
  drawBeachRocks();
  drawStall(145, 228, "#d77b55");
  drawStall(355, 154, "#d8a753");
  drawTree(185, 390, 28);
  drawTree(440, 520, 24);
  drawTree(825, 130, 20);
  drawFlowerPatch(150, 515, "#c86247");
  drawFlowerPatch(805, 500, "#4d67a9");
  drawFlowerPatch(500, 305, "#d8a753");
  drawWave(585, 510, 235);
  drawTable(625, 160);
  drawTable(725, 245);
  drawLantern(215, 125, "#f2c56b");
  drawLantern(460, 115, "#f1a36f");
  drawLantern(595, 110, "#f2c56b");
}

function drawWorkshopBuilding(x, y) {
  ctx.fillStyle = "rgba(91, 103, 148, 0.22)";
  roundRect(x - 28, y + 58, 172, 92, 14);
  ctx.fill();
  ctx.fillStyle = "rgba(255, 253, 247, 0.82)";
  roundRect(x, y + 48, 118, 76, 12);
  ctx.fill();
  ctx.fillStyle = "rgba(77, 103, 169, 0.28)";
  ctx.beginPath();
  ctx.moveTo(x - 12, y + 58);
  ctx.lineTo(x + 60, y + 18);
  ctx.lineTo(x + 132, y + 58);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "rgba(106, 155, 184, 0.5)";
  roundRect(x + 70, y + 68, 30, 28, 6);
  ctx.fill();
  ctx.fillStyle = "rgba(216, 167, 83, 0.56)";
  roundRect(x + 20, y + 72, 24, 52, 8);
  ctx.fill();
}

function drawBeachRocks() {
  const rocks = [[820, 458, 10], [850, 470, 7], [786, 510, 8], [610, 515, 6]];
  rocks.forEach(([x, y, r]) => {
    ctx.fillStyle = "rgba(95, 105, 112, 0.2)";
    ctx.beginPath();
    ctx.ellipse(x, y, r, r * 0.65, 0.2, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawStall(x, y, color) {
  ctx.fillStyle = "rgba(255, 253, 247, 0.72)";
  roundRect(x, y, 78, 36, 8);
  ctx.fill();
  ctx.fillStyle = color;
  roundRect(x + 8, y - 12, 62, 18, 6);
  ctx.fill();
  ctx.strokeStyle = "rgba(23, 25, 28, 0.16)";
  ctx.lineWidth = 2;
  for (let i = 0; i < 3; i += 1) {
    const rx = x + 18 + i * 16;
    ctx.beginPath();
    ctx.moveTo(rx, y - 8);
    ctx.lineTo(rx + Math.sin(frame / 28 + i) * 4, y + 8);
    ctx.stroke();
  }
}

function drawTree(x, y, r) {
  const sway = Math.sin(frame / 70 + x * 0.01) * 2;
  ctx.fillStyle = "rgba(70, 112, 78, 0.34)";
  ctx.beginPath();
  ctx.arc(x + sway, y, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(71, 124, 99, 0.24)";
  ctx.beginPath();
  ctx.arc(x - r * 0.35 + sway * 0.6, y - r * 0.2, r * 0.62, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(92, 70, 47, 0.36)";
  roundRect(x - 4, y + r - 5, 8, 22, 3);
  ctx.fill();
}

function drawWave(x, y, width) {
  ctx.strokeStyle = "rgba(69, 129, 153, 0.32)";
  ctx.lineWidth = 4;
  ctx.beginPath();
  for (let i = 0; i <= width; i += 18) {
    const px = x + i;
    const py = y + Math.sin(i / 16 + frame / 28) * 6;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();
  ctx.strokeStyle = "rgba(255, 253, 247, 0.42)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let i = 0; i <= width * 0.75; i += 16) {
    const px = x + 28 + i;
    const py = y + 14 + Math.sin(i / 14 + frame / 32) * 4;
    if (i === 0) ctx.moveTo(px, py);
    else ctx.lineTo(px, py);
  }
  ctx.stroke();
}

function drawTable(x, y) {
  ctx.fillStyle = "rgba(255, 253, 247, 0.62)";
  roundRect(x, y, 88, 34, 8);
  ctx.fill();
}

function drawLantern(x, y, color) {
  const sway = Math.sin(frame / 42 + x * 0.02) * 4;
  ctx.strokeStyle = "rgba(23, 25, 28, 0.24)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x, y - 16);
  ctx.lineTo(x + sway * 0.55, y - 3);
  ctx.stroke();
  ctx.fillStyle = `rgba(242, 197, 107, ${0.14 + (Math.sin(frame / 34 + x) + 1) * 0.04})`;
  ctx.beginPath();
  ctx.arc(x + sway, y + 8, 20, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = color;
  roundRect(x + sway - 8, y - 3, 16, 22, 7);
  ctx.fill();
}

function drawObjectAura(object) {
  if (nearest?.id !== object.id) return;
  const radius = object.radius + 12 + Math.sin(frame / 16) * 2;
  ctx.beginPath();
  ctx.strokeStyle = "rgba(23, 25, 28, 0.34)";
  ctx.lineWidth = 3;
  ctx.arc(object.x, object.y, radius, 0, Math.PI * 2);
  ctx.stroke();
}

function drawNameplate(text, x, y) {
  ctx.font = "800 13px sans-serif";
  const width = ctx.measureText(text).width + 18;
  ctx.fillStyle = "rgba(255, 253, 247, 0.88)";
  roundRect(x - width / 2, y - 13, width, 22, 7);
  ctx.fill();
  ctx.fillStyle = "#17191c";
  ctx.textAlign = "center";
  ctx.fillText(text, x, y + 2);
  ctx.textAlign = "start";
}

function drawPlayer() {
  const bob = Math.sin(frame / 12) * (moveTarget || keys.size ? 1.6 : 0.5);
  const x = player.x;
  const y = player.y + bob;
  ctx.fillStyle = "rgba(23, 25, 28, 0.18)";
  ctx.beginPath();
  ctx.ellipse(x, y + 18, 14, 5, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#202326";
  roundRect(x - 8, y - 2, 16, 24, 7);
  ctx.fill();
  ctx.fillStyle = "#f0d0b4";
  ctx.beginPath();
  ctx.arc(x, y - 9, 10, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "#17191c";
  ctx.beginPath();
  ctx.arc(x - 3, y - 10, 1.5, 0, Math.PI * 2);
  ctx.arc(x + 3, y - 10, 1.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.arc(x, y + 2, 18, 0, Math.PI * 2);
  ctx.stroke();
}

function drawVillager(object, x, y, completed, remembered) {
  const bodyColor = completed ? "#7f8b83" : remembered ? "#7d9488" : object.color;
  ctx.fillStyle = "rgba(23, 25, 28, 0.16)";
  ctx.beginPath();
  ctx.ellipse(x, y + object.radius + 5, object.radius * 0.82, object.radius * 0.28, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = bodyColor;
  roundRect(x - object.radius * 0.48, y - 2, object.radius * 0.96, object.radius * 1.25, 8);
  ctx.fill();
  ctx.fillStyle = lightenColor(bodyColor, 0.28);
  ctx.beginPath();
  ctx.arc(x, y - object.radius * 0.48, object.radius * 0.72, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = nearest?.id === object.id ? "#17191c" : "rgba(255,255,255,0.9)";
  ctx.lineWidth = nearest?.id === object.id ? 4 : 2;
  ctx.stroke();
  drawNpcFace(x, y - object.radius * 0.48, object.radius);
  ctx.strokeStyle = "rgba(23, 25, 28, 0.24)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x - object.radius * 0.5, y + object.radius * 0.3);
  ctx.lineTo(x - object.radius * 0.82, y + object.radius * 0.68);
  ctx.moveTo(x + object.radius * 0.5, y + object.radius * 0.3);
  ctx.lineTo(x + object.radius * 0.82, y + object.radius * 0.68);
  ctx.stroke();
}

function drawWorldObject(object, completed, remembered) {
  const color = completed ? "#7f8b83" : remembered ? "#7d9488" : object.color;
  ctx.fillStyle = "rgba(23, 25, 28, 0.12)";
  ctx.beginPath();
  ctx.ellipse(object.x, object.y + object.radius * 0.85, object.radius * 0.95, object.radius * 0.28, 0, 0, Math.PI * 2);
  ctx.fill();
  if (object.id === "fountain") {
    drawFountainObject(object.x, object.y, object.radius, color);
  } else if (object.id === "shell") {
    drawShellObject(object.x, object.y, object.radius);
  } else if (object.id === "threadbasket") {
    drawBasketObject(object.x, object.y, object.radius, color);
  } else if (object.id === "ribbonstall") {
    drawRibbonBundle(object.x, object.y, object.radius, color);
  } else if (object.id === "lanternline") {
    drawLanternLineObject(object.x, object.y, object.radius, color);
  } else if (object.id === "mossycedar") {
    drawCedarObject(object.x, object.y, object.radius, color);
  } else if (object.id === "tidepool") {
    drawTidePoolObject(object.x, object.y, object.radius, color);
  } else if (object.id === "workshopwindow") {
    drawWindowObject(object.x, object.y, object.radius);
  } else {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(object.x, object.y, object.radius, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.strokeStyle = nearest?.id === object.id ? "#17191c" : "rgba(255,255,255,0.9)";
  ctx.lineWidth = nearest?.id === object.id ? 4 : 2;
  ctx.stroke();
}

function drawFountainObject(x, y, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.ellipse(x, y, r * 1.1, r * 0.82, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = "rgba(255,253,247,0.36)";
  ctx.beginPath();
  ctx.ellipse(x, y - 2, r * 0.7, r * 0.45, 0, 0, Math.PI * 2);
  ctx.fill();
}

function drawShellObject(x, y, r) {
  ctx.fillStyle = "#f0f0df";
  ctx.beginPath();
  ctx.ellipse(x, y, r * 0.95, r * 0.7, -0.35, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "rgba(151,126,92,0.32)";
  ctx.lineWidth = 2;
  for (let i = -1; i <= 1; i += 1) {
    ctx.beginPath();
    ctx.moveTo(x - 3, y + 4);
    ctx.lineTo(x + i * 6, y - 8);
    ctx.stroke();
  }
}

function drawBasketObject(x, y, r, color) {
  ctx.fillStyle = color;
  roundRect(x - r, y - r * 0.45, r * 2, r * 1.25, 7);
  ctx.fill();
  ctx.strokeStyle = "rgba(255,253,247,0.38)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(x, y - r * 0.45, r * 0.75, Math.PI, Math.PI * 2);
  ctx.stroke();
}

function drawRibbonBundle(x, y, r, color) {
  ctx.fillStyle = color;
  for (let i = 0; i < 3; i += 1) {
    roundRect(x - r + i * 8, y - r * 0.55 + i * 2, r * 1.4, 8, 4);
    ctx.fill();
  }
}

function drawLanternLineObject(x, y, r, color) {
  ctx.strokeStyle = "rgba(92,70,47,0.35)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x - r * 1.4, y - 5);
  ctx.lineTo(x + r * 1.4, y - 5);
  ctx.stroke();
  drawLantern(x - 10, y - 4, color);
}

function drawCedarObject(x, y, r, color) {
  drawTree(x, y, r * 1.15);
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(x, y, r + 5, 0, Math.PI * 2);
  ctx.stroke();
}

function drawTidePoolObject(x, y, r, color) {
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.ellipse(x, y, r * 1.2, r * 0.76, -0.2, 0, Math.PI * 2);
  ctx.fill();
  ctx.strokeStyle = "rgba(255,253,247,0.44)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.ellipse(x + 2, y - 1, r * 0.78, r * 0.38, -0.2, 0, Math.PI * 2);
  ctx.stroke();
}

function drawWindowObject(x, y, r) {
  ctx.fillStyle = "rgba(255,253,247,0.86)";
  roundRect(x - r, y - r, r * 2, r * 1.6, 6);
  ctx.fill();
  ctx.strokeStyle = "rgba(77,103,169,0.45)";
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x, y - r);
  ctx.lineTo(x, y + r * 0.6);
  ctx.moveTo(x - r, y - r * 0.2);
  ctx.lineTo(x + r, y - r * 0.2);
  ctx.stroke();
}

function drawNpcFace(x, y, radius) {
  const look = Math.sin(frame / 90 + x * 0.01) * 2;
  ctx.fillStyle = "rgba(23, 25, 28, 0.52)";
  ctx.beginPath();
  ctx.arc(x - radius * 0.22 + look, y - radius * 0.1, 2, 0, Math.PI * 2);
  ctx.arc(x + radius * 0.22 + look, y - radius * 0.1, 2, 0, Math.PI * 2);
  ctx.fill();
}

function lightenColor(hex, amount) {
  const raw = hex.replace("#", "");
  const value = Number.parseInt(raw, 16);
  const r = Math.min(255, Math.round(((value >> 16) & 255) + 255 * amount));
  const g = Math.min(255, Math.round(((value >> 8) & 255) + 255 * amount));
  const b = Math.min(255, Math.round((value & 255) + 255 * amount));
  return `rgb(${r}, ${g}, ${b})`;
}

function drawFlowerPatch(x, y, color) {
  for (let i = 0; i < 7; i += 1) {
    const px = x + Math.cos(i * 1.7) * (8 + (i % 3) * 5);
    const py = y + Math.sin(i * 1.7) * (6 + (i % 2) * 5);
    ctx.fillStyle = i % 2 ? "rgba(255, 253, 247, 0.78)" : color;
    ctx.beginPath();
    ctx.arc(px, py + Math.sin(frame / 48 + i) * 0.8, 3, 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawLeafDrift() {
  const leaves = [
    [150, 105, 0.4],
    [250, 550, 1.3],
    [420, 365, 2.1],
    [515, 260, 2.9],
    [780, 130, 3.4],
    [845, 455, 4.2],
  ];
  leaves.forEach(([baseX, baseY, phase], index) => {
    const x = baseX + Math.sin(frame / 85 + phase) * 12;
    const y = baseY + ((frame * (0.18 + index * 0.015) + phase * 25) % 34);
    ctx.fillStyle = "rgba(216, 167, 83, 0.34)";
    ctx.beginPath();
    ctx.ellipse(x, y, 5, 2.5, phase + frame / 140, 0, Math.PI * 2);
    ctx.fill();
  });
}

function drawBellMotes() {
  for (let i = 0; i < 5; i += 1) {
    const alpha = 0.14 + (Math.sin(frame / 24 + i) + 1) * 0.08;
    ctx.fillStyle = `rgba(216, 167, 83, ${alpha})`;
    ctx.beginPath();
    ctx.arc(392 + Math.sin(frame / 30 + i) * 28, 238 + Math.cos(frame / 38 + i) * 22, 3 + (i % 2), 0, Math.PI * 2);
    ctx.fill();
  }
}

function drawFountainRipples(x, y) {
  for (let i = 0; i < 3; i += 1) {
    const r = 18 + ((frame / 4 + i * 12) % 36);
    const alpha = 0.22 * (1 - (r - 18) / 36);
    ctx.strokeStyle = `rgba(255, 253, 247, ${alpha})`;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.stroke();
  }
}

function drawPath(x1, y1, x2, y2) {
  ctx.strokeStyle = "rgba(151, 126, 92, 0.38)";
  ctx.lineWidth = 18;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
}

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

function setDialogueSpeaker(object, kicker) {
  const portrait = document.getElementById("dialogPortrait");
  document.getElementById("dialogKicker").textContent = kicker;
  document.getElementById("dialogTitle").textContent = object.name;
  portrait.textContent = object.name.charAt(0).toUpperCase();
  portrait.style.background = object.color || "var(--accent)";
}

function ensureAudioContext() {
  if (!audioContext) {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (audioContext.state === "suspended") {
    audioContext.resume();
  }
  return audioContext;
}

function setSoundEnabled(enabled) {
  soundEnabled = enabled;
  const button = document.getElementById("soundToggle");
  const popover = document.getElementById("soundPopover");
  button.setAttribute("aria-pressed", String(soundEnabled));
  button.setAttribute("aria-label", soundEnabled ? "Turn sound off" : "Turn sound on");
  button.querySelector("span").textContent = soundEnabled ? "🔊" : "🔇";
  popover.hidden = !soundEnabled;
  if (soundEnabled) {
    ensureAudioContext();
    playTone({ frequency: 440, duration: 0.08, volume: 0.36, type: "sine" });
    scheduleSoundPopoverClose();
  } else {
    window.clearTimeout(soundPopoverTimer);
  }
}

function setSoundVolume(value) {
  soundVolume = clamp(Number(value) / 100, 0, 1);
  scheduleSoundPopoverClose();
}

function scheduleSoundPopoverClose(delay = 2600) {
  window.clearTimeout(soundPopoverTimer);
  if (!soundEnabled) return;
  soundPopoverTimer = window.setTimeout(() => {
    document.getElementById("soundPopover").hidden = true;
  }, delay);
}

function showSoundPopover() {
  if (!soundEnabled) return;
  document.getElementById("soundPopover").hidden = false;
  scheduleSoundPopoverClose();
}

function playTone({ frequency, duration = 0.06, volume = 0.018, type = "sine", delay = 0 }) {
  if (!soundEnabled) return;
  const audio = ensureAudioContext();
  const start = audio.currentTime + delay;
  const osc = audio.createOscillator();
  const gain = audio.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(frequency, start);
  const adjustedVolume = Math.max(0.0001, volume * soundVolume);
  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(adjustedVolume, start + 0.012);
  gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
  osc.connect(gain);
  gain.connect(audio.destination);
  osc.start(start);
  osc.stop(start + duration + 0.02);
}

function playDialogueBlip(index) {
  if (!soundEnabled || index - lastDialogueBlipAt < 5) return;
  const char = activeDialogueText[index - 1] || "";
  if (/\s|["'.!?]/.test(char)) return;
  lastDialogueBlipAt = index;
  playTone({ frequency: 520 + (index % 4) * 18, duration: 0.028, volume: 0.22, type: "triangle" });
}

function playChoiceSound() {
  playTone({ frequency: 330, duration: 0.06, volume: 0.32, type: "sine" });
}

function playCompletionSound() {
  playTone({ frequency: 392, duration: 0.08, volume: 0.36, type: "sine" });
  playTone({ frequency: 523.25, duration: 0.12, volume: 0.32, type: "sine", delay: 0.08 });
}

function revealDialogueText(text) {
  const panel = document.getElementById("interactionPanel");
  const textEl = document.getElementById("dialogText");
  const prompt = document.getElementById("dialogPrompt");
  const choices = document.getElementById("dialogChoices");
  window.clearTimeout(dialogueRevealTimer);
  activeDialogueText = text;
  dialogueFullyRevealed = false;
  lastDialogueBlipAt = 0;
  textEl.textContent = "";
  choices.hidden = true;
  prompt.textContent = "Tap to finish the line.";
  panel.classList.add("revealing");

  let index = 0;
  const revealNext = () => {
    index = Math.min(activeDialogueText.length, index + DIALOGUE_REVEAL.charsPerStep);
    textEl.textContent = activeDialogueText.slice(0, index);
    playDialogueBlip(index);
    if (index >= activeDialogueText.length) {
      finishDialogueReveal();
      return;
    }
    const lastChar = activeDialogueText[index - 1] || "";
    const delay = /[.!?]/.test(lastChar)
      ? DIALOGUE_REVEAL.stepMs + DIALOGUE_REVEAL.punctuationPauseMs
      : DIALOGUE_REVEAL.stepMs;
    dialogueRevealTimer = window.setTimeout(revealNext, delay);
  };
  revealNext();
}

function finishDialogueReveal() {
  window.clearTimeout(dialogueRevealTimer);
  dialogueRevealTimer = null;
  dialogueFullyRevealed = true;
  document.getElementById("dialogText").textContent = activeDialogueText;
  document.getElementById("dialogChoices").hidden = false;
  document.getElementById("dialogPrompt").textContent = "Choose what to do.";
  document.getElementById("interactionPanel").classList.remove("revealing");
}

function completeDialogueReveal() {
  if (dialogueFullyRevealed) return false;
  finishDialogueReveal();
  return true;
}

function openInteraction(object) {
  const completedQuest = completedQuestForObject(object);
  if (completedQuest) {
    openCompletedInteraction(object, completedQuest);
    return;
  }
  if (model.relationships[object.id] && object.followup) {
    openFollowupInteraction(object);
    return;
  }

  setDialogueSpeaker(object, ROLE_LABELS[object.role] || (object.type === "npc" ? "Conversation" : "Object"));
  document.getElementById("dialogChoices").innerHTML = object.choices.map((choice, index) => (
    `<button type="button" data-choice="${index}">${choice.text}</button>`
  )).join("");

  document.querySelectorAll("[data-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      if (completeDialogueReveal()) return;
      chooseOption(object, object.choices[Number(button.dataset.choice)]);
      closeInteractionPanel();
    });
  });

  openInteractionPanel();
  revealDialogueText(contextualInteractionText(object));
}

function contextualInteractionText(object) {
  const trace = model.traces || createTraceState();
  const observed = Boolean(trace.observedBeforeInteraction?.[object.id] || (trace.nearTicks?.[object.id] || 0) >= 2);
  const cameFromQuiet = trace.lastPlace === "grove" || trace.zoneEntries?.grove > 0 || model.worldFlags.fountain || model.relationships.mossycedar;
  const sampledMany = Object.keys(trace.objectInteractions || {}).length >= 4;
  const repeatedSystem = strongestRepeatedSystem(trace);

  if (object.id === "mira" && observed) {
    return "Mira notices you waiting near the ribbons before stepping closer. \"You don't have to jump into the noisy bit all at once. Could you help me mark which lanterns still need oil?\"";
  }
  if (object.id === "saff" && cameFromQuiet) {
    return "Saff sees you come from the garden path and rests one hand over the bells. \"I can make the next test softer, or more predictable, if that helps.\"";
  }
  if (object.id === "lio" && (model.relationships.tidepool || model.relationships.shell)) {
    return "Lio looks at the tide pool and the shell baskets. \"You've already noticed the small beach things. Can you help me make the lantern path easy to follow?\"";
  }
  if (object.id === "nia" && sampledMany) {
    return "Nia glances from the baskets to the tide pools. \"You've looked at half the village already. Maybe you'll spot the moon charm from a different angle.\"";
  }
  if (object.id === "oren" && repeatedSystem === "workshop") {
    return "Oren watches you return to the workshop table. \"Good, you see why this is bothering me. The display needs a shape people can understand.\"";
  }
  if (object.id === "fountain" && model.state.sensory_load >= 0.20) {
    return "The fountain is steady under the market noise. The water gives the morning a quieter rhythm.";
  }
  if (object.id === "mossycedar" && model.state.sensory_load >= 0.20) {
    return "The cedar shade is cool after the square. Footsteps soften in the moss.";
  }
  return object.text;
}

function openFollowupInteraction(object) {
  const memory = model.relationships[object.id];
  const text = object.followup[memory] || `${object.name} has settled into the new shape of the morning.`;
  setDialogueSpeaker(object, "Follow-up");
  document.getElementById("dialogChoices").innerHTML = `<button type="button" data-close-dialog="true">Continue</button>`;
  document.querySelector("[data-close-dialog]").addEventListener("click", () => {
    if (completeDialogueReveal()) return;
    storyText = text;
    showToast(storyText);
    renderHud();
    closeInteractionPanel();
  });
  openInteractionPanel();
  revealDialogueText(text);
}

function completedQuestForObject(object) {
  const quest = object.choices.find((choice) => choice.complete && model.completed[choice.complete])?.complete;
  return quest || null;
}

function openCompletedInteraction(object, questKey) {
  setDialogueSpeaker(object, "Afterward");
  document.getElementById("dialogChoices").innerHTML = `<button type="button" data-close-dialog="true">Continue</button>`;
  document.querySelector("[data-close-dialog]").addEventListener("click", () => {
    if (completeDialogueReveal()) return;
    closeInteractionPanel();
  });
  openInteractionPanel();
  revealDialogueText(completedInteractionText(object, questKey));
}

function openInteractionPanel() {
  document.body.classList.add("dialog-open");
  document.getElementById("interactionPanel").hidden = false;
}

function closeInteractionPanel() {
  window.clearTimeout(dialogueRevealTimer);
  dialogueRevealTimer = null;
  dialogueFullyRevealed = true;
  document.getElementById("interactionPanel").hidden = true;
  document.getElementById("interactionPanel").classList.remove("revealing");
  document.body.classList.remove("dialog-open");
}

function isInteractionOpen() {
  return !document.getElementById("interactionPanel").hidden;
}

function completedInteractionText(object, questKey) {
  if (object.id === "mira" && model.worldFlags.mira_low_pressure) {
    return "Mira has the lantern oil list tucked under one ribbon-weighted hand. \"I left the side route open too, in case the square gets too much.\"";
  }
  if (object.id === "lio" && model.worldFlags.lio_beach_context) {
    return "Lio points proudly at the shell path. \"The tide-pool clues made the pattern easier to read.\"";
  }
  if (object.id === "oren" && model.worldFlags.oren_return_table) {
    return "Oren keeps one side of the tide-glass table exactly as you left it. \"If you need to check the pattern again, it is still here.\"";
  }
  const messages = {
    mira: "Mira has the lantern oil list tucked under one ribbon-weighted hand. \"That helped. If you want somewhere quieter, the garden path is open.\"",
    lio: "Lio points proudly at the shell path. \"It looks like the tide decided to help us.\"",
    oren: "Oren is already labeling the finished display. \"No one has asked me which row to follow for several minutes. A triumph.\"",
  };
  return messages[object.id] || `${QUESTS[questKey]} is already done.`;
}

function chooseOption(object, choice) {
  const wasComplete = choice.complete ? Boolean(model.completed[choice.complete]) : false;
  playChoiceSound();
  const preState = { ...model.state };
  recordInteractionTrace(object, preState);
  applyDelta(model.evidence, choice.evidence);
  applyDelta(model.state, choice.state);
  recalcDerivedStateFor(model);
  if (choice.complete) model.completed[choice.complete] = true;
  rememberInteraction(object, choice);
  applyObjectConsequence(object, choice);
  storyText = resultTextFor(object, choice, wasComplete);
  if (choice.complete && !wasComplete) {
    playCompletionSound();
  }
  showToast(storyText);
  model.events.unshift({
    label: `${object.name}: ${choice.text}`,
    result: choice.result || `${object.name} changed the shape of the morning.`,
    objectId: object.id,
    quest: choice.complete || null,
    completedNow: Boolean(choice.complete && !wasComplete),
    evidence: { ...(choice.evidence || {}) },
    assessment: assessmentLensFor(object, choice),
  });
  model.events = model.events.slice(0, 18);
  renderHud();
  renderDeveloper();
}

function recordInteractionTrace(object, preState) {
  if (!model.traces) return;
  const trace = model.traces;
  const system = systemKeyFor(object);
  trace.objectInteractions[object.id] = (trace.objectInteractions[object.id] || 0) + 1;
  trace.systemInteractions[system] = (trace.systemInteractions[system] || 0) + 1;
  trace.placeInteractions[object.place] = (trace.placeInteractions[object.place] || 0) + 1;
  if (trace.observedBeforeInteraction[object.id] || (trace.nearTicks[object.id] || 0) >= 2) {
    trace.observedThenEngaged[object.id] = true;
  }
  if (object.role === "comfort" && preState.sensory_load >= 0.18) {
    trace.comfortAfterLoad += 1;
  }
  if (object.place === "grove" && preState.sensory_load >= 0.18) {
    trace.quietReturnAfterLoad += 1;
  }
  trace.lastInteractionSystem = system;
}

function recordApproachTrace(x, y) {
  if (!model.traces) return;
  const nearbyNpc = OBJECTS
    .filter((object) => object.type === "npc" && !model.relationships[object.id] && !completedQuestForObject(object))
    .map((object) => ({ object, dist: distance({ x, y }, object) }))
    .filter(({ dist }) => dist < 90)
    .sort((a, b) => a.dist - b.dist)[0]?.object;
  if (nearbyNpc) {
    model.traces.observedBeforeInteraction[nearbyNpc.id] = true;
  }
}

function systemKeyFor(object) {
  const systems = {
    mira: "social-lanterns",
    ribbonstall: "social-lanterns",
    lanternline: "social-lanterns",
    saff: "bells",
    lio: "shell-path",
    shell: "shell-path",
    tidepool: "shell-path",
    nia: "tide-pool",
    oren: "tide-glass",
    workshopwindow: "tide-glass",
    threadbasket: "tide-glass",
    fountain: "quiet-recovery",
    mossycedar: "quiet-recovery",
  };
  return systems[object.id] || object.place || object.role;
}

function assessmentLensFor(object, choice) {
  const dims = Object.entries(choice.evidence || {})
    .filter(([, value]) => value > 0)
    .sort((a, b) => b[1] - a[1])
    .map(([dim]) => dim);
  const routeSignals = [];
  const trace = model.traces || createTraceState();
  if (trace.observedBeforeInteraction?.[object.id] || trace.observedThenEngaged?.[object.id]) {
    routeSignals.push("observed-before-engagement");
  }
  if (object.role === "comfort" && model.state.sensory_load <= 0.20) {
    routeSignals.push("quiet-preference");
  }
  if (object.role === "comfort" && (trace.comfortAfterLoad || trace.quietReturnAfterLoad)) {
    routeSignals.push("recovery-after-load");
  }
  const system = systemKeyFor(object);
  if ((trace.systemInteractions?.[system] || 0) >= 2) {
    routeSignals.push("same-system-return");
  }

  return {
    gamePurpose: gamePurposeFor(object, choice),
    evidencePurpose: evidencePurposeFor(dims, routeSignals),
    dims,
    routeSignals,
  };
}

function gamePurposeFor(object, choice) {
  if (choice.complete) return `moves ${QUEST_DETAILS[choice.complete]?.title || object.name} toward the festival`;
  if (object.role === "comfort") return "lets the player regulate and decide whether to return";
  if (object.type === "npc") return `changes the relationship with ${object.name}`;
  return `changes how ${object.name.toLowerCase()} sits in the village`;
}

function evidencePurposeFor(dims, routeSignals) {
  const families = [];
  if (dims.some((dim) => ["social_prediction_uncertainty", "social_monitoring_cost", "masking_adaptation"].includes(dim)) || routeSignals.includes("observed-before-engagement")) {
    families.push("social reading and adaptation");
  }
  if (dims.some((dim) => ["sensory_accumulation", "regulation_dependency"].includes(dim)) || routeSignals.includes("recovery-after-load")) {
    families.push("sensory load and regulation");
  }
  if (dims.some((dim) => ["focused_loop_depth", "systemizing_structure", "context_switch_friction", "ambiguity_avoidance"].includes(dim)) || routeSignals.includes("same-system-return")) {
    families.push("structure, focus, and predictability");
  }
  if (dims.includes("novelty_breadth")) {
    families.push("novelty and breadth as a confound guard");
  }
  if (dims.includes("social_drive") && families.length === 0) {
    families.push("social approach as context, not ASD evidence by itself");
  }
  return families.length ? families.join("; ") : "low-signal choice retained as contrast data";
}

function auditInteractionCoverage() {
  const issues = [];
  const unexplainedTerms = ["list-keeper", "households", "old display", "strand"];
  OBJECTS.forEach((object) => {
    const userFacingStrings = [
      object.prompt,
      object.text,
      ...Object.values(object.followup || {}),
      ...object.choices.flatMap((choice) => [choice.text, choice.result]),
    ].filter(Boolean);
    userFacingStrings.forEach((text) => {
      const normalized = text.toLowerCase();
      unexplainedTerms.forEach((term) => {
        if (normalized.includes(term)) {
          issues.push(`${object.name}: unexplained term "${term}" appears in "${text}".`);
        }
      });
    });
    object.choices.forEach((choice) => {
      const dims = Object.keys(choice.evidence || {}).filter((dim) => (choice.evidence?.[dim] || 0) > 0);
      if (!dims.length && !choice.memory && !choice.complete) {
        issues.push(`${object.name}: "${choice.text}" has no evidence, memory, or completion role.`);
      }
      if (object.type !== "npc" && dims.includes("social_prediction_uncertainty")) {
        issues.push(`${object.name}: "${choice.text}" uses social prediction outside an NPC scene.`);
      }
      if (object.role === "comfort" && dims.includes("social_drive")) {
        issues.push(`${object.name}: "${choice.text}" uses social drive in a comfort scene.`);
      }
      if (choice.evidence?.novelty_breadth && choice.evidence?.focused_loop_depth && choice.evidence.novelty_breadth > choice.evidence.focused_loop_depth * 2) {
        issues.push(`${object.name}: "${choice.text}" mixes novelty and focused-loop evidence too strongly.`);
      }
      if (choice.complete && !choice.result) {
        issues.push(`${object.name}: "${choice.text}" completes a preparation without a result line.`);
      }
    });
  });
  return issues;
}

function rememberInteraction(object, choice) {
  if (choice.memory && object.followup) {
    model.relationships[object.id] = choice.memory || "met";
    model.worldFlags[`${object.id}_met`] = true;
  }
  if (object.role === "villager" && !choice.memory) {
    model.relationships[object.id] = "met";
    model.worldFlags[`${object.id}_met`] = true;
  }
  if (object.role === "comfort") {
    model.worldFlags[object.id] = "visited";
  }
}

function applyObjectConsequence(object, choice) {
  const trace = model.traces || createTraceState();
  if (object.id === "shell" && choice.memory === "kept") {
    model.pouch.shell = true;
    model.objectState.shell = "removed";
  }
  if (object.id === "threadbasket" && choice.memory === "picked") {
    model.pouch.thread = true;
  }
  if (object.id === "shell" && choice.memory === "left") {
    model.worldFlags.shell = "noticed";
  }
  if (object.id === "threadbasket") {
    model.worldFlags.threadbasket = "noticed";
  }
  if (object.id === "fountain") {
    model.worldFlags.fountain = "visited";
  }
  if (object.id === "mira" && (trace.observedBeforeInteraction.mira || trace.observedThenEngaged.mira || choice.evidence?.social_monitoring_cost)) {
    model.worldFlags.mira_low_pressure = true;
  }
  if (object.id === "saff" && (trace.zoneEntries.grove || model.worldFlags.fountain || model.relationships.mossycedar || model.state.sensory_load >= 0.18 || choice.evidence?.regulation_dependency)) {
    model.worldFlags.saff_soft_bells = true;
  }
  if (object.id === "lio" && (model.relationships.tidepool || model.relationships.shell)) {
    model.worldFlags.lio_beach_context = true;
  }
  if (object.id === "nia" && Object.keys(trace.objectInteractions || {}).length >= 4) {
    model.worldFlags.nia_wide_search = true;
  }
  if (object.id === "oren" && (trace.systemInteractions?.["tide-glass"] || 0) >= 2) {
    model.worldFlags.oren_return_table = true;
  }
  if (object.id === "oren" && choice.evidence?.novelty_breadth) {
    model.worldFlags.oren_window_sampling = true;
  }
  if (choice.complete) {
    model.relationships[object.id] = choice.complete;
  }
}

let toastTimer = null;
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.hidden = false;
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => {
    toast.hidden = true;
  }, 3600);
}

function resultTextFor(object, choice, wasComplete) {
  if (choice.complete && !wasComplete) {
    return `${choice.result || `${object.name} nods as that part of the festival comes together.`} ${nextGoalText()}`;
  }
  if (choice.result) {
    return `${choice.result} ${object.role === "quest" ? nextGoalText() : ""}`.trim();
  }
  return "The choice changes the shape of the morning. Wander toward another person, object, or quiet spot when you are ready.";
}

function nextGoalText() {
  const nextQuest = Object.keys(QUESTS).find((key) => !model.completed[key]);
  return nextQuest
    ? `${QUEST_DETAILS[nextQuest].open}`
    : "The village has settled into festival mode. You can wander, talk, rest, or finish the morning when you want.";
}

function renderHud() {
  const place = PLACES[currentPlace()];
  document.getElementById("placeName").textContent = place.name;
  document.getElementById("placeDescription").textContent = place.description;

  const completedCount = Object.keys(QUESTS).filter((key) => model.completed[key]).length;
  const controls = document.getElementById("morningControls");
  controls.hidden = !playerHasMoved && !hasPlayerHistory();
  document.getElementById("profileBtn").textContent = completedCount === 3 ? "Watch Lanterns Light" : "See Morning Path";
  document.getElementById("dayPrompt").textContent = completedCount === 3 ? "The village is ready." : "Lantern Tide is tonight.";
  document.getElementById("dayHint").textContent = completedCount === 3
    ? "The lanterns are set. You can still wander, talk, rest, or finish the morning when you want."
    : "Lanterns, bells, shells, quiet corners, and people are all part of the morning. Follow what catches your eye.";
  document.getElementById("storyLog").textContent = storyText;
  renderVillageThreads();
  const items = pouchItems();
  document.getElementById("pouchSection").hidden = items.length === 0;
  document.getElementById("pouchText").textContent = items.join(", ");
  const notes = worldNotes();
  document.getElementById("worldNotesSection").hidden = notes.length === 0;
  document.getElementById("worldNotes").innerHTML = notes.map((note) => `<li>${note}</li>`).join("");
}

function renderVillageThreads() {
  document.getElementById("villageThreads").innerHTML = VILLAGE_THREADS.map((thread) => {
    const changed = thread.quest ? Boolean(model.completed[thread.quest]) : Boolean(model.relationships[thread.id] || model.worldFlags[thread.id]);
    const note = changed ? threadTextAfterChange(thread) : thread.open;
    return `
      <li class="${changed ? "changed" : ""}">
        <div>
          <span class="thread-title">${thread.title}</span>
          <span class="thread-text">${note}</span>
        </div>
      </li>
    `;
  }).join("");
}

function threadTextAfterChange(thread) {
  if (thread.quest && model.completed[thread.quest]) return thread.changed;
  const memory = model.relationships[thread.id];
  const memoryNote = WORLD_NOTE_BY_MEMORY[`${thread.id}_${memory}`];
  if (memoryNote) return memoryNote;
  if (thread.flag && model.worldFlags[thread.flag]) return thread.changed;
  return thread.changed || thread.open;
}

function pouchItems() {
  const items = [];
  if (model.pouch.shell) items.push("Smooth shell");
  if (model.pouch.thread) items.push("Sea-green thread");
  return items;
}

function worldNotes() {
  const notes = [];
  Object.entries(model.relationships).forEach(([id, memory]) => {
    const note = WORLD_NOTE_BY_MEMORY[`${id}_${memory}`];
    if (note) notes.push(note);
  });
  Object.entries(WORLD_NOTE_BY_FLAG).forEach(([flag, note]) => {
    if (model.worldFlags[flag]) notes.push(note);
  });
  if (model.worldFlags.fountain) notes.push("The garden fountain is a known quiet spot.");
  if (model.worldFlags.shell === "noticed") notes.push("The smooth shell is still by the fountain.");
  if (model.worldFlags.threadbasket) notes.push("You noticed Oren's thread basket in the workshop.");
  if (Object.keys(QUESTS).every((key) => model.completed[key])) notes.unshift("The village is ready for Lantern Tide.");
  return notes;
}

function projectAlignment(evidence) {
  const families = profileFamilies(evidence);
  const social = clamp(families.socialReading / 0.30);
  const sensory = clamp(families.sensoryRegulation / 0.30);
  const structure = clamp(families.structureFocus / 0.28);
  const noveltyConfound = clamp(families.noveltyConfound / 0.30);
  const pureSocialDrive = clamp(Math.max(0, evidence.social_drive - families.socialReading - families.sensoryRegulation) / 0.30);
  const score = clamp(
    0.34 * social +
      0.33 * sensory +
      0.33 * structure -
      0.12 * noveltyConfound -
      0.06 * pureSocialDrive
  );
  const values = Object.values(evidence);
  const mean = values.reduce((sum, value) => sum + value, 0) / values.length;
  const spikiness = Math.max(...values) - mean;
  const conflict = Math.abs(evidence.novelty_breadth - families.structureFocus);
  const totalSignal = values.reduce((sum, value) => sum + value, 0);
  const thinEvidence = clamp(1 - totalSignal / 0.75);
  return {
    score,
    uncertainty: clamp(0.16 + 0.28 * conflict + 0.16 * spikiness + 0.10 * thinEvidence + (noveltyConfound > 0.55 ? 0.08 : 0)),
    band: classifyScore(score),
    families,
  };
}

function profileFamilies(evidence) {
  const socialReading =
    0.40 * evidence.social_prediction_uncertainty +
    0.40 * evidence.social_monitoring_cost +
    0.20 * evidence.masking_adaptation;
  const sensoryRegulation =
    0.45 * evidence.sensory_accumulation +
    0.55 * evidence.regulation_dependency;
  const structureFocus =
    0.35 * evidence.focused_loop_depth +
    0.35 * evidence.systemizing_structure +
    0.20 * evidence.ambiguity_avoidance +
    0.10 * evidence.context_switch_friction;
  const focusAnchor = Math.max(evidence.focused_loop_depth, evidence.systemizing_structure, evidence.ambiguity_avoidance);
  return {
    socialReading,
    sensoryRegulation,
    structureFocus,
    noveltyConfound: Math.max(0, evidence.novelty_breadth - 0.55 * focusAnchor),
  };
}

function classifyScore(score) {
  if (score >= 0.30) return "higher";
  if (score >= 0.18) return "mixed";
  return "lower";
}

function profileFlags(evidence, uncertainty) {
  const families = profileFamilies(evidence);
  const interest = (evidence.focused_loop_depth + evidence.systemizing_structure) / 2;
  const flags = [];
  if (families.sensoryRegulation >= 0.13) flags.push("sensory-regulation");
  if (families.socialReading >= 0.09 || evidence.masking_adaptation >= 0.08) flags.push("social-masking");
  if (interest >= 0.16 || families.structureFocus >= 0.14) flags.push("focused-interest");
  if (evidence.ambiguity_avoidance >= 0.14 || evidence.ambiguity_avoidance + evidence.regulation_dependency >= 0.26) flags.push("predictability-support");
  if (families.noveltyConfound >= 0.16) flags.push("novelty-confound");
  if (uncertainty >= 0.34) flags.push("high-uncertainty");
  return flags.length ? flags : ["low-profile-evidence"];
}

function profileBand(scoreBand, flags) {
  const coreFlags = flags.filter((flag) => !["low-profile-evidence", "novelty-confound", "high-uncertainty"].includes(flag));
  if (scoreBand === "higher" && coreFlags.length >= 2) return "higher";
  if (scoreBand === "higher" || scoreBand === "mixed" || flags.some((flag) => flag !== "low-profile-evidence")) return "mixed";
  return scoreBand;
}

function currentProfile() {
  const evidence = blendedEvidence(model.evidence, traceEvidence(model));
  const projection = projectAlignment(evidence);
  const flags = profileFlags(evidence, projection.uncertainty);
  return {
    projection,
    flags,
    band: profileBand(projection.band, flags),
    evidence,
    traceEvidence: traceEvidence(model),
    state: { ...model.state },
  };
}

function blendedEvidence(baseEvidence, routeEvidence) {
  const merged = { ...baseEvidence };
  Object.entries(routeEvidence || {}).forEach(([dim, value]) => {
    merged[dim] = clamp((merged[dim] || 0) + value);
  });
  return merged;
}

function traceEvidence(targetModel) {
  const trace = targetModel.traces;
  const deltas = Object.fromEntries(EVIDENCE_DIMS.map((dim) => [dim, 0]));
  if (!trace) return deltas;

  const observedThenEngaged = Object.keys(trace.observedThenEngaged || {}).length;
  deltas.social_prediction_uncertainty += Math.min(0.08, observedThenEngaged * 0.025);
  deltas.social_monitoring_cost += Math.min(0.10, observedThenEngaged * 0.03);

  const plazaExposure = trace.zoneTicks?.plaza || 0;
  if (plazaExposure >= 8) {
    deltas.sensory_accumulation += Math.min(0.06, (plazaExposure - 7) * 0.006);
  }

  const recoveryLoops = (trace.comfortAfterLoad || 0) + Math.min(2, trace.quietReturnAfterLoad || 0);
  deltas.regulation_dependency += Math.min(0.12, recoveryLoops * 0.04);

  const systems = Object.values(trace.systemInteractions || {});
  const maxSystemCount = systems.length ? Math.max(...systems) : 0;
  if (maxSystemCount >= 3) {
    deltas.focused_loop_depth += Math.min(0.10, (maxSystemCount - 2) * 0.04);
    deltas.context_switch_friction += Math.min(0.05, (maxSystemCount - 2) * 0.02);
  }

  const objectCount = Object.keys(trace.objectInteractions || {}).length;
  const systemCount = Object.keys(trace.systemInteractions || {}).length;
  if (objectCount >= 5 && systemCount >= 4) {
    deltas.novelty_breadth += Math.min(0.12, (objectCount - 4) * 0.025);
  }

  return Object.fromEntries(Object.entries(deltas).map(([dim, value]) => [dim, clamp(value)]));
}

function profileNarrative(profile) {
  const e = profile.evidence;
  const lines = [];
  if (e.social_drive >= 0.12) lines.push("You moved toward people and joined village activity directly.");
  if (e.social_monitoring_cost + e.social_prediction_uncertainty >= 0.10) lines.push("You paused to read the social shape of a scene before stepping in.");
  if (e.masking_adaptation >= 0.08) lines.push("Introductions and social bridges gave the morning a clear entry point.");
  if (e.regulation_dependency + e.sensory_accumulation >= 0.12) lines.push("You noticed sensory intensity and used timing, distance, or quiet places to keep going.");
  if (e.ambiguity_avoidance >= 0.05) lines.push("Clear roles, rules, and schedules made choices more concrete.");
  if (e.focused_loop_depth + e.systemizing_structure >= 0.14) lines.push("You made objects readable by sorting, refining, or following a pattern.");
  if (e.novelty_breadth >= 0.08) lines.push("You were willing to choose lively, unusual, or less structured options.");
  if (!lines.length) lines.push("This short morning did not create a strong pattern yet; a longer day would be more informative.");
  return lines.slice(0, 3);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function completedPreparationItems() {
  return Object.keys(QUEST_DETAILS)
    .filter((key) => model.completed[key])
    .map((key) => QUEST_DETAILS[key]);
}

function remainingPreparationItems() {
  return Object.keys(QUEST_DETAILS)
    .filter((key) => !model.completed[key])
    .map((key) => QUEST_DETAILS[key]);
}

function concreteChangeItems() {
  const changes = completedPreparationItems().map((quest) => quest.done);
  worldNotes()
    .filter((note) => note !== "The village is ready for Lantern Tide.")
    .forEach((note) => changes.push(note));
  if (!changes.length) changes.push("The morning is still mostly open; no lasting village changes have happened yet.");
  return [...new Set(changes)].slice(0, 8);
}

function adaptationItems() {
  const items = [];
  if (model.worldFlags.mira_low_pressure) {
    items.push("Mira adjusted the supply errand around a lower-pressure way into the square.");
  }
  if (model.worldFlags.saff_soft_bells) {
    items.push("Saff changed the bell testing so the sound had a visible pause or softer entry.");
  }
  if (model.worldFlags.lio_beach_context) {
    items.push("Lio used earlier beach observations as part of the shell-path solution.");
  }
  if (model.worldFlags.nia_wide_search) {
    items.push("Nia treated your wide route through the village as useful search information.");
  }
  if (model.worldFlags.oren_return_table) {
    items.push("Oren preserved the workshop table for a return-to-pattern route.");
  }
  if (model.worldFlags.oren_window_sampling) {
    items.push("Oren left glass near the window for a lighter, trial-and-see route.");
  }
  return items;
}

function routeMomentItems() {
  if (!model.events.length) return ["You ended the morning before choosing a village interaction."];
  return [...model.events]
    .reverse()
    .slice(-6)
    .map((event) => event.result);
}

function routeTraceItems() {
  const trace = model.traces;
  if (!trace || !hasPlayerHistory()) return ["The route is still too short to read clearly."];
  const items = [];
  const observedNames = Object.keys(trace.observedThenEngaged || {})
    .map((id) => OBJECTS.find((object) => object.id === id)?.name)
    .filter(Boolean);
  if (observedNames.length) {
    items.push(`You spent a moment near ${formatList(observedNames.slice(0, 3))} before stepping into the interaction.`);
  }
  if ((trace.comfortAfterLoad || 0) || (trace.quietReturnAfterLoad || 0)) {
    items.push("You used a quieter place or comfort spot after the busier parts of the village.");
  }
  const objectCount = Object.keys(trace.objectInteractions || {}).length;
  const systemCount = Object.keys(trace.systemInteractions || {}).length;
  if (objectCount >= 5 && systemCount >= 4) {
    items.push("You sampled several different parts of Harborwake instead of staying with one thread.");
  }
  const repeatedSystem = strongestRepeatedSystem(trace);
  if (repeatedSystem) {
    items.push(`You came back to the ${repeatedSystem} thread more than once.`);
  }
  if (!items.length) {
    items.push("Most of the signal still comes from the choices inside scenes; more wandering would make the route pattern clearer.");
  }
  return items.slice(0, 4);
}

function strongestRepeatedSystem(trace) {
  const labels = {
    "social-lanterns": "lantern",
    bells: "bell",
    "shell-path": "shell",
    "tide-pool": "tide-pool",
    "tide-glass": "workshop",
    "quiet-recovery": "quiet-place",
  };
  const [system, count] = Object.entries(trace.systemInteractions || {})
    .sort((a, b) => b[1] - a[1])[0] || [];
  if (!system || count < 3) return null;
  return labels[system] || system;
}

function playPatternItems(profile) {
  if (model.events.length < 2) {
    return ["The current signal mostly comes from the first scene and any route behavior before it."];
  }
  return profileNarrative(profile);
}

function playProfileName(profile) {
  const families = profile.projection.families;
  const e = profile.evidence;
  if (model.events.length < 2) return "Early Route";
  if (families.sensoryRegulation >= 0.13 && families.structureFocus >= 0.11) return "Quiet Pattern-Maker";
  if (families.socialReading >= 0.09 && families.sensoryRegulation >= 0.12) return "Careful Connector";
  if (families.socialReading >= 0.09) return "Social Reader";
  if (families.structureFocus >= 0.14) return "Pattern-Maker";
  if (families.sensoryRegulation >= 0.13) return "Quiet Regulator";
  if (families.noveltyConfound >= 0.16 || e.novelty_breadth >= 0.18) return "Curious Sampler";
  if (e.social_drive >= 0.20) return "Direct Helper";
  return "Open Wanderer";
}

function axisResult(profile) {
  const mean = profile.projection.score;
  const spread = clamp(profile.projection.uncertainty * 0.55, 0.08, 0.30);
  const variance = spread * spread;
  const low = clamp(mean - spread);
  const high = clamp(mean + spread);
  const label = mean >= 0.62 ? "strong" : mean >= 0.34 ? "moderate" : mean >= 0.18 ? "soft" : "low";
  return { mean, variance, low, high, label };
}

function signalDrivers(profile) {
  const families = profile.projection.families;
  const e = profile.evidence;
  const drivers = [
    ["social reading", families.socialReading],
    ["sensory regulation", families.sensoryRegulation],
    ["pattern and structure", families.structureFocus],
    ["novelty sampling", Math.max(families.noveltyConfound, e.novelty_breadth * 0.45)],
    ["direct social approach", e.social_drive * 0.45],
  ]
    .filter(([, value]) => value >= 0.03)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([label]) => label);
  return drivers.length ? drivers : ["not enough signal yet"];
}

function profileLeadText(profile, axis, drivers) {
  if (model.events.length < 2) {
    return "This was only the start of a morning, so the read is intentionally light and centered on the first visible choices.";
  }
  const style = playProfileName(profile).toLowerCase();
  return `Your route played like a ${style}: ${axisSummaryText(axis)} The strongest signals came from ${formatList(drivers)}.`;
}

function axisSummaryText(axis) {
  if (model.events.length < 2) {
    return "This was a short slice of play, so the range is intentionally wide.";
  }
  return `In this short route, the ASD-aligned play signal was ${axis.label}, with a wider range when the route mixed several styles.`;
}

function formatList(items) {
  if (items.length <= 1) return items[0] || "";
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`;
}

function renderDeveloper() {
  document.getElementById("vectorList").innerHTML = EVIDENCE_DIMS.map((dim) => {
    const value = model.evidence[dim];
    return `
      <div>
        <div class="vector-label"><span>${titleize(dim)}</span><span>${value.toFixed(2)}</span></div>
        <div class="vector-track"><div class="vector-fill" style="width:${value * 100}%"></div></div>
      </div>
    `;
  }).join("");

  document.getElementById("eventLog").innerHTML = model.events.map((event) => (
    `<li><strong>${event.label}</strong><br>${Object.entries(event.evidence).map(([dim, value]) => `${titleize(dim)} +${value.toFixed(2)}`).join(", ") || "No vector change"}<br><em>${escapeHtml(event.assessment?.evidencePurpose || "assessment lens pending")}</em></li>`
  )).join("");
}

function showProfile() {
  const profile = currentProfile();
  const axis = axisResult(profile);
  const completedCount = Object.keys(QUESTS).filter((key) => model.completed[key]).length;
  const changes = concreteChangeItems();
  const adaptations = adaptationItems();
  const moments = routeMomentItems();
  const routeShape = routeTraceItems();
  const remaining = remainingPreparationItems();
  const pattern = playPatternItems(profile);
  const name = playProfileName(profile);
  const drivers = signalDrivers(profile);
  document.getElementById("profileBody").innerHTML = `
    <section class="profile-card profile-result">
      <p class="eyebrow">Lantern Tide Summary</p>
      <h2>${escapeHtml(name)}</h2>
      <p>${escapeHtml(profileLeadText(profile, axis, drivers))}</p>
      <ul class="summary-list">${pattern.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    </section>
    <section class="profile-card axis-card">
      <div class="axis-header">
        <div>
          <p class="eyebrow">Play signal range</p>
          <h2>${axis.label.charAt(0).toUpperCase() + axis.label.slice(1)}</h2>
        </div>
        <div class="axis-stats">
          <span>Mean ${axis.mean.toFixed(2)}</span>
          <span>Variance ${axis.variance.toFixed(2)}</span>
        </div>
      </div>
      <div class="axis-track" aria-hidden="true">
        <span class="axis-range" style="left:${axis.low * 100}%; width:${Math.max(4, (axis.high - axis.low) * 100)}%"></span>
        <span class="axis-mean" style="left:${axis.mean * 100}%"></span>
      </div>
      <div class="axis-labels"><span>lower</span><span>more aligned</span></div>
      <p>This is the current ASD-aligned estimate from the play trace, shown as a range because a short route leaves uncertainty.</p>
      <p><strong>Strongest drivers:</strong> ${escapeHtml(formatList(drivers))}.</p>
      <p class="profile-note">This is a play-based reflection from this short village scene, not a diagnosis.</p>
    </section>
    <section class="profile-card">
      <h2>Morning Path</h2>
      <ul class="summary-list">${routeShape.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    </section>
    ${adaptations.length ? `
      <section class="profile-card">
        <h2>How The Village Adapted</h2>
        <ul class="summary-list">${adaptations.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
      </section>
    ` : ""}
    <section class="profile-card">
      <h2>Village Snapshot</h2>
      <p>${festivalOutcomeText(completedCount)}</p>
      <ul class="summary-list">${changes.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    </section>
    <section class="profile-card">
      <h2>Route Moments</h2>
      <ul class="summary-list">${moments.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    </section>
    ${remaining.length ? `
      <section class="profile-card">
        <h2>Still Happening</h2>
        <ul class="summary-list">${remaining.map((quest) => `<li><strong>${escapeHtml(quest.title)}</strong>: ${escapeHtml(quest.place)}</li>`).join("")}</ul>
      </section>
    ` : ""}
  `;
  document.getElementById("profileDialog").showModal();
}

function festivalOutcomeText(completedCount) {
  const completed = completedPreparationItems();
  const remaining = remainingPreparationItems();
  if (completedCount >= 3) {
    return "The lanterns are ready, the shell path catches the last light, and Oren's tide-glass display is set for sunset.";
  }
  if (completed.length) {
    const doneText = formatList(completed.map((quest) => quest.title.toLowerCase()));
    const remainingText = formatList(remaining.map((quest) => quest.title.toLowerCase()));
    return `The ${doneText} ${completed.length === 1 ? "is" : "are"} ready. The ${remainingText} ${remaining.length === 1 ? "still needs" : "still need"} help before sunset.`;
  }
  return "The village is still waking into festival mode. Mira, Lio, and Oren are still waiting for help with the lantern oil, shell path, and tide-glass display.";
}

function resetGame() {
  model = createModel();
  player = startingPlayer();
  moveTarget = null;
  pendingInteraction = null;
  actionTarget = null;
  playerHasMoved = false;
  arrivalDismissed = true;
  storyText = "The market is already moving. Lanterns sway, shells glint, bells ring, and quiet paths branch away from the square.";
  document.getElementById("toast").hidden = true;
  document.getElementById("actionButton").hidden = true;
  renderHud();
  renderDeveloper();
}

// Scenario harness, kept for tuning but hidden from the player.
const SCENARIOS = [
  {
    name: "Social Low-Cost",
    run: () => {
      const m = createModel();
      applyDelta(m.evidence, { social_drive: 0.36, sensory_accumulation: 0.09 });
      return profileFor(m);
    },
    expects: [["profile is not higher", (p) => p.band !== "higher"]],
  },
  {
    name: "Quiet Only",
    run: () => {
      const m = createModel();
      applyDelta(m.evidence, { ambiguity_avoidance: 0.10, regulation_dependency: 0.06 });
      return profileFor(m);
    },
    expects: [["profile is not higher", (p) => p.band !== "higher"]],
  },
  {
    name: "Focused Systemizing",
    run: () => {
      const m = createModel();
      applyDelta(m.evidence, { focused_loop_depth: 0.54, systemizing_structure: 0.42, context_switch_friction: 0.11 });
      return profileFor(m);
    },
    expects: [["focused-interest flag present", (p) => p.flags.includes("focused-interest")]],
  },
  {
    name: "Completionist Confound",
    run: () => {
      const m = createModel();
      applyDelta(m.evidence, { novelty_breadth: 0.55, systemizing_structure: 0.28, focused_loop_depth: 0.22 });
      return profileFor(m);
    },
    expects: [["profile is not higher", (p) => p.band !== "higher"]],
  },
];

function profileFor(targetModel) {
  const projection = projectAlignment(targetModel.evidence);
  const flags = profileFlags(targetModel.evidence, projection.uncertainty);
  return { projection, flags, band: profileBand(projection.band, flags), evidence: { ...targetModel.evidence }, state: { ...targetModel.state } };
}

function runScenarioChecks() {
  lastScenarioResults = SCENARIOS.map((scenario) => {
    const profile = scenario.run();
    const checks = scenario.expects.map(([label, predicate]) => ({ label, pass: Boolean(predicate(profile)) }));
    return { name: scenario.name, profile, checks, pass: checks.every((check) => check.pass) };
  });
  const passed = lastScenarioResults.filter((result) => result.pass).length;
  const auditIssues = auditInteractionCoverage();
  document.getElementById("automationSummary").textContent = auditIssues.length
    ? `${passed}/${lastScenarioResults.length} checks, ${auditIssues.length} audit issues`
    : `${passed}/${lastScenarioResults.length} checks passing`;
  document.getElementById("scenarioResults").innerHTML = lastScenarioResults.map((result) => `
    <article class="scenario-result ${result.pass ? "pass" : "fail"}">
      <h3>${result.name}<span>${result.pass ? "PASS" : "FAIL"}</span></h3>
      <p>${result.profile.band} profile; score ${result.profile.projection.score.toFixed(2)}, uncertainty ${result.profile.projection.uncertainty.toFixed(2)}.</p>
      <ul>${result.checks.map((check) => `<li>${check.pass ? "PASS" : "FAIL"} - ${check.label}</li>`).join("")}</ul>
    </article>
  `).join("") + (auditIssues.length ? `
    <article class="scenario-result fail">
      <h3>Interaction Audit<span>CHECK</span></h3>
      <ul>${auditIssues.map((issue) => `<li>${escapeHtml(issue)}</li>`).join("")}</ul>
    </article>
  ` : "");
}

function exportScenarioResults() {
  const auditIssues = auditInteractionCoverage();
  return JSON.stringify({
    exportedAt: new Date().toISOString(),
    auditIssues,
    results: lastScenarioResults.map((result) => ({
      name: result.name,
      pass: result.pass,
      band: result.profile.band,
      score: Number(result.profile.projection.score.toFixed(4)),
      uncertainty: Number(result.profile.projection.uncertainty.toFixed(4)),
      flags: result.profile.flags,
      checks: result.checks,
    })),
  }, null, 2);
}

function beginMapDrag(event) {
  if (!compactInputMode() || event.pointerType === "mouse" || isInteractionOpen()) return;
  mapDrag = {
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    lastX: event.clientX,
    lastY: event.clientY,
    panning: false,
  };
  canvas.setPointerCapture?.(event.pointerId);
}

function updateMapDrag(event) {
  if (!mapDrag || mapDrag.pointerId !== event.pointerId) return;
  const totalX = event.clientX - mapDrag.startX;
  const totalY = event.clientY - mapDrag.startY;
  const absX = Math.abs(totalX);
  const absY = Math.abs(totalY);

  if (!mapDrag.panning) {
    if (absY > 12 && absY > absX * 1.15) return;
    if (absX < 10 || absX < absY * 1.05) return;
    mapDrag.panning = true;
    suppressNextCanvasClick = true;
    moveTarget = null;
    pendingInteraction = null;
  }

  event.preventDefault();
  const dx = event.clientX - mapDrag.lastX;
  const dy = event.clientY - mapDrag.lastY;
  cameraLookOffset.x -= dx / camera.scale;
  cameraLookOffset.y -= dy / camera.scale;
  mapDrag.lastX = event.clientX;
  mapDrag.lastY = event.clientY;
  updateCamera();
}

function endMapDrag(event) {
  if (!mapDrag || mapDrag.pointerId !== event.pointerId) return;
  if (mapDrag.panning) {
    suppressNextCanvasClick = true;
    window.setTimeout(() => {
      suppressNextCanvasClick = false;
    }, 80);
  }
  canvas.releasePointerCapture?.(event.pointerId);
  mapDrag = null;
}

document.addEventListener("keydown", (event) => {
  const key = event.key.toLowerCase();
  if (["arrowleft", "arrowright", "arrowup", "arrowdown", "w", "a", "s", "d"].includes(key)) {
    if (!arrivalDismissed) dismissArrival();
    keys.add(key);
    event.preventDefault();
  }
  if (key === "e" && nearest && !isInteractionOpen()) {
    openInteraction(nearest);
  }
});

document.addEventListener("keyup", (event) => {
  keys.delete(event.key.toLowerCase());
});

canvas.addEventListener("pointerdown", beginMapDrag);
canvas.addEventListener("pointermove", updateMapDrag);
canvas.addEventListener("pointerup", endMapDrag);
canvas.addEventListener("pointercancel", endMapDrag);

canvas.addEventListener("click", (event) => {
  if (suppressNextCanvasClick) {
    suppressNextCanvasClick = false;
    return;
  }
  if (!arrivalDismissed) dismissArrival();
  const rect = canvas.getBoundingClientRect();
  const screenX = ((event.clientX - rect.left) / rect.width) * canvas.width;
  const screenY = ((event.clientY - rect.top) / rect.height) * canvas.height;
  const { x, y } = screenToWorld(screenX, screenY);
  const visibleObjects = OBJECTS.filter((object) => model.objectState[object.id] !== "removed");
  const clickedVisible = visibleObjects.find((object) => distance({ x, y }, object) < object.radius + tapExtraRadius());
  if (clickedVisible) {
    playerHasMoved = true;
    resetCameraLookOffset();
    renderHud();
    if (distance(player, clickedVisible) < interactionRange()) {
      openInteraction(clickedVisible);
      return;
    }
    const dist = distance(player, clickedVisible);
    const stopDistance = approachStopDistance();
    moveTarget = {
      x: clickedVisible.x - ((clickedVisible.x - player.x) / dist) * stopDistance,
      y: clickedVisible.y - ((clickedVisible.y - player.y) / dist) * stopDistance,
    };
    pendingInteraction = clickedVisible.id;
    return;
  }
  recordApproachTrace(x, y);
  moveTarget = { x, y };
  pendingInteraction = null;
  playerHasMoved = true;
  resetCameraLookOffset();
  renderHud();
});

document.getElementById("resetBtn").addEventListener("click", resetGame);
document.getElementById("beginBtn")?.addEventListener("click", dismissArrival);
document.getElementById("profileBtn").addEventListener("click", showProfile);
document.getElementById("soundToggle").addEventListener("click", () => {
  if (soundEnabled && document.getElementById("soundPopover").hidden) {
    showSoundPopover();
    return;
  }
  setSoundEnabled(!soundEnabled);
});
document.getElementById("volumeSlider").addEventListener("input", (event) => {
  setSoundVolume(event.target.value);
});
document.getElementById("volumeSlider").addEventListener("pointerdown", () => {
  window.clearTimeout(soundPopoverTimer);
});
document.getElementById("volumeSlider").addEventListener("pointerup", () => {
  scheduleSoundPopoverClose();
});
document.getElementById("soundTestBtn").addEventListener("click", () => {
  if (!soundEnabled) setSoundEnabled(true);
  scheduleSoundPopoverClose();
  playTone({ frequency: 440, duration: 0.08, volume: 0.36, type: "sine" });
  playTone({ frequency: 587.33, duration: 0.1, volume: 0.32, type: "sine", delay: 0.09 });
});
document.getElementById("actionButton").addEventListener("click", () => {
  if (!arrivalDismissed) dismissArrival();
  const target = actionTarget || nearest || (pendingInteraction && OBJECTS.find((object) => object.id === pendingInteraction));
  if (target && !isInteractionOpen()) openInteraction(target);
});
document.getElementById("interactionCloseBtn").addEventListener("click", closeInteractionPanel);
document.querySelector(".interaction-panel-inner").addEventListener("click", (event) => {
  if (event.target.closest("button")) return;
  completeDialogueReveal();
});
document.getElementById("runAllScenariosBtn").addEventListener("click", runScenarioChecks);
document.getElementById("copyResultsBtn").addEventListener("click", async () => {
  await navigator.clipboard.writeText(exportScenarioResults());
});
document.getElementById("downloadResultsBtn").addEventListener("click", () => {
  const blob = new Blob([exportScenarioResults()], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "lantern-tide-scenario-results.json";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
});

renderHud();
renderDeveloper();
runScenarioChecks();
requestAnimationFrame(step);
