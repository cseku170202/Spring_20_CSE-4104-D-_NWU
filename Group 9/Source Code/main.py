from PySide6.QtWidgets import QApplication
from main_window_widget import MainWindowWidget

import sys

app = QApplication(sys.argv)
window = MainWindowWidget(app)

window.show()

sys.exit(app.exec())
