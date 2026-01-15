// Configuration de l'API
const API_BASE_URL = 'http://127.0.0.1:8000';

// Endpoints
const API_ENDPOINTS = {
    players: `${API_BASE_URL}/players`,
    ranking: `${API_BASE_URL}/ranking`,
    duoq: `${API_BASE_URL}/duoq`,
    globalStats: `${API_BASE_URL}/stats/global`,
    recentMatches: `${API_BASE_URL}/matches/recent`,
    playerById: (id) => `${API_BASE_URL}/players/${id}`,
    playerChampions: (id) => `${API_BASE_URL}/players/${id}/champions`,
    playerRoles: (id) => `${API_BASE_URL}/players/${id}/roles`,
    // Items
    popularItems: `${API_BASE_URL}/items/popular`,
    playerItems: (id) => `${API_BASE_URL}/players/${id}/items`
};

// Utilitaires
const utils = {
    formatWinrate: (wr) => `${wr.toFixed(1)}%`,
    formatKDA: (kda) => kda.toFixed(2),
    formatNumber: (num) => Math.round(num),

    getWinrateBadge: (wr) => {
        if (wr >= 60) return 'badge-success';
        if (wr >= 50) return 'badge-warning';
        return 'badge-danger';
    },

    getRankBadge: (rank) => {
        if (rank === 1) return 'gold';
        if (rank === 2) return 'silver';
        if (rank === 3) return 'bronze';
        return 'default';
    }
};
