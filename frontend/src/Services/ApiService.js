class ApiService {
    constructor(httpClient) {
        this.httpClient = httpClient
    }

    async getCategories() {
        try {
            const response = await this.httpClient.get('http://127.0.0.1:8000/api/v1/categories');
            const data = await response.json();
            console.log(data)
            return data;
        } catch (error) {
            console.log(error)
            throw error
        }
    }

    async getEvents(url) {
        try {
            const response = await this.httpClient.get(url);
            const data = await response.json();
            console.log(data)
            return data;
        } catch (error) {
            console.log(error)
            throw error
        }
    }
}

export default ApiService;