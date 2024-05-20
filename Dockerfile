FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Installer Jupyter
RUN pip install jupyter

# Copier le reste des fichiers de l'application dans le répertoire de travail
COPY . .

# Exposer le port pour Jupyter Notebook
EXPOSE 8888
