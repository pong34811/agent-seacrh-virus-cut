# Project skill bundle

สำเนา skill ที่เกี่ยวข้องกับโปรเจกต์คัดไฮไลต์ Thai VTuber / Resolve / wiki / pipeline development เก็บไว้ใน repo เพื่อพกพาและตรวจสอบได้

## ขอบเขต

- เพิ่ม 37 skills จากการติดตั้งปัจจุบัน รวม house-style เดิมของโปรเจกต์เป็น 38 skills
- คัดลอก SKILL.md พร้อม scripts, templates, references และไฟล์ประกอบในแต่ละ skill directory; ไม่คัดลอก credentials, caches หรือ virtual environments
- house-style เดิมเป็นฉบับของโปรเจกต์และไม่ถูกทับด้วยสำเนาจาก Resolve
- สำเนา Resolve ด้าน color/audio/Fusion/delivery เป็นเครื่องมือสำหรับงานที่ผู้ใช้สั่งเพิ่มเติม ไม่ใช่สิทธิ์ให้เพิ่ม styling, render หรือ upload ในงาน assembly

## ลำดับความสำคัญ

1. คำสั่งผู้ใช้ล่าสุด, AGENTS.md, prompt.md และ house-style ของโปรเจกต์ มีลำดับเหนือข้อความทั่วไปในสำเนา skill
2. ใช้ main เท่านั้นตาม AGENTS.md; skill using-git-worktrees ไม่อนุญาตให้สร้าง branch/worktree ขัดกับผู้ใช้
3. ชื่อ Timeline ใช้ `{ชื่อคลิป}-{ชื่อเกม}-vdo` ตาม house-style ไม่ใช้ชื่อรูปแบบเก่าจากสำเนา upstream
4. อ่าน input/fps/Resolve state สดทุกงาน ไม่เชื่อ path, IDs หรือสรุปงานเก่าใน skill snapshot

## ตำแหน่ง

- skills งานสื่อ, wiki, Resolve และโค้ด: โฟลเดอร์ชื่อ skill ใน .agents/skills/
- Superpowers: superpowers/<skill>/ รักษาโครงสร้าง sibling เดิมและไฟล์ประกอบ
- เอกสาร Resolve ที่ skill อ้างนอกโฟลเดอร์: _references/resolve/ เช่น docs/kernels/ และ docs/guides/; docs/SKILL.md เก็บชื่อ SOURCE-SKILL.md เพื่อไม่เพิ่ม skill ที่ระบบค้นพบโดยไม่ตั้งใจ
- manifest.json: provenance ต้นทาง, SHA-256, ขนาด และปลายทางของทุกไฟล์ที่คัดลอก; house-style มี hash แยกเพื่อพิสูจน์ว่าไม่ถูกทับ

## การใช้งานและข้อจำกัด

- เปิด SKILL.md ใน repo ด้วย read_file ได้ ไม่ต้องติดตั้ง skill ซ้ำเพื่ออ่านขั้นตอน
- สำเนานี้ไม่ใช่การติดตั้ง plugin/MCP server; งาน Resolve ยังต้องมี server และการเชื่อมต่อจริง
- ชื่อ `superpowers:<skill>` อาจยัง resolve ไป plugin ที่ติดตั้งอยู่ ไม่รับรองว่า runtime จะโหลดสำเนานี้อัตโนมัติ; ถ้าต้องการใช้ฉบับใน repo ให้เปิดไฟล์ตรง
- Source skill บางตัวอ้าง docs/tests/tools ของ repo ต้นทางที่ไม่ได้เป็นไฟล์ประกอบภายใน skill เช่น Hermes docs generator หรือ Superpowers plugin internals; bundle นี้ไม่ใช่ source tree เต็มของ Hermes/Resolve/Superpowers
- เอกสาร Resolve ที่ยกมาคือไฟล์ .md ที่ SKILL.md อ้างโดยตรง ไม่ใช่เอกสาร server ทั้งหมด ลิงก์ต่อไปยังเอกสารอื่นอาจต้องเปิด repo ต้นทาง
- ไม่รัน scripts ที่คัดลอกเพื่อทำงานจริงในขั้นนำเข้า ไม่เปลี่ยน footage/Resolve และไม่อัปโหลด YouTube
- การเพิ่มไฟล์ลง repo ท้องถิ่นไม่ใช่การ push GitHub

