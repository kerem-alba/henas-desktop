# **HENAS - DOKTOR NÖBET LİSTESİ HAZIRLAMA UYGULAMASI**  

## 📝 PROJE HAKKINDA  
**Henas**, hastanelerde nöbet usulü çalışan doktorlar için **ideal nöbet listesi oluşturmayı** hedefleyen bir uygulamadır.  
Kullanıcı dostu bir arayüzle, doktorların **nöbet planlama sürecini kolaylaştıran** ve **adil bir dağılım sağlayan** bir sistem geliştirilmiştir.  

---

## 🔗 CANLI SÜRÜM  
Uygulamanın canlı demosuna aşağıdaki bağlantıdan ulaşabilirsin:  

👉 **[Henas Live](https://henas.vercel.app/)**  

🔑 **Test Kullanıcı Bilgileri:**  
- **Kullanıcı Adı:** test  
- **Şifre:** test1234  

Bu bilgileri kullanarak giriş yapabilir ve uygulamayı inceleyebilirsin.

---

## 🔍 TEMEL ÖZELLİKLER  

- ✔️ **Kullanıcı Girişi:** OAuth tabanlı kimlik doğrulama  
- ✔️ **Kıdem Bazlı Nöbet Dağılımı:** Daha kıdemli doktorlara uygun dağılım  
- ✔️ **Esnek Nöbet Planlaması:** Kullanıcı tercihlerine göre esneklik  
- ✔️ **Optimizasyon Algoritması:** Genetik Algoritma & Hill Climbing  
- ✔️ **Manuel Düzenleme:** Kullanıcıların nöbet planında değişiklik yapabilmesi  
- ✔️ **JSON Formatında Veri Saklama:** Esnek ve hızlı  

---

---

## ⚙️ OPTİMİZASYON YÖNTEMLERİ  

Uygulamada **Hill Climbing** ve **Genetik Algoritma** optimizasyon yöntemleri kullanılmaktadır.  
**Demo sürümünde yalnızca Hill Climbing aktif** olup, **Genetik Algoritma üzerine çalışmalar devam etmektedir.**  

---

## 🛠 SOFT CONSTRAINTLER (ESNEK KISITLAR)  

Soft constraint'ler ihlal edildiğinde belirli bir ceza puanı uygulanır:  

- **Gündüz ve gece nöbetlerinin dengesiz dağılımı**  
- **Arka arkaya iki gece nöbeti atanması**  
- **Hafta sonlarının mümkün olduğunca boş bırakılması**  
- **Doktorun kıdemine uygun olmayan nöbet atanması**  
- **Opsiyonel izinli doktora nöbet atanması**  

---

## 🚨 HARD CONSTRAINTLER (ZORUNLU KISITLAR)  

Hard constraint'lerin ihlali kabul edilemez:  

- **Aynı nöbet içinde aynı doktor birden fazla kez atanamaz.**
- **Ardışık günlerde aynı doktora nöbet atanamaz.**  
- **Bir doktora üst üste 2'den fazla gece nöbeti atanamaz.**
- **Mecburi izinli doktora nöbet atanması**  


---


## 🛠 TEKNOLOJİLER  

- **Backend:** Python (Flask)  
- **Veritabanı:** PostgreSQL  
- **Frontend:** React Native  
- **Kimlik Doğrulama:** OAuth tabanlı sistem  
- **Optimizasyon Algoritması:** Genetik Algoritma & Hill Climbing  

---

## 📑 KURULUM VE ÇALIŞTIRMA  

### 🔹 **GEREKSİNİMLER**  
- Python 3.x  
- PostgreSQL veritabanı  
- Node.js & npm/yarn  

### 🔹 **BACKEND KURULUMU**  
```sh
# Gerekli paketleri yükle
pip install -r requirements.txt

# PostgreSQL bağlantı bilgilerini .env dosyasına ekle

```

# Flask uygulamasını çalıştır
flask run

### 🔹 **FRONTEND KURULUMU**  
```sh
# Gerekli modülleri yükle
npm install

# Uygulamayı başlat
npm start


