# Gönderi açıklaması

Önce görevi seç: A) Reels zaten dikkat çekiyorsa açıklama bağlamı ve çağrıyı tamamlasın. B) Fotoğraf veya carousel metni taşıyorsa ilk satır açılış olsun.

1. İlk satırı kısa ve somut yaz. Selamlaşma veya hashtag ile başlama. Ardından kısa paragraflar, tek eylem çağrısı ve gerekiyorsa ilgili hashtagler ekle.
2. Kullanıcının bulunmak istediği iki-üç arama ifadesini doğal cümlelere yerleştir. Hashtagleri erişim garantisi olarak sunma.
3. `ig-human` ile düzenle; ardından `python3 caption.py caption.txt --lang tr --keywords "satış otomasyonu,teklif hazırlama" --json` çalıştır.
4. İlk 125 karakterlik görünümü yaklaşık önizleme olarak ele al. Ekran ve arayüze göre değişir; `--truncate` ile değiştirilebilir. Varsayılan beş hashtag editoryal öneridir; `--hashtag-limit` ile değiştirilebilir, güncel platform limiti diye sunma.
5. FAIL sonuçlarını düzelt; WARN sonuçlarını anlamı koruyarak değerlendir. Teknik denetleyici her Türkçe çağrı biçimini tanıyamaz; elle de kontrol et.

Çıktı: kopyalanabilir açıklama, yaklaşık ilk görünüm, tek CTA, arama ifadeleri, denetim özeti. Fotoğraf/carousel için alt metin ekle. Açıklamadaki bağlantının tıklanabildiğini varsayma; uygun hedefi profil veya yetkili mesaj akışı olarak öner.
