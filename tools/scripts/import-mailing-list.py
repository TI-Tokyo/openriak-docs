#!/usr/bin/env python3
"""Import The Mail Archive HTML scrape as thread-oriented Hugo content."""

import argparse
import datetime as dt
import email.utils
import html
import json
import re
import shutil
import sys
import unicodedata
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path


MESSAGE_LINK_RE = re.compile(r"(?:^|/)msg(\d+)\.html(?:#.*)?$")
TAG_RE = re.compile(r"<[^>]+>")
ATTRIBUTION_RE = re.compile(
    r"^\s*(?:"
    r"On\s+.+?\s+(?:wrote|said):\s*|"
    r".+?\s+wrote:\s*|"
    r"-{2,}\s*Original Message\s*-{2,}\s*"
    r")$",
    re.IGNORECASE,
)
QUOTE_PREFIX_RE = re.compile(r"^\s*((?:>\s*)+)(.*)$")
LINK_RE = re.compile(r"https?://[^\s<>]+")
FOOTER_RE = re.compile(
    r"^(?:_+|-{8,}|riak-users mailing list|riak-users@lists\.basho\.com|"
    r"https?://lists\.basho\.com/mailman/listinfo/riak-users_lists\.basho\.com)\s*$",
    re.IGNORECASE,
)

CATEGORY_RULES = {
    "Riak CS": [r"\briak[ -]?cs\b", r"\bstanchion\b", r"\bs3cmd\b", r"\bobject storage\b"],
    "Riak TS": [r"\briak[ -]?ts\b", r"\btime series\b", r"\bts table\b"],
    "Security": [r"\bsecurity\b", r"\bauth(?:entication|orization)?\b", r"\bssl\b", r"\btls\b", r"\bcertificate\b", r"\bacl\b"],
    "Querying, Search & MapReduce": [r"\bmap\s*reduce\b", r"\bsearch\b", r"\bsolr\b", r"\byokozuna\b", r"\b2i\b", r"secondary index", r"\bquery\b"],
    "Replication & Clustering": [r"\breplication\b", r"\bcluster\b", r"\bnode\b", r"\briak repl\b", r"\bmdc\b", r"\bhandoff\b", r"\bring\b"],
    "Storage Backends": [r"\bbitcask\b", r"\bleveldb\b", r"\bbackend\b", r"\bstorage\b", r"\bmerge\b", r"\bdets\b"],
    "Performance & Monitoring": [r"\bperformance\b", r"\bbenchmark\b", r"\bslow\b", r"\blatency\b", r"\bthroughput\b", r"\bmonitor", r"\bstats?\b", r"\bmemory\b"],
    "Installation & Deployment": [r"\binstall", r"\bdeploy", r"\bpackage\b", r"\bchef\b", r"\bpuppet\b", r"\bdocker\b", r"\bamazon\b", r"\baws\b", r"\bec2\b", r"\bubuntu\b", r"\bcentos\b"],
    "Clients & APIs": [r"\bclient\b", r"\bapi\b", r"\bprotocol buffers?\b", r"\bhttp\b", r"\bjava\b", r"\bpython\b", r"\bruby\b", r"\berlang client\b", r"\bnode\.js\b", r"\bphp\b"],
    "Data Modeling": [r"\bdata model", r"\bbucket\b", r"\bkey\b", r"\bobject\b", r"\bschema\b", r"\bconflict\b", r"\bsibling\b", r"\bvector clock\b", r"\bcrdt\b"],
    "Operations & Administration": [r"\briak-admin\b", r"\briak attach\b", r"\bbackup\b", r"\brecover", r"\bupgrade\b", r"\bconfiguration\b", r"\briak\.conf\b", r"\bapp\.config\b", r"\boperator\b"],
    "Riak Core & Erlang": [r"\briak_core\b", r"\briak core\b", r"\berlang\b", r"\bbeam\b", r"\bgen_server\b", r"\bvnode\b"],
    "Community & Events": [r"\bcommunity\b", r"\bmeetup\b", r"\bconference\b", r"\bricon\b", r"\bwebinar\b", r"\bjob\b", r"\bhiring\b", r"\bannounce"],
}


