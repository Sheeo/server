for QtModuleName in ('PySide', 'PyQt4', 'PySide'):
    try:
        QtModule = __import__(QtModuleName)
    except ImportError:
        continue
    else:
        break
else:
    raise ImportError('No Qt implementations found')

QtCore = __import__(QtModuleName + '.QtCore', fromlist=(QtModuleName,))
QtGui = __import__(QtModuleName + '.QtGui', fromlist=(QtModuleName,))
QtNetwork = __import__(QtModuleName + '.QtNetwork', fromlist=(QtModuleName,))
if QtModuleName == 'PySide':
    from PySide import QtWidgets
    QApplication = QtWidgets.QApplication
else:
    QApplication = QtGui.QApplication

if not hasattr(QtCore, 'Signal'):
    QtCore.Signal = QtCore.pyqtSignal