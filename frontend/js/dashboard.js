// Dashboard - Page principale
document.addEventListener('DOMContentLoaded', async () => {
    // Declencher une mise a jour auto au chargement
    await triggerAutoUpdate();

    await loadGlobalStats();
    await loadRankedRanking();
    await loadPlayers();
    await loadPopularItems();

    // Verifier les mises a jour toutes les 10 minutes
    setInterval(async () => {
        await triggerAutoUpdate();
        await refreshAllData();
    }, 10 * 60 * 1000); // 10 minutes
});

// Declencher une mise a jour incrementale
async function triggerAutoUpdate() {
    try {
        const response = await fetch(`${API_BASE_URL}/update`, {
            method: 'POST'
        });
        const result = await response.json();
        console.log('Auto-update:', result);
    } catch (error) {
        console.error('Erreur auto-update:', error);
    }
}

// Rafraichir toutes les donnees
async function refreshAllData() {
    await loadGlobalStats();
    await loadRankedRanking();
    await loadPlayers();
    await loadPopularItems();
}

// Charger les stats globales
async function loadGlobalStats() {
    try {
        const stats = await API.getGlobalStats();

        document.getElementById('totalPlayers').textContent = stats.total_players;
        document.getElementById('totalGames').textContent = stats.total_games;
        document.getElementById('avgWinrate').textContent = utils.formatWinrate(stats.avg_winrate);
        document.getElementById('avgKDA').textContent = utils.formatKDA(stats.avg_kda);
    } catch (error) {
        console.error('Erreur chargement stats globales:', error);
    }
}

// Charger le classement SoloQ avec stats de performance
async function loadRankedRanking() {
    try {
        // Charger ranking et players en parallele
        const [ranking, players] = await Promise.all([
            API.getRankedRanking(),
            API.getPlayers()
        ]);

        const container = document.getElementById('rankedRankingContainer');

        if (!ranking || ranking.length === 0) {
            container.innerHTML = '<div class="loading">Aucun rang disponible</div>';
            return;
        }

        // Creer un map des stats joueurs par nom
        const playerStats = {};
        players.forEach(p => {
            playerStats[p.display_name] = p;
        });

        container.innerHTML = ranking.map(player => {
            const tierClass = player.tier !== 'UNRANKED' ? `tier-${player.tier.toLowerCase()}` : '';
            const stats = playerStats[player.display_name] || {};
            const hasStats = stats.total_games > 0;
            const clickHandler = player.player_id > 0 ? `onclick="goToPlayer(${player.player_id})"` : '';

            return `
            <div class="ranked-card ${tierClass}" ${clickHandler}>
                <div class="ranked-position">#${player.position}</div>
                <div class="ranked-emblem">
                    ${player.tier !== 'UNRANKED' ?
                        `<img src="${utils.getTierEmblem(player.tier)}"
                              alt="${player.tier}"
                              onerror="this.onerror=null; this.parentElement.innerHTML='<span class=\\'unranked-icon\\'>${player.tier.charAt(0)}</span>';">` :
                        '<span class="unranked-icon">?</span>'
                    }
                </div>
                <div class="ranked-info">
                    <div class="ranked-player-name">${player.display_name}</div>
                    <div class="ranked-tier" style="color: ${utils.getTierColor(player.tier)}">
                        ${utils.formatRank(player.tier, player.rank)}
                        ${player.tier !== 'UNRANKED' ? `<span class="ranked-lp">${player.lp} LP</span>` : ''}
                    </div>
                </div>
                <div class="ranked-stats">
                    ${player.tier !== 'UNRANKED' ? `
                        <div class="ranked-record">
                            <span class="wins">${player.wins}W</span>
                            <span class="losses">${player.losses}L</span>
                        </div>
                        <div class="ranked-winrate ${player.winrate >= 50 ? 'positive' : 'negative'}">
                            ${utils.formatWinrate(player.winrate)}
                        </div>
                    ` : '<div class="ranked-unranked">Non classe</div>'}
                </div>
                ${hasStats ? `
                <div class="ranked-performance">
                    <div class="perf-stat">
                        <span class="perf-label">Games</span>
                        <span class="perf-value">${stats.total_games}</span>
                    </div>
                    <div class="perf-stat">
                        <span class="perf-label">WR Grp</span>
                        <span class="perf-value ${stats.winrate_pct >= 50 ? 'positive' : 'negative'}">${utils.formatWinrate(stats.winrate_pct)}</span>
                    </div>
                    <div class="perf-stat">
                        <span class="perf-label">KDA</span>
                        <span class="perf-value">${utils.formatKDA(stats.kda_ratio)}</span>
                    </div>
                    <div class="perf-stat">
                        <span class="perf-label">DPM</span>
                        <span class="perf-value">${utils.formatNumber(stats.avg_dpm)}</span>
                    </div>
                </div>
                ` : ''}
            </div>
        `}).join('');
    } catch (error) {
        console.error('Erreur chargement ranking ranked:', error);
        document.getElementById('rankedRankingContainer').innerHTML =
            '<div class="loading">Erreur lors du chargement des rangs</div>';
    }
}

