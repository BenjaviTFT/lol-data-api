// Comparateur de joueurs
let players = [];
let player1Data = null;
let player2Data = null;
let comparisonChart = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadPlayers();
});

async function loadPlayers() {
    try {
        players = await API.getPlayers();

        const select1 = document.getElementById('player1Select');
        const select2 = document.getElementById('player2Select');

        players.forEach(player => {
            const option1 = document.createElement('option');
            option1.value = player.player_id;
            option1.textContent = player.display_name;
            select1.appendChild(option1);

            const option2 = document.createElement('option');
            option2.value = player.player_id;
            option2.textContent = player.display_name;
            select2.appendChild(option2);
        });
    } catch (error) {
        console.error('Erreur chargement joueurs:', error);
    }
}

async function onPlayerChange() {
    const player1Id = document.getElementById('player1Select').value;
    const player2Id = document.getElementById('player2Select').value;

    if (!player1Id || !player2Id) {
        document.getElementById('comparisonContainer').style.display = 'none';
        return;
    }

    if (player1Id === player2Id) {
        alert('Veuillez sélectionner deux joueurs différents');
        return;
    }

    try {
        player1Data = await API.getPlayerById(player1Id);
        player2Data = await API.getPlayerById(player2Id);

        showComparison();
    } catch (error) {
        console.error('Erreur chargement comparaison:', error);
    }
}

function showComparison() {
    document.getElementById('comparisonContainer').style.display = 'block';

    createComparisonRadar();
    createComparisonGrid();
    createFaceToFace();
}

function createComparisonRadar() {
    const ctx = document.getElementById('comparisonRadar');

    // Détruire l'ancien chart
    if (comparisonChart) {
        comparisonChart.destroy();
    }

    const data = {
        labels: ['Winrate', 'KDA', 'CS/min', 'DPM', 'GPM', 'Vision'],
        datasets: [
            {
                label: player1Data.display_name,
                data: [
                    player1Data.winrate_pct,
                    Math.min(player1Data.kda_ratio * 20, 100),
                    Math.min(player1Data.avg_cs_per_min * 10, 100),
                    Math.min(player1Data.avg_dpm / 10, 100),
                    Math.min(player1Data.avg_gpm / 5, 100),
                    Math.min(player1Data.avg_vision * 2, 100)
                ],
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(99, 102, 241, 1)',
                pointBorderColor: '#fff'
            },
            {
                label: player2Data.display_name,
                data: [
                    player2Data.winrate_pct,
                    Math.min(player2Data.kda_ratio * 20, 100),
                    Math.min(player2Data.avg_cs_per_min * 10, 100),
                    Math.min(player2Data.avg_dpm / 10, 100),
                    Math.min(player2Data.avg_gpm / 5, 100),
                    Math.min(player2Data.avg_vision * 2, 100)
                ],
                backgroundColor: 'rgba(245, 158, 11, 0.2)',
                borderColor: 'rgba(245, 158, 11, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(245, 158, 11, 1)',
                pointBorderColor: '#fff'
            }
        ]
    };

    comparisonChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#e8eaed',
                        font: { size: 14, weight: '600' },
                        padding: 20
                    }
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
                    grid: { color: '#374151' },
                    pointLabels: {
                        color: '#e8eaed',
                        font: { size: 13, weight: '600' }
                    }
                }
            }
        }
    });
}

function createComparisonGrid() {
    const stats = [
        { label: 'Total Games', key: 'total_games', format: (v) => v },
        { label: 'Winrate', key: 'winrate_pct', format: utils.formatWinrate },
        { label: 'KDA Ratio', key: 'kda_ratio', format: utils.formatKDA },
        { label: 'Kills (avg)', key: 'avg_kills', format: (v) => v.toFixed(1) },
        { label: 'Deaths (avg)', key: 'avg_deaths', format: (v) => v.toFixed(1) },
        { label: 'Assists (avg)', key: 'avg_assists', format: (v) => v.toFixed(1) },
        { label: 'CS/min', key: 'avg_cs_per_min', format: (v) => v.toFixed(1) },
        { label: 'DPM', key: 'avg_dpm', format: utils.formatNumber },
        { label: 'GPM', key: 'avg_gpm', format: utils.formatNumber },
        { label: 'Vision Score', key: 'avg_vision', format: (v) => v.toFixed(1) }
    ];

    document.getElementById('comparisonGrid').innerHTML = stats.map(stat => {
        const val1 = player1Data[stat.key];
        const val2 = player2Data[stat.key];
        const winner1 = val1 > val2;
        const winner2 = val2 > val1;

        return `
            <div class="comparison-stat-card">
                <div class="comparison-stat-label">${stat.label}</div>
                <div class="comparison-stat-values">
                    <div class="comparison-value">
                        <div class="comparison-player-label">${player1Data.display_name}</div>
                        <div class="comparison-value-number ${winner1 ? 'winner' : 'loser'}">
                            ${stat.format(val1)}
                        </div>
                    </div>
                    <div style="color: var(--text-muted); font-size: 1.5rem;">vs</div>
                    <div class="comparison-value">
                        <div class="comparison-player-label">${player2Data.display_name}</div>
                        <div class="comparison-value-number ${winner2 ? 'winner' : 'loser'}">
                            ${stat.format(val2)}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function createFaceToFace() {
    const stats = [
        { label: 'Winrate', key: 'winrate_pct' },
        { label: 'KDA Ratio', key: 'kda_ratio' },
        { label: 'Damage Per Minute', key: 'avg_dpm' },
        { label: 'CS Per Minute', key: 'avg_cs_per_min' },
        { label: 'Vision Score', key: 'avg_vision' }
    ];

    document.getElementById('faceToFace').innerHTML = stats.map(stat => {
        const val1 = player1Data[stat.key];
        const val2 = player2Data[stat.key];
        const total = val1 + val2;
        const percent1 = (val1 / total * 100).toFixed(0);
        const percent2 = (val2 / total * 100).toFixed(0);

        return `
            <div class="comparison-bar">
                <div class="comparison-bar-label">${stat.label}</div>
                <div class="comparison-bar-container">
                    <div class="comparison-bar-player">
                        <div class="comparison-bar-name">${player1Data.display_name}</div>
                        <div class="comparison-bar-value">${val1.toFixed(1)}</div>
                    </div>
                    <div class="comparison-bar-track">
                        <div class="comparison-bar-fill-left" style="width: ${percent1}%">
                            ${percent1}%
                        </div>
                        <div class="comparison-bar-fill-right" style="width: ${percent2}%">
                            ${percent2}%
                        </div>
                    </div>
                    <div class="comparison-bar-player">
                        <div class="comparison-bar-name">${player2Data.display_name}</div>
                        <div class="comparison-bar-value">${val2.toFixed(1)}</div>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}
