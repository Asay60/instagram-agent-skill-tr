# Metin düzenleme

Amaç anlamı ve marka sesini koruyup gereksiz kalıpları sadeleştirmektir. Noktalama, görünmez karakterler veya puanlar bir metnin AI tarafından yazıldığını kanıtlamaz. Tespit aracını atlatma veya görünmez filigran kaldırma garantisi verme.

Türkçe için `slop.tr.json`, İngilizce için `slop.json` kullanılır. Marka diline ait yerinde terimleri sırf listede diye silme; gerekirse özel sözlük kullan.

1. `python3 humanize.py draft.txt --lang tr -o clean.txt --report` çalıştır.
2. Değişiklikleri oku. URL, e-posta, özel isim, rakam, Türkçe ekler ve emoji anlamı korunmuş mu kontrol et. Araç emoji birleşimlerini korumaya çalışır; çıktıyı yine incele.
3. Yapısal uyarıları anlamı koruyarak elle düzelt. Her üçlü liste veya düzenli cümle yapısı kusur değildir.
4. `python3 detect.py draft.txt clean.txt --lang tr --json` ile editoryal ölçütleri karşılaştır. Türkçede İngilizce kısaltma/zamir beklentisi kullanılmaz. İki turdan fazla yalnızca puanı yükseltmek için metni bozma.

Çıktı: düzenlenmiş metin, önemli değişiklikler, kalan uyarılar. İstenirse editoryal puanı ve sınırlılığını açıkla. JSON alan adları ve bazı teknik tanı mesajları İngilizce kalır. Tek başına puan teslim etme.
