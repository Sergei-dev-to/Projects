from __future__ import annotations

import argparse
import json
from pathlib import Path

from config_utils import load_config
from swarm_world import SwarmWorld


def capture_frame(world: SwarmWorld, metrics: dict[str, int | str] | None = None) -> dict[str, object]:
    atoms: list[dict[str, int]] = []
    for (x, y), atom in sorted(world.grid.items()):
        atoms.append(
            {
                "x": x,
                "y": y,
                "emission": atom.emission,
                "prediction": atom.prediction,
                "mismatch": int(atom.mismatch),
            }
        )
    frame: dict[str, object] = {
        "tick": world.tick,
        "atoms": atoms,
    }
    if metrics is not None:
        frame.update(metrics)
    return frame


def html_template(payload: dict[str, object]) -> str:
    data = json.dumps(payload, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Swarm Visualization</title>
  <style>
    :root {{
      --bg: #f4f1e8;
      --ink: #171717;
      --muted: #6a645d;
      --panel: #fffaf0;
      --line: #d9cfbe;
      --accent: #b14d21;
      --alert: #d9483b;
      --quiet: #6f7d8c;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Iowan Old Style", serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top left, #fff9ef 0, transparent 22%),
        linear-gradient(180deg, #f5efe3 0%, var(--bg) 100%);
    }}
    .wrap {{
      max-width: 1320px;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: minmax(720px, 1fr) 360px;
      gap: 20px;
    }}
    .stage, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      box-shadow: 0 12px 40px rgba(38, 27, 12, 0.08);
    }}
    .stage {{
      padding: 16px;
    }}
    .stage-header {{
      display: flex;
      justify-content: space-between;
      gap: 16px;
      align-items: end;
      margin-bottom: 12px;
    }}
    .phase-badge {{
      display: inline-flex;
      align-items: center;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1px solid rgba(0,0,0,0.08);
      background: #fff3eb;
      color: #8a3c1b;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }}
    .phase-text {{
      max-width: 520px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }}
    canvas {{
      width: 100%;
      height: auto;
      display: block;
      background:
        linear-gradient(180deg, rgba(247, 241, 229, 0.8), rgba(237, 227, 210, 0.9));
      border-radius: 14px;
      border: 1px solid #d7ccb9;
    }}
    .timeline {{
      margin-top: 12px;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.55);
    }}
    .timeline-bar {{
      position: relative;
      height: 16px;
      border-radius: 999px;
      overflow: hidden;
      background: #e9dfcf;
      border: 1px solid rgba(0,0,0,0.08);
    }}
    .timeline-segment {{
      position: absolute;
      top: 0;
      bottom: 0;
    }}
    .timeline-segment.disturbance {{
      background: rgba(177, 77, 33, 0.30);
    }}
    .timeline-segment.damage {{
      width: 4px;
      background: var(--alert);
    }}
    .timeline-marker {{
      position: absolute;
      top: -4px;
      bottom: -4px;
      width: 2px;
      background: #171717;
      box-shadow: 0 0 0 1px rgba(255,255,255,0.5);
    }}
    .timeline-labels {{
      margin-top: 8px;
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 12px;
    }}
    .controls {{
      display: grid;
      grid-template-columns: auto 1fr auto;
      gap: 12px;
      align-items: center;
      margin-top: 14px;
    }}
    button {{
      border: 0;
      border-radius: 999px;
      background: var(--accent);
      color: white;
      padding: 10px 16px;
      font: inherit;
      cursor: pointer;
    }}
    input[type="range"] {{
      width: 100%;
      accent-color: var(--accent);
    }}
    .panel {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    h1 {{
      margin: 0;
      font-size: 24px;
      line-height: 1.1;
    }}
    .kicker {{
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-size: 12px;
    }}
    dl {{
      margin: 0;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px 12px;
    }}
    dt {{
      color: var(--muted);
    }}
    dd {{
      margin: 0;
      font-variant-numeric: tabular-nums;
      font-weight: 700;
    }}
    .legend {{
      display: grid;
      gap: 8px;
    }}
    .legend-row {{
      display: grid;
      grid-template-columns: 18px 1fr;
      gap: 10px;
      align-items: center;
    }}
    .swatch {{
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 1px solid rgba(0,0,0,0.12);
    }}
    .note {{
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }}
    .note strong {{
      color: var(--ink);
    }}
    .howto {{
      display: grid;
      gap: 10px;
      padding: 12px;
      border-radius: 12px;
      background: rgba(255,255,255,0.55);
      border: 1px solid var(--line);
    }}
    .howto-item {{
      font-size: 14px;
      line-height: 1.4;
      color: var(--muted);
    }}
    .howto-item strong {{
      color: var(--ink);
    }}
    .chart {{
      width: 100%;
      height: auto;
      display: block;
      border-radius: 12px;
      border: 1px solid #d7ccb9;
      background: linear-gradient(180deg, rgba(255,255,255,0.90), rgba(244,238,227,0.95));
    }}
    @media (max-width: 980px) {{
      .wrap {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="stage">
      <div class="stage-header">
        <div>
          <div class="kicker">Lexlife</div>
          <h1>Swarm Disturbance / Trace / Repair</h1>
        </div>
        <div>
          <div id="phaseBadge" class="phase-badge">Initial</div>
          <div id="phaseText" class="phase-text"></div>
        </div>
      </div>
      <canvas id="canvas" width="880" height="520"></canvas>
      <div class="timeline">
        <div class="timeline-bar" id="timelineBar"></div>
        <div class="timeline-labels">
          <span>Baseline</span>
          <span>Disturbance window</span>
          <span>Damage pulse</span>
          <span>Recovery</span>
        </div>
      </div>
      <div class="controls">
        <button id="play">Pause</button>
        <input id="scrub" type="range" min="0" max="0" value="0">
        <span id="frameLabel">0 / 0</span>
      </div>
    </section>
    <aside class="panel">
      <div>
        <div class="kicker">How To Read</div>
          <div class="howto">
          <div class="howto-item"><strong>Each circle</strong> is one swarm atom on the grid.</div>
          <div class="howto-item"><strong>Fill color</strong> is what the atom is emitting now.</div>
          <div class="howto-item"><strong>Center dot</strong> is what the atom predicts it will observe next in its local neighborhood.</div>
          <div class="howto-item"><strong>Dark outer ring</strong> means the atom's last prediction was wrong, so it is reacting under mismatch.</div>
          <div class="howto-item"><strong>Orange region</strong> is the disturbed zone; the red flash marks the damage tick.</div>
          <div class="howto-item"><strong>The question to watch</strong>: does local structure persist after disturbance, and does it re-form after damage?</div>
        </div>
      </div>
      <dl id="stats"></dl>
      <div>
        <div class="kicker">Emission Legend</div>
        <div class="legend">
          <div class="legend-row"><span class="swatch" style="background:#6f7d8c"></span><span>Emission 0: calm / diffuse</span></div>
          <div class="legend-row"><span class="swatch" style="background:#2a7fff"></span><span>Emission 1: scout / activity</span></div>
          <div class="legend-row"><span class="swatch" style="background:#32a852"></span><span>Emission 2: cohesion</span></div>
          <div class="legend-row"><span class="swatch" style="background:#d9483b"></span><span>Emission 3: alert / repair</span></div>
        </div>
      </div>
      <div>
        <div class="kicker">Prediction Dot</div>
        <p class="note">
          The small dot inside each atom shows the atom's <strong>predicted</strong> next local structure: gray = sparse/broken, blue = mixed, green = coherent, red = disturbed. A dark outer ring means its last prediction was wrong.
        </p>
      </div>
      <div>
        <div class="kicker">Time Series</div>
        <canvas id="trend" class="chart" width="320" height="180"></canvas>
      </div>
      <p class="note">
        Watch three things first: <strong>population inside the region</strong>, <strong>largest cluster size</strong>, and whether structure remains after the orange fill disappears and after the red damage pulse.
      </p>
    </aside>
  </div>
  <script>
    const DATA = {data};
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");
    const trend = document.getElementById("trend");
    const trendCtx = trend.getContext("2d");
    const scrub = document.getElementById("scrub");
    const playButton = document.getElementById("play");
    const frameLabel = document.getElementById("frameLabel");
    const stats = document.getElementById("stats");
    const phaseBadge = document.getElementById("phaseBadge");
    const phaseText = document.getElementById("phaseText");
    const timelineBar = document.getElementById("timelineBar");

    const colors = ["#6f7d8c", "#2a7fff", "#32a852", "#d9483b"];
    const frames = DATA.frames;
    const cell = 34;
    const padding = 34;
    const radius = 10;
    let index = 0;
    let playing = true;
    let timer = null;
    const phaseDescriptions = {{
      initial: "Initial random swarm placement before any external event.",
      baseline: "No disturbance is active. Watch whether the swarm drifts, clusters, or holds residual structure.",
      disturbance: "The orange zone is actively perturbing local observations. Watch whether atoms gather or change mode nearby.",
      damage: "A damage pulse removes part of the structure inside the region. Watch whether surrounding atoms move back in.",
      recovery: "The disturbance is gone. The question is whether the swarm keeps a trace and repairs damaged local structure."
    }};

    scrub.max = String(frames.length - 1);

    function percentAtTick(tick) {{
      if (DATA.max_tick <= 0) {{
        return 0;
      }}
      return (tick / DATA.max_tick) * 100;
    }}

    function buildTimeline() {{
      const disturbance = document.createElement("div");
      disturbance.className = "timeline-segment disturbance";
      disturbance.style.left = `${{percentAtTick(DATA.disturbance_start)}}%`;
      disturbance.style.width = `${{percentAtTick(DATA.disturbance_end - DATA.disturbance_start + 1)}}%`;
      timelineBar.appendChild(disturbance);

      const damage = document.createElement("div");
      damage.className = "timeline-segment damage";
      damage.style.left = `${{percentAtTick(DATA.damage_step)}}%`;
      timelineBar.appendChild(damage);

      const marker = document.createElement("div");
      marker.className = "timeline-marker";
      marker.id = "timelineMarker";
      timelineBar.appendChild(marker);
    }}

    function drawRegion(frame) {{
      const cx = padding + DATA.region_center_x * cell + cell / 2;
      const cy = padding + DATA.region_center_y * cell + cell / 2;
      const outer = DATA.region_radius * cell;
      ctx.save();
      ctx.beginPath();
      ctx.strokeStyle = "#b14d21";
      ctx.lineWidth = 2;
      ctx.arc(cx, cy, outer, 0, Math.PI * 2);
      ctx.stroke();
      if (frame.phase === "disturbance") {{
        ctx.fillStyle = "rgba(177, 77, 33, 0.10)";
        ctx.fill();
      }}
      if (frame.phase === "damage") {{
        ctx.beginPath();
        ctx.strokeStyle = "#d9483b";
        ctx.lineWidth = 6;
        ctx.arc(cx, cy, outer + 6, 0, Math.PI * 2);
        ctx.stroke();
      }}
      ctx.fillStyle = "#8a3c1b";
      ctx.font = "13px Georgia, serif";
      ctx.fillText("region of interest", cx - 48, cy - outer - 12);
      ctx.restore();
    }}

    function drawGrid() {{
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#efe6d6";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = "rgba(93, 74, 52, 0.10)";
      for (let x = 0; x <= DATA.width; x += 1) {{
        const px = padding + x * cell;
        ctx.beginPath();
        ctx.moveTo(px, padding);
        ctx.lineTo(px, padding + DATA.height * cell);
        ctx.stroke();
      }}
      for (let y = 0; y <= DATA.height; y += 1) {{
        const py = padding + y * cell;
        ctx.beginPath();
        ctx.moveTo(padding, py);
        ctx.lineTo(padding + DATA.width * cell, py);
        ctx.stroke();
      }}
    }}

    function drawAtoms(frame) {{
      for (const atom of frame.atoms) {{
        const x = padding + atom.x * cell + cell / 2;
        const y = padding + atom.y * cell + cell / 2;
        ctx.beginPath();
          ctx.fillStyle = colors[atom.emission] || "#111";
          ctx.arc(x, y, radius, 0, Math.PI * 2);
          ctx.fill();
          ctx.strokeStyle = atom.mismatch ? "rgba(23,23,23,0.78)" : "rgba(0,0,0,0.12)";
          ctx.lineWidth = atom.mismatch ? 2.4 : 1;
          ctx.stroke();
          ctx.beginPath();
          ctx.fillStyle = colors[atom.prediction] || "#111";
          ctx.arc(x, y, 3.5, 0, Math.PI * 2);
          ctx.fill();
      }}
    }}

    function updateStats(frame) {{
      const rows = [
        ["Tick", frame.tick],
        ["Phase", frame.phase],
        ["Population", frame.population],
        ["Largest Cluster", frame.largest_cluster],
        ["Components", frame.component_count],
        ["In Region", frame.in_region_population],
        ["Out Region", frame.out_region_population],
        ["Prediction Match", frame.matching_predictions],
        ["Prediction Mismatch", frame.mismatching_atoms],
        ["Disturbance Contacts", frame.disturbance_contacts],
      ];
      stats.innerHTML = rows.map(([k, v]) => `<dt>${{k}}</dt><dd>${{v}}</dd>`).join("");
      phaseBadge.textContent = frame.phase;
      phaseText.textContent = phaseDescriptions[frame.phase] || "";
      document.getElementById("timelineMarker").style.left = `${{percentAtTick(frame.tick)}}%`;
    }}

    function drawTrend() {{
      const width = trend.width;
      const height = trend.height;
      const chartPad = {{ left: 34, right: 10, top: 14, bottom: 26 }};
      const innerWidth = width - chartPad.left - chartPad.right;
      const innerHeight = height - chartPad.top - chartPad.bottom;
      const maxY = Math.max(
        1,
        ...frames.map((frame) => Math.max(frame.population, frame.in_region_population, frame.largest_cluster))
      );

      trendCtx.clearRect(0, 0, width, height);
      trendCtx.fillStyle = "#fbf8f0";
      trendCtx.fillRect(0, 0, width, height);
      trendCtx.strokeStyle = "rgba(0,0,0,0.10)";
      for (let i = 0; i <= 4; i += 1) {{
        const y = chartPad.top + (i / 4) * innerHeight;
        trendCtx.beginPath();
        trendCtx.moveTo(chartPad.left, y);
        trendCtx.lineTo(width - chartPad.right, y);
        trendCtx.stroke();
      }}

      function pointX(frameIndex) {{
        if (frames.length <= 1) {{
          return chartPad.left;
        }}
        return chartPad.left + (frameIndex / (frames.length - 1)) * innerWidth;
      }}

      function pointY(value) {{
        return chartPad.top + innerHeight - (value / maxY) * innerHeight;
      }}

      function drawSeries(key, color) {{
        trendCtx.beginPath();
        trendCtx.strokeStyle = color;
        trendCtx.lineWidth = 2;
        frames.forEach((frame, frameIndex) => {{
          const x = pointX(frameIndex);
          const y = pointY(frame[key]);
          if (frameIndex === 0) {{
            trendCtx.moveTo(x, y);
          }} else {{
            trendCtx.lineTo(x, y);
          }}
        }});
        trendCtx.stroke();
      }}

      drawSeries("population", "#5e6b77");
      drawSeries("largest_cluster", "#2a7fff");
      drawSeries("in_region_population", "#b14d21");

      trendCtx.fillStyle = "#6a645d";
      trendCtx.font = "12px Georgia, serif";
      trendCtx.fillText("0", 12, chartPad.top + innerHeight + 4);
      trendCtx.fillText(String(maxY), 6, chartPad.top + 8);
      trendCtx.fillText("t", width - 16, height - 8);

      const markerX = pointX(index);
      trendCtx.beginPath();
      trendCtx.strokeStyle = "rgba(23,23,23,0.8)";
      trendCtx.lineWidth = 1.5;
      trendCtx.moveTo(markerX, chartPad.top);
      trendCtx.lineTo(markerX, chartPad.top + innerHeight);
      trendCtx.stroke();

      trendCtx.fillStyle = "#171717";
      trendCtx.font = "11px Georgia, serif";
      trendCtx.fillText("gray population", chartPad.left, height - 8);
      trendCtx.fillText("blue largest cluster", chartPad.left + 96, height - 8);
      trendCtx.fillText("orange in-region", chartPad.left + 220, height - 8);
    }}

    function renderFrame(i) {{
      index = i;
      const frame = frames[index];
      drawGrid();
      drawRegion(frame);
      drawAtoms(frame);
      updateStats(frame);
      drawTrend();
      scrub.value = String(index);
      frameLabel.textContent = `${{index + 1}} / ${{frames.length}}`;
    }}

    function step() {{
      renderFrame((index + 1) % frames.length);
    }}

    function setPlaying(next) {{
      playing = next;
      playButton.textContent = playing ? "Pause" : "Play";
      if (timer) {{
        clearInterval(timer);
        timer = null;
      }}
      if (playing) {{
        timer = setInterval(step, DATA.frame_delay_ms);
      }}
    }}

    playButton.addEventListener("click", () => setPlaying(!playing));
    scrub.addEventListener("input", (event) => {{
      setPlaying(false);
      renderFrame(Number(event.target.value));
    }});

    buildTimeline();
    renderFrame(0);
    setPlaying(true);
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the swarm experiment as a self-contained HTML animation.")
    parser.add_argument("--config", type=Path, default=Path("swarm_config.yaml"))
    parser.add_argument("--output", type=Path, default=Path("swarm_viz.html"))
    parser.add_argument("--frame-delay-ms", type=int, default=350)
    args = parser.parse_args()

    config = load_config(args.config)
    world = SwarmWorld(config)
    world.seed_initial_population()

    frames: list[dict[str, object]] = [
        capture_frame(
            world,
            {
                "phase": "initial",
                "population": len(world.grid),
                "largest_cluster": world.largest_cluster(),
                "component_count": len(world.connected_components()),
                "in_region_population": world.region_populations()[0],
                "out_region_population": world.region_populations()[1],
                "matching_predictions": 0,
                "mismatching_atoms": 0,
                "disturbance_contacts": 0,
            },
        )
    ]

    for _ in range(int(config["steps"])):
        metrics = world.step()
        frames.append(
            capture_frame(
                world,
                {
                    "phase": metrics.phase,
                    "population": metrics.population,
                    "largest_cluster": metrics.largest_cluster,
                    "component_count": metrics.component_count,
                    "in_region_population": metrics.in_region_population,
                    "out_region_population": metrics.out_region_population,
                    "matching_predictions": metrics.matching_predictions,
                    "mismatching_atoms": metrics.mismatching_atoms,
                    "disturbance_contacts": metrics.disturbance_contacts,
                },
            )
        )

    payload = {
        "width": world.width,
        "height": world.height,
        "region_center_x": world.region_center[0],
        "region_center_y": world.region_center[1],
        "region_radius": world.region_radius,
        "disturbance_start": world.disturbance_start,
        "disturbance_end": world.disturbance_end,
        "damage_step": world.damage_step,
        "max_tick": int(config["steps"]),
        "frame_delay_ms": args.frame_delay_ms,
        "frames": frames,
    }
    args.output.write_text(html_template(payload), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
