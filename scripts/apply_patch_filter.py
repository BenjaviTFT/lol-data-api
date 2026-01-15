"""
Script pour appliquer les vues analytics filtrees par patch 16.1
"""

import sys
from pathlib import Path

# Ajouter le repertoire parent au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

def apply_patch_filter():
    """Execute le fichier SQL de creation des vues filtrees."""
    sql_file = Path(__file__).resolve().parent.parent / "db" / "create_analytics_views_patch_filtered.sql"

    # Lire le contenu SQL
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Executer le SQL
    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql_content)
                print("="*70)
                print("VUES ANALYTICS MISES A JOUR")
                print("="*70)
                print("Toutes les vues sont maintenant filtrees sur le patch 16.1")
                print()
                print("Vues affectees :")
                print("  - player_stats")
                print("  - player_champions")
                print("  - duoq_synergies")
                print("  - player_ranking")
                print("  - player_stats_by_role")
                print("  - popular_items")
                print("  - recent_matches")
                print()
                print("Le site web affichera maintenant uniquement les donnees du patch 16.1")
                print("="*70)
    finally:
        conn.close()

if __name__ == "__main__":
    apply_patch_filter()
