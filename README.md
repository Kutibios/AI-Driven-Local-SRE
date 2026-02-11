
#  AI-Powered Local SRE & Log Analysis System

Bu proje, sistem loglarını anlık olarak izleyen, hataları filtreleyen ve yerel bir yapay zeka (**TinyLlama**) kullanarak çözüm önerileri sunan bir DevOps asistanıdır. Proje, hassas sistem verilerini dışarı çıkarmadan, tamamen yerel kaynaklarla analiz yapar.

---

##  Temel Özellikler

* **Monitoring:** `logs/` klasöründeki tüm `.log` dosyalarını (Nginx, Database, App vb.) eşzamanlı ve anlık olarak izler.
* **Filtering:** Sadece `ERROR` ve `CRITICAL` seviyesindeki loglara odaklanarak sistem gürültüsünü (INFO, DEBUG vb.) eler.
* **Spam** Aynı hata mesajı 60 saniye içinde tekrar gelirse AI analizini atlar, işlemci gücünü ve kaynakları korur.
* **Safety Local AI:** Analizler için **Ollama** üzerinden **TinyLlama** kullanılır. Veriler internete çıkmaz, tamamen yerel makinede kalır.
* **Report** AI tarafından üretilen çözümler hem terminalde görselleştirilir hem de `reports/solutions.txt` dosyasına arşivlenir.

---

## Kurulum ve Çalıştırma

Sistemi en hızlı şekilde test etmek için aşağıdaki adımları sırasıyla takip edin:

### 1. Ortamı Hazırlama
Proje klasöründe bir terminal açın ve izole geliştirme ortamını (**Devbox**) aktif edin:
```bash
devbox shell
```
### 2\. Bağımlılıkları ve Modeli Hazırlama

Gerekli Python kütüphanelerini kurmak ve AI modelini hazırlamak için şu komutu çalıştırın:
```bash
task setup
```
(Not: Bu işlem sırasında TinyLlama modeli Ollama üzerinden otomatik olarak indirilecektir.)

### 3\. Sistemi Test Etme (Demo)

Sistemin çalışma mantığını gözlemlemek için **iki farklı terminal sekmesi** kullanılması önerilir:
```bash
*   task run
    
*   task error
```

 Analiz Süreci Nasıl İşler?
-----------------------------

1.  **Detection (Tespit):** watchdog kütüphanesi dosya sistemindeki her değişikliği anlık yakalar.
    
2.  **Context Aware (Bağlam):** Hata yakalandığında, hatanın hangi dosyadan geldiği bilgisi AI'ya iletilir.
    
3.  **Inference (Analiz):** Yapay zeka, hatanın kök nedenini belirler ve teknik bir çözüm yolu haritası çıkarır.
    
4.  **Archiving (Arşivleme):** Süreç terminalde Rich panelleriyle gösterilir ve kalıcı rapor dosyasına yazılır.
    

 Proje Yapısı
---------------

*   **main.py:** Akıllı izleme mantığı, spam filtresi ve AI entegrasyonunu içeren ana uygulama.
    
*   **scripts/generate_log.sh:** Dinamik ve rastgele hata senaryoları üreten test scripti.
    
*   **reports/solutions.txt:** Yapay zeka tarafından oluşturulan geçmiş hata-çözüm kütüphanesi.
    
*   **Taskfile.yml:** Tüm operasyonel süreçlerin (setup, run, clean, error) otomasyonu.
    
*   **devbox.json:** İzole ve taşınabilir geliştirme ortamı tanımı.