class ThreadIndexParser(HTMLParser):
    """Read MHonArc's nested thread list without depending on its malformed li tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_index = False
        self.in_threads = False
        self.depth = -1
        self.last_at_depth = {}
        self.entries = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        if tag == "div" and attributes.get("id") == "indexcontent":
            self.in_index = True
        if tag == "ul" and self.in_index:
            if not self.in_threads and "msglink" in classes:
                self.in_threads = True
                self.depth = 0
            elif self.in_threads:
                self.depth += 1
            return
        if tag != "a" or not self.in_threads:
            return
        match = MESSAGE_LINK_RE.search(attributes.get("href", ""))
        if not match:
            return
        message_id = f"msg{int(match.group(1)):05d}"
        parent_id = self.last_at_depth.get(self.depth - 1) if self.depth else ""
        self.entries.append((message_id, parent_id))
        self.last_at_depth[self.depth] = message_id
        for deeper in [key for key in self.last_at_depth if key > self.depth]:
            del self.last_at_depth[deeper]

    def handle_endtag(self, tag):
        if tag == "ul" and self.in_threads:
            if self.depth == 0:
                self.in_threads = False
                self.depth = -1
            else:
                self.depth -= 1


class ThreadSliceParser(HTMLParser):
    """Read the repeated per-message thread slice, including its current unlinked item."""

    def __init__(self, current_id):
        super().__init__(convert_charrefs=True)
        self.current_id = current_id
        self.in_slice = False
        self.in_threads = False
        self.depth = -1
        self.last_at_depth = {}
        self.entries = []

    def _record(self, message_id):
        parent_id = self.last_at_depth.get(self.depth - 1) if self.depth else ""
        self.entries.append((message_id, parent_id))
        self.last_at_depth[self.depth] = message_id
        for deeper in [key for key in self.last_at_depth if key > self.depth]:
            del self.last_at_depth[deeper]

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())
        if tag == "div" and "tSliceList" in classes:
            self.in_slice = True
        if tag == "ul" and self.in_slice:
            if not self.in_threads:
                self.in_threads = True
                self.depth = 0
            else:
                self.depth += 1
            return
        if tag == "li" and self.in_threads and "tSliceCur" in classes:
            self._record(self.current_id)
            return
        if tag == "a" and self.in_threads:
            match = MESSAGE_LINK_RE.search(attributes.get("href", ""))
            if match:
                self._record(f"msg{int(match.group(1)):05d}")

    def handle_endtag(self, tag):
        if tag == "ul" and self.in_threads:
            if self.depth == 0:
                self.in_threads = False
                self.depth = -1
            else:
                self.depth -= 1


class BodyTextParser(HTMLParser):
    """Convert the small HTML vocabulary in articleBody into depth-aware text lines."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.lines = []
        self.current = ""
        self.current_depth = 0

    def _break(self):
        self.lines.append((self.current_depth, self.current.rstrip()))
        self.current = ""
        self.current_depth = self.depth

    def handle_starttag(self, tag, attrs):
        if tag == "blockquote":
            if self.current.strip():
                self._break()
            self.depth += 1
            self.current_depth = self.depth
        elif tag == "br":
            self._break()
        elif tag in ("pre", "p", "div") and self.current.strip():
            self._break()

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self._break()

    def handle_endtag(self, tag):
        if tag == "blockquote":
            if self.current.strip():
                self._break()
            self.depth = max(0, self.depth - 1)
            self.current_depth = self.depth
        elif tag in ("pre", "p", "div") and self.current.strip():
            self._break()

    def handle_data(self, data):
        data = data.replace("\xa0", " ")
        parts = data.split("\n")
        for index, part in enumerate(parts):
            if self.current and self.current_depth != self.depth:
                self._break()
            self.current_depth = self.depth
            self.current += part
            if index < len(parts) - 1:
                self._break()

    def result(self):
        if self.current or not self.lines:
            self._break()
        normalized = []
        blank = False
        for depth, text in self.lines:
            match = QUOTE_PREFIX_RE.match(text)
            if match:
                depth += match.group(1).count(">")
                text = match.group(2)
            text = text.rstrip()
            if not text:
                if normalized and not blank:
                    normalized.append((depth, ""))
                blank = True
            else:
                normalized.append((depth, text))
                blank = False
        while normalized and not normalized[-1][1]:
            normalized.pop()
        return normalized


