# Joc de l'Espàrrek

Joc Esparrek és una aplicació web desenvolupada en Django per jugar al "Joc de l'Espàrrek" en el context d'activitats amb el MCECC. Aquest projecte inclou una interfície per als jugadors, lògica de joc i un panell d'administració per gestionar les partides.

## Funcionalitats

- **Registre d'usuaris:** Els jugadors poden crear comptes per participar en el joc.
- **Gestor de partides:** Els administradors poden crear i gestionar partides.
- **Classificacions:** Els jugadors poden consultar les puntuacions en temps real.
- **Panell d'administració:** Eina per gestionar els usuaris, partides i puntuacions.

## Requisits del sistema

- Python 3.8 o superior
- pip (gestor de paquets de Python)
- git (per gestionar el repositori)

## Configuració de l'entorn

Segueix aquests passos per configurar el projecte al teu ordinador:

### 1. Clona el repositori

```bash
git clone https://github.com/pauantonio/joc_esparrek.git
cd joc_esparrek
```

### 2. Crea i activa un entorn virtual

```bash
python3 -m venv env
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
python manage.py makemigrations
python manage.py migrate
```

### 6. Crea el fitxer .env

Crea un fitxer `.env` al directori arrel del projecte amb el següent contingut:

```
DEBUG=True
SECRET_KEY="your-secret-key"
```

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

## Mode de Debug

Si vols establir la configuració `DEBUG` a `False`, utilitza el flag `--insecure` en `runserver` per poder carregar el contingut estàtic:

```sh
python manage.py runserver --insecure
```

## Estrutura del projecte

```
joc_esparrek/
├── env/                # Entorn virtual
├── joc_esparrek/       # Configuració del projecte
│   ├── settings.py     # Configuració principal
│   ├── urls.py         # Rutes del projecte
│   ├── wsgi.py         # Entrades per a servidors web
├── joc/                # Aplicació principal del joc
│   ├── migrations/     # Migracions de la base de dades
│   ├── templates/      # Templates HTML
│   ├── static/         # Fitxers CSS i JavaScript
├── manage.py           # Eina per gestionar el projecte
├── requirements.txt    # Llista de dependències
├── .gitignore          # Fitxers i carpetes ignorats per Git
```

## Contribució

1. Fes un fork del repositori.
2. Crea una branca per la teva funcionalitat o correcció:
   ```bash
   git checkout -b nom-branca
   ```
3. Fes commit dels teus canvis:
   ```bash
   git commit -m "Descripció del canvi"
   ```
4. Puja els teus canvis:
   ```bash
   git push origin nom-branca
   ```
5. Obre una pull request.

## Llicència

Aquest projecte està llicenciat sota la [MIT License](LICENSE).

