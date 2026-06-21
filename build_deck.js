const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaLayerGroup, FaLaptopCode, FaShieldHalved, FaBrain, FaChartLine,
  FaGraduationCap, FaRoute, FaBriefcase, FaCubesStacked, FaCompass, FaArrowRightLong
} = require("react-icons/fa6");

// ---------- palette ----------
const INK = "0F172A";        // slate-900 (dark bg / primary text)
const INK2 = "1E293B";       // slate-800
const MUTED = "64748B";      // slate-500
const LIGHT = "F1F5F9";      // slate-100
const WHITE = "FFFFFF";
const LINE = "E2E8F0";

const TRACKS = [
  { key: "SE",  name: "Software Engineering",
    color: "2563EB", soft: "DBEAFE", icon: FaLaptopCode,
    tag: "Build and operate the systems the world runs on",
    roles: ["Full-Stack Software Developer", "DevOps Engineer", "QA Engineer"],
    core: [
      ["Cloud Computing & Cloud-Native Platforms", "SE1"],
      ["Secure & Reliable Software Development", "SE2"],
      ["LLM & Agentic Systems", "AI1"],
      ["Modern Front-End Web Development", "SE3"],
    ],
    adv: [
      ["Back-End Web Development & APIs", "SE4"],
      ["Engineering & Ops of AI Systems (DevOps/MLOps)", "SE5"],
      ["Mobile, IoT & Edge Software Development", "SE6"],
      ["Design of AI-based & Data-Intensive Systems", "SE7"],
    ] },
  { key: "CY",  name: "Networking & Cyber Security",
    color: "DC2626", soft: "FEE2E2", icon: FaShieldHalved,
    tag: "Defend networks, data, and infrastructure end to end",
    roles: ["Network Engineer", "DevSecOps Engineer", "Security Analyst"],
    core: [
      ["Cloud Computing & Cloud-Native Platforms", "SE1"],
      ["Secure & Reliable Software Development", "SE2"],
      ["LLM & Agentic Systems", "AI1"],
      ["Applied Cryptography", "CY1"],
    ],
    adv: [
      ["Engineering & Ops of AI Systems", "SE5"],
      ["Hardware & Embedded Systems Security", "CY3"],
      ["Security Governance, Risk & Compliance", "CY4"],
      ["Blockchain & Decentralized Systems", "CY5"],
    ] },
  { key: "AI",  name: "Artificial Intelligence",
    color: "7C3AED", soft: "EDE9FE", icon: FaBrain,
    tag: "Design intelligent systems that perceive, reason, and act",
    roles: ["ML / AI Engineer", "MLOps Engineer", "Applied Scientist"],
    core: [
      ["LLM & Agentic Systems", "AI1"],
      ["Temporal AI: Time Series & Decisions", "AI2"],
      ["Vision AI: Deep Learning for Vision", "AI3"],
      ["Scalable AI: Big-Data Algorithms", "AI4"],
    ],
    adv: [
      ["Engineering & Ops of AI Systems (MLOps/LLMOps)", "SE5"],
      ["Design of AI-based & Data-Intensive Systems", "SE7"],
      ["Generative AI: Deep Generative Models", "AI5"],
      ["Embodied AI: Robotics & Autonomous Systems", "AI6"],
    ] },
  { key: "QCF", name: "Comp. Finance, Optimization & Quantum",
    color: "D97706", soft: "FEF3C7", icon: FaChartLine,
    tag: "Quantitative modeling, optimization, and quantum algorithms",
    roles: ["Financial Software Engineer", "Algo-Trading Developer", "Quant Analyst"],
    core: [
      ["Cloud Computing & Cloud-Native Platforms", "SE1"],
      ["LLM & Agentic Systems", "AI1"],
      ["Applied Cryptography", "CY1"],
      ["Temporal AI: Time Series & Decisions", "AI2"],
    ],
    adv: [
      ["Design of AI-based & Data-Intensive Systems", "SE7"],
      ["Blockchain & Decentralized Systems", "CY5"],
      ["Quantum Optimization", "QCF1"],
      ["AI & Optimization for Finance", "QCF2"],
    ] },
];

