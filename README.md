# Advanced Password Inspector

## English

### Overview
Advanced Password Inspector is a Python-based tool that evaluates password strength, estimates cracking times, and checks passwords against breached databases. This tool aims to improve user security by providing comprehensive assessments and personalized recommendations to strengthen weak passwords.

### Features
- **Password Strength Evaluation**: Analyze password complexity based on length, character variety, and predictability.
- **Cracking Time Estimation**: Provide estimates on how long it would take to crack a password using various attack methods, including brute force and dictionary attacks.
- **Breach Database Checking**: Compare passwords against an online database of compromised passwords to alert users if their password is too common.
- **Detailed Reports and Recommendations**: Generate detailed security reports and suggest ways to improve password strength.
- **User Interface**: A simple graphical interface for non-technical users to easily evaluate their password security.
- **Developer API**: An API for developers to integrate this tool into other applications or systems.

### Target Users
- **Developers**: To integrate the password analyzer into larger applications, ensuring strong passwords during user registration or password changes.
- **System Administrators**: To assess and enhance password security within their organizations.
- **General Public**: To offer an easy-to-use tool for individuals to check the security of their personal passwords.

### Getting Started
To get started with Advanced Password Inspector, clone the repository and install the necessary dependencies:
```bash
git clone https://github.com/Tom-Souillard/advanced_password_inspector.git
cd advanced_password_inspector
pip install -r requirements.txt
```

### Usage

Here is how you can use the tool to analyze a password:
```python
from password_inspector import analyze_password

result = analyze_password("your_password_here")
print(result)
```

### Contributing
Contributions are welcome! Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

### License
This project is licensed under the Apache License - see the LICENSE.md file for details.

___________________________________________________________________________________________________
## Français

### Vue d'ensemble

Advanced Password Inspector est un outil basé sur Python qui évalue la force des mots de passe, estime les temps de craquage, et vérifie les mots de passe contre des bases de données de mots de passe compromis. Cet outil vise à améliorer la sécurité des utilisateurs en fournissant des évaluations complètes et des recommandations personnalisées pour renforcer les mots de passe faibles.

### Fonctionnalités

- **Évaluation de la force des mots de passe** : Analyse de la complexité des mots de passe basée sur la longueur, la diversité des caractères et la prévisibilité.
- **Estimation du temps de craquage** : Fournit des estimations du temps nécessaire pour craquer un mot de passe en utilisant diverses méthodes d'attaque, y compris la force brute et les attaques par dictionnaire.
- **Vérification contre les bases de données de mots de passe compromis** : Comparaison des mots de passe avec une base de données en ligne de mots de passe déjà compromis pour alerter les utilisateurs si leur mot de passe est trop commun.
- **Rapports détaillés et recommandations** : Génération de rapports de sécurité détaillés et suggestions pour améliorer la force des mots de passe.
- **Interface utilisateur** : Une interface graphique simple pour que les utilisateurs non techniques puissent facilement évaluer la sécurité de leur mot de passe.
- **API pour développeurs** : Une API permettant aux développeurs d'intégrer cet outil dans d'autres applications ou systèmes.

### Utilisateurs Cibles

- **Développeurs** : Pour intégrer l'analyseur de mot de passe dans des applications plus larges, assurant ainsi la création de mots de passe forts lors de l'enregistrement des utilisateurs ou la modification des mots de passe.
- **Administrateurs système** : Pour évaluer et améliorer la sécurité des mots de passe au sein de leur organisation.
- **Grand public** : Offrir un outil facile à utiliser pour que les individus puissent vérifier la sécurité de leurs mots de passe personnels.

### Pour Commencer

Pour commencer avec Advanced Password Inspector, clonez le dépôt et installez les dépendances nécessaires :
```bash
git clone https://github.com/Tom-Souillard/advanced_password_inspector.git
cd advanced_password_inspector
pip install -r requirements.txt
```

### Utilisation
Voici comment vous pouvez utiliser l'outil pour analyser un mot de passe :
```python
from password_inspector import analyze_password
result = analyze_password("votre_mot_de_passe_ici")
print(result)
```

### Licence
Ce projet est sous Apache License - voir le fichier LICENSE.md pour les détails.