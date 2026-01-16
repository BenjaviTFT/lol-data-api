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

// Liste des items a exclure (composants, bottes basiques, consommables, wards)
// Ces items ne sont pas des "items finaux" et encombrent l'affichage
const EXCLUDED_ITEMS = [
    // Bottes basiques
    1001, // Boots
    // Composants communs
    1004, 1006, 1011, 1018, 1026, 1027, 1028, 1029, 1031, 1033, 1035, 1036, 1037, 1038, 1039,
    1042, 1043, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1082, 1083,
    // Potions et consommables
    2003, 2010, 2031, 2033, 2055, 2138, 2139, 2140,
    // Wards
    3340, 3363, 3364, 2050, 2052,
    // Jungle items de base
    1101, 1102, 1103,
    // Support items de base
    3850, 3851, 3853, 3854, 3855, 3857, 3858, 3859, 3860, 3862, 3863, 3864,
    // Autres composants
    2015, 2051, 2420, 2421, 2422, 2423, 3024, 3035, 3044, 3051, 3057, 3066, 3067, 3076,
    3077, 3082, 3086, 3091, 3093, 3094, 3095, 3096, 3097, 3098, 3099, 3100, 3101, 3102,
    3105, 3108, 3111, 3113, 3114, 3116, 3117, 3123, 3133, 3134, 3140, 3145, 3155, 3191,
    3211, 3801, 3802, 3803, 4630, 4632, 4633, 4635, 4636, 4637, 4638, 4641, 4642, 4643,
    6029, 6035, 6660, 6670, 6671, 6672, 6673, 6675, 6676, 6677
];

// Items legendaires/mythiques (tier S - les plus importants)
const LEGENDARY_ITEMS = [
    // AD Items
    3031, 3033, 3036, 3072, 3074, 3078, 3139, 3142, 3153, 3156, 3161, 3179, 3181,
    // AP Items
    3003, 3020, 3089, 3115, 3116, 3135, 3157, 3165, 3285, 3504, 3907,
    // Tank Items
    3001, 3068, 3075, 3083, 3084, 3109, 3110, 3119, 3143, 3190, 3193, 3742, 3748,
    // Support Items
    3011, 3107, 3222, 3382, 3383, 3384, 3385, 3386,
    // Boots finales
    3006, 3009, 3020, 3047, 3111, 3117, 3158
];

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

    // URL de l'embleme du tier (utilise les PNG officiels)
    getTierEmblem: (tier) => {
        if (tier === 'UNRANKED') return '';
        const tierLower = tier.toLowerCase();
        // Utiliser CDragon avec un chemin plus stable
        return `https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/${tierLower}.png`;
    }
};
