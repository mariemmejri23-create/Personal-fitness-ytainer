# Personal Fitness Trainer — template WordPress / Elementor

Reproduction du design « Personal Fitness Trainer » (maquette 1440 px) sous forme de **template Elementor importable**, avec uniquement des widgets **gratuits** (aucun Elementor Pro requis).

![Aperçu](assets/images/hero-bg.jpg)

## Contenu du dépôt

| Fichier | Rôle |
|---|---|
| `elementor/personal-fitness-trainer.json` | **Le template à importer dans Elementor** |
| `elementor/custom.css` | Le CSS du design (déjà intégré dans le template, fourni à part pour référence) |
| `assets/images/` | Images extraites de la maquette (hero, coach, logos, avatars…) |
| `preview/index.html` | Aperçu statique approximatif (ouvrir dans un navigateur, sans WordPress) |
| `tools/build_template.py` | Script qui génère le JSON et l'aperçu (pour modifier le template en code) |

## Sections reproduites

1. **Hero** plein écran : badge « 30-Day Money-Back Guarantee », avis clients, grand titre, carte orange « Book your call »
2. **Chiffres clés** (+250, 98 %, 5, 3x)
3. **Témoignage** (Sara Chen)
4. **À propos** (« Hi, I'm Rachel Stone », signature, « My Philosophy ») + logos de certification
5. **Services** (fond noir, cartes NYC / Online / Nutrition / Group)
6. **How it works** (5 étapes)
7. **Signature Programs** (3 cartes tarifaires, « Most Popular » en orange)
8. **Résultats** (avant / après + avis Sophie Lammers)
9. **FAQ** (accordéon)
10. **Contact** (cartes Chat / Call us + formulaire)

Le tout est responsive (desktop, tablette, mobile).

## Installation

### Prérequis
- WordPress 6.x
- Plugin **Elementor** (gratuit) version **3.16 ou plus** — les *Conteneurs Flexbox* doivent être activés (c'est le cas par défaut sur les installations récentes ; sinon : *Elementor › Paramètres › Fonctionnalités › Conteneur Flexbox = Actif*).
- Un thème léger conseillé : **Hello Elementor**.

### Étapes
1. Téléchargez `elementor/personal-fitness-trainer.json` (bouton *Download raw file* sur GitHub).
2. Dans WordPress : **Modèles › Modèles enregistrés › Importer des modèles** (*Templates › Saved Templates › Import Templates*), choisissez le fichier JSON puis **Importer**.
   Les images sont téléchargées automatiquement dans votre médiathèque.
3. Créez une page (**Pages › Ajouter**), cliquez **Modifier avec Elementor**.
4. Cliquez sur l'icône dossier (*Ajouter un modèle*) › onglet **Mes modèles** › **Insérer** sur « Personal Fitness Trainer ».
5. Dans les réglages de la page (roue dentée en bas à gauche), choisissez la mise en page **Elementor Pleine largeur** (ou **Elementor Canvas** pour une page sans en-tête ni pied de page, comme sur la maquette).
6. **Publiez**. Pour en faire la page d'accueil : *Réglages › Lecture › Une page statique*.

> Si les images n'apparaissent pas après l'import (hébergeur qui bloque les téléchargements externes), importez manuellement le dossier `assets/images/` dans la médiathèque, puis remplacez chaque image dans Elementor.

## Plan B : copier-coller (sans import)

Si l'import du JSON ne fonctionne pas (droits insuffisants, erreur « This source does not support import »…) :

1. Ouvrez [`elementor/page-html-a-coller.html` en version brute](https://raw.githubusercontent.com/mariemmejri23-create/Personal-fitness-ytainer/claude/wordpress-elementor-design-4l07jm/elementor/page-html-a-coller.html), faites **⌘A** puis **⌘C** (Ctrl+A / Ctrl+C sur PC).
2. Dans Elementor, glissez un widget **HTML** dans la page et collez le code (**⌘V**) dans le champ « Code HTML ».
3. Sélectionnez le conteneur qui entoure le widget : *Mise en page › Largeur du contenu = Pleine largeur*, et *Avancé › Marge intérieure = 0*.
4. Réglages de la page (roue dentée) › Mise en page **Elementor Canvas**, puis enregistrez.

Ça marche aussi sans Elementor : bloc **HTML personnalisé** de l'éditeur WordPress. Les textes se modifient directement dans le code (les images sont chargées depuis GitHub).

## Personnalisation

- **Textes** : cliquez directement sur un texte dans Elementor pour le modifier (tout le contenu est en widgets Titre / Éditeur de texte / Bouton natifs, facilement traduisible en français).
- **Images** : sélectionnez un widget Image ou un conteneur (onglet *Style › Arrière-plan* pour le hero et la photo du coach) et remplacez l'image. Les photos fournies sont extraites de la maquette : remplacez-les par vos propres photos.
- **Liens** : les boutons pointent vers les ancres de la page (`#programs`, `#contact`…). Modifiez l'email `hello@example.com` et le téléphone `tel:+10000000000` avec vos coordonnées.
- **Couleurs / police** : définies en haut de `custom.css` (orange `#f9652f`, noir `#121212`, police *Instrument Sans*). Le CSS se trouve dans le premier widget **HTML** de la page (petit bloc invisible tout en haut, visible dans le *Navigateur* Elementor sous le nom « Conteneur »). Vous pouvez aussi le déplacer dans *Apparence › Personnaliser › CSS additionnel*.
- **Formulaire de contact** : le formulaire fourni utilise `mailto:` (ouvre la messagerie du visiteur). Pour un vrai envoi d'e-mails, installez **Contact Form 7** ou **WPForms** (gratuits) et remplacez le contenu du widget HTML du formulaire par le shortcode, en gardant `<div class="pft-form-wrap">…</div>` autour : le style est déjà prévu. Avec Elementor Pro, vous pouvez utiliser le widget *Formulaire*.
- **Avant / Après** : l'image fournie est une photo composite. Remplacez-la par votre propre visuel avant/après (ou un plugin de comparaison type *Before After Image Slider*).

## Régénérer le template (optionnel)

Le JSON est généré par `tools/build_template.py` à partir de `elementor/custom.css` :

```bash
python3 tools/build_template.py
```
