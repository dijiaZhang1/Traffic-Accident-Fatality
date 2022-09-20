import axios, { AxiosInstance } from "axios";
const apiClient: AxiosInstance = axios.create({
    baseURL: "http://localhost:12345",
    headers: {
        "Content-type": "application/json",
    },
});
export default apiClient;