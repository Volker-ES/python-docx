# encoding: utf-8

"""
Custom element classes related to paragraphs (CT_P).
"""

from docx.enum.fields import WD_FIELD_TYPE
from ..ns import qn
from ..xmlchemy import BaseOxmlElement, OxmlElement, ZeroOrMore, ZeroOrOne


class CT_P(BaseOxmlElement):
    """
    ``<w:p>`` element, containing the properties and text for a paragraph.
    """
    pPr = ZeroOrOne("w:pPr")
    r = ZeroOrMore("w:r")
    bookmarkStart = ZeroOrMore("w:bookmarkStart")
    bookmarkEnd = ZeroOrMore("w:bookmarkEnd")

    def add_bookmarkEnd(self, bookmark_id):
        """Return `w:bookmarkEnd` element added at end of document.
        The newly added `w:bookmarkEnd` element is linked to it's `w:bookmarkStart`
        counterpart by `bookmark_id`. It is the caller's responsibility to determine
        `bookmark_id` matches that of the intended `bookmarkStart` element.
        """
        bookmarkEnd = self._add_bookmarkEnd()
        bookmarkEnd.id = bookmark_id
        return bookmarkEnd

    def add_bookmarkStart(self, name, bookmark_id):
        """Return `w:bookmarkStart` element added at end of document.
        The newly added `w:bookmarkStart` element is identified by both `name` and
        `bookmark_id`. It is the caller's responsibility to determine that both `name`
        and `bookmark_id` are unique, document-wide.
        """
        bookmarkStart = self._add_bookmarkStart()
        bookmarkStart.name = name
        bookmarkStart.id = bookmark_id
        return bookmarkStart

    def add_field(self, fieldtype=WD_FIELD_TYPE.REF, switches="\h"):
        """Return a newly created ``<w:fldSimple>`` element containing a fieldcode."""
        fld = self._add_fldsimple(
            instr=WD_FIELD_TYPE.to_xml(fieldtype) + f" {switches}"
        )
        return fld

    def _insert_pPr(self, pPr):
        self.insert(0, pPr)
        return pPr

    def add_p_before(self):
        """
        Return a new ``<w:p>`` element inserted directly prior to this one.
        """
        new_p = OxmlElement('w:p')
        self.addprevious(new_p)
        return new_p

    @property
    def alignment(self):
        """
        The value of the ``<w:jc>`` grandchild element or |None| if not
        present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value):
        pPr = self.get_or_add_pPr()
        pPr.jc_val = value

    def clear_content(self):
        """
        Remove all child elements, except the ``<w:pPr>`` element if present.
        """
        for child in self[:]:
            if child.tag == qn('w:pPr'):
                continue
            self.remove(child)

    def set_sectPr(self, sectPr):
        """
        Unconditionally replace or add *sectPr* as a grandchild in the
        correct sequence.
        """
        pPr = self.get_or_add_pPr()
        pPr._remove_sectPr()
        pPr._insert_sectPr(sectPr)

    @property
    def style(self):
        """
        String contained in w:val attribute of ./w:pPr/w:pStyle grandchild,
        or |None| if not present.
        """
        pPr = self.pPr
        if pPr is None:
            return None
        return pPr.style

    @style.setter
    def style(self, style):
        pPr = self.get_or_add_pPr()
        pPr.style = style
