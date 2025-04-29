
import sys
import threading
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from flask_app import app

def run_flask():
    app.run(debug=False, use_reloader=False)

app_qt = QApplication(sys.argv)
browser = QWebEngineView()
browser.setWindowTitle("Sistema Adoção SEBEM")
browser.resize(1024, 768)
browser.setUrl(QUrl("http://127.0.0.1:5000"))

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

browser.show()
sys.exit(app_qt.exec_())
