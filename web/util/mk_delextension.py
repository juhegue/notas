# -*- coding: utf-8 -*-

from markdown.inlinepatterns import SimpleTagPattern
from markdown.extensions import Extension


DEL_RE = r"(\~\~)(.+?)(\~\~)"   # tachado


class DelExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('del', SimpleTagPattern(DEL_RE, 'del'), '<not_strong')


