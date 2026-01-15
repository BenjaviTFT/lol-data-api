// Page Profil Joueur
let currentPlayer = null;
let radarChart = null;
let championsChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const playerId = urlParams.get('id');

    if (!playerId) {
        alert('ID joueur manquant');
        window.location.href = 'index.html';
        return;
    }

    await loadPlayerProfile(playerId);
    await loadPlayerChampions(playerId);
    await loadPlayerRoles(playerId);
    await loadPlayerItems(playerId);
});

// Charger le profil
async function loadPlayerProfile(playerId) {
    try {
        const player = await API.getPlayerById(playerId);
        currentPlayer = player;

        // Header
        document.getElementById('playerHeader').innerHTML = `
            <div class="player-profile-name">${player.display_name}</div>
            <div class="player-profile-stats">
                <div class="player-profile-stat">
                    <span class="player-profile-stat-label">Total Games</span>
                    <span class="player-profile-stat-value">${player.total_games}</span>
                </div>
                <div class="player-profile-stat">
                    <span class="player-profile-stat-label">Winrate</span>
                    <span class="player-profile-stat-value" style="color: var(--accent-success)">
                        ${utils.formatWinrate(player.winrate_pct)}
                    </span>
                </div>
                <div class="player-profile-stat">
                    <span class="player-profile-stat-label">KDA Ratio</span>
                    <span class="player-profile-stat-value" style="color: var(--accent-primary)">
                        ${utils.formatKDA(player.kda_ratio)}
                    </span>
                </div>
                <div class="player-profile-stat">
                    <span class="player-profile-stat-label">Record</span>
                    <span class="player-profile-stat-value">
                        ${player.wins}W / ${player.losses}L
                    </span>
                </div>
            </div>
        `;

        // Stats grid
        document.getElementById('playerStatsGrid').innerHTML = `
            <div class="stat-card">
                <div class="stat-icon">⚔️</div>
                <div class="stat-content">
                    <div class="stat-label">Kills (avg)</div>
                    <div class="stat-value">${player.avg_kills}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💀</div>
                <div class="stat-content">
                    <div class="stat-label">Deaths (avg)</div>
                    <div class="stat-value">${player.avg_deaths}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🤝</div>
                <div class="stat-content">
                    <div class="stat-label">Assists (avg)</div>
                    <div class="stat-value">${player.avg_assists}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🌾</div>
                <div class="stat-content">
                    <div class="stat-label">CS/min</div>
                    <div class="stat-value">${player.avg_cs_per_min}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💥</div>
                <div class="stat-content">
                    <div class="stat-label">DPM</div>
                    <div class="stat-value">${utils.formatNumber(player.avg_dpm)}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-content">
                    <div class="stat-label">GPM</div>
                    <div class="stat-value">${utils.formatNumber(player.avg_gpm)}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">👁️</div>
                <div class="stat-content">
                    <div class="stat-label">Vision Score</div>
                    <div class="stat-value">${player.avg_vision}</div>
                </div>
            </div>
        `;

        // Créer le radar chart
        createRadarChart(player);

    } catch (error) {
        console.error('Erreur chargement profil:', error);
        document.getElementById('playerHeader').innerHTML =
            '<div class="loading">Erreur lors du chargement du profil</div>';
    }
}

// Charger les champions
async function loadPlayerChampions(playerId) {
    try {
        const champions = await API.getPlayerChampions(playerId);

        if (champions.length === 0) {
            document.getElementById('championsTableBody').innerHTML =
                '<tr><td colspan="6" class="loading">Aucun champion joué</td></tr>';
            return;
        }

        // Table
        document.getElementById('championsTableBody').innerHTML = champions.map(champ => `
            <tr>
                <td class="champion-name">${champ.champion_name}</td>
                <td>${champ.games_played}</td>
                <td>
                    <span class="badge ${utils.getWinrateBadge(champ.winrate_pct)}">
                        ${utils.formatWinrate(champ.winrate_pct)}
                    </span>
                </td>
                <td>${utils.formatKDA(champ.avg_kda)}</td>
                <td>${champ.avg_cs_per_min}</td>
                <td>${utils.formatNumber(champ.avg_dpm)}</td>
            </tr>
        `).join('');

        // Créer le chart (top 5)
        createChampionsChart(champions.slice(0, 5));

    } catch (error) {
        console.error('Erreur chargement champions:', error);
    }
}

