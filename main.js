const { app, BrowserWindow } = require("electron");
const path = require("path");
const { execFile } = require("child_process");

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    resizable: true,
    fullscreen: false,
    frame: true,
    webPreferences: {
      nodeIntegration: false,
      devTools: true,
    },
  });

  // Hata ayıklama için DevTools'u aç
  mainWindow.webContents.openDevTools();

  mainWindow.loadFile(path.join(__dirname, "frontend", "build", "index.html"));

  mainWindow.maximize();

  mainWindow.webContents.on("did-finish-load", () => {
    mainWindow.webContents.focus();
  });

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

function startFlask() {
  console.log("Starting Flask with DB_MODE=desktop");
  const env = Object.assign({}, process.env, {
    DB_MODE: "desktop",
    FLASK_ENV: "production",
    PYTHONUNBUFFERED: "1",
  });

  // Development ortamında Python kullanılır
  // Production ortamında paketlenmiş exe dosyası kullanılır
  let execPath;
  let args = [];

  const fs = require("fs");

  if (process.env.NODE_ENV === "development") {
    execPath = "python";
    args = [path.join(__dirname, "backend", "main.py")];
    console.log("Development mode: Using Python interpreter");
  } else {
    // Tüm olası yolları kontrol et
    const possiblePaths = [
      path.join(__dirname, "backend", "main.exe"),
      path.join(process.resourcesPath, "backend", "main.exe"),
      path.join(process.resourcesPath, "app.asar.unpacked", "backend", "main.exe"),
      path.join(app.getAppPath(), "backend", "main.exe"),
      path.join(app.getPath("exe"), "..\\resources", "backend", "main.exe"),
    ];

    console.log("Checking possible backend exe paths:");
    let foundPath = null;

    for (const p of possiblePaths) {
      console.log(`Checking path: ${p}`);
      if (fs.existsSync(p)) {
        console.log(`Found backend exe at: ${p}`);
        foundPath = p;
        break;
      }
    }

    if (foundPath) {
      execPath = foundPath;
    } else {
      console.error("Could not find backend exe file in any of the expected locations!");
      console.log("Listing files in resources directory:");
      try {
        const resourcesDir = path.join(process.resourcesPath);
        if (fs.existsSync(resourcesDir)) {
          const files = fs.readdirSync(resourcesDir);
          console.log(`Files in ${resourcesDir}:`, files);

          const backendDir = path.join(resourcesDir, "backend");
          if (fs.existsSync(backendDir)) {
            const backendFiles = fs.readdirSync(backendDir);
            console.log(`Files in ${backendDir}:`, backendFiles);
          } else {
            console.log(`Backend directory not found: ${backendDir}`);
          }
        } else {
          console.log(`Resources directory not found: ${resourcesDir}`);
        }
      } catch (err) {
        console.error("Error listing files:", err);
      }

      // Varsayılan olarak ilk yolu kullan
      execPath = possiblePaths[0];
    }
  }

  console.log("Starting Flask process with:", { execPath, args });

  try {
    flaskProcess = execFile(execPath, args, { env });
    console.log("Flask process started with PID:", flaskProcess.pid);
  } catch (error) {
    console.error("Error starting Flask process:", error);
  }

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask stdout: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask stderr: ${data}`);
  });

  flaskProcess.on("error", (err) => {
    console.error("Failed to start Flask:", err);
  });

  // Return a promise that resolves when the server is ready
  return new Promise((resolve) => {
    // Wait for Flask to start (give it a few seconds)
    setTimeout(() => {
      console.log("Flask server should be ready now");
      resolve();
    }, 3000);
  });
}

app.whenReady().then(async () => {
  await startFlask();
  createWindow();
});

app.on("window-all-closed", () => {
  // Flask sürecini düzgün şekilde sonlandır
  if (flaskProcess) {
    try {
      flaskProcess.kill();
      console.log("Flask process terminated");
    } catch (error) {
      console.error("Error terminating Flask process:", error);
    }
  }
  if (process.platform !== "darwin") app.quit();
});

// Uygulama kapanmadan önce Flask sürecini sonlandır
app.on("before-quit", () => {
  if (flaskProcess) {
    try {
      flaskProcess.kill();
      console.log("Flask process terminated before quit");
    } catch (error) {
      console.error("Error terminating Flask process before quit:", error);
    }
  }
});

app.on("activate", () => {
  if (mainWindow === null) createWindow();
});
