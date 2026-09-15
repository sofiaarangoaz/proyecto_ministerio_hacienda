set -e  # Detener el script si algún comando falla

APP_DIR="$HOME/mi_tablero"

echo ">> Actualizando paquetes del sistema..."
sudo apt update -y
sudo apt upgrade -y

echo ">> Instalando Python, venv y Nginx..."
sudo apt install -y python3-pip python3-venv nginx

echo ">> Creando entorno virtual e instalando dependencias de Python..."
cd "$APP_DIR"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo ">> Configurando el servicio systemd (dashapp)..."
sudo cp systemd/dashapp.service /etc/systemd/system/dashapp.service
sudo systemctl daemon-reload
sudo systemctl enable dashapp
sudo systemctl restart dashapp

echo ">> Configurando Nginx como proxy inverso..."
sudo cp nginx/dashapp.conf /etc/nginx/sites-available/dashapp
sudo ln -sf /etc/nginx/sites-available/dashapp /etc/nginx/sites-enabled/dashapp
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo ">> Listo. Verificando estado de los servicios..."
sudo systemctl status dashapp --no-pager
sudo systemctl status nginx --no-pager

IP_PUBLICA=$(curl -s ifconfig.me)
echo ""
echo "============================================================"
echo " Tablero desplegado. Ábrelo en tu navegador en:"
echo " http://${IP_PUBLICA}"
echo "============================================================"
