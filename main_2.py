from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats

PUUID_TEST = "rFWCHHZRZA6WmzfkBofol2jN5BKoPD0S8CYwPr-gmRhnOx6oRmeRNELX-rCL-nB8fCbpjAHswbWQSw"

if __name__ == "__main__":
    match_ids = get_match_ids(PUUID_TEST, count=5)

    for match_id in match_ids:
        print(f"\n{'='*60}")
        print(f"Traitement du match : {match_id}")
        print('='*60)

        match = get_match_detail(match_id)

        insert_match(match)
        insert_player_stats(match)

    print("\nPipeline termine - Verifie fact_player_match dans pgAdmin")
