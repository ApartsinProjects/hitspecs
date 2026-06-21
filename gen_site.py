# -*- coding: utf-8 -*-
"""Static-site generator for the CS degree concentrations."""
import os, html, shutil, json, glob

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# ----------------------------------------------------------------------------
# DATA
# ----------------------------------------------------------------------------
TRACKS = {
    "SE": dict(
        name="Intelligent Software Systems",
        he="הנדסת מערכות תוכנה תבוניות",
        nav="Intelligent Systems",
        color="3A4B9D", soft="E7EAF5", ink="2A3873",
        tag="Build and operate the intelligent software systems the world runs on.",
        tag_he="בונים ומפעילים את מערכות התוכנה התבוניות שעליהן העולם מתבסס.",
        rationale=(
            "This concentration trains you to design, build, test, and operate "
            "production-grade software systems at scale, increasingly powered by AI "
            "and data. The track spans the full delivery stack: cloud-native "
            "platforms, secure coding and quality assurance, front-end and back-end "
            "web, mobile and edge, and the engineering of AI-based and data-intensive "
            "systems that must run reliably in production."),
        roles=["Full-Stack Software Developer", "DevOps Engineer", "QA Engineer",
               "Cloud & Platform Engineer", "Backend Engineer", "Mobile Developer"],
    ),
    "CY": dict(
        name="Networking & Cyber Security",
        he="רשתות ואבטחת סייבר",
        nav="Cyber Security",
        color="9C3B2E", soft="F6E7E4", ink="7A2C22",
        tag="Defend networks, data, and infrastructure end to end.",
        tag_he="מגנים על רשתות, נתונים ותשתיות מקצה לקצה.",
        rationale=(
            "This concentration prepares you to secure systems, networks, and data "
            "against real adversaries. You combine a strong software and cloud "
            "foundation with applied cryptography, hardware and network security, "
            "blockchain, and the governance, risk, and compliance practices that "
            "turn security from an afterthought into an engineering discipline."),
        roles=["Network Engineer", "DevSecOps Engineer", "Security Analyst",
               "Penetration Tester", "Security Engineer", "SOC Analyst"],
    ),
    "AI": dict(
        name="AI & Robotics",
        he="בינה מלאכותית ורובוטיקה",
        nav="AI & Robotics",
        color="7A3E9D", soft="EFE7F6", ink="5D2F79",
        tag="Design intelligent systems that perceive, reason, and act.",
        tag_he="מתכננים מערכות אינטליגנטיות שתופסות, מסיקות ופועלות.",
        rationale=(
            "The AI track gives you the modeling depth to build systems that "
            "perceive, reason, and act. It covers the major modern paradigms: large "
            "language models and agents, temporal and sequential decision-making, "
            "computer vision, scalable big-data learning, generative models, and "
            "embodied AI for robotics, all grounded in the engineering needed to "
            "deploy them in production."),
        roles=["ML / AI Engineer", "MLOps Engineer", "Algorithm Engineer",
               "Data Scientist", "NLP Engineer", "Computer Vision Engineer"],
    ),
    "QCF": dict(
        name="Computational Finance, Optimization & Quantum Computing",
        he="הנדסת מערכות פיננסיות, אופטימיזציה וחישובים קוונטיים",
        nav="Computational Finance",
        color="B5530B", soft="FBEEDE", ink="8A3F08",
        tag="Quantitative modeling, optimization, and quantum algorithms.",
        tag_he="מידול כמותי, אופטימיזציה ואלגוריתמים קוונטיים.",
        rationale=(
            "This concentration sits at the intersection of quantitative modeling, "
            "optimization, and emerging quantum computing. You build the software "
            "and data foundations, then specialize in cryptography, decentralized "
            "finance, quantum optimization, and AI-driven financial modeling, "
            "preparing you for quantitative and algorithmic roles in finance and "
            "beyond."),
        roles=["Financial Software Engineer", "Algo-Trading Developer", "Quant Analyst",
               "Quantitative Developer", "Risk Analyst", "Data Engineer (Finance)"],
    ),
    "GM": dict(
        name="Immersive Systems & Game Development",
        he="מערכות אימרסיביות ופיתוח משחקים",
        nav="Immersive Systems",
        color="0B6B8A", soft="E0EEF2", ink="084E63",
        tag="Build immersive games and extended-reality worlds.",
        tag_he="בונים משחקים סוחפים ועולמות מציאות מורחבת.",
        rationale=(
            "This concentration trains you to build real-time interactive and "
            "immersive software: game engines, 3D graphics, virtual and augmented "
            "reality, and the AI, simulation, and cloud backends behind them. It "
            "pairs a strong computer-graphics and spatial-computing core with vision, "
            "generative, and embodied AI to create worlds that render, react, and "
            "scale."),
        roles=["Gameplay Programmer", "Graphics / Rendering Engineer",
               "XR / AR Software Developer", "Game Engine Developer",
               "Game Backend Engineer", "Simulation Software Engineer"],
    ),
    "DF": dict(
        name="Defense Technologies & Autonomous Systems",
        he="טכנולוגיות ביטחוניות ומערכות אוטונומיות",
        nav="Defense Technologies",
        color="1F6F54", soft="E1F0E9", ink="134734",
        tag="Engineer mission-critical defense and autonomous systems.",
        tag_he="מהנדסים מערכות ביטחוניות ואוטונומיות קריטיות למשימה.",
        rationale=(
            "This concentration prepares you to engineer mission-critical defense and "
            "autonomous systems: sensor fusion and signal processing, safety-critical "
            "real-time software, secure communications, and autonomous platforms. It "
            "builds on cryptography, embedded security, vision, and temporal AI to "
            "deliver systems that must perform reliably under real-world constraints."),
        roles=["Defense Software Engineer", "Embedded Software Engineer",
               "Autonomous Systems Software Engineer", "Signal-Processing Software Engineer",
               "Secure Communications Software Engineer", "Simulation & Modeling Engineer"],
    ),
}
TRACK_ORDER = ["SE", "CY", "AI", "QCF", "GM", "DF"]

# course id -> (title, description, [topics], {track: 'A'|'B'|'E'})
COURSES = {
    "SE1": ("Cloud Computing & Cloud-Native Platforms",
        "Design and operate applications built for the cloud, using containers, "
        "orchestration, and managed services to achieve elasticity, resilience, and "
        "cost efficiency.",
        ["Containers & Kubernetes", "Microservices & service meshes",
         "Infrastructure as code", "Scalability & cost management"],
        {"SE": "A", "CY": "A", "AI": "E", "QCF": "A"}),
    "SE2": ("Secure & Reliable Software Development",
        "Engineer software that is correct, testable, and secure by design, "
        "integrating quality assurance and application-security practices throughout "
        "the development lifecycle.",
        ["Automated testing & CI", "Secure coding (OWASP)",
         "Code review & static analysis", "Reliability & observability"],
        {"SE": "A", "CY": "A", "AI": "E", "QCF": "E"}),
    "SE3": ("Modern Front-End Web Development",
        "Build responsive, accessible, interactive user interfaces with modern "
        "component frameworks and front-end tooling.",
        ["Component frameworks (React/Vue)", "State management",
         "Responsive & accessible design", "Build tooling & performance"],
        {"SE": "A", "CY": "E", "AI": "E", "QCF": "E"}),
    "SE4": ("Back-End Web Development & APIs",
        "Design server-side applications and well-structured APIs that power web and "
        "mobile clients, with attention to data modeling, authentication, and scale.",
        ["REST & GraphQL APIs", "Databases & data modeling",
         "Authentication & sessions", "Caching & scaling"],
        {"SE": "B", "CY": "E", "AI": "E", "QCF": "E"}),
    "SE5": ("Engineering of AI Systems",
        "Apply DevOps discipline to machine-learning and LLM systems, automating "
        "training, deployment, monitoring, and continuous delivery of models in "
        "production.",
        ["CI/CD pipelines", "Model serving & versioning",
         "Monitoring & drift detection", "LLMOps & agent operations"],
        {"SE": "B", "CY": "B", "AI": "B", "QCF": "E"}),
    "SE6": ("Mobile, IoT & Edge Software Development",
        "Develop software for mobile, IoT, and edge devices where connectivity, "
        "power, and compute are constrained and data is processed close to where it "
        "is generated.",
        ["Mobile app development", "IoT protocols & sensors",
         "Edge computing", "Offline-first & sync"],
        {"SE": "B", "CY": "E", "AI": "E", "QCF": "E"}),
    "SE7": ("Design of AI-based & Data-Intensive Systems",
        "Architect large systems whose core is data and machine learning, balancing "
        "throughput, latency, consistency, and the demands of AI workloads.",
        ["Data pipelines & streaming", "System architecture & trade-offs",
         "Distributed storage", "ML system integration"],
        {"SE": "B", "CY": "E", "AI": "B", "QCF": "B"}),
    "CY1": ("Applied Cryptography",
        "Understand and correctly apply the cryptographic primitives that underpin "
        "secure communication, authentication, and data protection.",
        ["Symmetric & public-key crypto", "Hashing & digital signatures",
         "Key exchange & PKI", "Protocol design pitfalls"],
        {"SE": "E", "CY": "A", "AI": "E", "QCF": "E"}),
    "CY2": ("Network Security",
        "Secure networks and communication channels against interception, "
        "tampering, and intrusion across the protocol stack.",
        ["TLS & secure protocols", "Firewalls & IDS/IPS",
         "VPNs & network segmentation", "Attack detection"],
        {"SE": "E", "CY": "A", "AI": "E", "QCF": "E"}),
    "CY3": ("Hardware & Embedded Systems Security",
        "Examine security at the hardware and firmware level, where physical "
        "access, side channels, and constrained devices create distinct threats.",
        ["Side-channel attacks", "Secure boot & TPM",
         "Firmware analysis", "Embedded threat models"],
        {"SE": "E", "CY": "B", "AI": "E", "QCF": "E"}),
    "CY4": ("Cyber-Security Governance, Risk & Compliance",
        "Manage cyber-security as an organizational discipline through risk "
        "assessment, security policy, compliance frameworks, and incident response.",
        ["Risk assessment", "Standards (ISO 27001, NIST)",
         "Policy & audit", "Incident response"],
        {"SE": "E", "CY": "B", "AI": "E", "QCF": "A"}),
    "CY5": ("Blockchain & Decentralized Systems",
        "Study distributed ledgers, consensus, and smart contracts, and the "
        "security properties and limits of decentralized systems.",
        ["Consensus mechanisms", "Smart contracts",
         "Wallets & key management", "DeFi security"],
        {"SE": "E", "CY": "B", "AI": "E", "QCF": "B"}),
    "AI1": ("Language AI: LLMs and Agentic Systems",
        "Build applications on large language models and autonomous agents, "
        "covering prompting, tool use, retrieval, and orchestration of multi-step "
        "reasoning.",
        ["LLM fundamentals", "Prompting & RAG",
         "Tool use & agents", "Evaluation & guardrails"],
        {"SE": "A", "CY": "E", "AI": "A", "QCF": "A"}),
    "AI2": ("Temporal AI: Time Series & Sequential Decision Making",
        "Model data that unfolds over time and learn to make sequential decisions "
        "under uncertainty.",
        ["Time-series forecasting", "Sequence models",
         "Reinforcement learning", "Decision under uncertainty"],
        {"SE": "E", "CY": "E", "AI": "A", "QCF": "A"}),
    "AI3": ("Vision AI: Deep Learning for Computer Vision",
        "Apply deep learning to images and video for recognition, detection, and "
        "segmentation tasks.",
        ["CNNs & vision transformers", "Object detection",
         "Image segmentation", "Transfer learning"],
        {"SE": "E", "CY": "E", "AI": "A", "QCF": "E"}),
    "AI4": ("Scalable AI: Big-Data Algorithms",
        "Learn algorithms and systems for machine learning at scale, where datasets "
        "and models exceed a single machine.",
        ["Distributed training", "Big-data frameworks",
         "Approximate & streaming algorithms", "Scaling laws"],
        {"SE": "E", "CY": "E", "AI": "A", "QCF": "E"}),
    "AI5": ("Generative AI: Deep Generative Models",
        "Study the models that generate images, text, and audio, from diffusion "
        "models to GANs and autoregressive generators.",
        ["Diffusion models", "GANs & VAEs",
         "Autoregressive generation", "Evaluating generative output"],
        {"SE": "E", "CY": "E", "AI": "B", "QCF": "E"}),
    "AI6": ("Embodied AI: Robotics & Autonomous Systems",
        "Bring AI into the physical world through perception, planning, and control "
        "for robots and autonomous systems.",
        ["Perception & sensor fusion", "Motion planning",
         "Control & RL for robotics", "Simulation-to-real transfer"],
        {"SE": "E", "CY": "E", "AI": "B", "QCF": "E"}),
    "QCF1": ("Quantum Optimization",
        "Explore quantum and quantum-inspired approaches to hard optimization "
        "problems and the algorithms that exploit them.",
        ["Quantum computing basics", "QAOA & quantum annealing",
         "Combinatorial optimization", "Quantum-inspired methods"],
        {"SE": "E", "CY": "E", "AI": "E", "QCF": "B"}),
    "QCF2": ("AI & Optimization for Finance",
        "Apply machine learning and optimization to financial problems such as "
        "pricing, portfolio construction, and algorithmic trading.",
        ["Portfolio optimization", "Algorithmic trading",
         "Risk modeling", "Machine learning for finance"],
        {"SE": "E", "CY": "E", "AI": "E", "QCF": "B"}),
    "GM1": ("Computer Graphics",
        "Master the foundations of computer graphics: the rendering pipeline, "
        "rasterization and ray tracing, shading and lighting, and real-time "
        "rendering on modern GPUs and engines.",
        ["Rendering pipeline & rasterization", "Ray tracing & global illumination",
         "Shading, lighting & materials", "Real-time GPU rendering"],
        {}),
    "GM2": ("Spatial Computing",
        "Build spatial and immersive applications: 3D tracking and scene "
        "understanding, virtual and augmented reality, natural interaction, and "
        "spatial UX across XR devices.",
        ["VR/AR & OpenXR", "Tracking & spatial mapping (SLAM)",
         "Natural interaction & UX", "On-device performance"],
        {}),
    "DF1": ("Sensor Fusion & Signal Processing",
        "Process and fuse data from radar, electro-optical, infrared, and RF sensors "
        "using signal processing and estimation to build a coherent picture of the "
        "environment.",
        ["Digital signal processing", "Kalman filtering & estimation",
         "Multi-sensor fusion", "Radar, EO/IR and RF"],
        {}),
    "DF2": ("Mission-Critical Real-Time Systems",
        "Engineer software that must be correct and on time: real-time scheduling, "
        "safety-critical design, fault tolerance, and the reliability and "
        "certification practices defense systems demand.",
        ["Real-time scheduling", "Safety-critical software",
         "Fault tolerance & reliability", "Certification standards"],
        {}),
}
COURSE_ORDER = list(COURSES.keys())

