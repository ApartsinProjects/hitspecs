'use strict';
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, VerticalAlign, BorderStyle, PageOrientation,
} = require('docx');

const NAVY  = '0D1A30';
const TEAL  = '1B9E7A';
const LIGHT = 'EEF3FB';
const MID   = 'CDD8EE';
const WHITE = 'FFFFFF';
const SUB   = '4D6080';
const BLACK = '000000';
const DARK2 = '334466';
const PH    = 'AABBCC';

const PT = n => n * 2;

// Portrait Letter  8.5" × 11"  = 12240 × 15840 twips (portrait is default; no orientation flag)
const MARGIN = 576, GUTTER = 432;
const PG_W   = 12240;   // 8.5"
const PG_H   = 15840;   // 11"
const BODY_W = PG_W - 2 * MARGIN;               // 11088 tw  (7.7")
const COL_W  = Math.floor((BODY_W - GUTTER) / 2); // 5328 tw  (3.7")
const INNER_W = COL_W - 220;                      // 5108 tw  (3.55")

// Portrait column body ≈ 13000 tw available (after header ~1376 + footer ~290)
// Left  (01+02+03+04): 1402 + 3×1750_overhead + 2×Hro + 12×Hc + 10×Ht  →  24×H=6348 → H≈265
// Right (05+06+07):    2×1750 + 1200 + 10×Hpre + 4×Hproj  →  10×280+4×1375=8300 → OK
const H = {
  courseTitle: 360,   // Course Title row  (01 row 1)  — single-para label, natural≈350
  courseDesc:  460,   // Subject Desc row  (01 row 2)
  role:        265,   // each Job Roles data row         (02 × 2)
  con:         265,   // each Concepts data row          (03 × 12)
  tool:        265,   // each Tools data row             (04 × 10)
  pre:         280,   // each Prerequisites row          (05 × 5)
  gap:         280,   // each Topics Not Covered row     (06 × 5)
  proj:       1375,   // each Student Project row        (07 × 4)
};

const NO_BDR  = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const CELL_B  = (c=MID,s=3) => ({ style:BorderStyle.SINGLE, size:s, color:c });
const NO_ALL  = { top:NO_BDR, bottom:NO_BDR, left:NO_BDR, right:NO_BDR,
                  insideH:NO_BDR, insideV:NO_BDR };

const sp = (b=0,a=0) => ({ spacing:{ before:b, after:a } });

function secTitle(num, text) {
  return new Paragraph({ ...sp(80,10), children:[
    new TextRun({ text:num+' ', font:'Calibri', size:PT(8),  color:TEAL, bold:true }),
    new TextRun({ text,         font:'Calibri', size:PT(11), color:NAVY, bold:true }),
  ]});
}
function req(text) {
  return new Paragraph({ ...sp(0,12), children:[
    new TextRun({ text, font:'Calibri', size:PT(7.5), color:TEAL, italics:true }),
  ]});
}
function instr(text) {
  return new Paragraph({ ...sp(0,12), children:[
    new TextRun({ text, font:'Calibri', size:PT(7), color:SUB, italics:true }),
  ]});
}

// Section 01: Course Info (2-row labeled table, single-paragraph labels)
function courseInfoTable() {
  const labelW = Math.round(INNER_W * 0.30), ansW = INNER_W - labelW;
  const ROWS = [
    { label:'Course Title',
      ph:'e.g.  Language AI: LLMs and Agentic Systems',   h:H.courseTitle },
    { label:'Description (one sentence)',
      ph:'Describe the field, technology, or problem this course covers.',  h:H.courseDesc },
  ];
  return new Table({
    width:{size:INNER_W,type:WidthType.DXA}, columnWidths:[labelW,ansW], borders:NO_ALL,
    rows: ROWS.map((r,i) => {
      const fill = i%2===0 ? LIGHT : WHITE, b = CELL_B();
      return new TableRow({ height:{value:r.h,rule:'atLeast'}, children:[
        new TableCell({
          width:{size:labelW,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,color:'auto',fill:NAVY},
          borders:{top:b,bottom:b,left:b,right:CELL_B(DARK2)},
          margins:{top:55,bottom:55,left:80,right:60}, verticalAlign:VerticalAlign.TOP,
          // Single paragraph — natural height stays below atLeast value
          children:[new Paragraph({...sp(0,0),children:[
            new TextRun({text:r.label,font:'Calibri',size:PT(8),bold:true,color:WHITE})]})],
        }),
        new TableCell({
          width:{size:ansW,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,color:'auto',fill},
          borders:{top:b,bottom:b,left:CELL_B(DARK2),right:b},
          margins:{top:50,bottom:50,left:80,right:70}, verticalAlign:VerticalAlign.TOP,
          children:[new Paragraph({...sp(0,0),children:[
            new TextRun({text:r.ph,font:'Calibri',size:PT(8),color:PH,italics:true})]})],
        }),
      ]});
    }),
  });
}

