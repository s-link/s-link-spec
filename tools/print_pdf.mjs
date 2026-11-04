import { spawn } from 'node:child_process';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const [chrome, input, output] = process.argv.slice(2);
const profile = await mkdtemp(join(tmpdir(), 'slink-chrome-'));
const browser = spawn(chrome, [
  '--headless', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
  '--remote-debugging-port=0', '--remote-allow-origins=*',
  `--user-data-dir=${profile}`, 'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe'] });
let socket;
let stderr = '';
const timeout = setTimeout(() => browser.kill('SIGKILL'), 60000);
try {
  const address = await new Promise((resolve, reject) => {
    browser.stderr.on('data', chunk => {
      stderr += chunk;
      const match = stderr.match(/DevTools listening on (ws:\/\/\S+)/);
      if (match) resolve(match[1]);
    });
    browser.once('error', reject);
    browser.once('exit', code => reject(new Error(`Chromium exited: ${code}\n${stderr.slice(-1500)}`)));
  });
  socket = new WebSocket(address);
  await new Promise((resolve, reject) => {
    socket.addEventListener('open', resolve, { once: true });
    socket.addEventListener('error', reject, { once: true });
  });
  let id = 0;
  const pending = new Map();
  socket.addEventListener('message', event => {
    const message = JSON.parse(event.data);
    const request = pending.get(message.id);
    if (!request) return;
    pending.delete(message.id);
    if (message.error) request.reject(new Error(JSON.stringify(message.error)));
    else request.resolve(message.result);
  });
  const call = (method, params = {}, sessionId) => new Promise((resolve, reject) => {
    const requestId = ++id;
    pending.set(requestId, { resolve, reject });
    socket.send(JSON.stringify({ id: requestId, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  const { targetId } = await call('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await call('Target.attachToTarget', { targetId, flatten: true });
  await call('Page.enable', {}, sessionId);
  await call('Page.navigate', { url: pathToFileURL(input).href }, sessionId);
  for (let i = 0; i < 100; i++) {
    const { result } = await call('Runtime.evaluate', { expression: 'document.readyState' }, sessionId);
    if (result.value === 'complete') break;
    await new Promise(resolve => setTimeout(resolve, 50));
    if (i === 99) throw new Error('HTML load timed out');
  }
  const fonts = await call('Runtime.evaluate', {
    expression: "document.fonts.ready.then(() => document.fonts.check('10px SlinkJP'))",
    awaitPromise: true, returnByValue: true,
  }, sessionId);
  if (!fonts.result.value) throw new Error('IBM Plex Sans JP did not load');
  const { data } = await call('Page.printToPDF', {
    printBackground: true, preferCSSPageSize: true,
    generateDocumentOutline: true, generateTaggedPDF: true,
    displayHeaderFooter: false,
  }, sessionId);
  await writeFile(output, Buffer.from(data, 'base64'));
} finally {
  clearTimeout(timeout);
  socket?.close();
  browser.kill();
  await new Promise(resolve => browser.exitCode !== null ? resolve() : browser.once('exit', resolve));
  await rm(profile, { recursive: true, force: true, maxRetries: 8, retryDelay: 100 });
}
