# Örnek içerik araştırması

Amaç benzer hesapların kendi normaline göre iyi çalışan içerik yapısını anlamaktır. Ham izlenmeyi başarı garantisi veya kopyalanacak senaryo gibi sunma.

1. Kullanıcının hedef nişini ve kitleyi belirle. Kullanıcının verdiği veri, herkese açık erişilebilir sayfa veya ayrıca yetkilendirilmiş okuma aracı kullan. Bu paket Instagram veri toplayıcısı içermez; parola veya toplu tarama kurma.
2. Makul başlangıç örneği olarak on hesaptan yakın dönemdeki yaklaşık 12 Reels'i incele. Görünmeyen sayı ve medyanı uydurma. Her satıra kaynak URL ve gözlem tarihi ekle; aynı tarih aralığından kıyasla.
3. TSV başlığı: `account	followers	median	views	hook	url	observed_at`. Sayıları tam tamsayı yaz (4500); `4.5K`, `4,5 bin` gibi kısaltmaları doğrudan betiğe geçirme. Medyan yoksa boş bırak; takipçi tabanı aynı ölçüt değildir.
4. `python3 swipe.py captured.tsv --lang tr --json` çalıştır. Türkçe formüller `hooks.tr.json` içinden seçilir. `baseline_kind` alanı farklı olan satırları ayrı değerlendir; medyan katı ile takipçi oranını aynı sıralamada yorumlama.
5. Üst/alt grubun yapı farklarını, formül sayımlarını ve sınıflandırılamayanları bildir. Örnek sayısını ve belirsizliği açıkla; küçük örnekten kesin algoritma sonucu çıkarma.
6. Başarılı yapıların kullanıcının gerçek deneyimine uygun üç yeni versiyonunu öner; başka yaratıcının metnini veya sesini kopyalama. Senaryolar için `ig-reel` kullan.

Dosya istendiğinde `--out` ile `IG_AGENT_HOME/swipe.md` yolunu kullan. JSON alanları teknik uyumluluk için İngilizcedir. Araştırmayı tamamladığını söylemek için gerçek veri ve kaynaklar gerekir; yalnızca şablon doldurulduysa bunu belirt.
