# Profil değerlendirmesi

Kullanıcının verdiği profil görüntüsü veya metninden isim, kullanıcı adı, biyografi, bağlantı, öne çıkanlar, sabit gönderiler ve ilk dokuz kapağı incele. Görünmeyen öğeye sıfır verme; bilinmiyor olarak işaretle.

Türkçe için `rubric.tr.json`, İngilizce için `rubric.json` oku. 12 ölçütü ayrı puanla. Eksik veri varsa gözlenen puanı değerlendirilebilen toplam üzerinden göster; tam profil incelenmiş gibi 100 üzerinden sonuç uydurma.

Kaybedilen puana göre düzelt: üç isim alanı seçeneği, hedef kitleyi ve teklifi anlatan biyografi, kanıt/teklif/tanışma görevleri farklı üç sabit gönderi, alıcının sorularına göre öne çıkanlar, vaade uyan bağlantı ve okunaklı kapaklar. Karakter sınırını güncel uygulamada doğrulamadan kesinleştirme.

Kurumsal hesapta logo kullanımını kişisel hesap ölçütüyle cezalandırma. Mevcut gönderi ve kanıt gerektiren puanı yalnızca metin yeniden yazıldı diye yükseltme.

Çıktı: kanıta bağlı puan tablosu, eksik veriler, öncelikli düzeltmeler ve kopyalanabilir metinler. Önerilen profille mevcut profilin puanını ayrı göster; Instagram profilinde değişiklik yapma.
