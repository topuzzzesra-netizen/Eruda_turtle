import turtle
import os
import inspect

# ==========================================
# Gelişmiş Modüler Eruda UI Kütüphanesi
# ==========================================
class ErudaTurtle:
    def __init__(self, target_instance=None, position="sag-alt"):
        """
        :param target_instance: İncelenecek Python sınıfı/nesnesi (Elements için)
        :param position: Çark butonunun yeri -> 'sag-alt', 'sag-ust', 'sol-alt', 'sol-ust'
        """
        self.target_instance = target_instance
        self.position = position
        self.konsol_acik = True
        self.aktif_ana_sekme = "Console"
        self.aktif_filtre = "All"
        self.scroll_y = 0  # Kaydırma (Scroll) Konumu

        self._logs = []

        # Varsayılan düğüm açılış durumları (Hepsi kapalı başlar)
        self.node_states = {
            "root": False,
            "imports": False,
            "classes": False,
            "methods": False
        }

        # Turtle Ekran Ayarları
        self.ekran = turtle.Screen()
        self.ekran.title("QuickEdit Preview Engine")
        self.ekran.setup(width=360, height=640)
        self.ekran.setworldcoordinates(0, 0, 360, 640)
        self.ekran.bgcolor("#121212")
        self.ekran.tracer(0)

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.speed(0)

        # Olay Dinleyicileri (Tıklama ve Kaydırma)
        self.ekran.onclick(self._tiklama_yonetici)
        self.ekran.listen()
        
        # Fare Kaydırma (Scroll) Bağlantıları
        self.ekran.getcanvas().bind("<Button-4>", lambda e: self._scroll(15))   # Linux/Mac Yukarı
        self.ekran.getcanvas().bind("<Button-5>", lambda e: self._scroll(-15))  # Linux/Mac Aşağı
        self.ekran.getcanvas().bind("<MouseWheel>", lambda e: self._scroll(15 if e.delta > 0 else -15)) # Win

    def log(self, mesaj):
        """Herhangi bir Python kodundan konsola log basma fonksiyonu"""
        self._logs.append(str(mesaj))
        self.render()

    def _scroll(self, delta):
        """Fare tekerleği döndükçe ekranın kaymasını sağlar"""
        if self.konsol_acik:
            self.scroll_y = max(0, self.scroll_y + delta)
            self.render()

    def _buton_koordinatlari(self):
        """Butonun seçilen köşeye göre konumunu hesaplar"""
        if self.position == "sag-alt":
            return 295, 260
        elif self.position == "sag-ust":
            return 295, 570
        elif self.position == "sol-alt":
            return 15, 260
        elif self.position == "sol-ust":
            return 15, 570
        return 295, 260

    def _dikdortgen_ciz(self, x, y, g, yk, renk, kenarlik_renk=None):
        self.t.goto(x, y)
        self.t.fillcolor(renk)
        self.t.pencolor(kenarlik_renk if kenarlik_renk else renk)
        self.t.pensize(1)
        self.t.begin_fill()
        for _ in range(2):
            self.t.forward(g)
            self.t.left(90)
            self.t.forward(yk)
            self.t.left(90)
        self.t.end_fill()

    def _yuzen_buton_ciz(self):
        x, y = self._buton_koordinatlari()
        self._dikdortgen_ciz(x, y, 45, 45, "#1c1c1c", "#333333")
        self.t.goto(x + 22, y + 10)
        self.t.color("#aaaaaa")
        self.t.write("⚙", align="center", font=("Arial", 18, "normal"))

    def render(self):
        self.t.clear()

        if self.konsol_acik:
            self._dikdortgen_ciz(0, 0, 360, 350, "#181818")

            # Ana Sekmeler
            self._dikdortgen_ciz(0, 310, 360, 40, "#2b2b2b")
            sekmeler = [("Console", 0), ("Elements", 72), ("Network", 144), ("Resources", 216), ("Info", 288)]

            for isim, x_pos in sekmeler:
                is_active = (self.aktif_ana_sekme == isim)
                self._dikdortgen_ciz(x_pos, 310, 72, 40, "#000000" if is_active else "#2b2b2b")
                self.t.goto(x_pos + 36, 322)
                self.t.color("#ffffff" if is_active else "#999999")
                self.t.write(isim, align="center", font=("Arial", 9, "bold" if is_active else "normal"))

            # İçerik Alanı Renderlama
            if self.aktif_ana_sekme == "Console":
                self._render_console_tab()
            elif self.aktif_ana_sekme == "Elements":
                self._render_elements_tab()
            elif self.aktif_ana_sekme == "Network":
                self._render_network_tab()
            elif self.aktif_ana_sekme == "Resources":
                self._render_resources_tab()
            elif self.aktif_ana_sekme == "Info":
                self._render_info_tab()

            # Alt Girdi Çubuğu
            self._dikdortgen_ciz(0, 0, 360, 30, "#121212", "#222222")
            self.t.goto(12, 8)
            self.t.color("#666666")
            self.t.write(">", font=("Consolas", 12, "bold"))

        self._yuzen_buton_ciz()
        self.ekran.update()

    def _render_console_tab(self):
        y = 275 + self.scroll_y
        for log in self._logs:
            if 30 <= y <= 300: # Ekranda görünür bölgede tutma
                self.t.goto(10, y)
                self.t.color("#888888")
                self.t.write(">", font=("Consolas", 10, "normal"))
                self.t.goto(25, y)
                self.t.color("#ffffff")
                self.t.write(log, font=("Consolas", 10, "normal"))
            y -= 22

    def _render_elements_tab(self):
        """Herhangi bir nesneyi otomatik inceleyen ağaç (Dinamik Kaydırmalı)"""
        y = 285 + self.scroll_y

        ok_root = "▼" if self.node_states["root"] else "▶"
        target_name = self.target_instance.__class__.__name__ if self.target_instance else "MainApp"
        
        self.t.goto(10, y)
        self.t.color("#e5c07b")
        self.t.write(f"{ok_root} <module '{target_name}'>", font=("Consolas", 9, "bold"))
        y -= 18

        if self.node_states["root"]:
            # Modül Metotları
            ok_cls = "▼" if self.node_states["classes"] else "▶"
            self.t.goto(22, y)
            self.t.color("#61afef")
            self.t.write(f"{ok_cls} class {target_name}:", font=("Consolas", 9, "normal"))
            y -= 18

            if self.node_states["classes"] and self.target_instance:
                methods = [m for m in dir(self.target_instance) if not m.startswith('__')]
                for m in methods:
                    self.t.goto(34, y)
                    self.t.color("#98c379")
                    self.t.write(f"def {m}():", font=("Consolas", 8, "normal"))
                    y -= 16

    def _render_network_tab(self):
        self.t.goto(12, 280)
        self.t.color("#5c6370")
        self.t.write("STATUS  METHOD  NAME           SIZE", font=("Consolas", 9, "bold"))
        self.t.goto(12, 255)
        self.t.color("#98c379")
        self.t.write("200     GET     /local/app     1.2 KB", font=("Consolas", 9, "normal"))

    def _render_resources_tab(self):
        self.t.goto(12, 280)
        self.t.color("#e5c07b")
        self.t.write("▼ Dynamic Memory State", font=("Consolas", 9, "bold"))
        self.t.goto(12, 255)
        self.t.color("#abb2bf")
        self.t.write(f"  Logs Count: {len(self._logs)}", font=("Consolas", 9, "normal"))

    def _render_info_tab(self):
        self.t.color("#4fc3f7")
        self.t.goto(15, 240)
        self.t.write("Eruda Module v3.0", font=("Arial", 10, "bold"))
        self.t.goto(15, 215)
        self.t.write("Developer: gemini(AI) & yusuf", font=("Arial", 10, "bold"))

    def _tiklama_yonetici(self, x, y):
        bx, by = self._buton_koordinatlari()
        if bx <= x <= bx + 45 and by <= y <= by + 45:
            self.konsol_acik = not self.konsol_acik
            self.render()
            return

        if not self.konsol_acik:
            return

        # Sekme Geçişleri
        if 310 <= y <= 350:
            sekmeler = ["Console", "Elements", "Network", "Resources", "Info"]
            idx = int(x // 72)
            if 0 <= idx < len(sekmeler):
                self.aktif_ana_sekme = sekmeler[idx]
                self.scroll_y = 0  # Sekme değişince kaydırmayı sıfırla
                self.render()
            return

        # Elements Tıklamaları
        if self.aktif_ana_sekme == "Elements":
            if 270 <= y <= 295:
                self.node_states["root"] = not self.node_states["root"]
            elif 245 <= y <= 270 and self.node_states["root"]:
                self.node_states["classes"] = not self.node_states["classes"]
            self.render()


# =========================================================
# ÖRNEK KULLANIM: Başka herhangi bir Python kodunda kullanımı
# =========================================================
if __name__ == "__main__":
    
    # 1. Sen kendi kodlarını yazıyorsun
    class BenimUygulamam:
        def __init__(self):
            self.sayac = 0

        def veriyi_isle(self):
            self.sayac += 1

    app = BenimUygulamam()

    # 2. Eruda'yı koduna bağla (Köşeyi de belirle: 'sag-alt', 'sol-ust', vb.)
    eruda = ErudaTurtle(target_instance=app, position="sag-alt")

    # 3. İstediğin yerden log at
    eruda.log("Uygulama başlatıldı.")
    eruda.log("Veriler yükleniyor...")
    eruda.log("İşlem başarıyla tamamlandı.")

    turtle.mainloop()