// Section 02: Job Roles (nRows rows)
function rolesTable(nRows, rowH) {
  const w1 = Math.round(INNER_W * 0.30), w2 = INNER_W - w1;
  const mkHd = (txt,w) => new TableCell({
    width:{size:w,type:WidthType.DXA},
    shading:{type:ShadingType.CLEAR,color:'auto',fill:NAVY},
    borders:{top:NO_BDR,bottom:CELL_B(WHITE),left:NO_BDR,right:CELL_B(DARK2)},
    margins:{top:38,bottom:38,left:70,right:50},
    children:[new Paragraph({...sp(0,0),children:[
      new TextRun({text:txt,font:'Calibri',size:PT(7),bold:true,color:WHITE,allCaps:true})
    ]})],
  });
  const hdr = new TableRow({ tableHeader:true,
    children:[mkHd('Job Role',w1), mkHd('What professionals in this role actually do',w2)] });
  const dataRows = Array.from({length:nRows},(_,i) => {
    const fill=i%2===0?LIGHT:WHITE, b=CELL_B();
    return new TableRow({ height:{value:rowH,rule:'atLeast'}, children:[
      new TableCell({ width:{size:w1,type:WidthType.DXA},
        shading:{type:ShadingType.CLEAR,color:'auto',fill}, borders:{top:b,bottom:b,left:b,right:b},
        margins:{top:42,bottom:42,left:70,right:50}, verticalAlign:VerticalAlign.TOP,
        children:[new Paragraph({...sp(0,0),children:[new TextRun({text:'',font:'Calibri',size:PT(9)})]})] }),
      new TableCell({ width:{size:w2,type:WidthType.DXA},
        shading:{type:ShadingType.CLEAR,color:'auto',fill}, borders:{top:b,bottom:b,left:b,right:b},
        margins:{top:42,bottom:42,left:70,right:50}, verticalAlign:VerticalAlign.TOP,
        children:[new Paragraph({...sp(0,0),children:[new TextRun({text:'',font:'Calibri',size:PT(9),color:SUB,italics:true})]})]}),
    ]});
  });
  return new Table({width:{size:INNER_W,type:WidthType.DXA},columnWidths:[w1,w2],borders:NO_ALL,rows:[hdr,...dataRows]});
}

// Single-column numbered list: used for sections 03, 04, 05, 06
function singleList(n, colLabel, rowH) {
  const numW = 55, itemW = INNER_W - numW;
  const hdr = new TableRow({ tableHeader:true, children:[
    new TableCell({ width:{size:numW,type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR,color:'auto',fill:NAVY},
      borders:{top:NO_BDR,bottom:CELL_B(WHITE),left:NO_BDR,right:CELL_B(DARK2)},
      margins:{top:38,bottom:38,left:55,right:30},
      children:[new Paragraph({...sp(0,0),children:[new TextRun({text:'#',font:'Calibri',size:PT(7),bold:true,color:WHITE})]})] }),
    new TableCell({ width:{size:itemW,type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR,color:'auto',fill:NAVY},
      borders:{top:NO_BDR,bottom:CELL_B(WHITE),left:NO_BDR,right:NO_BDR},
      margins:{top:38,bottom:38,left:70,right:50},
      children:[new Paragraph({...sp(0,0),children:[new TextRun({text:colLabel,font:'Calibri',size:PT(7),bold:true,color:WHITE,allCaps:true})]})] }),
  ]});
  const dataRows = Array.from({length:n},(_,i)=>{
    const fill=i%2===0?LIGHT:WHITE, b=CELL_B();
    return new TableRow({ height:{value:rowH,rule:'atLeast'}, children:[
      new TableCell({ width:{size:numW,type:WidthType.DXA},
        shading:{type:ShadingType.CLEAR,color:'auto',fill}, borders:{top:b,bottom:b,left:b,right:b},
        margins:{top:36,bottom:36,left:55,right:30}, verticalAlign:VerticalAlign.TOP,
        children:[new Paragraph({...sp(0,0),children:[new TextRun({text:String(i+1).padStart(2,'0'),font:'Calibri',size:PT(7.5),color:TEAL,bold:true})]})]}),
      new TableCell({ width:{size:itemW,type:WidthType.DXA},
        shading:{type:ShadingType.CLEAR,color:'auto',fill}, borders:{top:b,bottom:b,left:b,right:b},
        margins:{top:36,bottom:36,left:70,right:50}, verticalAlign:VerticalAlign.TOP,
        children:[new Paragraph({...sp(0,0),children:[new TextRun({text:'',font:'Calibri',size:PT(9)})]})]}),
    ]});
  });
  return new Table({width:{size:INNER_W,type:WidthType.DXA},columnWidths:[numW,itemW],borders:NO_ALL,rows:[hdr,...dataRows]});
}

