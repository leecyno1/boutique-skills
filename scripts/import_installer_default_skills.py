#!/usr/bin/env python3
import argparse
import json
import shutil
from pathlib import Path

DEFAULT_INSTALLER = Path('/Volumes/PSSD/Projects/OpenClawInstaller')
REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / 'skills' / 'default'
TIERS_DIR = REPO / 'tiers'
DOC_TIERS_DIR = REPO / 'docs' / 'tiers'
MANUALS_DOC = REPO / 'docs' / 'SKILL_MANUALS.md'
CATALOG_OUT = REPO / 'catalog' / 'default-skills.json'

TIER_LABELS = {
    'low': '低档 / Low',
    'medium': '中档 / Medium',
    'high': '高档 / High',
}

TIER_DESCRIPTIONS = {
    'low': '稳定基础档，适合首次安装和轻量生产环境。只包含通用协作、搜索、文档、基础媒体和安全工作流。',
    'medium': '增强生产档，包含低档全部能力，并加入官方 MiniMax、本地增强、规划、图像、文档和常用扩展。',
    'high': '完整专家档，包含中档全部能力，并加入 Baoyu 创作套件、金融交易研究、AlphaEar 与高级分析技能。',
}

SOURCE_BASE = 'https://github.com/leecyno1/auto-install-Openclaw/tree/release/hermes-website-minimax-hardening-20260503'
BOUTIQUE_SOURCE_BASE = 'https://github.com/leecyno1/boutique-skills/tree/main'


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def skill_manual(skill_dir: Path, skill_id: str) -> str:
    guide = skill_dir / 'GUIDE.md'
    skill = skill_dir / 'SKILL.md'
    readme = skill_dir / 'README.md'
    if guide.exists():
        return f'skills/default/{skill_id}/GUIDE.md'
    if readme.exists():
        return f'skills/default/{skill_id}/README.md'
    if skill.exists():
        return f'skills/default/{skill_id}/SKILL.md'
    return f'skills/default/{skill_id}'


def first_sentence(text: str) -> str:
    text = ' '.join((text or '').split())
    if not text:
        return 'No description available.'
    for sep in ['。', '.', '！', '!', '？', '?']:
        idx = text.find(sep)
        if 24 <= idx <= 220:
            return text[: idx + 1]
    return text[:220]


def copy_skills(installer: Path) -> None:
    src = installer / 'skills' / 'default'
    if not src.exists():
        raise SystemExit(f'missing installer skills dir: {src}')
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    for child in sorted(src.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        dst = SKILLS_DIR / child.name
        if dst.exists():
            shutil.rmtree(dst)
        ignore = shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store', 'node_modules', '.git')
        shutil.copytree(child, dst, ignore=ignore)


def build_skill_index(installer: Path) -> tuple[dict, dict]:
    manifest = read_json(installer / 'skills' / 'manifest.json')
    by_id = {item['id']: item for item in manifest.get('skills', [])}
    bundles = manifest.get('bundles', {})
    return by_id, bundles


def tier_ids(bundle_name: str, bundles: dict) -> list[str]:
    return list(dict.fromkeys(bundles.get(bundle_name, [])))


def tier_item(skill_id: str, source_item: dict) -> dict:
    skill_dir = SKILLS_DIR / skill_id
    manual = skill_manual(skill_dir, skill_id)
    description = first_sentence(source_item.get('description', ''))
    groups = source_item.get('groups', []) or []
    return {
        'id': skill_id,
        'name': source_item.get('name') or skill_id,
        'description': description,
        'manual': manual,
        'manual_url': f'{BOUTIQUE_SOURCE_BASE}/{manual}',
        'source': f'{SOURCE_BASE}/skills/default/{skill_id}',
        'requires_api_keys': bool(source_item.get('requires_api_keys', False)),
        'api_keys': source_item.get('api_keys', []) or [],
        'groups': groups,
    }


def write_tiers(by_id: dict, bundles: dict) -> dict:
    TIERS_DIR.mkdir(parents=True, exist_ok=True)
    tier_map = {
        'low': tier_ids('basic', bundles),
        'medium': tier_ids('extended', bundles),
        'high': tier_ids('super', bundles),
    }
    out = {}
    for tier, ids in tier_map.items():
        skills = [tier_item(skill_id, by_id.get(skill_id, {'id': skill_id, 'name': skill_id})) for skill_id in ids]
        payload = {
            'id': tier,
            'title': TIER_LABELS[tier],
            'description': TIER_DESCRIPTIONS[tier],
            'source_bundle': {'low': 'basic', 'medium': 'extended', 'high': 'super'}[tier],
            'install_command': f'./scripts/install-tier.sh {tier}',
            'skills': skills,
        }
        (TIERS_DIR / f'{tier}.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        out[tier] = payload
    CATALOG_OUT.write_text(json.dumps({'version': 1, 'source': 'OpenClawInstaller skills/manifest.json', 'tiers': out}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return out


def table_for_skills(skills: list[dict]) -> list[str]:
    lines = ['| Skill | 说明 | 使用手册 | 原仓库链接 |', '|---|---|---|---|']
    for item in skills:
        manual = item['manual']
        lines.append(f"| `{item['id']}` | {item['description']} | [{manual}](../../{manual}) | [source]({item['source']}) |")
    return lines


def write_docs(tiers: dict) -> None:
    DOC_TIERS_DIR.mkdir(parents=True, exist_ok=True)
    for tier, data in tiers.items():
        lines = [
            f"# {data['title']} Skills",
            '',
            data['description'],
            '',
            f"- 技能数量：`{len(data['skills'])}`",
            f"- 安装命令：`{data['install_command']}`",
            f"- JSON 清单：`tiers/{tier}.json`",
            '',
            '## 技能清单',
            '',
            *table_for_skills(data['skills']),
            '',
        ]
        (DOC_TIERS_DIR / f'{tier}.md').write_text('\n'.join(lines), encoding='utf-8')

    all_skills = {}
    for data in tiers.values():
        for item in data['skills']:
            all_skills[item['id']] = item
    lines = [
        '# Default Skills Manual Index',
        '',
        '本文件由 `scripts/import_installer_default_skills.py` 生成，作为 boutique 仓库维护默认 skills 的统一手册索引。',
        '',
        '| Skill | 说明 | 使用手册 | 原仓库链接 |',
        '|---|---|---|---|',
    ]
    for skill_id in sorted(all_skills):
        item = all_skills[skill_id]
        lines.append(f"| `{skill_id}` | {item['description']} | [{item['manual']}]({item['manual']}) | [source]({item['source']}) |")
    lines.append('')
    MANUALS_DOC.write_text('\n'.join(lines), encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Import OpenClawInstaller default skills into boutique tiers')
    parser.add_argument('--installer-root', default=str(DEFAULT_INSTALLER))
    parser.add_argument('--no-copy', action='store_true')
    args = parser.parse_args()

    installer = Path(args.installer_root).resolve()
    by_id, bundles = build_skill_index(installer)
    if not args.no_copy:
        copy_skills(installer)
    tiers = write_tiers(by_id, bundles)
    write_docs(tiers)
    print(json.dumps({tier: len(data['skills']) for tier, data in tiers.items()}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
