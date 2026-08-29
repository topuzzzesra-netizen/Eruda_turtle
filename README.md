eruda_turtle quickedit konsolunu entegre eden bir açık kaynak kütüphanedir
## Kurulum

### python 3 ile
```python
import os
import subprocess
import sys
import urllib.request
import zipfile

url = "https://github.com/topuzzzesra-netizen/Eruda_turtle/archive/refs/heads/main.zip"
zip_path = "eruda_turtle.zip"

print("Kütüphane GitHub'dan indiriliyor...")
urllib.request.urlretrieve(url, zip_path)

print("Arşiv dosyaları açılıyor...")
extract_dir = "eruda_extracted"
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, "r") as z:
  z.extractall(extract_dir)

subfolders = os.listdir(extract_dir)
if subfolders:
  target_folder = os.path.join(extract_dir, subfolders[0])
  print("Hedef klasör bulundu: " + target_folder)

  print("Pip ile sisteme yükleniyor...")
  subprocess.check_call(
      [sys.executable, "-m", "pip", "install", target_folder]
  )
  print("İşlem tamamdır! Artık kütüphaneni projelerinde import edebilirsin.")
else:
  print("Hata: Arşiv içeriği okunamadı.")

if os.path.exists(zip_path):
  os.remove(zip_path)