// Section 07: 4-row labeled project table
function projectTable() {
  const labelW=Math.round(INNER_W*0.26), ansW=INNER_W-labelW;
  const ROWS = [
    { label:'Project Description',          tip:'What problem and solution?',
      ph:'Describe what students build: the problem addressed, what the system does, and what makes it non-trivial (technical depth, integration complexity, or originality).' },
    { label:'Tangible Demonstrable Outcome', tip:'What artefacts does the student submit?',
      ph:'Describe the deliverable: artefacts (code, notebooks, README, report), documentation level, and how the student presents or walks through it in an interview, portfolio, or recorded demo.' },
    { label:'Feedback Structure',            tip:'How is progress reviewed?',
      ph:'Describe milestone checkpoints during the semester: when presentations happen, what is reviewed at each stage, how feedback is delivered, and how it drives the next iteration.' },
    { label:'Conceptual and Technical Depth',tip:'What makes it demanding?',
      ph:'Explain which theoretical concepts and engineering principles from the course are integrated, and what technical challenges make the project genuinely demanding, not a tutorial reproduction.' },
  ];
  return new Table({
    width:{size:INNER_W,type:WidthType.DXA}, columnWidths:[labelW,ansW], borders:NO_ALL,
    rows: ROWS.map((r,i)=>{
      const fill=i%2===0?LIGHT:WHITE, b=CELL_B();
      return new TableRow({ height:{value:H.proj,rule:'atLeast'}, children:[
        new TableCell({
          width:{size:labelW,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,color:'auto',fill:NAVY},
          borders:{top:b,bottom:b,left:b,right:CELL_B(DARK2)},
          margins:{top:55,bottom:55,left:80,right:60}, verticalAlign:VerticalAlign.TOP,
          children:[
            new Paragraph({...sp(0,8),children:[new TextRun({text:r.label,font:'Calibri',size:PT(8),bold:true,color:WHITE})]}),
            new Paragraph({...sp(0,0),children:[new TextRun({text:r.tip,  font:'Calibri',size:PT(6.5),color:MID,italics:true})]}),
          ],
        }),
        new TableCell({
          width:{size:ansW,type:WidthType.DXA},
          shading:{type:ShadingType.CLEAR,color:'auto',fill},
          borders:{top:b,bottom:b,left:CELL_B(DARK2),right:b},
          margins:{top:50,bottom:50,left:80,right:70}, verticalAlign:VerticalAlign.TOP,
          children:[new Paragraph({...sp(0,0),children:[new TextRun({text:r.ph,font:'Calibri',size:PT(8),color:PH,italics:true})]})],
        }),
      ]});
    }),
  });
}

// Layout helpers
const NO_C = {top:NO_BDR,bottom:NO_BDR,left:NO_BDR,right:NO_BDR};
const colCell  = (ch,w) => new TableCell({ width:{size:w,type:WidthType.DXA}, borders:NO_C,
  margins:{top:0,bottom:0,left:0,right:0}, children:ch });
const gutterCell = () => new TableCell({ width:{size:GUTTER,type:WidthType.DXA}, borders:NO_C,
  margins:{top:0,bottom:0,left:0,right:0}, children:[new Paragraph({children:[]})] });
