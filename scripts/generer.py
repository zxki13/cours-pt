#!/usr/bin/env python3
"""Parcourt le dossier cours/ et écrit la liste des cours dans cours.json.

Organisation attendue :
  cours/<Matiere>/<fichier>
  cours/<Matiere>/<Chapitre>/<fichier>

Lancé automatiquement par GitHub à chaque ajout de fichier.
Tu peux aussi le lancer toi-même : python3 scripts/generer.py
"""
import json
import re
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER = RACINE / "cours"
SORTIE = RACINE / "cours.json"

EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif",
              ".docx", ".pptx", ".xlsx", ".zip", ".txt"}

JOLIS_NOMS = {
    "mathematiques": "Mathématiques",
    "maths": "Mathématiques",
    "physique-chimie": "Physique-Chimie",
    "physique": "Physique",
    "chimie": "Chimie",
    "sciences-industrielles": "Sciences industrielles",
    "si": "Sciences industrielles",
    "informatique": "Informatique",
    "francais-philo": "Français-Philo",
    "francais": "Français",
    "philosophie": "Philosophie",
    "anglais": "Anglais",
    "autres": "Autres",
}


def sans_prefixe(nom):
    """'01-Maths' -> 'Maths' (les chiffres servent seulement à trier)."""
    return re.sub(r"^\d+[\s._-]+", "", nom)


def cle_tri(texte):
    """Tri naturel : 2 avant 10."""
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", texte)]


def identifiant(nom):
    s = unicodedata.normalize("NFKD", sans_prefixe(nom))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "autres"


def joli(nom):
    propre = sans_prefixe(nom)
    cle = identifiant(nom)
    if cle in JOLIS_NOMS:
        return JOLIS_NOMS[cle]
    texte = re.sub(r"[-_]+", " ", propre).strip()
    return texte[:1].upper() + texte[1:]


def titre_fichier(nom):
    base = re.sub(r"[-_]+", " ", sans_prefixe(Path(nom).stem)).strip()
    return base[:1].upper() + base[1:]


def fichiers_de(dossier_matiere):
    resultat = []
    for chemin in sorted(dossier_matiere.rglob("*"), key=lambda p: cle_tri(str(p))):
        if not chemin.is_file() or chemin.name.startswith("."):
            continue
        if chemin.suffix.lower() not in EXTENSIONS:
            continue
        relatif = chemin.relative_to(dossier_matiere)
        chapitre = " / ".join(joli(p) for p in relatif.parts[:-1])
        resultat.append({
            "titre": titre_fichier(chemin.name),
            "chapitre": chapitre,
            "chemin": chemin.relative_to(RACINE).as_posix(),
            "type": chemin.suffix.lower().lstrip("."),
            "taille": chemin.stat().st_size,
        })
    return resultat


def main():
    matieres = []
    if DOSSIER.is_dir():
        sous_dossiers = sorted((d for d in DOSSIER.iterdir() if d.is_dir() and not d.name.startswith(".")),
                               key=lambda d: cle_tri(d.name))
        for d in sous_dossiers:
            fichiers = fichiers_de(d)
            if fichiers:
                matieres.append({"id": identifiant(d.name), "titre": joli(d.name), "fichiers": fichiers})
        vrac = [f for f in sorted(DOSSIER.iterdir(), key=lambda p: cle_tri(p.name))
                if f.is_file() and not f.name.startswith(".") and not f.name.upper().startswith("LISEZMOI")
                and f.suffix.lower() in EXTENSIONS]
        if vrac:
            matieres.append({"id": "autres", "titre": "Autres", "fichiers": [{
                "titre": titre_fichier(f.name), "chapitre": "",
                "chemin": f.relative_to(RACINE).as_posix(),
                "type": f.suffix.lower().lstrip("."), "taille": f.stat().st_size} for f in vrac]})
    SORTIE.write_text(json.dumps({"matieres": matieres}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    total = sum(len(m["fichiers"]) for m in matieres)
    print(f"{total} fichier(s) dans {len(matieres)} matière(s) -> {SORTIE.name}")


if __name__ == "__main__":
    main()
