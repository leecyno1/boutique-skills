# Xiaohongshu Skill Source Review - 2026-08-01

Six Xiaohongshu videos were downloaded, transcribed, visually inspected, and matched against first-party GitHub sources. Import decisions require a verifiable upstream, an explicit redistribution license, and an installable Agent Skill structure.

| Note | Identified source | Review | Decision |
|---|---|---|---|
| [AI UI taste](https://www.xiaohongshu.com/explore/6a69f62f0000000010026597) | [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), [pbakaus/impeccable](https://github.com/pbakaus/impeccable) | Taste Skill is already mirrored as its full multi-skill pack and remains 92/100. Impeccable is an Apache-2.0 design engineering workflow with review, implementation playbooks, detectors, live browser iteration, and 20+ focused commands; it was re-rated 92/100 after code and security review. | Taste: no duplicate import. Impeccable: refreshed to upstream `ae5e95101a6979e7f7973a4ff57680b3c7adc1ec` on 2026-08-05. |
| [Product promo video](https://www.xiaohongshu.com/explore/6a6c71ba0000000025007d5a) | [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | Apache-2.0 Remotion skill with shot recipes, motion previews, templates, code assets, review gates, and sound-design guidance. | Imported as `video-shotcraft`. Third-party MP3 binaries with unresolved provenance were not mirrored. |
| [Governed DCF valuation](https://www.xiaohongshu.com/explore/6a6b1231000000000503366e) | [noahnan-max/governed-dcf-skill](https://github.com/noahnan-max/governed-dcf-skill) | Strong fail-closed valuation workflow: method routing, evidence dossiers, three scenarios, sensitivity, reverse DCF, equity bridge, and independent checks. The repository has no license file or license metadata. | Source identified, not mirrored until the author adds a redistribution license. |
| [Short-video automation](https://www.xiaohongshu.com/explore/6a6bdb8c0000000033032c8e) | [Hao0321/video-autopilot-kit](https://github.com/Hao0321/video-autopilot-kit) | MIT project for CapCut JSON and ffmpeg automation, onboarding, templates, compliance notes, and production scripts. It does not contain `SKILL.md`. | Source identified, not imported as a skill. |
| [p5.js motion effects](https://www.xiaohongshu.com/explore/6a632c13000000000a03a59a) | Xiaohongshu REDSkill attachment by Livo | The video demonstrates local p5.js templates for rain curtains, branches, flowers, and swallows. No public GitHub repository or open-source license was found. | Not mirrored. Existing `algorithmic-art` covers general p5.js generation, but it is not the same package. |
| [Official GSAP AI Skills](https://www.xiaohongshu.com/explore/6a6d540000000000220144eb) | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | Official MIT skills covering GSAP core, frameworks, performance, plugins, React, ScrollTrigger, timelines, and utilities. | Imported as eight `gsap-*` skills and the `gsap-skills` suite. |

## Snapshot

| Project | Stars | License | Imported commit |
|---|---:|---|---|
| Taste Skill | 69,868 | MIT | Already present |
| Impeccable | 53,520 | Apache-2.0 | `c5e1ddd054dc093ef2546c36b82eddf2c4e84bb9` |
| video-shotcraft | 3,098 | Apache-2.0 | `d4915443232e89527fdc9d7e79f132ba411fc440` |
| governed-dcf-skill | 7 | Missing | Not imported |
| video-autopilot-kit | 1,538 | MIT | Project only; not a skill |
| GSAP AI Skills | 12,806 | MIT | `aed9cfd3277740755f6bfc1155c7aa645403b760` |

Star counts and repository metadata were verified on 2026-08-01.
