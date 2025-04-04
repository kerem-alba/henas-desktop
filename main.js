const { app, BrowserWindow } = require("electron");
const path = require("path");
const { execFile } = require("child_process");

let mainWindow;
let flaskProcess;

function createWindow() {
  // React frontend build klasöründen index.html'i yükleyeceğiz
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, "frontend", "build", "index.html"));

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

function startFlask() {
  const exePath = path.join(__dirname, "backend", "app.exe");
  flaskProcess = execFile(exePath);

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask Error: ${data}`);
  });

  flaskProcess.on("close", (code) => {
    console.log(`Flask exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  startFlask();
  createWindow();
});

app.on("window-all-closed", () => {
  if (flaskProcess) flaskProcess.kill();
  if (process.platform !== "darwin") app.quit();
});

app.on("activate", () => {
  if (mainWindow === null) createWindow();
});
