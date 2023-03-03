from dataclasses import dataclass
from typing import Optional, Iterator, Generator
from spexs2.xml import etree, Xpath, Element
from spexs2.document import DocumentParser
from spexs2.lint import Linter
from pathlib import Path
from spexs2.defs import Entity
from spexs2.quirks import QuirksMap, QUIRKS_MAP


@dataclass(frozen=True)
class SpecDocument:
    tree: Element
    key: str
    rev: str

    def get_parser(self, quirks_map: Optional[QuirksMap] = None) -> DocumentParser:
        if quirks_map is None:
            quirks_map = QUIRKS_MAP

        quirks_key = (self.key, self.rev)
        dp = quirks_map.get(quirks_key, DocumentParser)(self.tree, self.key, self.rev)
        return dp


# TODO determine what to return
def open_doc(spec: Path) -> SpecDocument:
    doc = etree.parse(str(spec.absolute()))

    doc_spec = Xpath.attr_first(doc, "./head/meta/@data-spec").lower()
    doc_rev = Xpath.attr_first(doc, "./head/meta/@data-revision").lower()
    return SpecDocument(tree=doc, key=doc_spec, rev=doc_rev)
