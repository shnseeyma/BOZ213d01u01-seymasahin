import random
import tkinter as tk
from tkinter import messagebox

# Örnek Kelime Havuzu: (Hedef Kelime, [3 İpucu Kelime])
KELIME_LISTESI = [
    ("PYTHON", ["Yazılım", "Yılan", "Programlama"]),
    ("KEDI", ["Miyav", "Patili", "Evcil"]),
    ("ANKARA", ["Başkent", "Anıtkabir", "Memleket"]),
    ("KAHVE", ["Kafein", "Filtre", "Çekirdek"]),
    ("BILGISAYAR", ["Donanım", "Teknoloji", "Ekran"]),
]


class KelimeBulmacaOyunu:

  def __init__(self, root):
    self.root = root
    self.root.title("Kelime Bulmaca Oyunu")
    self.root.geometry("450x450")
    self.root.config(bg="#f4f6f9")
    self.root.resizable(False, False)

    self.puan = 0
    self.aktif_kelime = ""
    self.ipuclari = []
    self.hak = 4

    # Giriş arayüzünü başlat
    self.giris_arayuzu_olustur()

  def arayuz_temizle(self):
    """Mevcut ekrandaki tüm widget'ları temizler."""
    for widget in self.root.winfo_children():
      widget.destroy()

  # ================= 1. GİRİŞ ARAYÜZÜ =================
  def giris_arayuzu_olustur(self):
    self.arayuz_temizle()

    baslik = tk.Label(
        self.root,
        text="KELİME BULMACA",
        font=("Arial", 22, "bold"),
        bg="#f4f6f9",
        fg="#2c3e50",
    )
    baslik.pack(pady=40)

    aciklama = tk.Label(
        self.root,
        text=(
            "Verilen 3 ipucu kelimeye dikkat et!\nGizli kelimeyi bulmak için"
            " 4 hakkın var.\nHadi başlayalım!"
        ),
        font=("Arial", 11),
        bg="#f4f6f9",
        fg="#555",
        justify="center",
    )
    aciklama.pack(pady=20)

    basla_btn = tk.Button(
        self.root,
        text="OYUNA BAŞLA",
        font=("Arial", 12, "bold"),
        bg="#27ae60",
        fg="white",
        width=18,
        height=2,
        command=self.oyun_arayuzu_olustur,
        relief="flat",
        cursor="hand2",
    )
    basla_btn.pack(pady=30)

  # ================= 2. OYUN ARAYÜZÜ =================
  def oyun_arayuzu_olustur(self):
    # Yeni oyun için verileri seç
    secilen = random.choice(KELIME_LISTESI)
    self.aktif_kelime = secilen[0]
    self.ipuclari = secilen[1]
    self.hak = 4

    self.arayuz_temizle()

    # Üst Bilgi (Hak durumu)
    self.hak_label = tk.Label(
        self.root,
        text=f"Kalan Hak: {self.hak}",
        font=("Arial", 11, "bold"),
        bg="#f4f6f9",
        fg="#e74c3c",
    )
    self.hak_label.pack(anchor="ne", padx=20, pady=10)

    oyun_baslik = tk.Label(
        self.root,
        text="İpuçlarını İncele, Kelimeyi Tahmin Et!",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#34495e",
    )
    oyun_baslik.pack(pady=10)

    # 3 İpucu Kelime Çerçevesi
    ipuclari_cerceve = tk.LabelFrame(
        self.root,
        text=" İpucu Kelimeler ",
        font=("Arial", 10, "bold"),
        bg="#f4f6f9",
        fg="#2980b9",
        padx=20,
        pady=10,
    )
    ipuclari_cerceve.pack(pady=15, fill="x", padx=40)

    for i, ipucu in enumerate(self.ipuclari):
      lbl = tk.Label(
          ipuclari_cerceve,
          text=f"{i+1}. İpucu: {ipucu}",
          font=("Arial", 11),
          bg="#f4f6f9",
          fg="#333",
      )
      lbl.pack(anchor="w", pady=4)

    # Tahmin Giriş Alanı
    self.tahmin_giris = tk.Entry(
        self.root, font=("Arial", 14), justify="center", width=15
    )
    self.tahmin_giris.pack(pady=15)
    self.tahmin_giris.focus()
    # Enter tuşuna basınca tahmini kontrol etsin
    self.tahmin_giris.bind("<Return>", lambda event: self.tahmini_kontrol_et())

    tahmin_btn = tk.Button(
        self.root,
        text="Tahmin Et",
        font=("Arial", 11, "bold"),
        bg="#2980b9",
        fg="white",
        width=15,
        command=self.tahmini_kontrol_et,
        relief="flat",
        cursor="hand2",
    )
    tahmin_btn.pack(pady=5)

  def tahmini_kontrol_et(self):
    tahmin = self.tahmin_giris.get().strip().upper()

    if not tahmin:
      messagebox.showwarning("Uyarı", "Lütfen boş bir tahmin girmeyin!")
      return

    if tahmin == self.aktif_kelime:
      self.puan += 10
      self.cikis_arayuzu_olustur(
          kazandi_mi=True, mesaj="Tebrikler, doğru tahmin!"
      )
    else:
      self.hak -= 1
      self.hak_label.config(text=f"Kalan Hak: {self.hak}")
      self.tahmin_giris.delete(0, tk.END)

      if self.hak <= 0:
        self.cikis_arayuzu_olustur(
            kazandi_mi=False,
            mesaj=f"Hakkınız bitti!\nDoğru Kelime: {self.aktif_kelime}",
        )
      else:
        messagebox.showerror(
            "Yanlış", f"Yanlış tahmin! Kalan hakkın: {self.hak}"
        )

  # ================= 3. ÇIKIŞ / SONUÇ ARAYÜZÜ =================
  def cikis_arayuzu_olustur(self, kazandi_mi, mesaj):
    self.arayuz_temizle()

    durum_renk = "#27ae60" if kazandi_mi else "#c0392b"
    durum_baslik = "OYUN BİTTİ" if not kazandi_mi else "TEBRİKLER!"

    baslik = tk.Label(
        self.root,
        text=durum_baslik,
        font=("Arial", 20, "bold"),
        bg="#f4f6f9",
        fg=durum_renk,
    )
    baslik.pack(pady=30)

    bilgi_lbl = tk.Label(
        self.root,
        text=mesaj,
        font=("Arial", 12),
        bg="#f4f6f9",
        fg="#333",
        justify="center",
    )
    bilgi_lbl.pack(pady=10)

    puan_lbl = tk.Label(
        self.root,
        text=f"Toplam Puanın: {self.puan}",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#2980b9",
    )
    puan_lbl.pack(pady=20)

    # Butonlar çerçevesi
    btn_cerceve = tk.Frame(self.root, bg="#f4f6f9")
    btn_cerceve.pack(pady=20)

    tekrar_btn = tk.Button(
        btn_cerceve,
        text="Tekrar Oyna",
        font=("Arial", 11, "bold"),
        bg="#27ae60",
        fg="white",
        width=12,
        height=2,
        command=self.oyun_arayuzu_olustur,
        relief="flat",
        cursor="hand2",
    )
    tekrar_btn.grid(row=0, column=0, padx=10)

    cikis_btn = tk.Button(
        btn_cerceve,
        text="Çıkış Yap",
        font=("Arial", 11, "bold"),
        bg="#7f8c8d",
        fg="white",
        width=12,
        height=2,
        command=self.root.quit,
        relief="flat",
        cursor="hand2",
    )
    cikis_btn.grid(row=0, column=1, padx=10)


# Uygulamayı Çalıştır
if __name__ == "__main__":
  root = tk.Tk()
  oyun = KelimeBulmacaOyunu(root)
  root.mainloop()
