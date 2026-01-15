"""
Script pour ajouter facilement un nouveau joueur au tracking.
Usage: python add_player.py "SummonerName#TAG" "puuid"
"""

import sys
from pathlib import Path

# Ajouter le repertoire parent au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def add_player_to_config(riot_id, puuid):
    """
    Ajoute un joueur au fichier config/players.py

    Args:
        riot_id (str): Nom Riot complet (ex: "Player#EUW")
        puuid (str): PUUID du joueur
    """
    config_file = Path(__file__).resolve().parent.parent / "config" / "players.py"

    # Lire le contenu actuel
    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verifier si le joueur existe deja
    if f'"{riot_id}"' in content:
        print(f"Le joueur {riot_id} existe deja dans la config.")
        return False

    if f'"{puuid}"' in content:
        print(f"Ce PUUID existe deja dans la config.")
        return False

    # Trouver la ligne de fermeture du dictionnaire
    if "}" in content:
        # Ajouter le nouveau joueur avant la fermeture
        lines = content.split('\n')
        new_lines = []
        inserted = False

        for line in lines:
            if not inserted and line.strip() == "}":
                # Ajouter le nouveau joueur
                new_lines.append(f'    "{riot_id}": "{puuid}",')
                inserted = True

            new_lines.append(line)

        # Ecrire le nouveau contenu
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        print(f"Joueur ajoute avec succes !")
        print(f"  Riot ID: {riot_id}")
        print(f"  PUUID: {puuid}")
        print(f"\nLance maintenant 'python ingest_all_players.py' pour charger ses matchs.")
        return True
    else:
        print("Erreur: format du fichier config/players.py inattendu")
        return False

def interactive_add():
    """Mode interactif pour ajouter un joueur."""
    print("="*70)
    print("AJOUT D'UN NOUVEAU JOUEUR")
    print("="*70)
    print()

    riot_id = input("Riot ID complet (ex: Player#EUW): ").strip()
    puuid = input("PUUID du joueur: ").strip()

    if not riot_id or not puuid:
        print("Erreur: Riot ID et PUUID requis.")
        return

    add_player_to_config(riot_id, puuid)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Mode ligne de commande
        riot_id = sys.argv[1]
        puuid = sys.argv[2]
        add_player_to_config(riot_id, puuid)
    else:
        # Mode interactif
        interactive_add()
