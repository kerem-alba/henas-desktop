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

  // Change this section to run Python directly instead of exe
  const pythonPath = "python"; // or 'python3' depending on your system
  const scriptPath = path.join(__dirname, "backend", "main.py");

  console.log("Starting Flask from:", scriptPath);
  flaskProcess = execFile(pythonPath, [scriptPath], { env });

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask stdout: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.log(`Flask stderr: ${data}`);
  });

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