async function iconPng(IconComponent, color, size = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

(async () => {
  const P = new pptxgen();
  P.defineLayout({ name: "W", width: 13.333, height: 7.5 });
  P.layout = "W";
  P.author = "CS Program Committee";
  P.title = "CS Degree Concentrations";
  const W = 13.333, H = 7.5;

  // pre-render icons
  const ic = {};
  for (const t of TRACKS) ic[t.key] = await iconPng(t.icon, "#" + t.color, 256);
  ic.WHITE = {};
  for (const t of TRACKS) ic[t.key + "_w"] = await iconPng(t.icon, "#FFFFFF", 256);
  const icLayer  = await iconPng(FaLayerGroup, "#FFFFFF", 256);
  const icCubes  = await iconPng(FaCubesStacked, "#" + INK, 256);
  const icGrad   = await iconPng(FaGraduationCap, "#" + INK, 256);
  const icRoute  = await iconPng(FaRoute, "#" + INK, 256);
  const icComp   = await iconPng(FaCompass, "#FFFFFF", 256);
  const icArrow  = {};
  for (const t of TRACKS) icArrow[t.key] = await iconPng(FaArrowRightLong, "#" + t.color, 256);
  const sh = () => ({ type: "outer", color: "0F172A", blur: 9, offset: 3, angle: 90, opacity: 0.12 });

  // dots motif helper
  function dots(slide, x, y, r = 0.11, gap = 0.34) {
    TRACKS.forEach((t, i) =>
      slide.addShape(P.shapes.OVAL, { x: x + i * gap, y, w: r, h: r, fill: { color: t.color } }));
  }

  // ============ SLIDE 1 — TITLE ============
  let s = P.addSlide();
  s.background = { color: INK };
  // faint side band of track colors
  TRACKS.forEach((t, i) =>
    s.addShape(P.shapes.RECTANGLE, { x: 0, y: i * (H / 4), w: 0.16, h: H / 4, fill: { color: t.color } }));
  s.addImage({ data: icLayer, x: 0.9, y: 1.15, w: 0.62, h: 0.62 });
  s.addText("UNDERGRADUATE CS PROGRAM", { x: 1.65, y: 1.18, w: 9, h: 0.5, fontFace: "Consolas", fontSize: 14, color: "94A3B8", charSpacing: 3, valign: "middle" });
  s.addText("Degree Concentrations", { x: 0.85, y: 1.95, w: 11.6, h: 1.3, fontFace: "Georgia", fontSize: 60, bold: true, color: WHITE });
  s.addText("Four specialization tracks students choose in their third year — each a focused path of core and advanced courses built on a shared CS backbone.",
    { x: 0.9, y: 3.35, w: 9.6, h: 1.0, fontFace: "Calibri", fontSize: 19, color: "CBD5E1", lineSpacingMultiple: 1.15 });

  // four mini chips
  const cw = 2.85, cg = 0.18, cx0 = 0.9, cyc = 4.75;
  TRACKS.forEach((t, i) => {
    const x = cx0 + i * (cw + cg);
    s.addShape(P.shapes.ROUNDED_RECTANGLE, { x, y: cyc, w: cw, h: 1.55, fill: { color: INK2 }, line: { color: t.color, width: 1.25 }, rectRadius: 0.08 });
    s.addImage({ data: ic[t.key + "_w"], x: x + 0.22, y: cyc + 0.24, w: 0.42, h: 0.42 });
    s.addShape(P.shapes.RECTANGLE, { x: x + 0.22, y: cyc + 0.8, w: 0.5, h: 0.045, fill: { color: t.color } });
    s.addText(t.name, { x: x + 0.18, y: cyc + 0.88, w: cw - 0.36, h: 0.6, fontFace: "Calibri", fontSize: 12.5, bold: true, color: WHITE, valign: "top", lineSpacingMultiple: 0.95 });
  });
  s.addText("New CS Program Plan  ·  Third-Year Specialization", { x: 0.9, y: 6.7, w: 11.5, h: 0.4, fontFace: "Consolas", fontSize: 12, color: "64748B" });

  // ============ SLIDE 2 — HOW IT WORKS ============
  s = P.addSlide();
  s.background = { color: WHITE };
  s.addText("How Concentrations Work", { x: 0.7, y: 0.5, w: 11, h: 0.7, fontFace: "Georgia", fontSize: 34, bold: true, color: INK });
  s.addText("Every student shares a common CS foundation, then specializes by completing one concentration: four core courses plus four advanced courses, rounded out with electives drawn from the shared catalog.",
    { x: 0.72, y: 1.28, w: 11.6, h: 0.8, fontFace: "Calibri", fontSize: 16, color: MUTED, lineSpacingMultiple: 1.1 });

  // stat callouts
  const stats = [
    [icRoute, "4", "Concentration tracks"],
    [icCubes, "8", "Designated courses each (4 core + 4 advanced)"],
    [icGrad, "20", "Courses in the shared catalog"],
  ];
  const stw = 3.85, stg = 0.3, stx0 = 0.72, sty = 2.35;
  stats.forEach((st, i) => {
    const x = stx0 + i * (stw + stg);
    s.addShape(P.shapes.ROUNDED_RECTANGLE, { x, y: sty, w: stw, h: 1.9, fill: { color: LIGHT }, rectRadius: 0.08, shadow: sh() });
    s.addImage({ data: st[0], x: x + 0.3, y: sty + 0.32, w: 0.5, h: 0.5 });
    s.addText(st[1], { x: x + 1.0, y: sty + 0.18, w: stw - 1.1, h: 0.9, fontFace: "Georgia", fontSize: 44, bold: true, color: INK, valign: "middle" });
    s.addText(st[2], { x: x + 0.32, y: sty + 1.12, w: stw - 0.6, h: 0.65, fontFace: "Calibri", fontSize: 13.5, color: INK2, valign: "top", lineSpacingMultiple: 0.95 });
  });

  // pathway strip
  const py = 4.75;
  s.addText("YOUR PATH THROUGH THE DEGREE", { x: 0.72, y: py, w: 8, h: 0.35, fontFace: "Consolas", fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
  const steps = [
    ["Years 1–2", "Shared CS core", "92A0B0"],
    ["Year 3", "Choose 1 concentration", "0F172A"],
    ["Core (A1–A4)", "Four foundation courses", "334155"],
    ["Advanced (B1–B4)", "Four depth courses + electives", "475569"],
  ];
  const pw = 2.85, pg = 0.32, px0 = 0.72, pby = py + 0.45;
  steps.forEach((st, i) => {
    const x = px0 + i * (pw + pg);
    s.addShape(P.shapes.ROUNDED_RECTANGLE, { x, y: pby, w: pw, h: 1.55, fill: { color: i === 1 ? INK : WHITE }, line: { color: i === 1 ? INK : LINE, width: 1.25 }, rectRadius: 0.07 });
    s.addText(st[0], { x: x + 0.22, y: pby + 0.22, w: pw - 0.4, h: 0.4, fontFace: "Consolas", fontSize: 12.5, bold: true, color: i === 1 ? "FFFFFF" : st[2] });
    s.addText(st[1], { x: x + 0.22, y: pby + 0.66, w: pw - 0.44, h: 0.8, fontFace: "Calibri", fontSize: 15, bold: true, color: i === 1 ? "FFFFFF" : INK, valign: "top", lineSpacingMultiple: 0.95 });
    if (i < steps.length - 1)
      s.addImage({ data: icArrow.AI, x: x + pw + (pg - 0.26) / 2, y: pby + 0.62, w: 0.26, h: 0.26 });
  });

  // ============ SLIDE 3 — FOUR CONCENTRATIONS AT A GLANCE ============
  s = P.addSlide();
  s.background = { color: WHITE };
  s.addText("The Four Concentrations", { x: 0.7, y: 0.45, w: 11, h: 0.7, fontFace: "Georgia", fontSize: 34, bold: true, color: INK });
  s.addText("Each track leads to a distinct family of careers.", { x: 0.72, y: 1.2, w: 11, h: 0.4, fontFace: "Calibri", fontSize: 16, color: MUTED });

  const gw = 5.95, gh = 2.42, gx0 = 0.72, gy0 = 1.85, gxg = 0.35, gyg = 0.3;
  TRACKS.forEach((t, i) => {
    const x = gx0 + (i % 2) * (gw + gxg);
    const y = gy0 + Math.floor(i / 2) * (gh + gyg);
    s.addShape(P.shapes.ROUNDED_RECTANGLE, { x, y, w: gw, h: gh, fill: { color: WHITE }, line: { color: LINE, width: 1 }, rectRadius: 0.06, shadow: sh() });
    s.addShape(P.shapes.RECTANGLE, { x, y, w: 0.13, h: gh, fill: { color: t.color } });
    s.addShape(P.shapes.OVAL, { x: x + 0.34, y: y + 0.32, w: 0.78, h: 0.78, fill: { color: t.soft } });
    s.addImage({ data: ic[t.key], x: x + 0.52, y: y + 0.5, w: 0.42, h: 0.42 });
    s.addText(t.name, { x: x + 1.28, y: y + 0.32, w: gw - 1.5, h: 0.78, fontFace: "Calibri", fontSize: 18.5, bold: true, color: INK, valign: "middle", lineSpacingMultiple: 0.95 });
    s.addText(t.tag, { x: x + 0.36, y: y + 1.2, w: gw - 0.65, h: 0.5, fontFace: "Calibri", fontSize: 13, italic: true, color: MUTED, valign: "top", lineSpacingMultiple: 0.95 });
    // role chips
    let rx = x + 0.36;
    const ry = y + 1.78;
    t.roles.slice(0, 2).forEach((r) => {
      const rwid = 0.16 + r.length * 0.082;
      s.addShape(P.shapes.ROUNDED_RECTANGLE, { x: rx, y: ry, w: rwid, h: 0.42, fill: { color: t.soft }, rectRadius: 0.06 });
      s.addText(r, { x: rx, y: ry, w: rwid, h: 0.42, fontFace: "Calibri", fontSize: 10.5, color: t.color, bold: true, align: "center", valign: "middle", margin: 1 });
      rx += rwid + 0.14;
    });
  });

  // ============ SLIDES 4-7 — PER CONCENTRATION ============
  for (const t of TRACKS) {
    s = P.addSlide();
    s.background = { color: WHITE };
    // left colored panel
    const lw = 4.4;
    s.addShape(P.shapes.RECTANGLE, { x: 0, y: 0, w: lw, h: H, fill: { color: t.color } });
    s.addShape(P.shapes.RECTANGLE, { x: 0, y: 0, w: lw, h: H, fill: { color: INK, transparency: 78 } });
    s.addShape(P.shapes.OVAL, { x: 0.6, y: 0.7, w: 1.15, h: 1.15, fill: { color: WHITE, transparency: 86 } });
    s.addImage({ data: ic[t.key + "_w"], x: 0.87, y: 0.97, w: 0.6, h: 0.6 });
    s.addText("CONCENTRATION", { x: 0.62, y: 2.1, w: lw - 1, h: 0.35, fontFace: "Consolas", fontSize: 12, color: "FFFFFF", charSpacing: 3 });
    s.addText(t.name, { x: 0.58, y: 2.45, w: lw - 0.8, h: 1.75, fontFace: "Georgia", fontSize: 26, bold: true, color: WHITE, valign: "top", lineSpacingMultiple: 0.98 });
    s.addText(t.tag, { x: 0.62, y: 4.35, w: lw - 0.95, h: 0.9, fontFace: "Calibri", fontSize: 15, italic: true, color: "F1F5F9", valign: "top", lineSpacingMultiple: 1.05 });
    // career roles block
    s.addText("CAREER ROLES", { x: 0.62, y: 5.35, w: lw - 1, h: 0.3, fontFace: "Consolas", fontSize: 11, color: "E2E8F0", charSpacing: 2 });
    s.addText(t.roles.map((r, i) => ({ text: r, options: { bullet: { code: "2022" }, breakLine: true, color: "FFFFFF" } })),
      { x: 0.66, y: 5.68, w: lw - 1.0, h: 1.4, fontFace: "Calibri", fontSize: 14, color: "FFFFFF", paraSpaceAfter: 6 });

    // right: course columns
    const rx0 = lw + 0.55;
    s.addText("Designated Courses", { x: rx0, y: 0.62, w: 7.8, h: 0.5, fontFace: "Georgia", fontSize: 26, bold: true, color: INK });
    s.addText("Eight courses define this track; remaining catalog courses count as electives.",
      { x: rx0, y: 1.22, w: 7.9, h: 0.4, fontFace: "Calibri", fontSize: 13.5, color: MUTED });

    const sections = [["CORE FOUNDATION", "A1 – A4", t.core], ["ADVANCED DEPTH", "B1 – B4", t.adv]];
    let cy = 1.85;
    sections.forEach((sec, si) => {
      s.addShape(P.shapes.OVAL, { x: rx0, y: cy + 0.02, w: 0.28, h: 0.28, fill: { color: t.color } });
      s.addText(si === 0 ? "A" : "B", { x: rx0, y: cy + 0.02, w: 0.28, h: 0.28, align: "center", valign: "middle", fontFace: "Consolas", fontSize: 13, bold: true, color: WHITE, margin: 0 });
      s.addText(sec[0], { x: rx0 + 0.4, y: cy, w: 4.5, h: 0.32, fontFace: "Consolas", fontSize: 13, bold: true, color: INK, charSpacing: 1.5, valign: "middle" });
      s.addText(sec[1], { x: rx0 + 5.0, y: cy, w: 2.85, h: 0.32, fontFace: "Consolas", fontSize: 12, color: MUTED, align: "right", valign: "middle" });
      cy += 0.46;
      sec[2].forEach((c, ci) => {
        const ry = cy + ci * 0.5;
        s.addShape(P.shapes.ROUNDED_RECTANGLE, { x: rx0, y: ry, w: 7.85, h: 0.46, fill: { color: si === 0 ? t.soft : LIGHT }, rectRadius: 0.05 });
        s.addShape(P.shapes.RECTANGLE, { x: rx0, y: ry, w: 0.07, h: 0.46, fill: { color: t.color } });
        s.addText(`${si === 0 ? "A" : "B"}${ci + 1}`, { x: rx0 + 0.18, y: ry, w: 0.55, h: 0.46, fontFace: "Consolas", fontSize: 12.5, bold: true, color: t.color, valign: "middle", margin: 0 });
        s.addText(c[0], { x: rx0 + 0.78, y: ry, w: 6.1, h: 0.46, fontFace: "Calibri", fontSize: 13, color: INK2, valign: "middle", margin: 0 });
        s.addText(c[1], { x: rx0 + 6.9, y: ry, w: 0.9, h: 0.46, fontFace: "Consolas", fontSize: 11, color: MUTED, align: "right", valign: "middle", margin: 0 });
      });
      cy += sec[2].length * 0.5 + 0.22;
    });
  }

  // ============ SLIDE 8 — COURSE MAP MATRIX ============
  s = P.addSlide();
  s.background = { color: WHITE };
  s.addText("Shared Course Catalog & Track Map", { x: 0.55, y: 0.4, w: 12, h: 0.6, fontFace: "Georgia", fontSize: 30, bold: true, color: INK });
  s.addText("One catalog feeds every concentration. A cell shows the role a course plays in each track: a core (A) or advanced (B) requirement, or an elective.",
    { x: 0.57, y: 1.04, w: 12.2, h: 0.45, fontFace: "Calibri", fontSize: 13.5, color: MUTED });

  // legend
  const leg = [["Core requirement (A)", null], ["Advanced requirement (B)", null], ["Elective", null]];
  let lx = 0.57;
  const lgy = 1.6;
  [["A · Core", "0F172A", WHITE], ["B · Advanced", "94A3B8", INK], ["· Elective", LIGHT, MUTED]].forEach((lg) => {
    s.addShape(P.shapes.ROUNDED_RECTANGLE, { x: lx, y: lgy, w: 1.9, h: 0.34, fill: { color: lg[1] }, line: { color: LINE, width: 0.75 }, rectRadius: 0.04 });
    s.addText(lg[0], { x: lx, y: lgy, w: 1.9, h: 0.34, align: "center", valign: "middle", fontFace: "Consolas", fontSize: 11, bold: true, color: lg[2], margin: 0 });
    lx += 2.05;
  });

  // full catalog with per-track role; [id, title, {SE,CY,AI,QCF}]
  const cat = [
    ["SE1", "Cloud Computing & Cloud-Native Platforms", "A","A","·","A"],
    ["SE2", "Secure & Reliable Software Development", "A","A","·","·"],
    ["SE3", "Modern Front-End Web Development", "A","·","·","·"],
    ["SE4", "Back-End Web Development & APIs", "B","·","·","·"],
    ["SE5", "Engineering & Ops of AI Systems (DevOps/MLOps)", "B","B","B","·"],
    ["SE6", "Mobile, IoT & Edge Software Development", "B","·","·","·"],
    ["SE7", "Design of AI-based & Data-Intensive Systems", "B","·","B","B"],
    ["CY1", "Applied Cryptography", "·","A","·","A"],
    ["CY2", "Network & Communication Security", "·","·","·","·"],
    ["CY3", "Hardware & Embedded Systems Security", "·","B","·","·"],
    ["CY4", "Security Governance, Risk & Compliance", "·","B","·","·"],
    ["CY5", "Blockchain & Decentralized Systems", "·","B","·","B"],
    ["AI1", "LLM & Agentic Systems", "A","A","A","A"],
    ["AI2", "Temporal AI: Time Series & Decisions", "·","·","A","A"],
    ["AI3", "Vision AI: Deep Learning for Vision", "·","·","A","·"],
    ["AI4", "Scalable AI: Big-Data Algorithms", "·","·","A","·"],
    ["AI5", "Generative AI: Deep Generative Models", "·","·","B","·"],
    ["AI6", "Embodied AI: Robotics & Autonomous Systems", "·","·","B","·"],
    ["QCF1","Quantum Optimization", "·","·","·","B"],
    ["QCF2","AI & Optimization for Finance", "·","·","·","B"],
  ];

  const hx = 0.57, hy = 2.12;
  const colID = 0.62, colTitle = 6.35, colT = 1.18; // track col width
  const rowH = 0.234;
  const headers = ["#", "Course", "SE", "Cyber", "AI", "QCF"];
  // header row
  let cxp = hx;
  const widths = [colID, colTitle, colT, colT, colT, colT];
  const trackColors = [null, null, "2563EB", "DC2626", "7C3AED", "D97706"];
  headers.forEach((h, ci) => {
    s.addShape(P.shapes.RECTANGLE, { x: cxp, y: hy, w: widths[ci], h: 0.4, fill: { color: ci >= 2 ? trackColors[ci] : INK } });
    s.addText(h, { x: cxp, y: hy, w: widths[ci], h: 0.4, align: ci === 1 ? "left" : "center", valign: "middle", fontFace: "Consolas", fontSize: 11, bold: true, color: WHITE, margin: ci === 1 ? 4 : 0 });
    cxp += widths[ci];
  });
  // data rows
  cat.forEach((row, ri) => {
    const ry = hy + 0.4 + ri * rowH;
    const zebra = ri % 2 === 0 ? WHITE : "F8FAFC";
    cxp = hx;
    // id
    s.addShape(P.shapes.RECTANGLE, { x: cxp, y: ry, w: colID, h: rowH, fill: { color: zebra }, line: { color: LINE, width: 0.5 } });
    s.addText(row[0], { x: cxp, y: ry, w: colID, h: rowH, align: "center", valign: "middle", fontFace: "Consolas", fontSize: 8.5, bold: true, color: MUTED, margin: 0 });
    cxp += colID;
    // title
    s.addShape(P.shapes.RECTANGLE, { x: cxp, y: ry, w: colTitle, h: rowH, fill: { color: zebra }, line: { color: LINE, width: 0.5 } });
    s.addText(row[1], { x: cxp + 0.05, y: ry, w: colTitle - 0.1, h: rowH, align: "left", valign: "middle", fontFace: "Calibri", fontSize: 9.5, color: INK2, margin: 0 });
    cxp += colTitle;
    // track cells
    for (let k = 0; k < 4; k++) {
      const v = row[2 + k];
      const tc = trackColors[2 + k];
      let fill = zebra, txt = "·", tcol = "CBD5E1", bold = false;
      if (v === "A") { fill = tc; txt = "A"; tcol = WHITE; bold = true; }
      else if (v === "B") { fill = TRACKS[k].soft; txt = "B"; tcol = tc; bold = true; }
      s.addShape(P.shapes.RECTANGLE, { x: cxp, y: ry, w: colT, h: rowH, fill: { color: fill }, line: { color: LINE, width: 0.5 } });
      s.addText(txt, { x: cxp, y: ry, w: colT, h: rowH, align: "center", valign: "middle", fontFace: "Consolas", fontSize: 9.5, bold, color: tcol, margin: 0 });
      cxp += colT;
    }
  });

  // ============ SLIDE 9 — CLOSING ============
  s = P.addSlide();
  s.background = { color: INK };
  TRACKS.forEach((t, i) =>
    s.addShape(P.shapes.RECTANGLE, { x: i * (W / 4), y: H - 0.16, w: W / 4, h: 0.16, fill: { color: t.color } }));
  s.addImage({ data: icComp, x: 0.9, y: 1.5, w: 0.7, h: 0.7 });
  s.addText("Choose Your Path", { x: 0.85, y: 2.35, w: 11.5, h: 1.1, fontFace: "Georgia", fontSize: 52, bold: true, color: WHITE });
  s.addText("Same rigorous foundation — four directions of depth. Your concentration shapes the projects you build, the courses you master, and the roles you step into after graduation.",
    { x: 0.9, y: 3.55, w: 9.8, h: 1.2, fontFace: "Calibri", fontSize: 19, color: "CBD5E1", lineSpacingMultiple: 1.2 });
  // mini summary row
  const fw = 2.85, fg = 0.18, fx0 = 0.9, fy = 5.1;
  TRACKS.forEach((t, i) => {
    const x = fx0 + i * (fw + fg);
    s.addImage({ data: ic[t.key + "_w"], x, y: fy, w: 0.4, h: 0.4 });
    s.addText(t.name, { x: x + 0.5, y: fy - 0.05, w: fw - 0.5, h: 0.55, fontFace: "Calibri", fontSize: 12, bold: true, color: WHITE, valign: "middle", lineSpacingMultiple: 0.9 });
    s.addText(t.roles[0], { x, y: fy + 0.5, w: fw, h: 0.35, fontFace: "Consolas", fontSize: 10, color: t.color });
  });

  await P.writeFile({ fileName: "CS_Concentrations.pptx" });
  console.log("WROTE CS_Concentrations.pptx");
})();
