## English

# Deployment Process

This document outlines the automated deployment process for the Advanced Password Inspector project using Docker and GitHub Actions. The process aims to simplify setup, ensure consistency across environments, and reduce manual deployment errors.

## Prerequisites

Before beginning the deployment process, ensure the following prerequisites are met:

- Docker installed on the deployment machine.
- GitHub account with permissions to the repository.
- Docker Hub account (if pushing the Docker image to a registry).

## Docker Configuration

### Building the Docker Image

1. **Dockerfile**: Ensure the Dockerfile is present in the project root with the appropriate configuration to build the application environment.

    ```Dockerfile
    # Use an official Python runtime as a parent image
    FROM python:3.12-slim

    # Set the working directory in the container
    WORKDIR /app

    # Copy the current directory contents into the container at /app
    COPY . /app

    # Install any needed packages specified in requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Make port 5000 available to the world outside this container
    EXPOSE 5000

    # Define environment variable
    ENV NAME World

    # Run app.py when the container launches
    CMD ["python", "main.py"]
    ```

2. **Build Command**: Build the Docker image using the following command:

    ```bash
    docker build -t advanced_password_inspector .
    ```

### Pushing the Image to Docker Hub

1. **Tagging the Image**: Tag your image with the Docker Hub repository:

    ```bash
    docker tag advanced_password_inspector username/advanced_password_inspector:latest
    ```

2. **Pushing the Image**:
    ```bash
    docker push username/advanced_password_inspector:latest
    ```

## GitHub Actions Configuration

### Workflow Setup

Create a `.github/workflows/deployment.yml` file to define the CI/CD pipeline:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.12
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Build Docker image
      run: docker build -t username/advanced_password_inspector:latest .
    - name: Push Docker image
      run: |
        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
        docker push username/advanced_password_inspector:latest
```

## Testing the Deployment

Ensure the workflow correctly builds and pushes the Docker image by making a commit to the main branch or creating a pull request.


## Conclusion

This automated deployment process using Docker and GitHub Actions provides a robust and error-free deployment flow, ensuring that the application can be consistently deployed across any environment with minimal setup.

___________________________________________________________________________________________________
## Français

# Processus de déploiement

Ce document décrit le processus de déploiement automatisé pour le projet Advanced Password Inspector en utilisant Docker et GitHub Actions. Le processus vise à simplifier la configuration, garantir la cohérence entre les environnements et réduire les erreurs de déploiement manuelles.

## Prérequis

Avant de commencer le processus de déploiement, assurez-vous que les prérequis suivants sont remplis :

- Docker installé sur la machine de déploiement.
- Un compte GitHub avec des autorisations pour le dépôt.
- Un compte Docker Hub (si vous poussez l'image Docker vers un registre).

## Configuration Docker

### Construction de l'image Docker

1. **Dockerfile** : Assurez-vous que le Dockerfile est présent à la racine du projet avec la configuration appropriée pour construire l'environnement de l'application.

    ```Dockerfile
    # Utilisez une image parente Python officielle
    FROM python:3.12-slim

    # Définissez le répertoire de travail dans le conteneur
    WORKDIR /app

    # Copiez le contenu du répertoire actuel dans le conteneur à /app
    COPY . /app

    # Installez les packages nécessaires spécifiés dans requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    # Rendez le port 5000 disponible pour le monde extérieur à ce conteneur
    EXPOSE 5000

    # Définissez la variable d'environnement
    ENV NAME World

    # Lancez app.py lorsque le conteneur démarre
    CMD ["python", "main.py"]
    ```

2. **Commande de construction**: Construisez l'image Docker en utilisant la commande suivante :

    ```bash
    docker build -t advanced_password_inspector .
    ```

### Pousser l'image vers Docker Hub

1. **Tagger l’image**: Taguez votre image avec le dépôt Docker Hub :

    ```bash
    docker tag advanced_password_inspector nom_utilisateur/advanced_password_inspector:latest

    ```

2. **Pushing the Image**:
    ```bash
    docker push nom_utilisateur/advanced_password_inspector:latest

    ```

## Configuration GitHub Actions

### Configuration du flux de travail

Créez un fichier .github/workflows/deployment.yml pour définir le pipeline CI/CD :

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.12
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Build Docker image
      run: docker build -t username/advanced_password_inspector:latest .
    - name: Push Docker image
      run: |
        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
        docker push username/advanced_password_inspector:latest
```

## Tester le déploiement

Assurez-vous que le flux de travail construit et pousse correctement l'image Docker en effectuant un commit sur la branche principale ou en créant une pull request.


## Conclusion

Ce processus de déploiement automatisé utilisant Docker et GitHub Actions fournit un flux de déploiement robuste et sans erreur, garantissant que l'application peut être déployée de manière cohérente sur n'importe quel environnement avec une configuration minimale.