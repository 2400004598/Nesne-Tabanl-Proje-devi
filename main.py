from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from urun import Stock, Product
from siparis import Order

class StokTakipArayuzu(QWidget):
    def __init__(self):
        super().__init__()
        self.stok = Stock()
        self.siparisler = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Stok Takip Sistemi")
        self.setGeometry(100, 100, 600, 400)

        self.urun_ad_giris = QLineEdit(self)
        self.urun_ad_giris.setPlaceholderText("Ürün Adı Girin")

        self.urun_stok_giris = QLineEdit(self)
        self.urun_stok_giris.setPlaceholderText("Stok Miktarı Girin")

        self.ekle_buton = QPushButton("Ürün Ekle", self)
        self.ekle_buton.clicked.connect(self.urun_ekle)

        self.stok_goster_buton = QPushButton("Stok Durumunu Göster", self)
        self.stok_goster_buton.clicked.connect(self.stok_goster)

    
        self.siparis_buton = QPushButton("Sipariş Oluştur", self)
        self.siparis_buton.clicked.connect(self.siparis_olustur)

        self.siparis_listesi = QListWidget(self)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ürün Adı:"))
        layout.addWidget(self.urun_ad_giris)
        layout.addWidget(QLabel("Ürün Stok Miktarı:"))
        layout.addWidget(self.urun_stok_giris)
        layout.addWidget(self.ekle_buton)
        layout.addWidget(self.stok_goster_buton)
        layout.addWidget(self.siparis_buton)
        layout.addWidget(QLabel("Sipariş Listesi:"))
        layout.addWidget(self.siparis_listesi)

        self.urun_listesi = QListWidget(self)
        self.urun_listesi.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(QLabel("Stok Listesi:"))
        layout.addWidget(self.urun_listesi)

        self.setLayout(layout)

    def urun_ekle(self):
        ad = self.urun_ad_giris.text()
        try:
            stok_miktari = int(self.urun_stok_giris.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Stok miktarı geçerli bir sayı olmalıdır.")
            return

        urun = Product(ad, stok_miktari)
        self.stok.add_product(urun)
        self.urun_ad_giris.clear()
        self.urun_stok_giris.clear()

        self.urun_listesi.addItem(f"{ad} - Stok: {stok_miktari}")

    def stok_goster(self):
        self.urun_listesi.clear()
        for product in self.stok.products.values():
            self.urun_listesi.addItem(f"{product.name} - Stok: {product.stock_quantity}")

    def siparis_olustur(self):
        urun_ad = self.urun_ad_giris.text()
        try:
            miktar = int(self.urun_stok_giris.text())
        except ValueError:
            QMessageBox.warning(self, "Hata", "Geçerli bir miktar girin.")
            return

        product = self.stok.get_product(urun_ad)
        if not product or product.stock_quantity < miktar:
            QMessageBox.warning(self, "Hata", "Stokta yeterli ürün yok veya ürün bulunmuyor.")
            return

        siparis_id = len(self.siparisler) + 1
        siparis = Order(siparis_id, urun_ad, miktar)
        self.siparisler.append(siparis)
        self.siparis_listesi.addItem(str(siparis))

        product.stock_quantity -= miktar
        self.stok.update_product(urun_ad, product.stock_quantity)

        self.urun_ad_giris.clear()
        self.urun_stok_giris.clear()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = StokTakipArayuzu()
    window.show()
    sys.exit(app.exec_())