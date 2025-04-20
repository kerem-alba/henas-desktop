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
    },
  });

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
    FLASK_ENV: "development",
    PYTHONUNBUFFERED: "1",
  });

  const pythonPath = "python";
  const scriptPath = path.join(__dirname, "backend", "main.py");

  flaskProcess = execFile(pythonPath, [scriptPath], { env });

  flaskProcess.on("error", (err) => {
    console.error("Failed to start Flask:", err);
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
