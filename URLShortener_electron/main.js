const { app, BrowserWindow, ipcMain, clipboard } = require('electron');
const path = require('path');
const axios = require('axios');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: true,
    },
  });

  mainWindow.loadFile('index.html');
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('shorten-url', async (event, url) => {
  console.log('URL recebida para encurtar:', url);
  try {
    const response = await axios.post('https://api.tinyurl.com/create', {
      url: url,
      domain: 'tiny.one',
      alias: '',
    }, {
      headers: {
        Authorization: 'Bearer ruKTbLMkz92YkCftr6l3Bf4Y0MYQFNXb8pQHSREXMMvRGr0lRiQNBWmMvhgN',
        'Content-Type': 'application/json'
      }
    });
    console.log('Resposta da API:', response.data);
    return response.data.data.tiny_url;
  } catch (error) {
    console.error('Erro ao encurtar URL:', error);
    return `Error: ${error.message}`;
  }
});

ipcMain.handle('copy-to-clipboard', (event, text) => {
  clipboard.writeText(text);
});
