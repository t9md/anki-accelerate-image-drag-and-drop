from aqt.utils import showInfo, openLink
from aqt.qt import *
import anki
import aqt

FIELD_WIDENED = False

JavaScriptCode = """
function tamperEditorStyle(enabled) {
  var f0Style = document.getElementById('f0')
  if (enabled) {
    f0Style.style.height = '800px'
    f0Style.style.backgroundColor = 'coral'
  } else {
    f0Style.removeAttribute("style")
  }
}
tamperEditorStyle(%s)
"""

def widenFirstField(editor):
    global FIELD_WIDENED
    code = JavaScriptCode % ("true" if FIELD_WIDENED else "false")
    editor.web.eval(code)

def toggleWidenFirstField(browser):
    global FIELD_WIDENED
    FIELD_WIDENED = not FIELD_WIDENED
    widenFirstField(browser.editor)

previewQueue = []

def onSetupMenus(browser):
    global FIELD_WIDENED
    from PyQt5 import QtWidgets

    menu = QtWidgets.QMenu("Accelerate Image Drag&Drop", browser.form.menubar)
    browser.form.menubar.addMenu(menu)
    actionTamperStyle = QAction("Widen First field", menu)
    actionTamperStyle.setCheckable(True)
    actionTamperStyle.setChecked(FIELD_WIDENED)
    actionTamperStyle.toggled.connect(lambda _: toggleWidenFirstField(browser))
    actionTamperStyle.setShortcut(QKeySequence("Shift+Ctrl+E"))
    menu.addAction(actionTamperStyle)

    def previewNextIfExists():
        if browser._previewWindow:
            browser._onPreviewNext()

    def previewPrevIfExists():
        if browser._previewWindow:
            browser._onPreviewPrev()

    def clickLink(editor):
        global previewQueue
        clickDelayInMS = 500
        if previewQueue:
            code = "setTimeout(function() { document.getElementById('primal-image-link').click() }, %s)" % clickDelayInMS
            browser._previewWeb.eval(code)
            del previewQueue[:]

    anki.hooks.addHook('loadNote', clickLink)

    def previewNextAndClickPrimalImageLink():
        if browser._previewWindow:
            browser._onPreviewNext()
            previewQueue.append(1)

    actionPreviewNext = QAction("Preview Next", menu)
    actionPreviewNext.triggered.connect(previewNextIfExists)
    actionPreviewNext.setShortcut(QKeySequence("Shift+Ctrl+N"))
    menu.addAction(actionPreviewNext)

    actionPreviewPrev = QAction("Preview Prev", menu)
    actionPreviewPrev.triggered.connect(previewPrevIfExists)
    actionPreviewPrev.setShortcut(QKeySequence("Shift+Ctrl+P"))
    menu.addAction(actionPreviewPrev)

    actionPreviewNextAndClickPrimalImageLink = QAction("Preview Next And Click Primal Image Link", menu)
    actionPreviewNextAndClickPrimalImageLink.triggered.connect(previewNextAndClickPrimalImageLink)
    actionPreviewNextAndClickPrimalImageLink.setShortcut(QKeySequence("Shift+Ctrl+O"))
    menu.addAction(actionPreviewNextAndClickPrimalImageLink)

def main():
    anki.hooks.addHook('browser.setupMenus', onSetupMenus)
    anki.hooks.addHook('loadNote', widenFirstField)


main()
