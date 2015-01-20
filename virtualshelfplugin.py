#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import with_statement

__license__   = 'GPL v3'
__copyright__ = '2015, Carles Pina i Estany <carles@pina.cat>'
__docformat__ = 'restructuredtext en'

from calibre.gui2 import gprefs
from calibre.gui2.ui import get_gui
from PyQt5.Qt import QWidget, QListWidgetItem, Qt, QVBoxLayout, QLabel, QListWidget

class PluginWidget(QWidget):
    TITLE = _('HTML Virtual Shelf options')
    HELP  = _('Options specific to Virtual Shelf plugin')
    sync_enabled = False
    formats = set(['html'])

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.l = l = QVBoxLayout(self)
        self.la = la = QLabel(_("This plugin doesn't need any configuration"))
        la.setWordWrap(True)
        l.addWidget(la)

    def initialize(self, catalog_name):
        print "def Virtual Shelf initialize"

    def options(self):
        print "def Virtual Shelf options"
        return list()

