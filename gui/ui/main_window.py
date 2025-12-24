from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QSpinBox, QDoubleSpinBox
)
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt

import qtawesome as qta
from api import get_products, add_product


APP_QSS = """
QMainWindow { background: #0b0f1a; }
QLabel { color: #e6e6e6; }

#Sidebar {
    background: #0f1629;
    border-right: 1px solid #1e2a44;
}
#Brand {
    font-size: 16px;
    font-weight: 900;
    letter-spacing: 0.5px;
}
.SideBtn {
    text-align: left;
    padding: 12px 14px;
    border-radius: 12px;
    color: #d6d6d6;
    background: transparent;
    font-size: 13px;
}
.SideBtn:hover { background: rgba(59,130,246,0.10); }
.SideBtn:pressed { background: rgba(59,130,246,0.16); }

#Title { font-size: 22px; font-weight: 900; }
#Subtle { color:#9aa4b2; font-size:11px; font-weight:700; }

#Card {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 16px;
}
#MiniCardTitle { color:#9aa4b2; font-size:11px; font-weight:800; letter-spacing:0.6px; }
#MiniCardValue { color:#e6e6e6; font-size:20px; font-weight:900; }

#Chip {
    background: rgba(59,130,246,0.16);
    border: 1px solid rgba(59,130,246,0.35);
    border-radius: 999px;
    padding: 6px 10px;
    color: #cfe2ff;
    font-size: 11px;
    font-weight: 800;
}
#ChipDanger {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.30);
    border-radius: 999px;
    padding: 6px 10px;
    color: #ffd0d0;
    font-size: 11px;
    font-weight: 900;
}
#Divider { background: rgba(30,42,68,0.9); }

QLineEdit {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 12px;
    padding: 10px 12px;
    color: #e6e6e6;
    font-size: 13px;
}
QLineEdit:focus { border: 1px solid rgba(59,130,246,0.9); }

.SideBtnActive {
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.22);
}

QPushButton.SideBtn[active="true"] {
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.22);
}

#PrimaryBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 rgba(59,130,246,1), stop:1 rgba(99,102,241,1));
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    font-weight: 900;
}
#PrimaryBtn:hover { opacity: 0.95; }
#PrimaryBtn:pressed { opacity: 0.9; }

#GhostBtn {
    background: rgba(15, 22, 41, 0.6);
    color: #cfd8e3;
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid rgba(30, 42, 68, 0.9);
    font-weight: 800;
}
#GhostBtn:hover { background: rgba(59,130,246,0.10); }

QTableWidget {
    background: transparent;
    border: none;
    color: #e6e6e6;
    gridline-color: rgba(30,42,68,0.9);
    font-size: 13px;
}
QHeaderView::section {
    background: transparent;
    color: #9aa4b2;
    border: none;
    padding: 10px;
    font-weight: 900;
}
QTableWidget::item { padding: 10px; }
QTableWidget::item:selected { background: rgba(59,130,246,0.12); }

QTableCornerButton::section {
    background: transparent;
    border: none;
}

QHeaderView::section {
    background: rgba(15, 22, 41, 0.55);
    color: #9aa4b2;
    border: none;
    padding: 10px;
    font-weight: 900;
}

QDialog { background: #0b0f1a; }
QSpinBox, QDoubleSpinBox {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 12px;
    padding: 8px 10px;
    color: #e6e6e6;
}
QSpinBox:focus, QDoubleSpinBox:focus { border: 1px solid rgba(59,130,246,0.9); }
"""


def make_chip(text: str, danger: bool = False) -> QLabel:
    chip = QLabel(text)
    chip.setObjectName("ChipDanger" if danger else "Chip")
    chip.setAlignment(Qt.AlignCenter)
    return chip

