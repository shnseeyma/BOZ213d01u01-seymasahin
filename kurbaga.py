import tkinter as tk
import time

# ---------------- AYARLAR ----------------
HIZ_KMH = 6.0                     # koşu hızı (km/saat)
HIZ = HIZ_KMH * 1000 / 3600       # m/s  (~1.667 m/s)
ZIPLAMA = {"a": 2.0, "w": 3.0, "s": 0.5}   # tuş -> metre
ZIPLAMA_SURESI = 0.25             # bir zıplamanın süresi (sn)
SU_UZUNLUK = 1.5                  # su engeli uzunluğu (m)
TOPRAK_ALAN = 2.0                 # su engelinden sonraki güvenli toprak alan (m)
SU_ARALIK = 10.0                  # kaç saniyede bir su çıkar
SU_MESAFE = 8.0                   # su, kurbağanın kaç metre önünde çıkar
AV_HIZ = 1.2                      # kovalanan avın hızı (m/s)
AV_BASLANGIC = 25.0               # av başta kaç metre önde
PX_M = 100                        # 1 metre = 100 piksel
EKRAN_W, EKRAN_H = 900, 400
ZEMIN_Y = 280
KURBAGA_EKRAN_X = 200


class Oyun:
    def __init__(self, root):
        self.root = root
        root.title("Kurbağa Kovalamaca")
        self.canvas = tk.Canvas(root, width=EKRAN_W, height=EKRAN_H, bg="#9fd8ff")
        self.canvas.pack()
        root.bind("<KeyPress>", self.tus)
        self.sifirla()
        self.son = time.time()
        self.dongu()

    def sifirla(self):
        self.x = 0.0                 # kurbağa konumu (m)
        self.av_x = AV_BASLANGIC
        self.sureler = 0.0
        self.sonraki_su = SU_ARALIK
        self.sular = []              # (baslangic, bitis) metre
        self.ziplama = None          # (baslangic_x, hedef_x, gecen_sure)
        self.bitti = False
        self.mesaj = ""

    # ---------- Girdi ----------
    def tus(self, e):
        k = e.keysym.lower()
        if k == "r":
            self.sifirla()
            return
        if self.bitti or self.ziplama is not None:
            return
        if k in ZIPLAMA:
            self.ziplama = (self.x, self.x + ZIPLAMA[k], 0.0)

    # ---------- Mantık ----------
    def suda_mi(self, x):
        return any(b <= x <= s for b, s in self.sular)

    def bitir(self, mesaj):
        self.bitti = True
        self.mesaj = mesaj

    def guncelle(self, dt):
        if self.bitti:
            return
        self.sureler += dt
        self.av_x += AV_HIZ * dt

        # Her 10 saniyede bir su engeli
        if self.sureler >= self.sonraki_su:
            self.sonraki_su += SU_ARALIK
            baslangic = max(self.x + SU_MESAFE, self.av_x if False else 0)
            # son suyun + toprak alanın sonrasında olsun
            if self.sular:
                baslangic = max(baslangic, self.sular[-1][1] + TOPRAK_ALAN)
            self.sular.append((baslangic, baslangic + SU_UZUNLUK))

        # Hareket
        if self.ziplama:
            bx, hx, t = self.ziplama
            t += dt
            if t >= ZIPLAMA_SURESI:
                self.x = hx
                self.ziplama = None
                if self.suda_mi(self.x):
                    self.bitir("Suya düştün! Kaybettin.  (R = yeniden başla)")
            else:
                self.x = bx + (hx - bx) * (t / ZIPLAMA_SURESI)
                self.ziplama = (bx, hx, t)
        else:
            self.x += HIZ * dt
            if self.suda_mi(self.x):
                self.bitir("Suya düştün! Kaybettin.  (R = yeniden başla)")

        if not self.bitti and self.x >= self.av_x:
            self.bitir("Avı yakaladın! Kazandın!  (R = yeniden başla)")

    # ---------- Çizim ----------
    def ekran_x(self, metre):
        return KURBAGA_EKRAN_X + (metre - self.x) * PX_M

    def ciz(self):
        c = self.canvas
        c.delete("all")
        # zemin (toprak)
        c.create_rectangle(0, ZEMIN_Y, EKRAN_W, EKRAN_H, fill="#8b5a2b", outline="")
        c.create_rectangle(0, ZEMIN_Y, EKRAN_W, ZEMIN_Y + 12, fill="#4caf50", outline="")
        # sular
        for b, s in self.sular:
            c.create_rectangle(self.ekran_x(b), ZEMIN_Y, self.ekran_x(s), EKRAN_H,
                               fill="#1e6fd9", outline="")
        # av (sinek)
        ax = self.ekran_x(self.av_x)
        if -50 < ax < EKRAN_W + 50:
            c.create_oval(ax - 8, ZEMIN_Y - 40, ax + 8, ZEMIN_Y - 28, fill="black")
            c.create_oval(ax - 14, ZEMIN_Y - 48, ax, ZEMIN_Y - 38, fill="white")
        else:
            c.create_text(EKRAN_W - 60, 60, text="Av →  %.0f m" % (self.av_x - self.x),
                          font=("Arial", 12), fill="black")
        # kurbağa (zıplarken yay çizer)
        yukari = 0
        if self.ziplama:
            oran = self.ziplama[2] / ZIPLAMA_SURESI
            yukari = 4 * oran * (1 - oran) * 70
        kx, ky = KURBAGA_EKRAN_X, ZEMIN_Y - 20 - yukari
        c.create_oval(kx - 22, ky - 16, kx + 22, ky + 16, fill="#2ecc40", outline="black")
        c.create_oval(kx + 6, ky - 24, kx + 18, ky - 12, fill="white", outline="black")
        c.create_oval(kx - 8, ky - 24, kx + 4, ky - 12, fill="white", outline="black")
        c.create_oval(kx + 10, ky - 21, kx + 15, ky - 15, fill="black")
        c.create_oval(kx - 4, ky - 21, kx + 1, ky - 15, fill="black")
        # HUD
        kalan = max(0.0, self.sonraki_su - self.sureler)
        c.create_text(10, 10, anchor="nw", font=("Arial", 12), text=(
            "Süre: %.1f sn   Mesafe: %.1f m   Sonraki su: %.1f sn\n"
            "A = 2 m   W = 3 m   S = 0.5 m zıpla   |   Hız: %.0f km/s"
            % (self.sureler, self.x, kalan, HIZ_KMH)))
        if self.bitti:
            c.create_rectangle(120, 130, EKRAN_W - 120, 210, fill="white", outline="black")
            c.create_text(EKRAN_W // 2, 170, text=self.mesaj, font=("Arial", 16, "bold"))

    def dongu(self):
        simdi = time.time()
        dt = min(simdi - self.son, 0.05)
        self.son = simdi
        self.guncelle(dt)
        self.ciz()
        self.root.after(16, self.dongu)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    Oyun(root)
    root.mainloop()