def plain_html(value):
    return html.unescape(TAG_RE.sub("", value)).strip()


def extract_message(path):
    raw = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    subject_match = re.search(r'<span class="subject"[^>]*>.*?<span itemprop="name">(.*?)</span>', raw, re.S)
    author_match = re.search(r'<span itemprop="author".*?<span itemprop="name">(.*?)</span>', raw, re.S)
    date_match = re.search(r'<span class="date"[^>]*>.*?<a[^>]*>(.*?)</a>', raw, re.S)
    body_start = raw.find('<div itemprop="articleBody"')
    body_open_end = raw.find(">", body_start)
    body_end = raw.find('<div class="msgButtons', body_open_end)
    if body_end < 0:
        body_end = len(raw)
    if not subject_match or not author_match or not date_match or min(body_start, body_open_end) < 0:
        raise ValueError(f"missing message fields in {path}")
    parser = BodyTextParser()
    parser.feed(raw[body_open_end + 1:body_end])
    slice_parser = ThreadSliceParser(path.stem)
    slice_parser.feed(raw)
    parsed_date = email.utils.parsedate_to_datetime(plain_html(date_match.group(1)))
    if parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=dt.timezone.utc)
    return {
        "id": path.stem,
        "title": plain_html(subject_match.group(1)) or "(no subject)",
        "author": plain_html(author_match.group(1)) or "Unknown sender",
        "sent_date": parsed_date.isoformat(),
        "date": parsed_date,
        "lines": parser.result(),
        "thread_entries": slice_parser.entries,
    }


def canonical(lines):
    cleaned = []
    for _, text in lines:
        text = re.sub(r"<mailto:([^>]+)>", r"\1", text, flags=re.I)
        text = re.sub(r"mailto:", "", text, flags=re.I)
        if not text or FOOTER_RE.match(text.strip()):
            continue
        cleaned.append(text)
    return re.sub(r"\s+", "", " ".join(cleaned)).casefold()


def remove_duplicate_quote(message, earlier_messages):
    lines = message["lines"]
    earlier = {canonical(item["lines"]): item["id"] for item in earlier_messages if canonical(item["lines"])}
    for index, (_, text) in enumerate(lines):
        if not ATTRIBUTION_RE.match(text):
            continue
        candidate = canonical(lines[index + 1:])
        if candidate and candidate in earlier:
            trimmed = lines[:index]
            while trimmed and not trimmed[-1][1]:
                trimmed.pop()
            message["lines"] = trimmed
            message["deduplicated_message_id"] = earlier[candidate]
            return True
    return False


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", value))


def render_inline(text):
    output, cursor = [], 0
    for match in LINK_RE.finditer(text):
        output.append(html.escape(text[cursor:match.start()]))
        original = match.group(0)
        url = original.rstrip(".,;:!?)]\"")
        output.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(url)}</a>')
        output.append(html.escape(original[len(url):]))
        cursor = match.end()
    output.append(html.escape(text[cursor:]))
    return "".join(output)


def render_body(message):
    if not message["lines"]:
        return '<div class="mailing-list-message__body"><em>Repeated quoted message removed.</em></div>'
    output = ['<div class="mailing-list-message__body">']
    depth = 0
    for next_depth, line in message["lines"]:
        while depth < next_depth:
            output.append("<blockquote>")
            depth += 1
        while depth > next_depth:
            output.append("</blockquote>")
            depth -= 1
        output.append(render_inline(line) + "\n")
    output.extend("</blockquote>" for _ in range(depth))
    output.append("</div>")
    return "".join(output)


def human_date(message):
    parsed = message["date"]
    hour = parsed.hour % 12 or 12
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year} at {hour}:{parsed.strftime('%M %p')}"


