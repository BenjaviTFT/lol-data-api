"""
Pydantic models pour l'API
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PlayerStats(BaseModel):
    player_id: int
    display_name: str
    summoner_name: str
    tag_line: str
    total_games: int
    wins: int
    losses: int
    winrate_pct: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float
    kda_ratio: float
    avg_cs_per_min: float
    avg_dpm: float
    avg_gpm: float
    avg_vision: float


class PlayerChampion(BaseModel):
    player_id: int
    display_name: str
    champion_id: int
    champion_name: str
    champion_key: str
    games_played: int
    wins: int
    losses: int
    winrate_pct: float
    avg_kills: float
    avg_deaths: float
    avg_assists: float
    avg_kda: float
    avg_cs_per_min: float
    avg_dpm: float


class DuoQSynergy(BaseModel):
    player_1_id: int
    player_1_name: str
    player_2_id: int
    player_2_name: str
    games_together: int
    wins_together: int
    losses_together: int
    winrate_pct: float
    p1_avg_kda: float
    p2_avg_kda: float
    last_played: Optional[datetime]


class PlayerRanking(BaseModel):
    rank: int
    player_id: int
    display_name: str
    total_games: int
    winrate_pct: float
    kda_ratio: float
    avg_dpm: float
    avg_cs_per_min: float
    avg_vision: float
    score: float


class RecentMatch(BaseModel):
    match_id: str
    game_start: datetime
    game_duration: int
    player_name: str
    champion: str
    win: bool
    kills: int
    deaths: int
    assists: int
    kda: float
    role: str


class PlayerStatsByRole(BaseModel):
    player_id: int
    display_name: str
    role: str
    games_played: int
    wins: int
    winrate_pct: float
    avg_kda: float
    avg_cs_per_min: float
    avg_dpm: float


class PopularItem(BaseModel):
    item_id: int
    item_name: str
    times_bought: int
    winrate_with_item: float


class PlayerItem(BaseModel):
    player_id: int
    display_name: str
    item_id: int
    item_name: str
    times_bought: int
    winrate_with_item: float
