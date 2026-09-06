class CacheService {
  constructor() {
    this.store = {};
  }

  set(key, data) {
    this.store[key] = data;
  }

  get(key) {
    return this.store[key];
  }
}

// Instância única, encapsulada e injetável — substitui o `globalCache` mutável
// que antes vivia solto no escopo do módulo utils.js.
const cache = new CacheService();

function logAndCache(key, data) {
  cache.set(key, data);
}

module.exports = { CacheService, cache, logAndCache };
