import axios from 'axios'
import dayjs from 'dayjs';
import store from '@/store';
import HttpStatus from 'http-status-codes'
import router from '@/router';
import toastMixin from '@/services/alerts'


const baseURL = 'http://127.0.0.1:8000/api/v1/'

axios.defaults.baseURL = baseURL

const axiosInstance = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    }
});

axiosInstance.interceptors.request.use(async req => {
    const controller = new AbortController();
    
    const isExpired = dayjs.unix(store.getters.getUserExpiry).diff(dayjs()) < 1;
    if (isExpired) {
        const context = { refresh: store.getters.getRefresh }
        await axios
            .post('auth/token/refresh/', context)
            .then(response => {
                console.log(`Tokens Refreshed: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
                store.commit('setAuthTokens', response.data)
                store.commit('setUserObject', response.data.access)
                req.headers.Authorization = 'Bearer ' + response.data.access
            })
            .catch(error => {
                console.error(`Tokens Refreshed: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
                if (error.response.status == 401) { 
                    console.error('User authorization timed out. Login required.') 
                    store.commit('removeAuthTokens')
                    store.commit('removeUserObject')
                    req.headers.Authorization = ''
                    router.push('/login')
                    toastMixin.fire({ icon: 'warning', title: 'Authorization timed out. Please login again.', timer: 5000 })   
                }
                controller.abort()
            })
    }
    return {
        ...req,
        signal: controller.signal
    }
    
})

export default axiosInstance