// Charger les joueurs
async function loadPlayers() {
    try {
        const players = await API.getPlayers();
        const container = document.getElementById('playersGrid');

        if (players.length === 0) {
            container.innerHTML = '<div class="loading">Aucun joueur trouve</div>';
            return;
        }

        container.innerHTML = players.map(player => `
            <div class="player-card" onclick="goToPlayer(${player.player_id})">
                <div class="player-header">
                    <div class="player-name">${player.display_name}</div>
                    <div class="player-games">${player.total_games} games</div>
                </div>
                <div class="player-stats">
                    <div class="player-stat">
                        <span class="player-stat-label">Winrate</span>
                        <span class="player-stat-value winrate">${utils.formatWinrate(player.winrate_pct)}</span>
                    </div>
                    <div class="player-stat">
                        <span class="player-stat-label">KDA</span>
                        <span class="player-stat-value kda">${utils.formatKDA(player.kda_ratio)}</span>
                    </div>
                    <div class="player-stat">
                        <span class="player-stat-label">CS/min</span>
                        <span class="player-stat-value">${player.avg_cs_per_min}</span>
                    </div>
                    <div class="player-stat">
                        <span class="player-stat-label">DPM</span>
                        <span class="player-stat-value">${utils.formatNumber(player.avg_dpm)}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur chargement joueurs:', error);
        document.getElementById('playersGrid').innerHTML =
            '<div class="loading">Erreur lors du chargement des joueurs</div>';
    }
}

// Navigation vers profil joueur
function goToPlayer(playerId) {
    window.location.href = `player.html?id=${playerId}`;
}

// Charger les items populaires (filtres pour ne garder que les items finaux)
async function loadPopularItems() {
    try {
        // Charger plus d'items pour avoir assez apres filtrage
        const items = await API.getPopularItems(50);
        const container = document.getElementById('itemsGrid');

        if (!items || items.length === 0) {
            container.innerHTML = '<div class="loading">Aucun item disponible</div>';
            return;
        }

        // Filtrer les items: exclure composants, potions, wards, etc.
        const filteredItems = items
            .filter(item => !EXCLUDED_ITEMS.includes(item.item_id))
            .slice(0, 12); // Garder les 12 premiers apres filtrage

        if (filteredItems.length === 0) {
            container.innerHTML = '<div class="loading">Aucun item legendaire disponible</div>';
            return;
        }

        container.innerHTML = filteredItems.map(item => `
            <div class="item-card">
                <div class="item-icon">
                    <img src="https://ddragon.leagueoflegends.com/cdn/14.24.1/img/item/${item.item_id}.png"
                         alt="${item.item_name}"
                         onerror="this.onerror=null; this.style.display='none';">
                </div>
                <div class="item-info">
                    <div class="item-name">${item.item_name}</div>
                    <div class="item-stats">
                        <span class="item-stat">
                            <span class="item-stat-label">Achats</span>
                            <span class="item-stat-value">${item.times_bought}</span>
                        </span>
                        <span class="item-stat">
                            <span class="item-stat-label">Winrate</span>
                            <span class="item-stat-value ${item.winrate_with_item >= 50 ? 'winrate' : ''}">${utils.formatWinrate(item.winrate_with_item)}</span>
                        </span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur chargement items:', error);
        document.getElementById('itemsGrid').innerHTML =
            '<div class="loading">Erreur lors du chargement des items</div>';
    }
}