def set_colored_icon(btn, icon_name: str, color: str, size: int = 18):
    btn.setIcon(qta.icon(icon_name, color=color))
    btn.setIconSize(QSize(size, size))


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Ürün")
        self.setModal(True)
        self.resize(440, 280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_row = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(qta.icon("fa5s.box-open").pixmap(18, 18))
        title = QLabel("Yeni Ürün Ekle")
        title.setStyleSheet("font-size:16px; font-weight:900;")
        title_row.addWidget(icon)
        title_row.addWidget(title)
        title_row.addStretch(1)
        layout.addLayout(title_row)

        form = QFormLayout()
        form.setSpacing(10)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Örn: Espresso")

        self.category = QLineEdit()
        self.category.setPlaceholderText("Örn: Kahve")

        self.stock = QSpinBox()
        self.stock.setRange(0, 1_000_000)

        self.price = QDoubleSpinBox()
        self.price.setRange(0, 1_000_000_000)
        self.price.setDecimals(2)

        form.addRow("Ürün Adı", self.name)
        form.addRow("Kategori", self.category)
        form.addRow("Stok", self.stock)
        form.addRow("Fiyat (₺)", self.price)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        cancel = QPushButton("İptal")
        cancel.setObjectName("GhostBtn")
        cancel.clicked.connect(self.reject)

        save = QPushButton("Kaydet")
        save.setObjectName("PrimaryBtn")
        save.clicked.connect(self.on_save)

        btn_row.addWidget(cancel)
        btn_row.addWidget(save)
        layout.addLayout(btn_row)

        self.result_payload = None

    def on_save(self):
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Uyarı", "Ürün adı boş olamaz.")
            return

        self.result_payload = {
            "name": name,
            "category": self.category.text().strip() or None,
            "stock": int(self.stock.value()),
            "price": float(self.price.value()),
        }
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok & Kasa")
        self.resize(1200, 760)

        self.all_products = []
        self.selected = None

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(252)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(14, 14, 14, 14)
        side_layout.setSpacing(10)

        brand_row = QHBoxLayout()
        brand_icon = QLabel()
        brand_icon.setPixmap(qta.icon("fa5s.mug-hot", color="#964B00").pixmap(18, 18))  # premium mavi
        brand = QLabel("StokKasa")
        brand.setObjectName("Brand")
        brand_row.addWidget(brand_icon)
        brand_row.addWidget(brand)
        brand_row.addStretch(1)
        side_layout.addLayout(brand_row)

        side_layout.addSpacing(8)

        self.btn_products = QPushButton(" Ürünler")
        set_colored_icon(self.btn_products, "fa5s.boxes", "#3b82f6")      # mavi

        self.btn_dashboard = QPushButton(" Dashboard")
        set_colored_icon(self.btn_dashboard, "fa5s.chart-pie", "#22c55e") # yeşil

        self.btn_cash = QPushButton(" Kasa")
        set_colored_icon(self.btn_cash, "fa5s.wallet", "#f59e0b")         # turuncu

        self.btn_reports = QPushButton(" Raporlar")
        set_colored_icon(self.btn_reports, "fa5s.chart-line", "#a855f7")  # mor

        self.btn_products.clicked.connect(lambda: self.set_active_sidebar(self.btn_products))
        self.btn_dashboard.clicked.connect(lambda: self.set_active_sidebar(self.btn_dashboard))
        self.btn_cash.clicked.connect(lambda: self.set_active_sidebar(self.btn_cash))
        self.btn_reports.clicked.connect(lambda: self.set_active_sidebar(self.btn_reports))

        # başlangıç
        self.set_active_sidebar(self.btn_products)

        for b in (self.btn_dashboard, self.btn_products, self.btn_cash, self.btn_reports):
            b.setProperty("class", "SideBtn")
            b.setCursor(Qt.PointingHandCursor)
            side_layout.addWidget(b)

        side_layout.addStretch(1)
        hint = QLabel("v0.3 • FastAPI • Local")
        hint.setObjectName("Subtle")
        side_layout.addWidget(hint)

        # Content
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(18, 18, 18, 18)
        content_layout.setSpacing(14)

        # Topbar
        top = QHBoxLayout()
        self.title = QLabel("Ürünler")
        self.title.setObjectName("Title")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Ara: ürün / kategori…")
        self.search.textChanged.connect(self.apply_filter)

        self.btn_refresh = QPushButton(" Yenile")
        self.btn_refresh.setIcon(qta.icon("fa5s.sync-alt", color="#cfd8e3"))
        self.btn_refresh.setObjectName("GhostBtn")
        self.btn_refresh.clicked.connect(self.load_products)

        self.btn_new = QPushButton(" + Yeni Ürün")
        self.btn_new.setIcon(qta.icon("fa5s.plus", color="#ffffff"))
        self.btn_new.setObjectName("PrimaryBtn")
        self.btn_new.clicked.connect(self.open_add_dialog)

        top.addWidget(self.title)
        top.addStretch(1)
        top.addWidget(self.search, 2)
        top.addWidget(self.btn_refresh)
        top.addWidget(self.btn_new)
        content_layout.addLayout(top)

        # Stats row
        stats = QHBoxLayout()
        stats.setSpacing(12)
        self.card_total_products = self.make_stat_card(
            "TOPLAM ÜRÜN", "0", "fa5s.cubes", "#3b82f6"      # mavi
        )

        self.card_total_stock = self.make_stat_card(
            "TOPLAM STOK", "0", "fa5s.layer-group", "#22c55e"  # yeşil
        )

        self.card_avg_price = self.make_stat_card(
            "ORT. FİYAT", "₺0.00", "fa5s.tags", "#f59e0b"      # turuncu
        )
        stats.addWidget(self.card_total_products)
        stats.addWidget(self.card_total_stock)
        stats.addWidget(self.card_avg_price)
        stats.addStretch(1)
        content_layout.addLayout(stats)

        # Main area: table + detail panel
        main_row = QHBoxLayout()
        main_row.setSpacing(12)

        # Table card
        table_card = QFrame()
        table_card.setObjectName("Card")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(14, 14, 14, 14)
        table_layout.setSpacing(10)

        head_row = QHBoxLayout()
        head = QLabel("Stok Tablosu")
        head.setStyleSheet("font-size:13px; font-weight:900; color:#cfd8e3;")
        head_row.addWidget(head)
        head_row.addStretch(1)
        self.critical_chip = make_chip("Kritik stok: < 5", danger=True)
        head_row.addWidget(self.critical_chip)
        table_layout.addLayout(head_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Ürün", "Kategori", "Stok / Fiyat"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False) 
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.on_row_selected)
        table_layout.addWidget(self.table)

        # Detail panel
        detail = QFrame()
        detail.setObjectName("Card")
        detail.setFixedWidth(320)
        dlay = QVBoxLayout(detail)
        dlay.setContentsMargins(14, 14, 14, 14)
        dlay.setSpacing(10)

        dhead = QLabel("Ürün Detayı")
        dhead.setStyleSheet("font-size:13px; font-weight:900; color:#cfd8e3;")
        dlay.addWidget(dhead)

        self.detail_name = QLabel("Bir ürün seç")
        self.detail_name.setStyleSheet("font-size:18px; font-weight:900;")
        dlay.addWidget(self.detail_name)

        self.detail_chips_row = QHBoxLayout()
        self.detail_chip_category = make_chip("Kategori: -")
        self.detail_chip_stock = make_chip("Stok: -")
        self.detail_chips_row.addWidget(self.detail_chip_category)
        self.detail_chips_row.addWidget(self.detail_chip_stock)
        self.detail_chips_row.addStretch(1)
        dlay.addLayout(self.detail_chips_row)

        line = QFrame()
        line.setObjectName("Divider")
        line.setFixedHeight(1)
        dlay.addWidget(line)

        self.detail_price = QLabel("₺0.00")
        self.detail_price.setStyleSheet("font-size:26px; font-weight:900;")
        dlay.addWidget(self.detail_price)

        self.detail_hint = QLabel("Satış/Gider/Gelir ekranlarını sonra bağlayacağız.")
        self.detail_hint.setObjectName("Subtle")
        self.detail_hint.setWordWrap(True)
        dlay.addWidget(self.detail_hint)

        dlay.addStretch(1)

        main_row.addWidget(table_card, 1)
        main_row.addWidget(detail)
        content_layout.addLayout(main_row, 1)

        # Assemble
        root_layout.addWidget(sidebar)
        root_layout.addWidget(content, 1)

        self.setStyleSheet(APP_QSS)

        # default
        self.load_products()

    def set_active_sidebar(self, active_btn):
        for b in (self.btn_dashboard, self.btn_products, self.btn_cash, self.btn_reports):
            b.setProperty("active", False)
            b.setStyleSheet("")  # refresh

        active_btn.setProperty("active", True)
        active_btn.setStyleSheet("")  # refresh

    def make_stat_card(self, title: str, value: str, icon_name: str, icon_color: str) -> QFrame:
        c = QFrame()
        c.setObjectName("Card")
        c.setFixedHeight(88)

        lay = QHBoxLayout(c)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(10)

        ic = QLabel()
        ic.setPixmap(qta.icon(icon_name, color=icon_color).pixmap(18, 18))

        text = QVBoxLayout()
        t = QLabel(title); t.setObjectName("MiniCardTitle")
        v = QLabel(value); v.setObjectName("MiniCardValue")
        text.addWidget(t); text.addWidget(v)

        lay.addWidget(ic)
        lay.addLayout(text)
        lay.addStretch(1)

        c.value_label = v
        return c

    def set_loading(self, loading: bool):
        self.btn_refresh.setDisabled(loading)
        self.btn_new.setDisabled(loading)
        self.search.setDisabled(loading)
        if loading:
            self.title.setText("Ürünler • Yükleniyor…")
        else:
            self.title.setText("Ürünler")

    def set_colored_icon(btn: QPushButton, icon_name: str, color: str, size: int = 18):
        btn.setIcon(qta.icon(icon_name, color=color))
        btn.setIconSize(QSize(size, size))

    def open_add_dialog(self):
        dlg = AddProductDialog(self)
        if dlg.exec() == QDialog.Accepted and dlg.result_payload:
            try:
                self.set_loading(True)
                add_product(dlg.result_payload)
                self.load_products()
            except Exception as e:
                self.set_loading(False)
                QMessageBox.critical(self, "Hata", f"Ürün eklenemedi:\n{e}")

    def load_products(self):
        try:
            self.set_loading(True)
            self.all_products = get_products()
            self.apply_filter()
            self.set_loading(False)
        except Exception as e:
            self.set_loading(False)
            QMessageBox.critical(self, "Hata", f"API'den ürünler çekilemedi:\n{e}")

    def apply_filter(self):
        q = (self.search.text() or "").strip().lower()
        filtered = self.all_products

        if q:
            def match(p):
                name = (p.get("name") or "").lower()
                cat = (p.get("category") or "").lower()
                return (q in name) or (q in cat)
            filtered = [p for p in self.all_products if match(p)]

        total_products = len(filtered)
        total_stock = sum(int(p.get("stock") or 0) for p in filtered) if filtered else 0
        avg_price = (sum(float(p.get("price") or 0) for p in filtered) / total_products) if total_products else 0.0

        self.card_total_products = self.make_stat_card("TOPLAM ÜRÜN", "0", "fa5s.cubes", "#3b82f6")      # mavi
        self.card_total_stock    = self.make_stat_card("TOPLAM STOK", "0", "fa5s.layer-group", "#22c55e") # yeşil
        self.card_avg_price      = self.make_stat_card("ORT. FİYAT", "₺0.00", "fa5s.tags", "#f59e0b")     # turuncu

        self.table.setRowCount(0)
        if not filtered:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("-"))
            self.table.setItem(0, 1, QTableWidgetItem("Sonuç yok. Aramayı temizle veya '+ Yeni Ürün' ekle."))
            self.table.setItem(0, 2, QTableWidgetItem(""))
            self.table.setItem(0, 3, QTableWidgetItem(""))
            self.detail_name.setText("Bir ürün seç")
            self.detail_price.setText("₺0.00")
            self.detail_chip_category.setText("Kategori: -")
            self.detail_chip_stock.setText("Stok: -")
            return

        self.table.setRowCount(len(filtered))
        for r, p in enumerate(filtered):
            self.table.setItem(r, 0, QTableWidgetItem(str(p["id"])))
            self.table.setItem(r, 1, QTableWidgetItem(str(p["name"])))
            self.table.setItem(r, 2, QTableWidgetItem(str(p.get("category") or "-")))

            stock = int(p.get("stock") or 0)
            price = float(p.get("price") or 0)
            text = f"Stok: {stock}   |   ₺{price:.2f}"
            self.table.setItem(r, 3, QTableWidgetItem(text))

        # otomatik ilk satırı seç (premium his)
        self.table.selectRow(0)
        self.on_row_selected(0, 0)

    def on_row_selected(self, row: int, col: int):
        try:
            pid_item = self.table.item(row, 0)
            if not pid_item:
                return
            pid = int(pid_item.text())

            p = next((x for x in self.all_products if int(x["id"]) == pid), None)
            if not p:
                return

            name = p.get("name") or "-"
            cat = p.get("category") or "-"
            stock = int(p.get("stock") or 0)
            price = float(p.get("price") or 0)

            self.detail_name.setText(name)
            self.detail_price.setText(f"₺{price:.2f}")

            self.detail_chip_category.setText(f"Kategori: {cat}")

            # stok chip: kritikse kırmızı
            if stock < 5:
                self.detail_chip_stock.setObjectName("ChipDanger")
                self.detail_chip_stock.setText(f"Kritik Stok: {stock}")
            else:
                self.detail_chip_stock.setObjectName("Chip")
                self.detail_chip_stock.setText(f"Stok: {stock}")

            # ObjectName değişince style yenile
            self.detail_chip_stock.style().unpolish(self.detail_chip_stock)
            self.detail_chip_stock.style().polish(self.detail_chip_stock)

        except Exception:
            pass