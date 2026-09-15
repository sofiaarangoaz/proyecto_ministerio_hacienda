Esta carpeta contiene la última versión del tablero (Dash) junto con todo lo necesario para replicar su despliegue en una instancia de AWS EC2, tal como se hizo para este proyecto.

## Requisitos previos

- Una instancia de AWS EC2 con Ubuntu Server 24.04 LTS (tipo `t3.micro` es suficiente).
- Un Security Group con los puertos abiertos:
  - `22` (SSH) — origen: tu IP.
  - `80` (HTTP) — origen: `0.0.0.0/0`.
- La llave `.pem` generada al crear la instancia.

## Pasos para desplegar

### 1. Subir esta carpeta al servidor

Desde tu computador (reemplaza la llave y la IP pública por las tuyas):

```bash
scp -i tu-llave.pem -r despliegue ubuntu@TU_IP_PUBLICA:~/mi_tablero
```

### 2. Conectarte por SSH

```bash
ssh -i tu-llave.pem ubuntu@TU_IP_PUBLICA
```

### 3. Ejecutar el script de despliegue

Ya dentro del servidor:

```bash
cd ~/mi_tablero
chmod +x deploy.sh
./deploy.sh
```

Este script automáticamente:
1. Actualiza los paquetes del sistema.
2. Instala Python, `venv` y Nginx.
3. Crea un entorno virtual e instala las librerías de `requirements.txt`.
4. Configura Gunicorn como servicio systemd (`dashapp`), para que el tablero se mantenga corriendo de forma permanente y se reinicie solo ante fallos o reinicios del servidor.
5. Configura Nginx como proxy inverso, para que el tablero sea accesible por el puerto 80 (sin necesidad de especificar el puerto 8050 en la URL).
6. Muestra al final la IP pública para acceder al tablero.

### 4. Verificar el despliegue

Al terminar el script, abre en el navegador:

```
http://TU_IP_PUBLICA
```