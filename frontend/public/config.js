// API yapılandırması
window.API_CONFIG = {
  // Localhost yerine 0.0.0.0 kullanıyoruz, böylece tüm ağ arayüzlerinden bağlantı kabul edilir
  API_BASE_URL: "http://localhost:5000",
};

// API bağlantısını test et
function testApiConnection() {
  console.log("Testing API connection to: " + window.API_CONFIG.API_BASE_URL);
  fetch(window.API_CONFIG.API_BASE_URL + "/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username: "test", password: "test" }),
  })
    .then((response) => {
      console.log("API connection test response status:", response.status);
      if (response.ok) {
        console.log("API connection successful!");
      } else {
        console.error("API connection failed with status:", response.status);
      }
    })
    .catch((error) => {
      console.error("API connection test error:", error);
      // Alternatif port dene
      console.log("Trying alternative port...");
      window.API_CONFIG.API_BASE_URL = "http://localhost:5000";
      console.log("Updated API_BASE_URL to:", window.API_CONFIG.API_BASE_URL);
    });
}

// Sayfa yüklendiğinde API bağlantısını test et
window.addEventListener("load", function () {
  setTimeout(testApiConnection, 2000); // 2 saniye bekle, Flask'in başlaması için zaman tanı
});
