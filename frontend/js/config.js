// Configuration de l'API
// Utilise l'URL relative (meme origine) - fonctionne en local et en prod
const API_BASE_URL = '';

// Endpoints
const API_ENDPOINTS = {
    players: `${API_BASE_URL}/players`,
    ranking: `${API_BASE_URL}/ranking`,
    rankedRanking: `${API_BASE_URL}/ranking/ranked`,
    duoq: `${API_BASE_URL}/duoq`,
    globalStats: `${API_BASE_URL}/stats/global`,
    recentMatches: `${API_BASE_URL}/matches/recent`,
    playerById: (id) => `${API_BASE_URL}/players/${id}`,
    playerChampions: (id) => `${API_BASE_URL}/players/${id}/champions`,
    playerRoles: (id) => `${API_BASE_URL}/players/${id}/roles`,
    // Items
    popularItems: `${API_BASE_URL}/items/popular`,
    playerItems: (id) => `${API_BASE_URL}/players/${id}/items`,
    playerChampionItems: (playerId, champId) => `${API_BASE_URL}/players/${playerId}/champions/${champId}/items`,
    playerBuilds: (id) => `${API_BASE_URL}/players/${id}/builds`
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
    },

    // Formatage du rang ranked
    formatRank: (tier, rank) => {
        if (tier === 'UNRANKED') return 'Unranked';
        return `${tier.charAt(0)}${tier.slice(1).toLowerCase()} ${rank}`;
    },

    // Couleur du tier
    getTierColor: (tier) => {
        const colors = {
            'CHALLENGER': '#f4c874',
            'GRANDMASTER': '#cd3d45',
            'MASTER': '#9d48e0',
            'DIAMOND': '#576cbd',
            'EMERALD': '#0fa94d',
            'PLATINUM': '#4e9996',
            'GOLD': '#cd8837',
            'SILVER': '#80989d',
            'BRONZE': '#8c523a',
            'IRON': '#5e5550',
            'UNRANKED': '#666'
        };
        return colors[tier] || '#666';
    },

    // URL de l'embleme du tier (utilise les PNG officiels plus fiables)
    getTierEmblem: (tier) => {
        if (tier === 'UNRANKED') return '';
        // Utiliser les emblemes PNG de Data Dragon (plus fiable que les SVG)
        const tierLower = tier.toLowerCase();
        return `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-emblem/emblem-${tierLower}.png`;
    },

    // URL alternative pour les mini-crests
    getTierMiniCrest: (tier) => {
        if (tier === 'UNRANKED') return '';
        return `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-static-assets/global/default/images/ranked-mini-crests/${tier.toLowerCase()}.svg`;
    }
};