# New-concentration core assignments: course_id -> {track: "A"|"B"}.
# (Every other track defaults to "E" via the normalization loop below.)
NEW_CORE = {
    # Immersive Systems & Game Development (GM): A1-A4 then B1-B4
    "GM1": {"GM": "A"}, "AI3": {"GM": "A", "DF": "A"}, "SE3": {"GM": "A"},
    "SE6": {"GM": "A", "DF": "B"},
    "GM2": {"GM": "B"}, "AI5": {"GM": "B"}, "AI6": {"GM": "B", "DF": "B"},
    "SE1": {"GM": "B"},
    # Defense Technologies & Autonomous Systems (DF): A1-A4 then B1-B4
    "DF1": {"DF": "A"}, "CY1": {"DF": "A"}, "CY3": {"DF": "A"},
    "DF2": {"DF": "B"}, "AI2": {"DF": "B"},
}
# Ensure every course's role map has all tracks, then apply the new-core overrides.
for _cid, _c in COURSES.items():
    _roles = _c[3]
    for _t in TRACK_ORDER:
        _roles.setdefault(_t, "E")
    for _t, _v in NEW_CORE.get(_cid, {}).items():
        _roles[_t] = _v

# Hebrew course names (shown as a light-grey subtitle alongside the English title).
COURSE_HE = {
    "SE1": "מחשוב ענן ופלטפורמות ענן-נייטיב",
    "SE2": "פיתוח תוכנה מאובטח ואמין",
    "SE3": "פיתוח צד-לקוח מודרני",
    "SE4": "פיתוח צד-שרת ו-APIs",
    "SE5": "הנדסת מערכות בינה מלאכותית",
    "SE6": "פיתוח תוכנה לנייד, IoT וקצה",
    "SE7": "תכן מערכות מבוססות-AI ועתירות-נתונים",
    "CY1": "קריפטוגרפיה יישומית",
    "CY2": "אבטחת רשתות",
    "CY3": "אבטחת חומרה ומערכות משובצות",
    "CY4": "ממשל אבטחת סייבר, סיכון וציות",
    "CY5": "בלוקצ'יין ומערכות מבוזרות",
    "AI1": "בינת שפה: מודלי שפה גדולים ומערכות סוכניות",
    "AI2": "AI טמפורלי: סדרות עתיות וקבלת החלטות רציפה",
    "AI3": "בינת ראייה: למידה עמוקה לראייה ממוחשבת",
    "AI4": "AI בקנה מידה: אלגוריתמים לנתוני עתק",
    "AI5": "AI יוצר: מודלים גנרטיביים עמוקים",
    "AI6": "AI מגולם: רובוטיקה ומערכות אוטונומיות",
    "QCF1": "אופטימיזציה קוונטית",
    "QCF2": "בינה מלאכותית ואופטימיזציה למימון",
    "GM1": "גרפיקה ממוחשבת",
    "GM2": "מחשוב מרחבי",
    "DF1": "מיזוג חיישנים ועיבוד אותות",
    "DF2": "מערכות זמן-אמת קריטיות למשימה",
}

# A course is "core-bearing" if it is a core course (A or B) in at least one
# concentration. Such a course is an elective to the other concentrations.
CORE_COURSES = [c for c in COURSE_ORDER
                if any(v in ("A", "B") for v in COURSES[c][3].values())]
# Additional elective catalogue: courses not core to any concentration.
EXTRA_ELECTIVES = [c for c in COURSE_ORDER if c not in CORE_COURSES]

# Detailed syllabi (objectives, tools, 12-week plan, references), one JSON per
# concentration family, keyed by course id.
SYLLABI = {}
for _f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "syllabi", "*.json"))):
    with open(_f, encoding="utf-8") as _fh:
        SYLLABI.update(json.load(_fh))

# Career-role profiles (description, responsibilities, knowledge, skills, tools).
CAREERS = {}
_cf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "careers.json")
if os.path.isfile(_cf):
    with open(_cf, encoding="utf-8") as _fh:
        CAREERS = json.load(_fh)

# Free online video courses that can serve as a self-study basis, per course.
ONLINE_BASIS = {}
for _f in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "onlinebasis", "*.json"))):
    with open(_f, encoding="utf-8") as _fh:
        ONLINE_BASIS.update(json.load(_fh))

