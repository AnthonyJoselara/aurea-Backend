import express from 'express';
import { spawn, ChildProcess } from 'child_process';
import http from 'http';

const app = express();
const PORT = 3000;
const PYTHON_PORT = 8000;

let pythonProcess: ChildProcess | null = null;

function startPythonBackend() {
  console.log('[FastAPI] Iniciando proceso uvicorn en puerto', PYTHON_PORT);
  pythonProcess = spawn('python3', [
    '-m', 'uvicorn',
    'main:app',
    '--host', '127.0.0.1',
    '--port', String(PYTHON_PORT),
    '--log-level', 'info'
  ], {
    stdio: 'inherit',
    env: { ...process.env, PORT: String(PYTHON_PORT) }
  });

  pythonProcess.on('error', (err) => {
    console.error('[FastAPI] Error al iniciar backend Python:', err);
  });

  pythonProcess.on('exit', (code, signal) => {
    console.log(`[FastAPI] Proceso terminó con código ${code} y señal ${signal}`);
  });
}

// Iniciar Python
startPythonBackend();

// Proxy inverso transparente hacia FastAPI
app.use((req, res) => {
  const options: http.RequestOptions = {
    hostname: '127.0.0.1',
    port: PYTHON_PORT,
    path: req.url,
    method: req.method,
    headers: {
      ...req.headers,
      host: `127.0.0.1:${PYTHON_PORT}`
    }
  };

  const proxyReq = http.request(options, (proxyRes) => {
    res.writeHead(proxyRes.statusCode || 500, proxyRes.headers);
    proxyRes.pipe(res, { end: true });
  });

  proxyReq.on('error', (err) => {
    console.error('[Proxy Error]:', err.message);
    if (!res.headersSent) {
      res.status(502).json({
        error: {
          module: 'gateway',
          message: 'El backend de FastAPI está iniciando o no responde.',
          statusCode: 502
        }
      });
    }
  });

  req.pipe(proxyReq, { end: true });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  if (pythonProcess) pythonProcess.kill();
  process.exit(0);
});
process.on('SIGINT', () => {
  if (pythonProcess) pythonProcess.kill();
  process.exit(0);
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`[Áurea Gateway] Gateway escuchando en http://0.0.0.0:${PORT} -> redirigiendo a FastAPI`);
});