def render_header(message, include_subject=False):
    subject = f'<span class="mailing-list-message__subject">{html.escape(message["title"])}</span>' if include_subject else ""
    return (
        '<header class="mailing-list-message__header">'
        f'<span class="mailing-list-message__author">{html.escape(message["author"])}</span>'
        f'<time datetime="{html.escape(message["sent_date"], quote=True)}">{human_date(message)}</time>{subject}'
        '</header>'
    )


def render_reply(message, children):
    nested = "".join(render_reply(child, children) for child in children.get(message["id"], []))
    nested = f'<ol class="mailing-list-replies">{nested}</ol>' if nested else ""
    return (
        '<li class="mailing-list-reply">'
        f'<details id="{message["id"]}" class="mailing-list-message">'
        f'<summary>{render_header(message, True)}</summary>'
        f'<div class="mailing-list-message__content">{render_body(message)}{nested}</div>'
        '</details></li>'
    )


def render_toc_item(message, children):
    nested = "".join(render_toc_item(child, children) for child in children.get(message["id"], []))
    nested = f"<ol>{nested}</ol>" if nested else ""
    return (
        f'<li><a href="#{message["id"]}"><span>{html.escape(message["title"])}</span>'
        f'<small>{html.escape(message["author"])} · {message["date"].strftime("%b %-d, %Y")}</small></a>{nested}</li>'
    )


def render_thread(root, children):
    toc = render_toc_item(root, children)
    replies = "".join(render_reply(child, children) for child in children.get(root["id"], []))
    replies = f'<ol class="mailing-list-replies">{replies}</ol>' if replies else ""
    return (
        '<nav class="mailing-list-toc" aria-label="Thread contents"><h2>In this thread</h2>'
        f'<ol>{toc}</ol></nav>'
        f'<section class="mailing-list-thread" data-thread-root="{root["id"]}">'
        f'<article id="{root["id"]}" class="mailing-list-message mailing-list-message--root">'
        f'{render_header(root)}{render_body(root)}{replies}</article></section>'
    )


def category_for(thread):
    title_text = " ".join(message["title"] for message in thread).lower()
    body_text = " ".join(text for message in thread for _, text in message["lines"]).lower()
    best_category, best_score = "General", 0
    for category, patterns in CATEGORY_RULES.items():
        score = sum(4 * len(re.findall(pattern, title_text, re.I)) for pattern in patterns)
        score += sum(len(re.findall(pattern, body_text, re.I)) for pattern in patterns)
        if score > best_score:
            best_category, best_score = category, score
    return best_category


def display_title(title, reply_count):
    if reply_count == 0:
        return title
    if reply_count == 1:
        return f"{title} (and 1 reply)"
    return f"{title} (and {reply_count} replies)"


def front_matter(values):
    lines = ["---"]
    for key, value in values.items():
        if isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        elif isinstance(value, (int, bool)):
            lines.append(f"{key}: {str(value).lower()}")
        else:
            lines.append(f"{key}: {json.dumps(str(value), ensure_ascii=False)}")
    return "\n".join(lines + ["---", ""])


def write_index(path, **values):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(values), encoding="utf-8")


def thread_index_paths(source):
    paths = [source / "index.html"]
    paths.extend(source / f"thrd{number}.html" for number in range(2, 17))
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise ValueError(f"missing thread indexes: {', '.join(map(str, missing))}")
    return paths


def read_thread_graph(source):
    entries = []
    for path in thread_index_paths(source):
        parser = ThreadIndexParser()
        parser.feed(path.read_text(encoding="utf-8", errors="replace"))
        entries.extend(parser.entries)
    return entries


def find_root(message_id, parents):
    seen = set()
    current = message_id
    while parents.get(current):
        if current in seen:
            raise ValueError(f"parent cycle containing {current}")
        seen.add(current)
        current = parents[current]
    return current


