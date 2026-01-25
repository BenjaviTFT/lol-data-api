# Guide de Déploiement - VPS Hostinger (Ubuntu 22.04+)

Ce guide détaillé vous accompagnera pas à pas pour déployer **LoL Analytics V1.0.0** sur votre VPS Hostinger.

## 1. Connexion et Préparation du Serveur

Ouvrez un terminal sur votre ordinateur et connectez-vous en SSH :
```bash
ssh root@<IP_DE_VOTRE_VPS>
```

Mettez à jour le système pour garantir la sécurité et la stabilité :
```bash
apt update && apt upgrade -y
```

Installez les outils nécessaires (Python, Git, PostgreSQL, Nginx) :
```bash
apt install -y python3-pip python3-venv postgresql postgresql-contrib git nginx
```

## 2. Configuration de la Base de Données (PostgreSQL)

Connectez-vous à l'utilisateur PostgreSQL :
```bash
sudo -u postgres psql
```

Exécutez les commandes SQL suivantes (remplacez `votre_mot_de_passe` par un mot de passe sûr) :
```sql
-- Création de la base de données
CREATE DATABASE lol_data_analytics_discord;

-- Création de l'utilisateur
CREATE USER benja WITH ENCRYPTED PASSWORD 'votre_mot_de_passe';

-- Attribution des droits
GRANT ALL PRIVILEGES ON DATABASE lol_data_analytics_discord TO benja;
ALTER DATABASE lol_data_analytics_discord OWNER TO benja;

-- Connexion à la base pour donner les droits sur le schéma public (important pour Ubuntu 22.04+)
\c lol_data_analytics_discord
GRANT ALL ON SCHEMA public TO benja;
\q
```

## 3. Installation de l'Application

Allez dans le dossier `/var/www` et récupérez votre code :
```bash
mkdir -p /var/www/lol-data
cd /var/www/lol-data
```

**Note :** Vous pouvez soit utiliser `git clone` si votre code est sur GitHub, soit transférer vos fichiers via SFTP (WinSCP ou FileZilla) dans ce dossier.

Une fois les fichiers présents, créez l'environnement virtuel Python :
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configuration de l'Environnement

Créez le fichier de configuration `.env` dans le dossier `config/` :
```bash
nano config/.env
```

Copiez et collez la configuration suivante (adaptez les valeurs) :
```ini
RIOT_API_KEY=RGAPI-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
POSTGRES_USER=benja
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_DB=lol_data_analytics_discord
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
*(Appuyez sur `Ctrl+O` puis `Entrée` pour sauvegarder, et `Ctrl+X` pour quitter)*

## 5. Initialisation de la Base de Données

Lancez le script d'initialisation complet pour créer toutes les tables nécessaires (champions, joueurs, matchs) :
```bash
python3 scripts/init_vps_db.py
```

Une fois les tables créées, déployez les vues SQL :
```bash
psql -h localhost -U benja -d lol_data_analytics_discord -f db/migrations/deploy_views_vps.sql
```

## 6. Automatisation avec Systemd (Service)

Pour que l'application démarre toute seule et reste active, créez un service :
```bash
nano /etc/systemd/system/lol-analytics.service
```

Collez ce bloc :
```ini
[Unit]
Description=Backend LoL Analytics V1
After=network.target postgresql.service

[Service]
User=root
WorkingDirectory=/var/www/lol-data
Environment="PATH=/var/www/lol-data/venv/bin"
ExecStart=/var/www/lol-data/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Activez et démarrez le service :
```bash
systemctl daemon-reload
systemctl enable lol-analytics
systemctl start lol-analytics
```

Vérifiez que tout fonctionne :
```bash
systemctl status lol-analytics
```

## 7. Configuration de Nginx (Accès via Port 80)

Configurez Nginx pour rediriger le trafic vers votre application :
```bash
nano /etc/nginx/sites-available/lol-analytics
```

Collez ceci (remplacez `votre_ip_ou_domaine` par l'IP du VPS) :
```nginx
server {
    listen 80;
    server_name votre_ip_ou_domaine;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activez le site et redémarrez Nginx :
```bash
ln -s /etc/nginx/sites-available/lol-analytics /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

## 8. Maintenance et Logs

- **Voir les logs en direct** (très utile pour débugger) :
  ```bash
  journalctl -u lol-analytics -f
  ```
- **Redémarrer l'app** après une modif :
  ```bash
  systemctl restart lol-analytics
  ```
- **Mettre à jour la clé API** :
  Modifiez `config/.env`, sauvegardez, puis redémarrez le service.

---
**Félicitations !** Votre site est maintenant accessible sur `http://<VOTRE_IP_VPS>`.
