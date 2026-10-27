"""Load and validate the synthetic runbook corpus and evaluation questions."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    title: str
    section: str
    text: str
    path: str

    @property
    def searchable_text(self) -> str:
        return f'{self.title} {self.section} {self.text}'


@dataclass(frozen=True)
class Question:
    qid: str
    query: str
    gold_doc_ids: tuple[str, ...]
    split: str

    @property
    def answerable(self) -> bool:
        return bool(self.gold_doc_ids)


def load_chunks(corpus_dir: Path) -> list[Chunk]:
    """Parse one Markdown runbook into one chunk per second-level heading."""
    chunks: list[Chunk] = []
    files = sorted(corpus_dir.glob('*.md'))
    if not files:
        raise ValueError(f'No Markdown runbooks found in {corpus_dir}')
    for path in files:
        raw = path.read_text(encoding='utf-8')
        lines = raw.splitlines()
        if not lines or not lines[0].startswith('# '):
            raise ValueError(f'Missing H1 title: {path}')
        title = lines[0][2:].strip()
        doc_id = path.stem
        match = re.search(r'^Document ID: (.+)$', raw, flags=re.MULTILINE)
        if not match or match.group(1).strip() != doc_id:
            raise ValueError(f'ID does not match filename: {path}')
        sections = re.split(r'^## ', raw, flags=re.MULTILINE)
        for part in sections[1:]:
            section, _, body = part.partition('\n')
            body = body.strip()
            if body:
                chunks.append(Chunk(doc_id, title, section.strip(), body, f'data/runbooks/{path.name}'))
    if not chunks:
        raise ValueError('Corpus has no nonempty sections')
    return chunks


def load_questions(path: Path, known_ids: set[str]) -> list[Question]:
    questions: list[Question] = []
    seen: set[str] = set()
    for line_num, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        qid, query = item['qid'], item['query']
        gold = tuple(item['gold_doc_ids'])
        split = item['split']
        if qid in seen or not query.strip() or split not in {'dev', 'test', 'challenge'}:
            raise ValueError(f'Invalid question on line {line_num}')
        if not set(gold).issubset(known_ids):
            raise ValueError(f'Unknown gold doc ID on line {line_num}')
        seen.add(qid)
        questions.append(Question(qid, query, gold, split))
    if not questions:
        raise ValueError('No questions found')
    return questions