def build(source, destination):
    index_entries = read_thread_graph(source)
    paths = sorted(source.glob("msg[0-9]*.html"))
    messages = {message["id"]: message for message in (extract_message(path) for path in paths)}
    available = set(messages)
    parent_votes = defaultdict(Counter)
    for message in messages.values():
        for message_id, parent_id in message.pop("thread_entries"):
            if message_id in available and (not parent_id or parent_id in available):
                parent_votes[message_id][parent_id] += 1
    for message_id, parent_id in index_entries:
        if message_id in available and (not parent_id or parent_id in available):
            parent_votes[message_id][parent_id] += 1
    missing_parents = sorted(available - set(parent_votes))
    for message_id in missing_parents:
        parent_votes[message_id][""] = 1
    parents = {
        message_id: max(votes.items(), key=lambda item: (item[1], bool(item[0])))[0]
        for message_id, votes in parent_votes.items()
    }

    children = defaultdict(list)
    by_root = defaultdict(list)
    for message_id in sorted(messages, key=lambda item: (messages[item]["date"], item)):
        parent_id = parents[message_id]
        if parent_id:
            children[parent_id].append(messages[message_id])
        by_root[find_root(message_id, parents)].append(messages[message_id])
    for replies in children.values():
        replies.sort(key=lambda item: (item["date"], item["id"]))

    deduplicated = 0
    for thread in by_root.values():
        earlier = []
        for message in sorted(thread, key=lambda item: (item["date"], item["id"])):
            deduplicated += int(remove_duplicate_quote(message, earlier))
            earlier.append(message)

    generated = destination / "generated"
    if generated.exists():
        shutil.rmtree(generated)
    threads_dir, categories_dir, dates_dir = generated / "threads", generated / "categories", generated / "by-date"
    threads_dir.mkdir(parents=True)
    write_index(threads_dir / "_index.md", title="Archived Mailing List", type="mailing-list")

    category_counts = defaultdict(lambda: [0, 0])
    date_counts = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for root_id, thread in by_root.items():
        root = messages[root_id]
        reply_count = len(thread) - 1
        category = category_for(thread)
        category_counts[category][0] += 1
        category_counts[category][1] += reply_count
        date_counts[root["date"].year][root["date"].month][0] += 1
        date_counts[root["date"].year][root["date"].month][1] += reply_count
        values = {
            "title": display_title(root["title"], reply_count),
            "date": root["sent_date"],
            "author": root["author"],
            "categories": [category],
            "thread_id": root_id,
            "reply_count": reply_count,
            "type": "mailing-list",
        }
        (threads_dir / f"{root_id}.md").write_text(front_matter(values) + "\n" + render_thread(root, children) + "\n", encoding="utf-8")

    write_index(categories_dir / "_index.md", title="By Category", description="Browse archived mailing-list conversations by subject.", type="mailing-list", layout="categories")
    for category in sorted(category_counts):
        category_dir = categories_dir / slugify(category)
        description = f"Archived mailing-list conversations about {category.lower()}."
        write_index(category_dir / "_index.md", title=category, description=description, category=category, type="mailing-list", layout="category", sort="date")
        write_index(category_dir / "title" / "_index.md", title=category, description=description, category=category, type="mailing-list", layout="category", sort="title")

    write_index(dates_dir / "_index.md", title="By Date", description="Browse archived mailing-list conversations by year and month.", type="mailing-list", layout="by-date")
    for year in sorted(date_counts, reverse=True):
        write_index(dates_dir / str(year) / "_index.md", title=str(year), description=f"Mailing-list conversations started in {year}.", archive_year=year, type="mailing-list", layout="date")
        for month in sorted(date_counts[year], reverse=True):
            name = dt.date(2000, month, 1).strftime("%B")
            write_index(dates_dir / str(year) / name.lower() / "_index.md", title=f"{name} {year}", description=f"Mailing-list conversations started in {name} {year}.", archive_year=year, archive_month=month, type="mailing-list", layout="date")

    print(f"imported {len(messages)} HTML messages as {len(by_root)} threads in {len(category_counts)} categories")
    print(f"removed {deduplicated} exact repeated-message quotations")
    if missing_parents:
        print(f"treated {len(missing_parents)} messages with empty source thread slices as standalone threads")


def main():
    project = Path(__file__).resolve().parents[2]
    default_source = project.parent / "riak-docs-fork" / "external-data" / "mailing-list" / "riak-users@lists.basho.com"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=default_source)
    parser.add_argument("--destination", type=Path, default=project / "content" / "archive-mailing-list")
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error(f"source directory does not exist: {args.source}")
    build(args.source.resolve(), args.destination.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
