import json, pypandoc
from pathlib import Path


class GetText:
    def __init__(self, ):
        self.ret = ""

    def _run(self, src):
        self.suffix = Path(src).suffix
        if self.suffix == ".md":
            self.doc = json.loads(pypandoc.convert_file(src, "json", format="markdown",
                                                        extra_args=[
                                                            "--from=markdown-markdown_in_html_blocks+raw_html"]))
        elif self.suffix == ".docx":
            self.doc = json.loads(pypandoc.convert_file(src, "json", format="docx",
                                                        ))
        for blk in self.doc["blocks"]:
            if blk["t"] == "RawBlock":
                continue
            self._p(blk)

    def _p(self, blk):
        if isinstance(blk, dict):
            if blk["t"] == "Str":
                q = f"{blk['c']}"
                self.ret = self.ret + q
                print(q)
            elif "c" in blk.keys():
                self._p(blk["c"])
        elif isinstance(blk, list):
            for content in blk:
                self._p(content)

    def __call__(self, p, *args, **kwargs) -> str:
        self._run(p)
        r = self.ret
        self.ret = ""
        return r