import re as _re
def slugify(s):
    return _re.sub(r"-+", "-", _re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")

# Shared elective catalogue (HIT enrichment electives, not core to any concentration).
# (number, english name, hebrew name, credits, instructor, domain, category)
ELECTIVE_CATALOGUE = [
    ("67018", "Android App Development in Kotlin", "פיתוח אפליקציות אנדרואיד בשפת קוטלין", "3.5", "Eran Katzav", "SE", "Software"),
    ("65363", "Classic Software Design Patterns", "תבניות עיצוב תוכנה קלאסיות", "3", "Michael Haim", "SE", "Software"),
    ("65355", "Principles of Functional Programming", "עקרונות התכנות הפונקציונלי", "3", "Michael Haim", "SE", "Software"),
    ("65346", "Human-Computer Interaction (UI)", "ממשקי אדם מחשב UI", "3", "Dr. Naava Shaked", "SE", "Software"),
    ("65365", "Parallel Programming", "תכנות מקבילי", "3", "Michael Haim", "SE", "Software"),
    ("65345", "Competitive Programming", "תכנות תחרותי", "3.5", "Yuval Meir", "SE", "Project"),
    ("67000", "Advanced Software Solutions Engineering, Part A", "הנדסת פתרונות תוכנה מתקדמים חלק א'", "3.5", "Dr. Yossi Eliaz", "SE", "Project"),
    ("67013", "Advanced Software Solutions Engineering, Part B", "הנדסת פתרונות תוכנה מתקדמים חלק ב'", "3.5", "Dr. Yossi Eliaz", "SE", "Project"),
    ("62121", "LLM-Augmented Software Practice", "LLM-Augmented Software Practice", "3.5", "Michael Gorsky", "SE", "AI-assisted coding"),
    ("62304", "Software for Human-Humanoid Robot Interaction", "פיתוח תוכנה לאינטראקציה בין אדם ורובוט הומנואיד", "3.5", "Idan Tovis", "AI", "Robotics"),
    ("67006", "Software for Intelligent Autonomous Vehicles", "פיתוח תוכנה עבור רכב אוטונומי אינטליגנטי", "3.5", "Yuri Yurchenko", "AI", "Robotics"),
    ("62211", "Generative AI in Science, Technology and Society", "בינה מלאכותית גנרטיבית במדע, טכנולוגיה וחברה", "3", "Prof. Ilya Levin", "AI", "AI & Society"),
    ("67021", "Ethics of Artificial Intelligence", "אתיקה של בינה מלאכותית", "3.5", "Dr. Galit Wellner", "AI", "AI & Society"),
    ("67023", "Introduction to Information Retrieval", "מבוא לאחזור מידע", "3.5", "Moshe Friedman", "AI", "Information Retrieval"),
    ("67028", "Human-Smart AI Interaction Workshop", "Human - Smart AI Interaction Workshop", "3.5", "Eran Aharonson", "AI", "AI UX"),
    ("65361", "Basic AI Algorithms and Applications in Digital Medicine", "אלגוריתמים בסיסיים של בינה מלאכותית ויישומים ברפואה דיגיטלית", "3.5", "Prof. Eugene Levner", "AI", "AI in Medicine"),
    ("67011", "Audio Processing for Intelligent Systems", "עיבוד קול למערכות תבוניות", "3", "Dr. Naava Shaked and Yuri Yurchenko", "AI", "Voice"),
    ("60309", "Image Processing for Computer Science", "עיבוד תמונה למדעי המחשב", "3.5", "Dr. Kornel Lustig", "AI", "Vision"),
    ("62206", "Introduction to AI-Driven Cyber Security", "מבוא לאבטחת סייבר מונחית בינה מלאכותית", "3.5", "Vyacheslav Nepdov", "CY", "Cyber & AI"),
    ("65343", "Reverse Engineering and Malware Analysis", "הנדסה לאחור וניתוח תוכנות זדוניות", "3", "Shorna Frayer", "CY", "Reverse Engineering"),
]

# Existing HIT courses that currently cover a planned core course (gap analysis).
# core_id -> list of (number, english name, instructor, coverage note)
BASE_AVAILABLE = {
    "SE1": [("62213", "Introduction to Cloud and Development with AWS Serverless", "Yogev Shani", "")],
    "SE2": [("64444", "Software Testing", "David Tobias", "About 50%: covers correctness and QA; application-security half to add")],
    "SE3": [("65364", "Client-Side Development", "Michael Haim", "")],
    "SE4": [("64410", "Server-Side Systems Development (Open Source)", "Ofer Vald", "")],
    "SE5": [("65353", "Introduction to DevOps", "Moshe Mamia", "About 30%: DevOps basics; DataOps, MLOps, LLMOps, AgentOps to add")],
    "SE6": [("65348", "Software for IoT in a Smart-City Environment", "Yuri Yurchenko", ""),
            ("65351", "Android Client-Side Development 1", "Effi Propes", "")],
    "GM1": [("65235", "Computer Graphics", "Dr. Vladimir Nodelman", "")],
    "CY1": [("68012", "Applied Introduction to Modern Cryptography", "Zeev Geyzel", "")],
    "CY2": [("65338", "Network and Internet Security", "Adrian Shpeler", "")],
    "DF2": [("67026", "Introduction to Embedded Software and Applications", "Vladi Sorkin", "Partial: covers embedded software foundations; real-time scheduling, safety-critical design, and certification to add")],
    "CY5": [("67007", "Blockchain: Vision and Practice", "Michael Bershadsky", "")],
    "AI1": [("65339", "LLM & Agents (NLP)", "Dr. Alexander Apartsin", "")],
    "AI3": [("67025", "Deep-Learning-Based Computer Vision", "Lehav Yefet", "")],
    "AI5": [("67030", "Deep Models for Generative AI", "Dr. Alexander Apartsin", "")],
    "AI6": [("69983", "Robotics for Computer Science", "Dr. Eliyahu Matzliach", "")],
}

# Every designated course is a CORE course; A = first semester, B = second semester.
ROLE_LABEL = {"A": "Core · Sem 1", "B": "Core · Sem 2", "E": "Elective"}

# Standard course shape shared by every course (project-based, 13 weeks).
PRESENTATION_WEEKS = {5, 8, 13}
COURSE_FORMAT_NOTE = ("Thirteen weeks, four contact hours each: a two-hour lecture "
    "(concepts and theory) and a two-hour practice session. The course is "
    "project-based; teams carry one running project end to end and present it "
    "three times, in weeks 5, 8, and 13.")
ASSESSMENT = [
    ("Project · Specification", "Presentation 1 (week 5): problem, objectives, and architecture", "20%"),
    ("Project · Interim", "Presentation 2 (week 8): the working system demonstrated live", "30%"),
    ("Project · Final", "Presentation 3 (week 13): end-to-end demo with oral defense", "50%"),
]
# What the running project must be (depth, real systems, not exercises).
PROJECT_REQUIREMENTS = [
    "Build a working system, not a set of disconnected exercises.",
    "Be original: a new system that solves a real problem, not a re-implementation of a tutorial or course demo.",
    "Show real depth: real data, real users or realistic load, and engineering trade-offs that are measured rather than assumed.",
    "Carry one running project from specification to a deployed, defensible result across the whole term.",
    "Work in a team of three or four and defend the design at each of the three presentations (weeks 5, 8, and 13).",
]
# Year-3 baseline assumed for every concentration course.
ASSUMED_BACKGROUND = ("This is a Year-3 course. It assumes the mandatory CS core: "
    "data structures and algorithms, operating systems, computer networks, databases, "
    "software engineering, and the core mathematics (linear algebra, probability and "
    "statistics, calculus, discrete mathematics). It additionally requires the "
    "specific prior courses listed below.")

# Audited, course-specific prerequisites (only what each course genuinely needs).
PREREQS = {
    "SE1": ["Operating systems and computer networks", "Software engineering and a programming language"],
    "SE2": ["Software engineering and object-oriented programming", "Basic computer networks and web applications"],
    "SE3": ["Programming fundamentals", "Basic web technologies (HTML, CSS, JavaScript)"],
    "SE4": ["Databases", "Computer networks", "Software engineering and a server-side language"],
    "SE5": ["Machine Learning", "Software engineering and Python", "Operating systems and networking"],
    "SE6": ["Programming fundamentals", "Operating systems and computer networks"],
    "SE7": ["Databases", "Algorithms and data structures", "Machine Learning"],
    "CY1": ["Discrete mathematics and number-theory basics", "Algorithms", "Probability"],
    "CY2": ["Computer networks", "Operating systems"],
    "CY3": ["Computer organization and architecture", "Operating systems", "C or embedded programming"],
    "CY4": ["Software engineering", "Basic information-security concepts"],
    "CY5": ["Cryptography fundamentals", "Distributed systems and computer networks"],
    "AI1": ["Machine Learning and Deep Learning", "Probability and linear algebra", "Python"],
    "AI2": ["Machine Learning", "Probability and statistics", "Linear algebra"],
    "AI3": ["Deep Learning", "Linear algebra and calculus"],
    "AI4": ["Machine Learning", "Algorithms and data structures", "Distributed systems or databases basics"],
    "AI5": ["Deep Learning", "Probability and linear algebra"],
    "AI6": ["Machine Learning and basic reinforcement learning", "Linear algebra", "Calculus and basic physics"],
    "QCF1": ["Basic Quantum Algorithms", "Linear algebra", "Algorithms and optimization basics"],
    "QCF2": ["Machine Learning", "Probability and statistics", "Calculus and convex optimization"],
    "GM1": ["Linear algebra", "Programming in C++ or C#", "Data structures and algorithms"],
    "GM2": ["Computer Graphics or 3D graphics basics", "Linear algebra", "Computer vision basics"],
    "DF1": ["Signals and systems or linear algebra", "Probability and statistics", "Programming in Python or C++"],
    "DF2": ["Operating systems", "Embedded or systems programming", "Software engineering"],
}

# The design principles behind the concentration structure (the "Six Pillars").
# Bullet strings contain inline HTML and must NOT be html-escaped.
PILLARS = [
    ("Job role-oriented", "EA6A52", "FBE6E1", [
        'A sequence of <b>8 core courses</b> that prepares students for <a href="careers.html"><b>target job roles</b></a>.',
        "Gives students a <b>complete toolbox</b> for the job role."]),
    ("Structured progression", "5F8A6B", "E7EFE9", [
        "Advanced courses may <b>depend on</b> earlier concentration courses.",
        "Avoids conceptual redundancy for the best use of <b>limited time</b>."]),
    ("Portfolio-driven", "3B82F6", "DBEAFE", [
        "A <b>guided</b> effort to help students build a strong <b>project portfolio</b>.",
        "Project-based learning stresses project depth and <b>demonstrable artifacts</b>."]),
    ("Academic depth with tools", "A855F7", "F2E8FE", [
        "Combines rigorous academic foundations with current <b>tools</b>, programming languages, and platforms.",
        "Embeds <b>AI-assisted</b> development practices."]),
    ("Enrichment electives", "F59E0B", "FEF1CF", [
        'Deepen expertise beyond core courses, improving fit for concentration <a href="careers.html"><b>job roles</b></a>.',
        "Prepare students for <b>graduate studies</b>."]),
    ("Core course reuse", "2FA161", "DDF4E6", [
        "Core courses are a <b>flagship</b>: high-quality, comprehensive, current, and project-based.",
        "Some core courses are <b>shared between concentrations</b>."]),
]

def course_family(cid):
    for p in ("QCF", "SE", "CY", "AI"):
        if cid.startswith(p):
            return p
    return "SE"

def designated(track):
    """Return (core_ids, adv_ids) for a track, ordered A1..A4 / B1..B4 is not
    encoded, so we order by appearance in COURSE_ORDER."""
    core = [c for c in COURSE_ORDER if COURSES[c][3][track] == "A"]
    adv = [c for c in COURSE_ORDER if COURSES[c][3][track] == "B"]
    return core, adv

# ----------------------------------------------------------------------------
# HTML helpers
# ----------------------------------------------------------------------------
def e(s):
    return html.escape(str(s), quote=True)

def page(title, body, depth, accent=None):
    p = "" if depth == 0 else "../"
    style = f' style="--accent:#{accent}"' if accent else ""
    nav = nav_html("", p) if depth == 0 else body_nav(p)
    return f"""<!DOCTYPE html>
<html lang="en"{style}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<link rel="stylesheet" href="{p}style.css">
</head>
<body>
{body}
<footer>
  <div class="wrap">
    <span class="foot-brand"><img class="foot-logo" src="{p}assets/hit-logo.png" alt="HIT logo"> Holon Institute of Technology &middot; Undergraduate Computer Science</span>
    <a href="{p}index.html">Program overview</a>
  </div>
</footer>
</body>
</html>"""

def body_nav(p):  # unused placeholder
    return ""

def nav_html(active, p):
    links = [("Overview", f"{p}index.html", active == "home")]
    for t in TRACK_ORDER:
        links.append((TRACKS[t]["name"],
                      f"{p}concentrations/{t}.html", active == t))
    links.append(("Careers", f"{p}careers.html", active == "careers"))
    items = "".join(
        f'<a class="{"on" if on else ""}" href="{e(href)}">{e(label)}</a>'
        for label, href, on in links)
    return f"""<header class="topbar">
  <div class="wrap">
    <a class="brand" href="{p}index.html"><img class="logo" src="{p}assets/hit-logo.png" alt="HIT logo"> <span>HIT &middot; CS Concentrations</span></a>
    <nav>{items}</nav>
  </div>
</header>"""

def cell(track, role):
    """Regular-path matrix cell (A = semester 1, B = semester 2, elective)."""
    c = TRACKS[track]
    if role == "A":
        return f'<td class="m a" data-sort="0" style="background:#{c["color"]}">A</td>'
    if role == "B":
        return f'<td class="m b" data-sort="1" style="background:#{c["soft"]};color:#{c["color"]}">B</td>'
    return '<td class="m e" data-sort="2">&middot;</td>'

# Flexible path: spread each concentration's eight core courses across THREE
# semesters (3, 3, 2) instead of two. FLEX[track][course_id] = semester (1..3).
FLEX = {t: {} for t in TRACK_ORDER}
def _build_flex():
    for t in TRACK_ORDER:
        core = [c for c in COURSE_ORDER if COURSES[c][3][t] == "A"]
        adv = [c for c in COURSE_ORDER if COURSES[c][3][t] == "B"]
        seq = core + adv  # eight core courses in catalogue order
        for i, cid in enumerate(seq):
            FLEX[t][cid] = 1 if i < 3 else (2 if i < 6 else 3)
_build_flex()

def flexcell(track, cid):
    """Flexible-path matrix cell (S1 / S2 / S3, or elective)."""
    c = TRACKS[track]
    sem = FLEX[track].get(cid)
    if sem == 1:
        return f'<td class="m a" data-sort="0" style="background:#{c["color"]}">S1</td>'
    if sem == 2:
        return f'<td class="m b" data-sort="1" style="background:#{c["soft"]};color:#{c["color"]}">S2</td>'
    if sem == 3:
        return f'<td class="m c" data-sort="2" style="color:#{c["ink"]};border:1px solid #{c["color"]}">S3</td>'
    return '<td class="m e" data-sort="3">&middot;</td>'

def build_track_table(table_id, cellfn):
    """Build a sortable course x track table using cellfn(track, cid) for cells."""
    thead = ('<th class="cseq">#</th><th class="cnum">Code</th><th class="cttl">Course</th>'
             + "".join(f'<th class="mh" style="background:#{TRACKS[t]["color"]}">{t}</th>'
                       for t in TRACK_ORDER))
    rows = ""
    for i, cid in enumerate(CORE_COURSES, 1):
        title = COURSES[cid][0]
        cells = "".join(cellfn(t, cid) for t in TRACK_ORDER)
        rows += (f'<tr><td class="cseq" data-sort="{i}">{i}</td>'
                 f'<td class="cnum" data-sort="{e(cid)}">{e(cid)}</td>'
                 f'<td class="cttl" data-sort="{e(title.lower())}"><a href="courses/{cid}.html">{e(title)}</a>'
                 f'<div class="hetx" dir="rtl">{e(COURSE_HE.get(cid,""))}</div></td>'
                 f'{cells}</tr>')
    return (f'<table class="matrix sortable" id="{table_id}">'
            f'<thead><tr>{thead}</tr></thead><tbody>{rows}</tbody></table>')

def filter_bar(table_id):
    """Search box + per-track 'core in' filter + job-role filter for a table."""
    opts = '<option value="">All concentrations</option>' + "".join(
        f'<option value="{t}">Core in {TRACKS[t]["name"]}</option>' for t in TRACK_ORDER)
    role_opts = '<option value="">Any job role</option>' + "".join(
        f'<option value="{t}">{e(r)}</option>' for t in TRACK_ORDER for r in TRACKS[t]["roles"])
    return (f'<div class="filterbar">'
            f'<input class="tfilter" data-target="{table_id}" type="search" placeholder="Filter by course name or code...">'
            f'<select class="tselect" data-target="{table_id}">{opts}</select>'
            f'<select class="tselect" data-target="{table_id}">{role_opts}</select>'
            f'</div>')

def build_base_table():
    """Map the planned core courses to existing HIT courses and flag gaps."""
    n_av = n_pt = n_gap = 0
    rows = ""
    for seq, cid in enumerate(CORE_COURSES, 1):
        fam = course_family(cid)
        col = TRACKS[fam]["color"]
        avail = BASE_AVAILABLE.get(cid, [])
        partial = any(a[3] for a in avail)
        if not avail:
            status, scls = "To develop", "gap"; n_gap += 1
        elif partial:
            status, scls = "Partial", "pt"; n_pt += 1
        else:
            status, scls = "Available", "av"; n_av += 1
        if avail:
            ac = "".join(
                f'<div class="bav"><span class="bnum">{e(a[0])}</span> {e(a[1])}'
                f'<span class="binstr">{e(a[2])}</span>'
                + (f'<span class="bnote">{e(a[3])}</span>' if a[3] else "")
                + '</div>' for a in avail)
        else:
            ac = '<span class="muted">No existing course yet; to be developed.</span>'
        rows += (f'<tr><td class="bseq">{seq}</td>'
                 f'<td class="bcid"><span class="dot" style="background:#{col}"></span>'
                 f'<a href="courses/{cid}.html">{e(cid)}</a></td>'
                 f'<td class="bname"><a href="courses/{cid}.html">{e(COURSES[cid][0])}</a></td>'
                 f'<td>{ac}</td>'
                 f'<td><span class="bstatus {scls}">{status}</span></td></tr>')
    summary = (f'<div class="legend"><span><i class="sw" style="background:#1F6F54"></i> '
               f'{n_av} available</span><span><i class="sw" style="background:#B5530B"></i> '
               f'{n_pt} partial</span><span><i class="sw" style="background:#9C3B2E"></i> '
               f'{n_gap} to develop</span><span class="muted">of {len(CORE_COURSES)} core courses</span></div>')
    table = (f'<table class="basetbl"><thead><tr><th>#</th><th>Core course</th><th>Title</th>'
             f'<th>Currently available at HIT</th><th>Status</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    return summary + '<div class="tablewrap">' + table + '</div>'

# ----------------------------------------------------------------------------
# PAGE: INDEX
# ----------------------------------------------------------------------------
def build_index():
    p = ""
    cards = ""
    for t in TRACK_ORDER:
        c = TRACKS[t]
        core, adv = designated(t)
        roles = "".join(f'<span class="chip" style="background:#{c["soft"]};color:#{c["color"]}">{e(r)}</span>'
                        for r in c["roles"][:3])
        cards += f"""
      <a class="ccard" style="--accent:#{c['color']};--soft:#{c['soft']}" href="concentrations/{t}.html">
        <div class="ccard-top">
          <span class="ccard-tag">Concentration</span>
          <h3>{e(c['name'])}</h3>
          <div class="hetx" dir="rtl">{e(c.get('he',''))}</div>
        </div>
        <p class="ccard-tagline">{e(c['tag'])}</p>
        <p class="hetx" dir="rtl">{e(c.get('tag_he',''))}</p>
        <div class="chip-label">Potential job roles</div>
        <div class="chips">{roles}</div>
      </a>"""

    pillars_html = ""
    for i, (ptitle, pc, ps, bullets) in enumerate(PILLARS, 1):
        blis = "".join(f"<li>{b}</li>" for b in bullets)  # bullets carry inline HTML
        pillars_html += f"""
      <div class="pcard" style="background:#{ps}">
        <div class="pcard-head"><span class="pnum" style="background:#{pc}">{i}</span><h3>{e(ptitle)}</h3></div>
        <ul>{blis}</ul>
      </div>"""

    # course x track tables (regular 2-semester path, flexible 3-semester path)
    matrix_regular = build_track_table("catalogRegular", lambda t, cid: cell(t, COURSES[cid][3][t]))
    matrix_flexible = build_track_table("catalogFlexible", flexcell)

    # Shared elective catalogue, grouped by domain
    dom_names = {"SE": "Software Engineering", "AI": "AI & Robotics",
                 "CY": "Networking & Cyber Security"}
    extra_html = ""
    for dom in ("SE", "AI", "CY"):
        rows = [x for x in ELECTIVE_CATALOGUE if x[5] == dom]
        if not rows:
            continue
        col = TRACKS[dom]["color"]
        ecards = ""
        for num, en, he, cr, instr, _d, cat in rows:
            ecards += (f'<div class="ecard">'
                       f'<div class="ecard-top"><span class="ecode">{e(num)}</span>'
                       f'<span class="ecat" style="background:#{TRACKS[dom]["soft"]};color:#{col}">{e(cat)}</span>'
                       f'<span class="ecr">{e(cr)} cr</span></div>'
                       f'<div class="ename">{e(en)}</div>'
                       f'<div class="ehe" dir="rtl">{e(he)}</div>'
                       f'<div class="einstr">{e(instr)}</div></div>')
        extra_html += (f'<h3 class="pathhead" style="color:#{col}">{e(dom_names[dom])} '
                       f'<span class="lbl">{len(rows)} electives</span></h3>'
                       f'<div class="egrid">{ecards}</div>')

    body = f"""{nav_html('home', p)}
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">UNDERGRADUATE CS PROGRAM</p>
    <h1>Degree Concentrations</h1>
    <p class="lead">Six specialization tracks students choose in their third year. Each is a focused sequence of eight core courses built on one shared computer-science backbone.</p>
  </div>
</section>

<main class="wrap">
  <section class="block">
    <h2>The Concentration Model</h2>
    <p>Every student completes a shared computer-science core, then chooses one concentration: a curated sequence of <b>eight core courses</b>, across two semesters (three on the flexible program), that turns a broad CS foundation into a job-ready specialization. Each concentration equips a complete toolbox for a <a href="careers.html">cluster of roles</a>, pairs academic rigor with state-of-the-art tools, and produces a demonstrable portfolio of project-based work, all while reusing a shared core so courses stay cross-disciplinary. Six principles shape how every concentration is designed:</p>
    <div class="pillars">{pillars_html}
    </div>
  </section>

  <section class="block">
    <h2>The six concentrations <span class="hetx" dir="rtl">שש האשכולות</span></h2>
    <div class="cgrid">{cards}
    </div>
  </section>

  <section class="block">
    <h2>Core course catalogue &amp; track map</h2>
    <p class="muted">Every course below is a <b>core course</b> in one or more concentrations and an <b>elective</b> to the others. The same eight core courses can be scheduled two ways. Click a course to open it; click any column header to sort.</p>

    <details class="collapse" open>
      <summary><span class="pathhead">Regular Path <span class="lbl">2 semesters</span></span><span class="toggle"><span class="toggle-show">Show</span><span class="toggle-hide">Hide</span></span></summary>
      <p class="muted">Within a concentration, core courses are taught in the <b>first semester (A)</b> or <b>second semester (B)</b>.</p>
      <div class="legend">
        <span><i class="sw" style="background:#14385C"></i> Core &middot; semester 1 (A)</span>
        <span><i class="sw" style="background:#94A3B8"></i> Core &middot; semester 2 (B)</span>
        <span><i class="sw e"></i> Elective to that concentration</span>
      </div>
      {filter_bar('catalogRegular')}
      <div class="tablewrap">{matrix_regular}</div>
    </details>

    <details class="collapse">
      <summary><span class="pathhead">Flexible Path <span class="lbl">3 semesters</span></span><span class="toggle"><span class="toggle-show">Show</span><span class="toggle-hide">Hide</span></span></summary>
      <p class="muted">A lighter schedule that spreads the same eight core courses across <b>three semesters</b> (three, three, then two), for students who want a gentler load or room for more electives.</p>
      <div class="legend">
        <span><i class="sw" style="background:#14385C"></i> Semester 1 (S1)</span>
        <span><i class="sw" style="background:#94A3B8"></i> Semester 2 (S2)</span>
        <span><i class="sw" style="background:#fff;border:1px solid #14385C"></i> Semester 3 (S3)</span>
        <span><i class="sw e"></i> Elective to that concentration</span>
      </div>
      {filter_bar('catalogFlexible')}
      <div class="tablewrap">{matrix_flexible}</div>
    </details>
  </section>

  <section class="block">
    <details class="collapse">
      <summary><h2>Base courses: current coverage &amp; gaps</h2><span class="toggle"><span class="toggle-show">Show</span><span class="toggle-hide">Hide</span></span></summary>
      <p class="muted">How each planned core course maps to a course HIT already runs, and where new courses still need to be built.</p>
      {build_base_table()}
    </details>
  </section>

  <section class="block">
    <details class="collapse">
      <summary><h2>Selected elective catalogue</h2><span class="toggle"><span class="toggle-show">Show</span><span class="toggle-hide">Hide</span></span></summary>
      <p class="muted">A selection of example electives, open to every concentration, that deepen or broaden a student's expertise beyond the core eight. These are examples, not the full list; the elective catalogue is larger and grows over time.</p>
      {extra_html}
    </details>
  </section>
</main>
<script>{TABLE_JS}</script>"""
    write("index.html", page("CS Degree Concentrations", body, 0))

# ----------------------------------------------------------------------------
# PAGE: CAREERS
# ----------------------------------------------------------------------------
def build_careers():
    if not CAREERS:
        return
    sections = ""
    for t in TRACK_ORDER:
        c = TRACKS[t]
        roles = [(slug, r) for slug, r in CAREERS.items() if r.get("concentration") == t]
        if not roles:
            continue
        cards = ""
        for slug, r in roles:
            def col(title, items):
                lis = "".join(f"<li>{e(x)}</li>" for x in items)
                return f'<div class="rcol"><h4>{title}</h4><ul>{lis}</ul></div>'
            emp = ""
            if r.get("example_employers"):
                chips = "".join(f'<span class="chip" style="background:#{c["soft"]};color:#{c["color"]}">{e(x)}</span>'
                                for x in r["example_employers"])
                emp = f'<div class="employers"><h4>Example employers</h4><div class="chips">{chips}</div></div>'
            he = (f'<span class="rhe" dir="rtl">{e(r["title_he"])}</span>' if r.get("title_he") else "")
            cards += f"""
      <article class="role" id="{e(slug)}" style="--accent:#{c['color']}">
        <p class="role-eyebrow">Job role</p>
        <div class="role-head"><h3>{e(r['title'])}{he}</h3>
          <a class="role-conc" href="concentrations/{t}.html" style="background:#{c['soft']};color:#{c['color']}">Concentration: {e(c['name'])}</a></div>
        <p>{e(r.get('summary',''))}</p>
        <div class="role-grid">
          {col('Responsibilities', r.get('responsibilities', []))}
          {col('Required knowledge', r.get('knowledge', []))}
          {col('Skills', r.get('skills', []))}
          {col('Tools &amp; technologies', r.get('tools', []))}
        </div>
        {emp}
      </article>"""
        sections += f"""
  <section class="block">
    <p class="conc-eyebrow">Concentration</p>
    <h2 style="color:#{c['color']}">{e(c['name'])} <span class="hetx" dir="rtl">{e(c.get('he',''))}</span></h2>
    <p class="muted" style="margin:-.2rem 0 1.1rem">Job roles a graduate of this concentration can step into:</p>
    <div class="roles">{cards}
    </div>
  </section>"""

    body = f"""{nav_html('careers', '')}
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">CAREERS &amp; OUTCOMES</p>
    <h1>Where these concentrations lead</h1>
    <p class="lead">A concentration is a third-year specialization. Each one prepares graduates for a family of job roles. Below, the roles are grouped by the concentration that leads to them, with what you do, the knowledge and skills you need, the tools you use, and example employers for each.</p>
  </div>
</section>
<main class="wrap">{sections}
</main>"""
    write("careers.html", page("Careers & Outcomes | CS Concentrations", body, 0))

# ----------------------------------------------------------------------------
# PAGE: CONCENTRATION
# ----------------------------------------------------------------------------
def build_concentration(t):
    c = TRACKS[t]
    core, adv = designated(t)

    def course_list(ids, kind):
        out = ""
        for n, cid in enumerate(ids, 1):
            title = COURSES[cid][0]
            desc = COURSES[cid][1]
            out += f"""
        <a class="course-row" href="../courses/{cid}.html">
          <span class="tier" style="background:#{c['color']}">{kind}{n}</span>
          <span class="cr-body"><b>{e(title)}</b><span class="hetx" dir="rtl">{e(COURSE_HE.get(cid,""))}</span><small>{e(desc)}</small></span>
          <span class="cr-id">{e(cid)}</span>
        </a>"""
        return out

    # electives available
    electives = [cid for cid in COURSE_ORDER if COURSES[cid][3][t] == "E"]
    elec_html = "".join(
        f'<a class="elec" href="../courses/{cid}.html">{e(cid)} &middot; {e(COURSES[cid][0])}</a>'
        for cid in electives)

    roles = "".join(
        f'<li><a href="../careers.html#{slugify(r)}">{e(r)}</a></li>' for r in c["roles"])

    # Careers & outcomes (target roles + salary + employers)
    careers_section = ""
    croles = [(slug, r) for slug, r in CAREERS.items() if r.get("concentration") == t]
    if croles:
        items, emp_set = "", []
        for slug, r in croles:
            rhe = (f'<span class="rhe" dir="rtl">{e(r["title_he"])}</span>' if r.get("title_he") else "")
            items += (f'<a class="co-role" href="../careers.html#{e(slug)}">'
                      f'<b>{e(r["title"])}</b>{rhe}<span class="co-more">Full profile &rarr;</span></a>')
            for x in r.get("example_employers", []):
                if x not in emp_set:
                    emp_set.append(x)
        emp_chips = "".join(f'<span class="chip" style="background:#{c["soft"]};color:#{c["color"]}">{e(x)}</span>'
                            for x in emp_set[:12])
        emp_block = (f'<h3 class="subhead">Example employers</h3><div class="chips">{emp_chips}</div>'
                     if emp_chips else "")
        careers_section = f"""
      <section class="block">
        <h2>Careers &amp; outcomes</h2>
        <p class="muted">This concentration prepares you for these roles. Open the <a href="../careers.html">careers page</a> for full profiles, responsibilities, and required skills.</p>
        <div class="co-roles">{items}</div>
        {emp_block}
      </section>"""

    body = f"""{nav_html(t, '../')}
<section class="chero" style="--accent:#{c['color']};--ink:#{c['ink']}">
  <div class="wrap">
    <p class="eyebrow">CONCENTRATION</p>
    <h1>{e(c['name'])}</h1>
    <p class="hetx" dir="rtl">{e(c.get('he',''))}</p>
    <p class="lead">{e(c['tag'])}</p>
  </div>
</section>

<main class="wrap conc">
  <section class="block">
    <h2>Rationale</h2>
    <p>{e(c['rationale'])}</p>
  </section>

  <section class="block">
    <h2>Core courses &middot; Semester 1 <span class="lbl">A1 to A4</span></h2>
    <div class="courses">{course_list(core, 'A')}
    </div>
  </section>

  <section class="block">
    <h2>Core courses &middot; Semester 2 <span class="lbl">B1 to B4</span></h2>
    <div class="courses">{course_list(adv, 'B')}
    </div>
  </section>

  {careers_section}
</main>"""
    write(f"concentrations/{t}.html", page(f"{c['name']} | CS Concentrations", body, 1, c['color']))

# ----------------------------------------------------------------------------
# PAGE: COURSE
# ----------------------------------------------------------------------------
def build_course(cid):
    title, desc, topics, roles = COURSES[cid]
    fam = course_family(cid)
    c = TRACKS[fam]

    topic_html = "".join(f'<li>{e(tp)}</li>' for tp in topics)

    # role-in-each-track table
    rrows = ""
    for t in TRACK_ORDER:
        r = roles[t]
        lbl = ROLE_LABEL[r]
        badge = {
            "A": f'<span class="rbadge" style="background:#{TRACKS[t]["color"]};color:#fff">Core &middot; Semester 1</span>',
            "B": f'<span class="rbadge" style="background:#{TRACKS[t]["soft"]};color:#{TRACKS[t]["color"]}">Core &middot; Semester 2</span>',
            "E": '<span class="rbadge e">Elective</span>',
        }[r]
        rrows += (f'<tr><td><a href="../concentrations/{t}.html">{e(TRACKS[t]["name"])}</a></td>'
                  f'<td>{badge}</td></tr>')

    # tracks where this is a core course for the summary line
    req_in = [TRACKS[t]["name"] for t in TRACK_ORDER if roles[t] in ("A", "B")]
    req_line = ("Core course in: " + ", ".join(req_in)) if req_in else "Available as an elective across all tracks."

    # prev / next
    idx = COURSE_ORDER.index(cid)
    prev_id = COURSE_ORDER[idx - 1] if idx > 0 else None
    next_id = COURSE_ORDER[idx + 1] if idx < len(COURSE_ORDER) - 1 else None
    pn = '<div class="prevnext">'
    pn += (f'<a href="{prev_id}.html">&larr; {e(prev_id)} &middot; {e(COURSES[prev_id][0])}</a>'
           if prev_id else '<span></span>')
    pn += (f'<a href="{next_id}.html">{e(next_id)} &middot; {e(COURSES[next_id][0])} &rarr;</a>'
           if next_id else '<span></span>')
    pn += '</div>'

    # ---- detailed syllabus (new schema) ----
    syl = SYLLABI.get(cid, {})
    has_syl = bool(syl.get("weeks"))
    tagline = syl.get("tagline", "")
    objectives = syl.get("objectives", [])
    prereqs = PREREQS.get(cid, [])
    weeks = syl.get("weeks", [])
    tools = syl.get("tools", [])
    refs = syl.get("references", [])
    proj = syl.get("project", {})
    subtitle = syl.get("subtitle", "")
    foundations = syl.get("foundations", [])
    literature = syl.get("literature", [])
    build_txt = syl.get("build", "")

    # "What you'll build" resume-bullet box
    build_box = ""
    if build_txt:
        build_box = (f'<div class="buildbox" style="border-left:4px solid #{c["color"]}">'
                     f'<span class="bk" style="color:#{c["color"]}">What you will build</span>'
                     f'<p>{e(build_txt)}</p></div>')

    # Theoretical foundations
    foundations_section = ""
    if foundations:
        fh = "".join(f"<li>{e(x)}</li>" for x in foundations)
        foundations_section = f"""
      <section class="block">
        <h2>Theoretical foundations</h2>
        <p class="muted">The concepts and results this course rests on.</p>
        <ul class="foundations" style="--accent:#{c['color']}">{fh}</ul>
      </section>"""

    # Free online courses (self-study basis)
    basis_section = ""
    basis = ONLINE_BASIS.get(cid, [])
    if basis:
        bitems = ""
        for r in basis:
            url = r.get("url", "")
            ttl = e(r.get("title", ""))
            ttl_html = (f'<a href="{e(url)}" target="_blank" rel="noopener">{ttl}</a>' if url else f"<b>{ttl}</b>")
            bitems += (f'<li class="ref"><span class="refkind">{e(r.get("provider",""))}</span>'
                       f'<span class="reftitle">{ttl_html}</span>'
                       f'<div class="meta">{e(r.get("note",""))}</div></li>')
        basis_section = f"""
      <section class="block">
        <h2>Free online courses</h2>
        <p class="muted">Existing free, video-based courses this course can build on, for self-study or as a teaching basis.</p>
        <ul class="refs">{bitems}</ul>
      </section>"""

    # Primary literature (seminal works, linked)
    literature_section = ""
    if literature:
        li = ""
        for r in literature:
            meta = ", ".join(b for b in [str(r.get("authors", "")), str(r.get("year", ""))] if b)
            ttl = e(r.get("title", ""))
            url = r.get("url", "")
            ttl_html = (f'<a href="{e(url)}" target="_blank" rel="noopener">{ttl}</a>' if url else f"<b>{ttl}</b>")
            li += (f'<li class="ref"><span class="refkind">Paper</span>'
                   f'<span class="reftitle">{ttl_html}</span><div class="meta">{e(meta)}</div></li>')
        literature_section = f"""
      <section class="block">
        <h2>Primary literature</h2>
        <p class="muted">Seminal works to read for graduate-level depth.</p>
        <ul class="refs">{li}</ul>
      </section>"""

    # Course format callout
    format_section = ""
    if has_syl:
        format_section = f"""
      <div class="formatbox" style="border-left:4px solid #{c['color']}">
        <b>Course format.</b> {e(COURSE_FORMAT_NOTE)}
      </div>"""

    # Expected outcomes
    obj_section = ""
    if objectives:
        obj_html = "".join(f"<li>{e(o)}</li>" for o in objectives)
        obj_section = f"""
      <section class="block">
        <h2>Expected outcomes</h2>
        <ul class="objectives" style="--accent:#{c['color']}">{obj_html}</ul>
      </section>"""

    # Prerequisites (standard assumed background + course-specific)
    prereq_section = ""
    if has_syl:
        ph = "".join(f"<li>{e(x)}</li>" for x in prereqs)
        spec = (f'<p class="muted" style="margin:.2rem 0 .6rem">Course-specific prerequisites:</p>'
                f'<ul class="prereqs" style="--accent:#{c["color"]}">{ph}</ul>') if prereqs else ""
        prereq_section = f"""
      <section class="block">
        <h2>Prerequisites</h2>
        <div class="formatbox" style="border-left:4px solid #{c['color']}">{e(ASSUMED_BACKGROUND)}</div>
        {spec}
      </section>"""

    # Weekly schedule (grouped by part, lecture + practice + project, presentations flagged)
    weeks_section = ""
    if weeks:
        wrows, cur_part = "", None
        for w in weeks:
            part = w.get("part")
            if part and part != cur_part:
                wrows += f'<div class="wpart">{e(part)}</div>'
                cur_part = part
            is_pres = w.get("week") in PRESENTATION_WEEKS
            badge = '<span class="presbadge">Presentation</span>' if is_pres else ""
            if "lecture" in w or "practice" in w:
                rows = (f'<div class="wk-line"><span class="wk-tag lec">Lecture</span>{e(w.get("lecture",""))}</div>'
                        f'<div class="wk-line"><span class="wk-tag pra">Practice</span>{e(w.get("practice",""))}</div>')
                if w.get("project"):
                    rows += f'<div class="wk-proj"><span class="wk-tag prj">Project</span>{e(w["project"])}</div>'
            else:  # legacy fallback
                rows = f'<div class="wk-line">{e(w.get("details",""))}</div>'
            wrows += (f'<div class="week{" pres" if is_pres else ""}">'
                      f'<div class="wk-num" style="color:#{c["color"]}">Wk {e(w.get("week",""))}</div>'
                      f'<div class="wk-body"><b>{e(w.get("title",""))}{badge}</b>{rows}</div></div>')
        weeks_section = f"""
      <section class="block">
        <h2>Weekly schedule <span class="lbl">{len(weeks)} weeks &middot; lecture + practice</span></h2>
        <div class="weeks">{wrows}</div>
      </section>"""

    # Student project: requirements (depth, new systems not exercises) + examples
    project_section = ""
    if has_syl:
        req_html = "".join(f"<li>{e(x)}</li>" for x in PROJECT_REQUIREMENTS)
        summary = proj.get("summary", "")
        ideas = "".join(f'<span class="chip" style="background:#{c["soft"]};color:#{c["color"]}">{e(i)}</span>'
                        for i in proj.get("ideas", []))
        examples_block = (f'<h3 class="subhead">Example projects</h3>'
                          f'<div class="chips">{ideas}</div>') if ideas else ""
        summary_block = f"<p>{e(summary)}</p>" if summary else ""
        project_section = f"""
      <section class="block">
        <h2>Student project</h2>
        {summary_block}
        <h3 class="subhead">Requirements</h3>
        <ul class="objectives" style="--accent:#{c['color']}">{req_html}</ul>
        {examples_block}
      </section>"""

    # Assessment (standard, project-based)
    assessment_section = ""
    if has_syl:
        arows = "".join(
            f'<tr><td><b>{e(comp)}</b></td><td>{e(cov)}</td><td class="wt">{e(wt)}</td></tr>'
            for comp, cov, wt in ASSESSMENT)
        assessment_section = f"""
      <section class="block">
        <h2>Assessment &amp; grading</h2>
        <p class="muted">Grading is project-based, with no written exam. Teams of three or four present one running project three times.</p>
        <table class="assess"><thead><tr><th>Component</th><th>What it covers</th><th>Weight</th></tr></thead><tbody>{arows}</tbody></table>
      </section>"""

    # Tools
    tools_section = ""
    if tools:
        items = ""
        for tdef in tools:
            name, sep, purpose = tdef.partition(":")
            items += (f'<li><b>{e(name.strip())}</b>: {e(purpose.strip())}</li>' if sep
                      else f'<li><b>{e(tdef.strip())}</b></li>')
        tools_section = f"""
      <section class="block">
        <h2>Tools &amp; platforms</h2>
        <ul class="tools" style="--accent:#{c['color']}">{items}</ul>
      </section>"""

    # References (with links)
    refs_section = ""
    if refs:
        ritems = ""
        for r in refs:
            meta_bits = [str(r.get("authors", "")), str(r.get("year", "")), str(r.get("note", ""))]
            meta = ", ".join(b for b in meta_bits if b)
            ttl = e(r.get("title", ""))
            url = r.get("url", "")
            ttl_html = f'<a href="{e(url)}" target="_blank" rel="noopener">{ttl}</a>' if url else f"<b>{ttl}</b>"
            ritems += (f'<li class="ref"><span class="refkind">{e(r.get("kind",""))}</span>'
                       f'<span class="reftitle">{ttl_html}</span><div class="meta">{e(meta)}</div></li>')
        refs_section = f"""
      <section class="block">
        <h2>References</h2>
        <p class="muted">Books and resources link to an online or publisher page.</p>
        <ul class="refs">{ritems}</ul>
      </section>"""

    # sidebar syllabus stats
    syl_stats = ""
    if has_syl:
        syl_stats = f"""
      <div class="side-card">
        <h3>Syllabus</h3>
        <dl>
          <dt>Duration</dt><dd>{len(weeks)} weeks</dd>
          <dt>Per week</dt><dd>2h + 2h</dd>
          <dt>Outcomes</dt><dd>{len(objectives)}</dd>
          <dt>Presentations</dt><dd>3</dd>
          <dt>Tools</dt><dd>{len(tools)}</dd>
          <dt>References</dt><dd>{len(refs)}</dd>
        </dl>
      </div>"""

    lead = tagline if tagline else req_line
    meta_strip = ('<div class="cmeta"><span>Year 3</span><span>13 weeks</span>'
                  '<span>2h lecture + 2h practice</span><span>Project-based</span></div>') if has_syl else ""

    body = f"""{nav_html(fam, '../')}
<section class="chero course" style="--accent:#{c['color']};--ink:#{c['ink']}">
  <div class="wrap">
    <p class="eyebrow">COURSE &middot; {e(cid)}</p>
    <h1>{e(title)}</h1>
    {f'<p class="hetx" dir="rtl">{e(COURSE_HE[cid])}</p>' if cid in COURSE_HE else ''}
    {f'<p class="csub">{e(subtitle)}</p>' if subtitle else ''}
    <p class="lead">{e(lead)}</p>
    {meta_strip}
  </div>
</section>

<main class="wrap course-body">
  <div class="conc-grid">
    <div class="conc-main">
      <section class="block">
        <h2>About this course</h2>
        <p>{e(desc)}</p>
      </section>{format_section}{build_box}{obj_section}
      <section class="block">
        <h2>Key topics</h2>
        <ul class="topics" style="--accent:#{c['color']}">{topic_html}</ul>
      </section>{foundations_section}{prereq_section}{weeks_section}{project_section}{assessment_section}{tools_section}{basis_section}{literature_section}{refs_section}
      <section class="block">
        <h2>Role in each concentration</h2>
        <table class="roletable">
          <thead><tr><th>Concentration</th><th>Role</th></tr></thead>
          <tbody>{rrows}</tbody>
        </table>
      </section>
      {pn}
    </div>
    <aside class="conc-side">
      <div class="side-card" style="border-top:4px solid #{c['color']}">
        <h3>Course</h3>
        <dl>
          <dt>Code</dt><dd>{e(cid)}</dd>
          <dt>Home area</dt><dd><a href="../concentrations/{fam}.html">{e(c['name'])}</a></dd>
        </dl>
        <p class="muted" style="margin:.6rem 0 0;font-size:.85rem">{e(req_line)}</p>
      </div>{syl_stats}
      <div class="side-card">
        <h3>Browse</h3>
        <p class="muted" style="margin:0 0 .5rem">Jump to a concentration:</p>
        <ul class="rolelist" style="--accent:#{c['color']}">
          {''.join(f'<li><a href="../concentrations/{t}.html">{e(TRACKS[t]["name"])}</a></li>' for t in TRACK_ORDER)}
        </ul>
      </div>
    </aside>
  </div>
</main>"""
    write(f"courses/{cid}.html", page(f"{cid}: {title} | CS Concentrations", body, 1, c['color']))

# ----------------------------------------------------------------------------
# CSS
# ----------------------------------------------------------------------------
CSS = """:root{
  --ink:#14385C; --ink2:#2C3138; --muted:#5A626C; --line:#D1D4D8;
  --bg:#FFFFFF; --soft:#F7F8FA; --accent:#14385C;
  --font:"Charter","Iowan Old Style","Source Serif Pro",Georgia,"Times New Roman",serif;
  --serif:"Charter","Iowan Old Style","Source Serif Pro",Georgia,"Times New Roman",serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:var(--font);color:var(--ink2);background:var(--bg);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.5rem}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{font-family:var(--serif);color:var(--ink);line-height:1.15}

/* top bar */
.topbar{position:sticky;top:0;z-index:20;background:rgba(20,56,92,.97);backdrop-filter:blur(6px);border-bottom:1px solid rgba(255,255,255,.12)}
.topbar .wrap{display:flex;align-items:center;justify-content:space-between;min-height:58px;padding-top:.35rem;padding-bottom:.35rem;gap:1rem}
.brand{color:#fff;font-weight:700;font-size:1.02rem;display:flex;align-items:center;gap:.55rem}
.brand:hover{text-decoration:none}
.logo{height:30px;width:auto;display:block;background:#fff;border-radius:4px;padding:2px}
.topbar nav{display:flex;gap:.25rem;flex-wrap:wrap}
.topbar nav a{color:#CBD5E1;font-size:.82rem;padding:.35rem .6rem;border-radius:6px}
.topbar nav a:hover{color:#fff;background:rgba(255,255,255,.08);text-decoration:none}
.topbar nav a.on{color:#fff;background:rgba(255,255,255,.14)}

/* hero (home) */
.hero{background:var(--ink);color:#fff;padding:3.2rem 0 2.6rem;
  background-image:linear-gradient(120deg,#14385C 0%,#0F2A45 100%)}
.eyebrow{font-family:var(--mono);font-size:.74rem;letter-spacing:.22em;color:#94A3B8;margin:0 0 .6rem}
.hero h1{font-size:3.1rem;margin:0 0 .8rem;color:#fff}
.lead{font-size:1.18rem;color:#CBD5E1;max-width:46rem;margin:0}
.stats{display:flex;gap:1rem;margin-top:2rem;flex-wrap:wrap}
.stat{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:1rem 1.3rem;min-width:170px}
.stat b{font-family:var(--serif);font-size:2.4rem;color:#fff;display:block;line-height:1}
.stat span{font-size:.84rem;color:#94A3B8;display:block;margin-top:.3rem}

/* blocks */
main{padding:2.6rem 0 3rem}
.block{margin:0 0 2.6rem}
.block h2{font-size:1.7rem;margin:0 0 .8rem}
.block h2 .lbl,.lbl{font-family:var(--mono);font-size:.8rem;color:var(--muted);font-weight:400;letter-spacing:.05em}
.muted{color:var(--muted)}
.why{list-style:none;padding:0;margin:1.2rem 0 0;display:grid;grid-template-columns:1fr 1fr;gap:.7rem 1.5rem}
.why li{padding-left:1.1rem;position:relative}
.why li:before{content:'';position:absolute;left:0;top:.62em;width:.45rem;height:.45rem;border-radius:50%;background:var(--accent)}

/* six pillars */
.pillars{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.pcard{border-radius:14px;padding:1.2rem 1.3rem;border:1px solid rgba(15,23,42,.05)}
.pcard-head{display:flex;align-items:center;gap:.6rem;margin-bottom:.55rem}
.pcard .pnum{flex:none;width:2rem;height:2rem;border-radius:8px;color:#fff;font-weight:700;font-family:var(--serif);
  display:flex;align-items:center;justify-content:center;font-size:1.1rem}
.pcard h3{font-size:1.18rem;margin:0}
.pcard ul{margin:0;padding-left:1.05rem}
.pcard li{font-size:.91rem;line-height:1.5;margin-bottom:.4rem;color:var(--ink2)}
.pcard li:last-child{margin-bottom:0}
.pcard li b{color:var(--ink)}

/* concentration grid (home) */
.cgrid{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem}
.ccard{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:14px;padding:1.3rem 1.4rem;color:var(--ink2);
  border-left:5px solid var(--accent);transition:box-shadow .15s,transform .15s;background:#fff}
.ccard .chip-label{margin-top:.2rem;padding-top:.5rem}
.ccard:hover{text-decoration:none;box-shadow:0 12px 30px -12px rgba(15,23,42,.25);transform:translateY(-2px)}
.ccard-tag{font-family:var(--mono);font-size:.74rem;font-weight:700;color:var(--accent);background:var(--soft);padding:.15rem .5rem;border-radius:5px}
.ccard h3{font-size:1.3rem;margin:.5rem 0 0;min-height:3rem}
.ccard p{margin:.5rem 0 .9rem;color:var(--muted);font-size:.96rem}
.ccard .ccard-tagline{margin:.5rem 0 .15rem;min-height:3.1rem}
.ccard p.hetx{margin:0 0 .7rem;min-height:2.3rem}
.chips{display:flex;flex-wrap:wrap;gap:.4rem}
.chip{font-size:.74rem;font-weight:600;padding:.22rem .55rem;border-radius:20px}
.chip-label{font-family:var(--mono);font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:.1rem 0 .4rem}
.role-eyebrow{font-family:var(--mono);font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);margin:0 0 .25rem}
.conc-eyebrow{font-family:var(--mono);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:0 0 .15rem}
.ccard-meta{margin-top:1rem;font-size:.82rem;color:var(--muted);font-family:var(--mono);display:flex;justify-content:space-between;align-items:center}
.ccard-meta .go{font-size:1.1rem;color:var(--accent)}

/* legend + matrix */
.legend{display:flex;gap:1.4rem;flex-wrap:wrap;margin:.4rem 0 1rem;font-size:.84rem;color:var(--muted)}
.legend .sw{display:inline-block;width:.8rem;height:.8rem;border-radius:3px;vertical-align:-1px;margin-right:.35rem}
.legend .sw.e{background:#fff;border:1px solid var(--line)}
.tablewrap{overflow-x:auto}
.matrix{border-collapse:collapse;width:100%;font-size:.86rem;min-width:640px}
.matrix th,.matrix td{border:1px solid var(--line);padding:.4rem .5rem}
.matrix thead th{background:var(--ink);color:#fff;font-family:var(--mono);font-size:.78rem;font-weight:700;text-align:center}
.matrix th.cttl{text-align:left}
.matrix .cseq{font-family:var(--mono);font-size:.76rem;color:var(--muted);text-align:center;white-space:nowrap;width:2.2rem}
.matrix .cnum{font-family:var(--mono);font-size:.76rem;color:var(--muted);text-align:center;white-space:nowrap}
.matrix .cttl{font-size:.86rem}
.matrix .cttl a{color:var(--ink2)}
.matrix .mh a{display:block}
.matrix tbody tr:nth-child(even){background:#F8FAFC}
.matrix td.m{text-align:center;font-family:var(--mono);font-weight:700;width:58px}
.matrix td.m.a{color:#fff}
.matrix td.m.e{color:#CBD5E1;font-weight:400}
/* sortable headers + filter bar */
.matrix.sortable thead th{cursor:pointer;user-select:none;position:relative}
.matrix.sortable thead th:hover{filter:brightness(1.15)}
.matrix.sortable thead th:after{content:' \\21C5';font-size:.74rem;opacity:.45;margin-left:.15rem}
.matrix.sortable thead th:hover:after{opacity:.85}
.matrix.sortable thead th[data-dir=asc]:after{content:' \\25B2';font-size:.66rem;opacity:1}
.matrix.sortable thead th[data-dir=desc]:after{content:' \\25BC';font-size:.66rem;opacity:1}
.pathhead{font-size:1.25rem;margin:1.8rem 0 .35rem}
/* collapsible sections */
.collapse{margin:.5rem 0 1.4rem}
.collapse>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:.7rem;
  padding:.65rem .95rem;background:var(--soft);border:1px solid var(--line);border-radius:8px}
.collapse>summary:hover{background:#EBEEF2}
.collapse>summary::-webkit-details-marker{display:none}
.collapse>summary::before{content:'';width:0;height:0;flex:none;
  border-left:8px solid var(--accent);border-top:6px solid transparent;border-bottom:6px solid transparent;
  transition:transform .15s ease}
.collapse[open]>summary::before{transform:rotate(90deg)}
.collapse[open]>summary{margin-bottom:.9rem}
.collapse>summary h2,.collapse>summary .pathhead{margin:0}
.collapse>summary .toggle{margin-left:auto;font-family:var(--mono);font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--accent)}
.collapse[open]>summary .toggle-show{display:none}
.collapse:not([open])>summary .toggle-hide{display:none}
.pathhead .lbl{font-family:var(--mono);font-size:.78rem;color:var(--muted);font-weight:400;background:var(--soft);padding:.12rem .5rem;border-radius:5px;margin-left:.4rem;vertical-align:2px}
.filterbar{display:flex;gap:.6rem;flex-wrap:wrap;margin:.2rem 0 .7rem}
.filterbar input,.filterbar select{font:inherit;font-size:.88rem;padding:.45rem .65rem;border:1px solid var(--line);border-radius:8px;background:#fff;color:var(--ink2)}
.filterbar input{flex:1;min-width:220px}
.filterbar input:focus,.filterbar select:focus{outline:none;border-color:var(--accent)}

/* concentration / course hero */
.chero{color:#fff;padding:2.6rem 0 2.2rem;
  background-image:linear-gradient(120deg,var(--ink) 0%,var(--accent) 230%)}
.chero h1{color:#fff;font-size:2.5rem;margin:0 0 .5rem}
.chero .eyebrow{color:rgba(255,255,255,.75)}
.chero .lead{color:rgba(255,255,255,.92)}
.chero.course .lead{font-size:1.02rem}

/* concentration body */
.conc-grid{display:grid;grid-template-columns:1fr 300px;gap:2.2rem;align-items:start}
.courses{display:flex;flex-direction:column;gap:.55rem}
.course-row{display:flex;align-items:center;gap:.9rem;border:1px solid var(--line);border-radius:10px;
  padding:.7rem .9rem;background:#fff;color:var(--ink2)}
.course-row:hover{text-decoration:none;border-color:var(--accent);box-shadow:0 6px 16px -10px rgba(15,23,42,.3)}
.tier{flex:none;width:2.4rem;height:2.4rem;border-radius:8px;color:#fff;font-family:var(--mono);font-weight:700;
  display:flex;align-items:center;justify-content:center;font-size:.92rem}
.cr-body{display:flex;flex-direction:column;flex:1;min-width:0}
.cr-body b{color:var(--ink);font-size:1rem}
.cr-body small{color:var(--muted);font-size:.84rem;line-height:1.35}
.cr-id{font-family:var(--mono);font-size:.78rem;color:var(--muted);flex:none}
.elecs{display:flex;flex-direction:column;gap:.3rem}
.elec{font-size:.9rem;padding:.35rem .2rem;border-bottom:1px dashed var(--line);color:var(--ink2)}
.elec:hover{color:var(--accent)}

/* sidebar */
.conc-side{display:flex;flex-direction:column;gap:1rem;position:sticky;top:74px}
.side-card{border:1px solid var(--line);border-radius:12px;padding:1.1rem 1.2rem;background:#fff}
.side-card h3{font-size:1.05rem;margin:0 0 .7rem}
.side-card dl{margin:0;display:grid;grid-template-columns:1fr auto;gap:.4rem .8rem;font-size:.9rem}
.side-card dt{color:var(--muted)}
.side-card dd{margin:0;text-align:right;font-weight:600;color:var(--ink)}
.rolelist{list-style:none;margin:0;padding:0}
.rolelist li{padding:.35rem 0 .35rem 1.1rem;position:relative;font-size:.92rem;border-bottom:1px solid var(--line)}
.rolelist li:last-child{border-bottom:0}
.rolelist li:before{content:'';position:absolute;left:0;top:.85em;width:.42rem;height:.42rem;border-radius:50%;background:var(--accent)}

/* course page */
.topics{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.5rem .9rem}
.topics li{padding-left:1.4rem;position:relative;font-size:.96rem}
.topics li:before{content:'\\2713';position:absolute;left:0;top:0;color:var(--accent);font-weight:700}

/* syllabus: objectives, tools, weekly plan, references */
.objectives{list-style:none;padding:0;margin:0}
.objectives li{position:relative;padding:.4rem 0 .4rem 1.7rem;font-size:.97rem;border-bottom:1px solid var(--line)}
.objectives li:last-child{border-bottom:0}
.objectives li:before{content:'\\2713';position:absolute;left:0;top:.42rem;color:var(--accent);font-weight:700}
.tools{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.45rem 1.2rem}
.tools li{position:relative;padding-left:.95rem;font-size:.92rem;line-height:1.45}
.tools li:before{content:'';position:absolute;left:0;top:.55em;width:.4rem;height:.4rem;border-radius:50%;background:var(--accent)}
.tools b{color:var(--ink)}
.formatbox{background:var(--soft);border-radius:10px;padding:.85rem 1.1rem;margin:0 0 1.6rem;font-size:.95rem}
.csub{font-family:var(--serif);font-style:italic;font-size:1.18rem;color:rgba(255,255,255,.92);margin:.1rem 0 .5rem;max-width:48rem;line-height:1.35}
/* Hebrew co-text, light grey */
.hetx{color:#9AA3AE;font-size:.85rem;font-weight:400;line-height:1.35}
.chero .hetx,.hero .hetx{color:rgba(255,255,255,.72);font-size:1.05rem;margin:.1rem 0 .5rem}
.ccard .hetx{margin-top:.15rem}
.role-head .rhe{color:#9AA3AE;font-size:.92rem;font-weight:400;margin-right:.5rem;font-family:var(--font)}
.co-role .rhe{color:#9AA3AE;font-size:.8rem;display:block;margin:.15rem 0 .3rem}
h2 .hetx{font-size:1rem;font-weight:400}
.buildbox{background:var(--soft);border-radius:10px;padding:.85rem 1.1rem;margin:0 0 1.6rem}
.buildbox .bk{font-family:var(--mono);font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;display:block;margin-bottom:.25rem}
.buildbox p{margin:0;font-size:.97rem;color:var(--ink2)}
.foundations{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:.4rem 1.3rem}
.foundations li{position:relative;padding-left:1.1rem;font-size:.93rem;line-height:1.45;color:var(--ink2)}
.foundations li:before{content:'\\25B8';position:absolute;left:0;top:.02rem;color:var(--accent)}
.prereqs{list-style:none;padding:0;margin:0}
.prereqs li{position:relative;padding:.35rem 0 .35rem 1.3rem;font-size:.95rem;border-bottom:1px solid var(--line)}
.prereqs li:last-child{border-bottom:0}
.prereqs li:before{content:'\\203A';position:absolute;left:.2rem;top:.32rem;color:var(--accent);font-weight:700}
.weeks{border:1px solid var(--line);border-radius:12px;overflow:hidden}
.wpart{background:var(--ink);color:#fff;font-family:var(--mono);font-size:.74rem;font-weight:700;letter-spacing:.05em;
  text-transform:uppercase;padding:.5rem .9rem}
.week{display:flex;gap:1rem;padding:.85rem .9rem;border-bottom:1px solid var(--line)}
.week:last-child{border-bottom:0}
.week.pres{background:#FFFBEB}
.wk-num{flex:none;width:2.6rem;font-family:var(--mono);font-size:.8rem;font-weight:700;padding-top:.15rem}
.wk-body{flex:1;min-width:0}
.wk-body>b{color:var(--ink);font-size:.99rem;display:block;margin-bottom:.4rem}
.wk-line,.wk-proj{font-size:.89rem;color:var(--ink2);line-height:1.5;margin-top:.25rem}
.wk-proj{color:var(--muted)}
.wk-tag{display:inline-block;font-family:var(--mono);font-size:.62rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;
  padding:.1rem .4rem;border-radius:4px;margin-right:.5rem;vertical-align:1px}
.wk-tag.lec{background:#E0E7FF;color:#3730A3}
.wk-tag.pra{background:#DCFCE7;color:#166534}
.wk-tag.prj{background:var(--soft);color:var(--muted)}
.presbadge{display:inline-block;font-family:var(--mono);font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;
  background:#F59E0B;color:#fff;padding:.1rem .45rem;border-radius:4px;margin-left:.55rem;vertical-align:2px}
.assess{border-collapse:collapse;width:100%;font-size:.92rem}
.assess th,.assess td{border-bottom:1px solid var(--line);padding:.55rem .5rem;text-align:left;vertical-align:top}
.assess th{font-family:var(--mono);font-size:.74rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.assess .wt{font-family:var(--mono);font-weight:700;color:var(--ink);text-align:right;white-space:nowrap}
.refs{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.55rem}
.ref{padding:.6rem .85rem;border:1px solid var(--line);border-radius:10px;background:#fff}
.ref .reftitle{font-weight:700;color:var(--ink);font-size:.97rem}
.ref .reftitle a{color:var(--accent)}
.ref .meta{font-size:.84rem;color:var(--muted);margin-top:.15rem}
.refkind{display:inline-block;font-family:var(--mono);font-size:.66rem;font-weight:700;text-transform:uppercase;
  letter-spacing:.05em;padding:.12rem .45rem;border-radius:4px;background:var(--soft);color:var(--muted);margin-right:.55rem;vertical-align:1px}
.cmeta{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem}
.cmeta span{font-family:var(--mono);font-size:.74rem;background:rgba(255,255,255,.16);color:#fff;padding:.25rem .6rem;border-radius:6px}
.rolelist li a{color:var(--ink2)}
.rolelist li a:hover{color:var(--accent)}

/* careers page */
.roles{display:flex;flex-direction:column;gap:1.1rem}
.role{border:1px solid var(--line);border-radius:14px;padding:1.3rem 1.4rem;background:#fff;border-left:5px solid var(--accent)}
.role-head{display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;margin-bottom:.4rem}
.role-head h3{font-size:1.4rem;margin:0}
.role-conc{font-size:.78rem;font-weight:700;padding:.2rem .6rem;border-radius:20px;white-space:nowrap}
.role-conc:hover{text-decoration:none;filter:brightness(.95)}
.role-grid{display:grid;grid-template-columns:1fr 1fr;gap:.6rem 1.6rem;margin-top:.6rem}
.rcol h4{font-family:var(--mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent);margin:.4rem 0 .35rem}
.rcol ul{margin:0;padding-left:1.05rem}
.rcol li{font-size:.9rem;line-height:1.45;margin-bottom:.25rem;color:var(--ink2)}
.employers{margin-top:.9rem;border-top:1px solid var(--line);padding-top:.8rem}
.employers h4{font-family:var(--mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.05em;color:var(--muted);margin:0 0 .5rem}

/* careers & outcomes block on concentration pages */
.co-roles{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7rem;margin-bottom:.4rem}
.co-role{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:10px;padding:.75rem .85rem;color:var(--ink2);border-top:3px solid var(--accent)}
.co-role:hover{text-decoration:none;box-shadow:0 6px 16px -10px rgba(20,56,92,.3)}
.co-role b{color:var(--ink);font-size:1rem}
.co-sal{font-size:.78rem;color:var(--muted);margin:.3rem 0 .5rem;line-height:1.4}
.co-more{font-family:var(--mono);font-size:.74rem;color:var(--accent);margin-top:auto}

/* shared elective catalogue */
.egrid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7rem}
.ecard{border:1px solid var(--line);border-radius:10px;padding:.7rem .8rem;background:#fff;display:flex;flex-direction:column;gap:.2rem}
.ecard-top{display:flex;align-items:center;gap:.4rem;flex-wrap:wrap}
.ecode{font-family:var(--mono);font-size:.74rem;font-weight:700;color:var(--muted)}
.ecat{font-size:.66rem;font-weight:700;padding:.1rem .4rem;border-radius:4px}
.ecr{margin-left:auto;font-family:var(--mono);font-size:.72rem;color:var(--muted)}
.ename{font-weight:700;color:var(--ink);font-size:.94rem;line-height:1.25}
.ehe{font-size:.84rem;color:var(--muted);line-height:1.3}
.einstr{font-size:.8rem;color:var(--muted);font-style:italic}

/* base courses coverage table */
.basetbl{border-collapse:collapse;width:100%;font-size:.88rem;min-width:760px}
.basetbl th,.basetbl td{border:1px solid var(--line);padding:.5rem .6rem;text-align:left;vertical-align:top}
.basetbl thead th{background:var(--ink);color:#fff;font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.04em}
.basetbl .bseq{font-family:var(--mono);font-size:.78rem;color:var(--muted);text-align:center;width:2.2rem}
.basetbl .bcid{font-family:var(--mono);font-weight:700;white-space:nowrap}
.basetbl .bcid a{color:var(--ink2)}
.dot{display:inline-block;width:.55rem;height:.55rem;border-radius:50%;margin-right:.35rem;vertical-align:1px}
.bname{font-weight:600;color:var(--ink)}
.bname a{color:var(--ink)}
.bname a:hover{color:var(--accent)}
.bav{margin-bottom:.35rem}
.bav:last-child{margin-bottom:0}
.bnum{font-family:var(--mono);font-size:.78rem;color:var(--muted);margin-right:.3rem}
.binstr{display:block;font-size:.8rem;color:var(--muted);font-style:italic}
.bnote{display:block;font-size:.8rem;color:#B5530B;margin-top:.15rem}
.bstatus{display:inline-block;font-family:var(--mono);font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;padding:.15rem .5rem;border-radius:20px;white-space:nowrap}
.bstatus.av{background:#E1F0E9;color:#1F6F54}
.bstatus.pt{background:#FBEEDE;color:#B5530B}
.bstatus.gap{background:#F6E7E4;color:#9C3B2E}
.roletable{border-collapse:collapse;width:100%;font-size:.92rem}
.roletable th,.roletable td{border-bottom:1px solid var(--line);padding:.6rem .4rem;text-align:left}
.roletable th{font-family:var(--mono);font-size:.78rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}
.rbadge{font-size:.76rem;font-weight:700;padding:.2rem .6rem;border-radius:20px}
.rbadge.e{background:var(--soft);color:var(--muted)}
.prevnext{display:flex;justify-content:space-between;gap:1rem;margin-top:1.5rem;font-size:.86rem;font-family:var(--mono)}
.prevnext a{padding:.5rem .2rem}

/* footer */
footer{border-top:1px solid var(--line);background:var(--soft);padding:1.4rem 0;margin-top:1rem}
footer .wrap{display:flex;justify-content:space-between;align-items:center;font-size:.84rem;color:var(--muted);gap:1rem;flex-wrap:wrap}
.foot-brand{display:flex;align-items:center;gap:.5rem}
.foot-logo{height:22px;width:auto;background:#fff;border-radius:3px;padding:1px}
.subhead{font-size:1.1rem;margin:1.4rem 0 .55rem;color:var(--ink)}

@media(max-width:900px){.pillars{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.pillars{grid-template-columns:1fr}}
@media(max-width:820px){
  .cgrid,.why,.topics,.tools,.role-grid,.co-roles,.egrid,.foundations{grid-template-columns:1fr}
  .conc-grid{grid-template-columns:1fr}
  .conc-side{position:static;flex-direction:row;flex-wrap:wrap}
  .side-card{flex:1;min-width:220px}
  .hero h1{font-size:2.3rem}
  .chero h1{font-size:1.9rem}
}
"""

# ----------------------------------------------------------------------------
# Client-side sort + filter for the catalogue tables (vanilla JS, no deps).
TABLE_JS = r"""
(function(){
  function sortVal(cell){
    var v = cell.getAttribute('data-sort'); if(v===null) v = cell.textContent;
    v = (v||'').trim(); var n = parseFloat(v);
    return isNaN(n) ? v.toLowerCase() : n;
  }
  function sortTable(table, idx, asc){
    var tbody = table.tBodies[0];
    var rows = Array.prototype.slice.call(tbody.rows);
    rows.sort(function(a,b){
      var x = sortVal(a.cells[idx]), y = sortVal(b.cells[idx]);
      if(x<y) return asc?-1:1; if(x>y) return asc?1:-1; return 0;
    });
    rows.forEach(function(r){ tbody.appendChild(r); });
    table._sortIdx = idx; table._sortAsc = asc;
    var ths = table.tHead.rows[0].cells;
    Array.prototype.forEach.call(ths, function(h){ h.removeAttribute('data-dir'); });
    ths[idx].setAttribute('data-dir', asc ? 'asc' : 'desc');
  }
  document.querySelectorAll('table.sortable').forEach(function(table){
    Array.prototype.forEach.call(table.tHead.rows[0].cells, function(th, idx){
      th.addEventListener('click', function(){
        var asc = !(table._sortIdx === idx && table._sortAsc);
        sortTable(table, idx, asc);
      });
    });
  });
  function colIndex(table, code){
    var ths = table.tHead.rows[0].cells;
    for(var i=0;i<ths.length;i++){ if(ths[i].textContent.trim()===code) return i; }
    return -1;
  }
  function applyFilter(id){
    var table = document.getElementById(id); if(!table) return;
    var search = document.querySelector('.tfilter[data-target="'+id+'"]');
    var q = ((search && search.value) || '').toLowerCase();
    var sels = document.querySelectorAll('.tselect[data-target="'+id+'"]');
    var cols = [];
    Array.prototype.forEach.call(sels, function(s){
      if(s.value){ var ci = colIndex(table, s.value); if(ci >= 0) cols.push(ci); }
    });
    // When a concentration/role filter is active, also sort by that column.
    if(cols.length){ sortTable(table, cols[0], true); }
    Array.prototype.forEach.call(table.tBodies[0].rows, function(r){
      var matchText = r.textContent.toLowerCase().indexOf(q) !== -1;
      var matchCore = cols.every(function(ci){ return !r.cells[ci].classList.contains('e'); });
      r.style.display = (matchText && matchCore) ? '' : 'none';
    });
  }
  document.querySelectorAll('.tfilter, .tselect').forEach(function(el){
    var ev = el.classList.contains('tfilter') ? 'input' : 'change';
    el.addEventListener(ev, function(){ applyFilter(el.getAttribute('data-target')); });
  });
})();
"""

# ----------------------------------------------------------------------------
def write(rel, content):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def copy_assets():
    """Copy static brand assets into the output tree (survives the rmtree)."""
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand")
    dst = os.path.join(OUT, "assets")
    os.makedirs(dst, exist_ok=True)
    if os.path.isdir(src):
        for fn in os.listdir(src):
            shutil.copy2(os.path.join(src, fn), os.path.join(dst, fn))

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_assets()
    write(".nojekyll", "")  # serve files as-is on GitHub Pages
    write("CNAME", "hitspecs.apartsin.com")  # GitHub Pages custom domain
    write("style.css", CSS)
    build_index()
    build_careers()
    for t in TRACK_ORDER:
        build_concentration(t)
    for cid in COURSE_ORDER:
        build_course(cid)
    n = 2 + len(TRACK_ORDER) + len(COURSE_ORDER)
    print(f"Generated {n} pages + style.css in {OUT}")

if __name__ == "__main__":
    main()