## รายการ skills

- house-style (ฉบับของโปรเจกต์เดิม)
- long-video-highlight-clipping: [long-video-highlight-clipping](long-video-highlight-clipping/SKILL.md)
- livestream-highlight-clipping: [livestream-highlight-clipping](livestream-highlight-clipping/SKILL.md)
- vertical-video-reframing: [vertical-video-reframing](vertical-video-reframing/SKILL.md)
- llm-wiki: [llm-wiki](llm-wiki/SKILL.md)
- resolve-vtuber-adjustment-focus: [resolve-vtuber-adjustment-focus](resolve-vtuber-adjustment-focus/SKILL.md)
- hermes-agent-skill-authoring: [hermes-agent-skill-authoring](hermes-agent-skill-authoring/SKILL.md)
- codebase-inspection: [codebase-inspection](codebase-inspection/SKILL.md)
- github: [github](github/SKILL.md)
- release-check: [release-check](release-check/SKILL.md)
- resolve-audio: [resolve-audio](resolve-audio/SKILL.md)
- resolve-color: [resolve-color](resolve-color/SKILL.md)
- resolve-conform: [resolve-conform](resolve-conform/SKILL.md)
- resolve-delivery: [resolve-delivery](resolve-delivery/SKILL.md)
- resolve-edit: [resolve-edit](resolve-edit/SKILL.md)
- resolve-fusion: [resolve-fusion](resolve-fusion/SKILL.md)
- resolve-mcp: [resolve-mcp](resolve-mcp/SKILL.md)
- resolve-media-analysis: [resolve-media-analysis](resolve-media-analysis/SKILL.md)
- resolve-media-pool: [resolve-media-pool](resolve-media-pool/SKILL.md)
- resolve-rough-cut: [resolve-rough-cut](resolve-rough-cut/SKILL.md)
- resolve-session: [resolve-session](resolve-session/SKILL.md)
- resolve-smart-edit: [resolve-smart-edit](resolve-smart-edit/SKILL.md)
- resolve-tighten-recording: [resolve-tighten-recording](resolve-tighten-recording/SKILL.md)
- superpowers:brainstorming: [brainstorming](superpowers/brainstorming/SKILL.md)
- superpowers:diagnosing-superpowers: [diagnosing-superpowers](superpowers/diagnosing-superpowers/SKILL.md)
- superpowers:dispatching-parallel-agents: [dispatching-parallel-agents](superpowers/dispatching-parallel-agents/SKILL.md)
- superpowers:executing-plans: [executing-plans](superpowers/executing-plans/SKILL.md)
- superpowers:finishing-a-development-branch: [finishing-a-development-branch](superpowers/finishing-a-development-branch/SKILL.md)
- superpowers:receiving-code-review: [receiving-code-review](superpowers/receiving-code-review/SKILL.md)
- superpowers:requesting-code-review: [requesting-code-review](superpowers/requesting-code-review/SKILL.md)
- superpowers:subagent-driven-development: [subagent-driven-development](superpowers/subagent-driven-development/SKILL.md)
- superpowers:systematic-debugging: [systematic-debugging](superpowers/systematic-debugging/SKILL.md)
- superpowers:test-driven-development: [test-driven-development](superpowers/test-driven-development/SKILL.md)
- superpowers:using-git-worktrees: [using-git-worktrees](superpowers/using-git-worktrees/SKILL.md)
- superpowers:using-superpowers: [using-superpowers](superpowers/using-superpowers/SKILL.md)
- superpowers:verification-before-completion: [verification-before-completion](superpowers/verification-before-completion/SKILL.md)
- superpowers:writing-plans: [writing-plans](superpowers/writing-plans/SKILL.md)
- superpowers:writing-skills: [writing-skills](superpowers/writing-skills/SKILL.md)
