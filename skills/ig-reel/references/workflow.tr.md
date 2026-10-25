# Reels senaryosu

1. Konuyu, hedef izleyiciyi, tek somut sorunu, doğrulanmış örneği ve istenen süreyi belirle. Tek videoya tek fikir koy.
2. Türkçe için `hooks.tr.json`, İngilizce için `hooks.json` oku. Varsa `swipe.md` içindeki kullanıcı verisini genel önerilerin önüne koy.
3. Birbirinden farklı üç formülle üç açılış yaz. Her biri için konuşulan cümleyi ve en fazla altı sözcüklük ekran metnini ayrı ver.
4. Üç konuşma açılışını `hooks.txt` dosyasına yaz. `python3 hookscore.py hooks.txt --lang tr --json` çalıştır. Açık zayıflıkları düzelt; en yüksek puanı izlenme garantisi gibi sunma.
5. Seçilen açılışla senaryoyu satır başına bir sahne olacak biçimde yaz: açılış, sorunun önemi, açıklama, karşılık ve tek eylem çağrısı. Son satır uygunsa ilk satırdaki fikre bağlansın.
6. `python3 beats.py script.txt --lang tr --target 30 --wpm 165 --json` çalıştır. Hedef süreyi talebe göre değiştir. Kullanıcının ölçülmüş konuşma hızını tercih et; Türkçede sözcük sayısından hesaplanan süreyi kayıtla doğrulamak gerektiğini belirt. Üç saniyeyi aşan açılışı ve dört saniyeyi aşan durağan sahneleri gözden geçir.
7. Metni `ig-human` ile düzenle. İki düzeltme turundan sonra puanı zorlamak yerine kalan sorunu açıkla.

Çıktı: üç açılış ve araç puanları, seçimin nedeni, kopyalanabilir konuşma metni, zamanlı ekran metinleri, sahne/görüntü önerileri ve tek CTA. 1080×1920 tasarımda metni arayüz alanlarından uzak tut; önizlemede doğrula. Bu iş akışı video render etmez.

Kullanıcı içerik kaydı isterse tarih, formül ve açılışı `log.md` dosyasına ekle. Yayınlanmamış taslağı yayınlanmış gibi kaydetme.
