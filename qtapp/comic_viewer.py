import sys
import zipfile
#import rarfile
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class ComicViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Cómics")
        self.setGeometry(100, 100, 800, 1000)
        
        # Variables
        self.current_page = 0
        self.pages = []
        self.folder_path = ""
        
        # Widgets
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Toolbar
        self.create_toolbar()
        
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        open_action = QAction("Abrir cómic", self)
        open_action.triggered.connect(self.open_comic)
        toolbar.addAction(open_action)
        
        prev_action = QAction("Anterior", self)
        prev_action.triggered.connect(self.prev_page)
        toolbar.addAction(prev_action)
        
        next_action = QAction("Siguiente", self)
        next_action.triggered.connect(self.next_page)
        toolbar.addAction(next_action)
    
    def open_comic(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", 
            "Archivos de cómic (*.cbz *.cbr *.zip *.rar);;Imágenes (*.jpg *.png)"
        )
        
        if file_path:
            self.folder_path = file_path
            self.pages = self.extract_images(file_path)
            self.current_page = 0
            self.show_page()
    
    def extract_images(self, file_path):
        pages = []
        
        if file_path.endswith(".cbz") or file_path.endswith(".zip"):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        pages.append(file)
        
        elif file_path.endswith(".cbr") or file_path.endswith(".rar"):
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                for file in rar_ref.namelist():
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        pages.append(file)
        
        return sorted(pages)
    
    def show_page(self):
        if not self.pages:
            return
        
        if self.folder_path.endswith(".cbz") or self.folder_path.endswith(".zip"):
            with zipfile.ZipFile(self.folder_path, 'r') as zip_ref:
                with zip_ref.open(self.pages[self.current_page]) as page:
                    img = Image.open(page)
                    img.save("temp_page.png")  # Guardamos temporalmente
                    
        elif self.folder_path.endswith(".cbr") or self.folder_path.endswith(".rar"):
            with rarfile.RarFile(self.folder_path, 'r') as rar_ref:
                with rar_ref.open(self.pages[self.current_page]) as page:
                    img = Image.open(page)
                    img.save("temp_page.png")
        
        pixmap = QPixmap("temp_page.png")
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), 
            self.image_label.height(), 
            Qt.KeepAspectRatio
        ))
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()
    
    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ComicViewer()
    viewer.show()
    sys.exit(app.exec_())