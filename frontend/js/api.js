// Module API - Gestion des appels HTTP
const API = {
    async get(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Players
    async getPlayers() {
        return this.get(API_ENDPOINTS.players);
    },

    async getPlayerById(id) {
        return this.get(API_ENDPOINTS.playerById(id));
    },

    async getPlayerChampions(id) {
        return this.get(API_ENDPOINTS.playerChampions(id));
    },

    async getPlayerRoles(id) {
        return this.get(API_ENDPOINTS.playerRoles(id));
    },

    // Ranking
    async getRanking() {
        return this.get(API_ENDPOINTS.ranking);
    },

    async getRankedRanking() {
        return this.get(API_ENDPOINTS.rankedRanking);
    },

    // DuoQ
    async getDuoQ() {
        return this.get(API_ENDPOINTS.duoq);
    },

    // Stats
    async getGlobalStats() {
        return this.get(API_ENDPOINTS.globalStats);
    },

    async getRecentMatches(limit = 20) {
        return this.get(`${API_ENDPOINTS.recentMatches}?limit=${limit}`);
    },

    // Items
    async getPopularItems(limit = 20) {
        return this.get(`${API_ENDPOINTS.popularItems}?limit=${limit}`);
    },

    async getPlayerItems(id, limit = 20) {
        return this.get(`${API_ENDPOINTS.playerItems(id)}?limit=${limit}`);
    },

    async getPlayerChampionItems(playerId, championId) {
        return this.get(API_ENDPOINTS.playerChampionItems(playerId, championId));
    },

    async getPlayerBuilds(id) {
        return this.get(API_ENDPOINTS.playerBuilds(id));
    }
};
