import axios from 'axios'
import dayjs from 'dayjs';
import store from '@/store';


const baseURL = 'http://127.0.0.1:8000/api/v1/'

const axiosInstance = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    }
});

axiosInstance.interceptors.request.use(async req => {
    const isExpired = dayjs.unix(store.getters.getUser.exp).diff(dayjs()) < 1;
    if (isExpired) {
        const context = { refresh: store.getters.getRefresh }
        await axios
            .post(`${baseURL}/auth/token/refresh/`, context)
            .then(response => {
                console.log(`Tokens Refreshed: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
                store.commit('setAuthTokens', response.data)
                store.commit('setUser', response.data.access)
            })
            .catch(error => {
                console.error(`Tokens Refreshed: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
                if (error.response.status == 401) { console.error('Login required.') }
            })
    }
    return req
})

export default axiosInstance