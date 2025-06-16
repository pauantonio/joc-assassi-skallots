# Joc de l'Assassí de la Pinça

Joc de l'Assassí de la Pinça és una aplicació web desenvolupada en Django per jugar al joc en el context de la Festa Major Alternativa de Sant Vicenç dels Horts, organitzada per Skallots. Aquest projecte inclou una interfície per als jugadors, lògica de joc i un panell d'administració per gestionar les partides.

## Funcionalitats

- **Registre d'usuaris:** Els jugadors poden crear comptes per participar en el joc.
- **Gestor de partides:** Els administradors poden crear i gestionar partides.
- **Classificacions:** Els jugadors poden consultar les puntuacions en temps real.
- **Panell d'administració:** Eina per gestionar els usuaris, partides i puntuacions.

## Requisits del sistema

- Python 3.11 o superior
- pip (gestor de paquets de Python)
- git (per gestionar el repositori)

## Configuració de l'entorn

Segueix aquests passos per configurar el projecte al teu ordinador:

### 1. Clona el repositori

```bash
git clone https://github.com/pauantonio/joc-assassi-skallots.git
cd joc-assassi-skallots
```

### 2. Crea i activa un entorn virtual

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows
```

### 3. Instal·la les dependències

```bash
pip install -r requirements.txt
```

### 4. Configura la base de dades SQLite

No cal configuració addicional per a SQLite, ja que Django la configura automàticament. La base de dades es guardarà en un fitxer anomenat `db.sqlite3` al directori principal del projecte.

### 5. Aplica les migracions de la base de dades

```bash
python manage.py migrate
```

### 6. Crea el fitxer .env

Crea un fitxer `.env` al directori arrel del projecte amb el següent contingut:

```
DEBUG=True
SECRET_KEY="your-secret-key"
AWS_ACCESS_KEY_ID="your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY="your-aws-secret-access-key"
AWS_STORAGE_BUCKET_NAME="your-aws-storage-bucket-name"
AWS_S3_REGION_NAME="your-aws-s3-region-name"
DATABASE_URL=postgres://user:password@hostname:port/dbname
```

Nota: La variable `DATABASE_URL` només és necessària si no vols utilitzar SQLite com a base de dades.

### 7. Executa el servidor de desenvolupament

```bash
python manage.py runserver
```

Per executar el servidor a `0.0.0.0:8000`, utilitza la següent comanda:

```sh
python manage.py runserver 0.0.0.0:8000
```

Accedeix al projecte al navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 8. Crea un superusuari (opcional)

Per accedir al panell d'administració:

```bash
python manage.py createsuperuser
```

Segueix les instruccions per crear un usuari administrador.

## Configuració de la base de dades de producció

Per configurar una base de dades de producció, com PostgreSQL, segueix aquests passos:

1. Actualitza el fitxer `.env` amb la URL de la base de dades:

```
DATABASE_URL=postgres://user:password@hostname:port/dbname
```

2. Aplica les migracions de la base de dades:

```bash
python manage.py migrate
```

## Procfile

El fitxer `Procfile` és utilitzat per especificar els processos que han de ser executats per l'aplicació en un entorn de producció. En aquest projecte, el `Procfile` conté les següents línies:

```
release: python manage.py migrate
web: gunicorn joc_assassi.wsgi:application --log-file -
```

- `release`: Executa les migracions de la base de dades abans de llançar l'aplicació.
- `web`: Utilitza Gunicorn per servir l'aplicació Django.

## Mode de Debug

Si vols establir la configuració `DEBUG` a `False`, utilitza el flag `--insecure` en `runserver` per poder carregar el contingut estàtic:

```sh
python manage.py runserver --insecure
```

## Estrutura del projecte

```
joc-assassi-skallots/
├── env/                # Entorn virtual
├── joc_assassi/       # Configuració del projecte
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py     # Configuració principal
│   ├── urls.py         # Rutes del projecte
│   ├── wsgi.py         # Entrades per a servidors web
├── joc/                # Aplicació principal del joc
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py
│   ├── forms.py
│   ├── middleware.py
│   ├── migrations/     # Migracions de la base de dades
│   ├── models.py
│   ├── static/         # Fitxers CSS i JavaScript
│   ├── templates/      # Templates HTML
│   ├── tests.py
│   ├── utils.py
│   ├── views.py
├── manage.py           # Eina per gestionar el projecte
├── requirements.txt    # Llista de dependències
├── .gitignore          # Fitxers i carpetes ignorats per Git
├── Procfile            # Fitxer per especificar els processos de l'aplicació
├── .env                # Configuració d'entorn
└── README.md           # Documentació del projecte
```

## Nota sobre les migracions

Quan facis canvis als models, és necessari executar `makemigrations` per generar els fitxers de migració. Aquests fitxers de migració han de ser pujats al repositori git per assegurar que els canvis es despleguen correctament a producció.

```bash
python manage.py makemigrations
```

## Llicència

Aquest projecte està llicenciat sota la [MIT License](LICENSE).