// Charger les rôles
async function loadPlayerRoles(playerId) {
    try {
        const roles = await API.getPlayerRoles(playerId);

        if (roles.length === 0) {
            document.getElementById('rolesGrid').innerHTML =
                '<div class="loading">Aucune donnée de rôle disponible</div>';
            return;
        }

        const roleIcons = {
            'TOP': '⚔️',
            'JUNGLE': '🌳',
            'MIDDLE': '✨',
            'BOTTOM': '🏹',
            'UTILITY': '🛡️'
        };

        document.getElementById('rolesGrid').innerHTML = roles.map(role => `
            <div class="role-card">
                <div class="role-header">
                    <div class="role-icon">${roleIcons[role.role] || '🎮'}</div>
                    <div class="role-name">${role.role}</div>
                </div>
                <div class="role-stats">
                    <div class="role-stat">
                        <span class="role-stat-label">Games</span>
                        <span class="role-stat-value">${role.games_played}</span>
                    </div>
                    <div class="role-stat">
                        <span class="role-stat-label">Winrate</span>
                        <span class="role-stat-value" style="color: var(--accent-success)">
                            ${utils.formatWinrate(role.winrate_pct)}
                        </span>
                    </div>
                    <div class="role-stat">
                        <span class="role-stat-label">KDA</span>
                        <span class="role-stat-value">${utils.formatKDA(role.avg_kda)}</span>
                    </div>
                    <div class="role-stat">
                        <span class="role-stat-label">CS/min</span>
                        <span class="role-stat-value">${role.avg_cs_per_min}</span>
                    </div>
                </div>
            </div>
        `).join('');

    } catch (error) {
        console.error('Erreur chargement rôles:', error);
    }
}

// Créer le radar chart
function createRadarChart(player) {
    const ctx = document.getElementById('radarChart');

    // Normaliser les stats sur 100
    const data = {
        labels: ['Winrate', 'KDA', 'CS/min', 'DPM', 'GPM', 'Vision'],
        datasets: [{
            label: player.display_name,
            data: [
                player.winrate_pct,
                Math.min(player.kda_ratio * 20, 100), // Cap à 100
                Math.min(player.avg_cs_per_min * 10, 100),
                Math.min(player.avg_dpm / 10, 100),
                Math.min(player.avg_gpm / 5, 100),
                Math.min(player.avg_vision * 2, 100)
            ],
            backgroundColor: 'rgba(99, 102, 241, 0.2)',
            borderColor: 'rgba(99, 102, 241, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(99, 102, 241, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(99, 102, 241, 1)'
        }]
    };

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: '#9ca3af',
                        backdropColor: 'transparent'
                    },
                    grid: {
                        color: '#374151'
                    },
                    pointLabels: {
                        color: '#e8eaed',
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}

// Créer le chart champions
function createChampionsChart(champions) {
    const ctx = document.getElementById('championsChart');

    const data = {
        labels: champions.map(c => c.champion_name),
        datasets: [{
            label: 'Games joués',
            data: champions.map(c => c.games_played),
            backgroundColor: [
                'rgba(99, 102, 241, 0.8)',
                'rgba(139, 92, 246, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)',
                'rgba(239, 68, 68, 0.8)'
            ],
            borderColor: [
                'rgba(99, 102, 241, 1)',
                'rgba(139, 92, 246, 1)',
                'rgba(16, 185, 129, 1)',
                'rgba(245, 158, 11, 1)',
                'rgba(239, 68, 68, 1)'
            ],
            borderWidth: 2
        }]
    };

    championsChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#e8eaed',
                        font: {
                            size: 12
                        },
                        padding: 15
                    }
                }
            }
        }
    });
}

// Charger les items du joueur
async function loadPlayerItems(playerId) {
    try {
        const items = await API.getPlayerItems(playerId);
        const container = document.getElementById('playerItemsGrid');

        if (!items || items.length === 0) {
            container.innerHTML = '<div class="loading">Aucun item disponible</div>';
            return;
        }

        container.innerHTML = items.map(item => `
            <div class="item-card">
                <div class="item-icon">
                    <img src="https://ddragon.leagueoflegends.com/cdn/14.1.1/img/item/${item.item_id}.png"
                         alt="${item.item_name}"
                         onerror="this.src='https://ddragon.leagueoflegends.com/cdn/14.1.1/img/item/0.png'">
                </div>
                <div class="item-info">
                    <div class="item-name">${item.item_name}</div>
                    <div class="item-stats">
                        <span class="item-stat">
                            <span class="item-stat-label">Achats</span>
                            <span class="item-stat-value">${item.purchase_count}</span>
                        </span>
                        <span class="item-stat">
                            <span class="item-stat-label">Winrate</span>
                            <span class="item-stat-value ${item.winrate_pct >= 50 ? 'winrate' : ''}">${utils.formatWinrate(item.winrate_pct)}</span>
                        </span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur chargement items:', error);
        document.getElementById('playerItemsGrid').innerHTML =
            '<div class="loading">Erreur lors du chargement des items</div>';
    }
}
