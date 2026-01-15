// DuoQ Matrix & Synergies
let players = [];
let duoqData = [];

document.addEventListener('DOMContentLoaded', async () => {
    await loadData();
});

async function loadData() {
    try {
        players = await API.getPlayers();
        duoqData = await API.getDuoQ();

        createMatrix();
        createDuoQList();

        document.getElementById('matrixLoading').style.display = 'none';
        document.getElementById('duoqMatrix').style.display = 'grid';
    } catch (error) {
        console.error('Erreur chargement DuoQ:', error);
        document.getElementById('matrixLoading').innerHTML =
            '<div class="loading">Erreur lors du chargement des données</div>';
    }
}

function createMatrix() {
    const container = document.getElementById('duoqMatrix');
    const playerCount = players.length;

    // Définir la grille
    container.style.gridTemplateColumns = `150px repeat(${playerCount}, 1fr)`;

    // Header row
    const headerRow = document.createElement('div');
    headerRow.className = 'matrix-row';
    headerRow.style.gridTemplateColumns = `150px repeat(${playerCount}, 1fr)`;

    // Empty top-left cell
    headerRow.innerHTML = '<div class="matrix-cell header"></div>';

    // Player headers (colonnes)
    players.forEach(player => {
        headerRow.innerHTML += `
            <div class="matrix-cell header" title="${player.display_name}">
                ${getShortName(player.display_name)}
            </div>
        `;
    });

    container.appendChild(headerRow);

    // Data rows
    players.forEach((player1, i) => {
        const row = document.createElement('div');
        row.className = 'matrix-row';
        row.style.gridTemplateColumns = `150px repeat(${playerCount}, 1fr)`;

        // Player header (ligne)
        row.innerHTML = `
            <div class="matrix-cell header" title="${player1.display_name}">
                ${getShortName(player1.display_name)}
            </div>
        `;

        // Cells
        players.forEach((player2, j) => {
            if (i === j) {
                // Même joueur = cellule vide
                row.innerHTML += '<div class="matrix-cell empty">-</div>';
            } else {
                // Chercher la synergie
                const synergy = findSynergy(player1.player_id, player2.player_id);

                if (synergy) {
                    const cellClass = getWinrateClass(synergy.winrate_pct);
                    row.innerHTML += `
                        <div class="matrix-cell ${cellClass}"
                             onclick="showDuoQDetails(${player1.player_id}, ${player2.player_id})"
                             title="${player1.display_name} + ${player2.display_name}">
                            <div class="matrix-cell-games">${synergy.games_together}G</div>
                            <div class="matrix-cell-winrate">${synergy.winrate_pct.toFixed(0)}%</div>
                        </div>
                    `;
                } else {
                    row.innerHTML += `
                        <div class="matrix-cell empty" title="Aucune game ensemble">
                            <div style="font-size: 0.75rem; color: var(--text-muted);">0G</div>
                        </div>
                    `;
                }
            }
        });

        container.appendChild(row);
    });
}

function createDuoQList() {
    const container = document.getElementById('duoqList');

    if (duoqData.length === 0) {
        container.innerHTML = '<div class="loading">Aucune synergie DuoQ détectée</div>';
        return;
    }

    // Trier par winrate puis par games
    const sorted = [...duoqData].sort((a, b) => {
        if (b.winrate_pct !== a.winrate_pct) {
            return b.winrate_pct - a.winrate_pct;
        }
        return b.games_together - a.games_together;
    });

    container.innerHTML = sorted.map((duo, index) => `
        <div class="duoq-card">
            <div class="duoq-rank ${index < 3 ? 'top' : ''}">
                #${index + 1}
            </div>
            <div class="duoq-players">
                <div class="duoq-players-names">
                    ${duo.player_1_name} <span>+</span> ${duo.player_2_name}
                </div>
                <div class="duoq-stats-row">
                    <div class="duoq-stat">
                        <span class="duoq-stat-label">Games</span>
                        <span class="duoq-stat-value">${duo.games_together}</span>
                    </div>
                    <div class="duoq-stat">
                        <span class="duoq-stat-label">Victoires</span>
                        <span class="duoq-stat-value">${duo.wins_together}</span>
                    </div>
                    <div class="duoq-stat">
                        <span class="duoq-stat-label">KDA P1</span>
                        <span class="duoq-stat-value">${duo.p1_avg_kda.toFixed(2)}</span>
                    </div>
                    <div class="duoq-stat">
                        <span class="duoq-stat-label">KDA P2</span>
                        <span class="duoq-stat-value">${duo.p2_avg_kda.toFixed(2)}</span>
                    </div>
                </div>
            </div>
            <div class="duoq-winrate">
                ${duo.winrate_pct.toFixed(1)}%
            </div>
        </div>
    `).join('');
}

function findSynergy(player1Id, player2Id) {
    return duoqData.find(duo =>
        (duo.player_1_id === player1Id && duo.player_2_id === player2Id) ||
        (duo.player_1_id === player2Id && duo.player_2_id === player1Id)
    );
}

function getWinrateClass(winrate) {
    if (winrate >= 70) return 'excellent';
    if (winrate >= 50) return 'good';
    return 'average';
}

function getShortName(displayName) {
    // Prendre seulement le nom avant le #
    const parts = displayName.split('#');
    const name = parts[0];

    // Si > 8 caractères, couper
    if (name.length > 8) {
        return name.substring(0, 8) + '...';
    }
    return name;
}

function showDuoQDetails(player1Id, player2Id) {
    const synergy = findSynergy(player1Id, player2Id);
    if (!synergy) return;

    alert(`
${synergy.player_1_name} + ${synergy.player_2_name}

Games ensemble: ${synergy.games_together}
Victoires: ${synergy.wins_together}
Winrate: ${synergy.winrate_pct.toFixed(1)}%

KDA ${synergy.player_1_name}: ${synergy.p1_avg_kda.toFixed(2)}
KDA ${synergy.player_2_name}: ${synergy.p2_avg_kda.toFixed(2)}
    `.trim());
}
