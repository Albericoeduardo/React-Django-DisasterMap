const FetchClient = {
    async get(url) {
        return await fetch(url);
    }
}

export default FetchClient;