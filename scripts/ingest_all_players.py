"""
Script d'ingestion massive pour tous les joueurs du projet.
Charge tous les matchs de chaque PUUID, mais ne stocke que les stats des joueurs trackes.
"""

from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats
from config.players import TRACKED_PLAYERS
import time

# Configuration
MATCHS_PAR_JOUEUR = 100  # Nombre de matchs a recuperer par joueur
DELAY_API = 0.5  # Delai entre les appels API (rate limiting - Riot permet 20 req/s)

def ingest_all():
    print("="*70)
    print("INGESTION MASSIVE - LEAGUE OF LEGENDS DATA PIPELINE")
    print("="*70)
    print(f"Joueurs a traiter : {len(TRACKED_PLAYERS)}")
    print(f"Matchs par joueur : {MATCHS_PAR_JOUEUR}")
    print("="*70 + "\n")

    total_matches_traites = 0
    total_stats_inserees = 0
    match_ids_globaux = set()

    for i, (name, puuid) in enumerate(TRACKED_PLAYERS.items(), 1):
        print(f"\n[{i}/{len(TRACKED_PLAYERS)}] Traitement de {name}")
        print("-" * 70)

        try:
            # Recuperation des match IDs
            match_ids = get_match_ids(puuid, count=MATCHS_PAR_JOUEUR)
            print(f"  -> {len(match_ids)} matchs trouves")

            # Traitement de chaque match
            for j, match_id in enumerate(match_ids, 1):

                # Eviter de traiter le meme match plusieurs fois
                if match_id in match_ids_globaux:
                    print(f"  [{j}/{len(match_ids)}] {match_id} - Deja traite (skip)")
                    continue

                match_ids_globaux.add(match_id)

                # Recuperation du detail
                match = get_match_detail(match_id)

                if match is None:
                    print(f"  [{j}/{len(match_ids)}] {match_id} - Erreur API (skip)")
                    continue

                # Insertion (match + stats filtrees)
                insert_match(match)
                insert_player_stats(match, tracked_only=True)

                total_matches_traites += 1

                # Compter le nombre de joueurs trackes dans ce match
                tracked_in_match = sum(
                    1 for p in match["info"]["participants"]
                    if p["puuid"] in [puuid for puuid in TRACKED_PLAYERS.values()]
                )
                total_stats_inserees += tracked_in_match

                print(f"  [{j}/{len(match_ids)}] {match_id} - OK ({tracked_in_match} joueurs trackes)")

                # Rate limiting
                time.sleep(DELAY_API)

        except Exception as e:
            print(f"  ERREUR sur {name} : {e}")
            continue

    # Resume final
    print("\n" + "="*70)
    print("INGESTION TERMINEE")
    print("="*70)
    print(f"Matchs uniques traites : {total_matches_traites}")
    print(f"Stats inserees (estimation) : {total_stats_inserees}")
    print("\nVerifie les donnees dans pgAdmin avec :")
    print("  SELECT COUNT(*) FROM riot_fact.match_game;")
    print("  SELECT COUNT(*) FROM riot_fact.fact_player_match;")
    print("="*70)


if __name__ == "__main__":
    ingest_all()