const outerTable = (L,R) => new Table({
  width:{size:BODY_W,type:WidthType.DXA}, columnWidths:[COL_W,GUTTER,COL_W],
  borders:NO_ALL,
  rows:[new TableRow({children:[colCell(L,COL_W), gutterCell(), colCell(R,COL_W)]})] });

// Portrait single page — LEFT: 01 02 03 04  |  RIGHT: 05 06 07
const LEFT1 = [
  secTitle('01','Course Info'),
  instr('Course title and a one-sentence description of the subject this course covers.'),
  courseInfoTable(),

  secTitle('02','Target Job Roles and Responsibilities'),
  req('Prepare students for 2 specific industry roles; scope the course around '
    + 'what professionals in those roles actually build and deliver.'),
  instr('Each role as it appears in real job postings, and what professionals in that role actually build, decide, and deliver.'),
  rolesTable(2, H.role),

  secTitle('03','Transferable Engineering and Scientific Principles'),
  req('Ground students in principles that remain valid regardless of which tools or '
    + 'platforms are in use: theory, algorithms, data structures, or domain science.'),
  instr('Ten transferable principles students carry beyond this course: theory, algorithms, data structures, or domain science that holds regardless of which tools are in use.'),
  singleList(10,'Transferable Principle', H.con),

  secTitle('04','Tools, Platforms, and Libraries'),
  req('Give students direct hands-on experience with the tools professionals use today, '
    + 'not just conceptual familiarity.'),
  instr('Ten tools, platforms, libraries, or APIs students work with hands-on during this course.'),
  singleList(10,'Tool / Platform / Library / API', H.tool),
];

const RIGHT1 = [
  secTitle('05','Prerequisite Requirements'),
  req('Require students to enter with a defined baseline; every item on this list must be '
    + 'mastered before starting the course.'),
  instr('Up to five prerequisite concepts or skills students must have mastered before starting the course.'),
  singleList(5,'Prerequisite Concept / Skill', H.pre),

  secTitle('06','Topics Not Covered in This Course'),
  req('These topics are part of the field but are intentionally excluded due to lack of '
    + 'teaching time; each one belongs in a follow-up or advanced course.'),
  instr('Up to five topics that belong to the field but are intentionally excluded due to lack of teaching time.'),
  singleList(5,'Topic Not Covered', H.gap),

  secTitle('07','Student Project'),
  req('Build a significant project progressively throughout the semester, '
    + 'resulting in a technically deep, demonstrable, portfolio-ready outcome.'),
  instr('Four dimensions of the student project: description, tangible deliverable, feedback structure, and conceptual and technical depth.'),
  projectTable(),
];

const doc = new Document({
  styles:{ default:{ document:{
    run:{ font:'Calibri', size:PT(9), color:BLACK },
    paragraph:{ spacing:{ line:240, lineRule:'auto' } },
  }}},
  sections:[{
    properties:{ page:{
      size:{ width:12240, height:15840 },   // Portrait Letter 8.5"×11" (no landscape)
      margin:{ top:MARGIN, bottom:MARGIN, left:MARGIN, right:MARGIN },
    }},
    children:[
      new Paragraph({...sp(0,16),children:[
        new TextRun({text:'HIT · Advanced CS Electives  ·  Core Elective Course Card',
          font:'Calibri',size:PT(7.5),color:TEAL,bold:true}),
      ]}),
      new Paragraph({...sp(0,10),children:[
        new TextRun({text:'Core Elective Course Card',
          font:'Calibri',size:PT(14.5),bold:true,color:NAVY}),
      ]}),
      new Paragraph({...sp(0,28),
        border:{bottom:{style:BorderStyle.SINGLE,size:4,color:MID}},
        children:[new TextRun({text:
          'Complete all 7 sections. Be specific and thorough: this guides course development '
        + 'and programme-level quality review.',
          font:'Calibri',size:PT(7.5),color:SUB})],
      }),

      outerTable(LEFT1, RIGHT1),

      new Paragraph({...sp(28,0),
        border:{top:{style:BorderStyle.SINGLE,size:3,color:MID}},
        children:[new TextRun({text:'', font:'Calibri', size:PT(7), color:SUB})],
      }),
    ],
  }],
});

const OUT = 'E:/Projects/Courses/Concentrations/core-elective-course-form.docx';
Packer.toBuffer(doc).then(buf => {
  require('fs').writeFileSync(OUT, buf);
  console.log('OK ' + OUT);
}).catch(e => { console.error(e); process.exit(1); });
