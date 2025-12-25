from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QMessageBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFormLayout, QSpinBox, QDoubleSpinBox,
)
from PySide6.QtCore import QSize
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor


import qtawesome as qta
from api import get_products, add_product, update_product, delete_product


APP_QSS = """
QMainWindow { background: #0b0f1a; }
QLabel { color: #e6e6e6; }

/* ===== SIDEBAR ===== */
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
    border: 1px solid transparent;
}
.SideBtn:hover { background: rgba(59,130,246,0.10); }
.SideBtn:pressed { background: rgba(59,130,246,0.16); }

QPushButton.SideBtn[active="true"] {
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.22);
}

/* ===== HEADERS ===== */
#Title { font-size: 22px; font-weight: 900; }
#Subtle { color:#9aa4b2; font-size:11px; font-weight:700; }

/* ===== CARDS ===== */
#Card {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 16px;
}
#MiniCardTitle { color:#9aa4b2; font-size:11px; font-weight:800; letter-spacing:0.6px; }
#MiniCardValue { color:#e6e6e6; font-size:20px; font-weight:900; }

/* ===== CHIPS ===== */
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

/* ===== INPUTS ===== */
QLineEdit {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 12px;
    padding: 10px 12px;
    color: #e6e6e6;
    font-size: 13px;
}
QLineEdit:focus { border: 1px solid rgba(59,130,246,0.9); }

/* ===== BUTTONS ===== */
#PrimaryBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 rgba(59,130,246,1), stop:1 rgba(99,102,241,1));
    color: white;
    padding: 10px 14px;
    border-radius: 12px;
    font-weight: 900;
    border: none;
}
#PrimaryBtn:hover { background: rgba(59,130,246,0.92); }
#PrimaryBtn:pressed { background: rgba(59,130,246,0.82); }

#GhostBtn {
    background: rgba(15, 22, 41, 0.6);
    color: #cfd8e3;
    padding: 10px 14px;
    border-radius: 12px;
    border: 1px solid rgba(30, 42, 68, 0.9);
    font-weight: 800;
}
#GhostBtn:hover { background: rgba(59,130,246,0.10); }

/* ===== TABLE (SAFE + PREMIUM) ===== */
QTableWidget {
    background: transparent;
    border: none;
    color: #e6e6e6;
    gridline-color: rgba(30,42,68,0.35);
    font-size: 13px;
}

QHeaderView::section {
    background: rgba(15, 22, 41, 0.55);
    color: #cfd8ff;
    border: none;
    padding: 10px;
    font-weight: 900;
}

QTableWidget::item {
    padding: 10px;
    color: #e6ebff;
    border: none;
}

QTableWidget::item:hover {
    background: rgba(120,140,255,0.10);
}

/* ✅ Seçimde yazı görünür: color white */
QTableWidget::item:selected {
    background: rgba(59,130,246,0.35);
    color: #ffffff;
}

QTableCornerButton::section {
    background: transparent;
    border: none;
}

/* ===== DIALOG + SPIN ===== */
QDialog { background: #0b0f1a; }

QSpinBox, QDoubleSpinBox {
    background: rgba(15, 22, 41, 0.85);
    border: 1px solid rgba(30, 42, 68, 0.9);
    border-radius: 12px;
    padding: 8px 10px;
    color: #e6e6e6;
}
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 1px solid rgba(59,130,246,0.9);
}
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
    def __init__(self, parent=None, initial = None):
        super().__init__(parent)
        self.initial = initial or {}
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
        is_edit = bool(self.initial.get("id"))
        title.setText("Ürünü Düzenle" if is_edit else "Yeni Ürün Ekle")

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

        if self.initial:
            self.name.setText(str(self.initial.get("name", "") or ""))
            self.category.setText(str(self.initial.get("category", "") or ""))
            self.stock.setValue(int(self.initial.get("stock", 0) or 0))
            self.price.setValue(float(self.initial.get("price", 0) or 0))

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


class ClickableTable(QTableWidget):
    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        #Boş alana tıklandıysa seçimi kaldırır.
        if item is None:
            self.clearSelection()
            self.setCurrentCell(-1, -1)
        super().mousePressEvent(event)

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
            "TOPLAM ÜRÜN", "0", "fa5s.cubes", "#3b82f6"      
        )

        self.card_total_stock = self.make_stat_card(
            "TOPLAM STOK", "0", "fa5s.layer-group", "#22c55e"  
        )

        self.card_avg_price = self.make_stat_card(
            "ORT. FİYAT", "₺0.00", "fa5s.tags", "#f59e0b"      
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

        self.table = ClickableTable(0, 4)
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
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
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

        # Actions
        actions = QHBoxLayout()
        actions.setSpacing(10)

        self.btn_edit = QPushButton(" Düzenle")
        self.btn_edit.setIcon(qta.icon("fa5s.edit", color="#ffffff"))
        self.btn_edit.setObjectName("GhostBtn")
        self.btn_edit.setCursor(Qt.PointingHandCursor)
        self.btn_edit.clicked.connect(self.edit_selected)

        self.btn_delete = QPushButton(" Sil")
        self.btn_delete.setIcon(qta.icon("fa5s.trash", color="#ffffff"))
        self.btn_delete.setObjectName("GhostBtn")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(self.delete_selected)

        actions.addWidget(self.btn_edit)
        actions.addWidget(self.btn_delete)
        dlay.addLayout(actions)

        # başlangıçta pasif
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)


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


    def sync_selected_from_table(self) -> bool:
        row = self.table.currentRow()
        if row < 0:
            return False

        item_id = self.table.item(row, 0)
        if not item_id:
            return False

        p = item_id.data(Qt.UserRole)
        if not p or not isinstance(p, dict) or p.get("id") is None:
            return False

        self.selected = p
        if hasattr(self, "btn_edit"):
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)

        # detail panel varsa güncelle
        if hasattr(self, "update_detail_panel"):
            self.update_detail_panel(p)

        return True


    def update_detail_panel(self, p: dict):
        name = p.get("name") or "-"
        cat = p.get("category") or "-"
        stock = int(p.get("stock") or 0)
        price = float(p.get("price") or 0)

        self.detail_name.setText(name)
        self.detail_price.setText(f"₺{price:.2f}")

        self.detail_chip_category.setText(f"Kategori: {cat}")

        if stock < 5:
            self.detail_chip_stock.setObjectName("ChipDanger")
            self.detail_chip_stock.setText(f"Kritik Stok: {stock}")
        else:
            self.detail_chip_stock.setObjectName("Chip")
            self.detail_chip_stock.setText(f"Stok: {stock}")

        self.detail_chip_stock.style().unpolish(self.detail_chip_stock)
        self.detail_chip_stock.style().polish(self.detail_chip_stock)



    def on_selection_changed(self):
        row = self.table.currentRow()
        if row < 0:
            self.selected = None
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)

            # boş state
            self.detail_name.setText("Bir ürün seç")
            self.detail_price.setText("₺0.00")
            self.detail_chip_category.setText("Kategori: -")
            self.detail_chip_stock.setObjectName("Chip")
            self.detail_chip_stock.setText("Stok: -")
            self.detail_chip_stock.style().unpolish(self.detail_chip_stock)
            self.detail_chip_stock.style().polish(self.detail_chip_stock)
            return

        self.sync_selected_from_table()

        item_id = self.table.item(row, 0)
        if not item_id:
            self.selected = None
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            return

        p = item_id.data(Qt.UserRole)  # ✅ direkt ürün objesi
        if not p or not isinstance(p, dict) or p.get("id") is None:
            self.selected = None
            self.btn_edit.setEnabled(False)
            self.btn_delete.setEnabled(False)
            return

        self.selected = p
        self.btn_edit.setEnabled(True)
        self.btn_delete.setEnabled(True)

        # Detay panelini güncelle (varsa)
        self.update_detail_panel(p)


    def edit_selected(self):
        if not self.selected:
            self.sync_selected_from_table()

        if not self.selected:
            QMessageBox.warning(self, "Uyarı", "Önce bir ürün seç.")
            return

        pid = self.selected.get("id")
        if pid is None:
            QMessageBox.critical(self, "Hata", f"Seçili üründe id yok: {self.selected}")
            return

        dlg = AddProductDialog(self, initial=self.selected)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return

        if not dlg.result_payload:
            QMessageBox.warning(self, "Uyarı", "Form verisi alınamadı.")
            return

        try:
            self.set_loading(True)
            update_product(int(pid), dlg.result_payload)
            self.load_products()
        except Exception as e:
            self.set_loading(False)
            QMessageBox.critical(self, "Hata", f"Ürün güncellenemedi:\n{e}")

        if not self.selected:
            QMessageBox.warning(self, "Uyarı", "Önce bir ürün seç.")
            return

        pid = self.selected.get("id")
        if pid is None:
            QMessageBox.critical(self, "Hata", f"Seçili ürün id yok!\nselected={self.selected}")
            return

        dlg = AddProductDialog(self, initial=self.selected)
        res = dlg.exec()

        if res != 1:
            return

        payload = dlg.result_payload
        if not payload:
            QMessageBox.warning(self, "Uyarı", "Payload boş geldi.")
            return

        try:
            self.set_loading(True)
            update_product(int(pid), payload)
            self.load_products()
        except Exception as e:
            self.set_loading(False)
            QMessageBox.critical(self, "Hata", f"Update patladı:\n{e}")


    def delete_selected(self):
        if not self.selected:
            QMessageBox.warning(self, "Uyarı", "Önce bir ürün seç.")
            return

        pid = self.selected.get("id")
        if pid is None:
            QMessageBox.critical(self, "Hata", f"Seçili ürün id yok!\nselected={self.selected}")
            return

        name = self.selected.get("name", "Ürün")
        reply = QMessageBox.question(
            self,
            "Silme Onayı",
            f"'{name}' silinsin mi?\nBu işlem geri alınamaz.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.set_loading(True)
            delete_product(int(pid))
            self.selected = None
            self.load_products()
        except Exception as e:
            self.set_loading(False)
            QMessageBox.critical(self, "Hata", f"Delete patladı:\n{e}")


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
        self.selected = None
        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
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
            item_id = QTableWidgetItem(str(p["id"]))
            item_id.setData(Qt.UserRole, p)          # ✅ Ürünü satıra gömdük
            self.table.setItem(r, 0, item_id)

            self.table.setItem(r, 1, QTableWidgetItem(str(p["name"])))
            self.table.setItem(r, 2, QTableWidgetItem(str(p.get("category") or "-")))

            stock = int(p.get("stock") or 0)
            price = float(p.get("price") or 0)
            self.table.setItem(r, 3, QTableWidgetItem(f"Stok: {stock}   |   ₺{price:.2f}"))
            # kritik stok highlight
            if stock < 5:
                for c in range(self.table.columnCount()):
                    it = self.table.item(r, c)
                    if it:
                        it.setBackground(QColor(180, 60, 60, 120))  # soft kırmızı




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
            self.selected = p
            self.btn_edit.setEnabled(True)
            self.btn_delete.setEnabled(True)
            self.selected = None
            if hasattr(self, "btn_edit"):
                self.btn_edit.setEnabled(True)
                self.btn_delete.setEnabled(True)

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