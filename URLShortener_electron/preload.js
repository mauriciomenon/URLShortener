const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  shortenUrl: (url) => ipcRenderer.invoke('shorten-url', url),
  copyToClipboard: (text) => ipcRenderer.invoke('copy-to-clipboard', text),
});
