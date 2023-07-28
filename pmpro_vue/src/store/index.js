import { createStore } from 'vuex'
import router from '@/router'
import axiosInstance from '@/services/api'
import jwtDecode from 'jwt-decode'
import HttpStatus from 'http-status-codes'
import toastMixin from '@/services/alerts'


export default createStore({
  state: {
    isAuthenticated: false,
    authTokens: {
      access: '',
      refresh: ''
    },
    user: {},
  },
  getters: {
    getRefresh(state) {
      return state.authTokens.refresh
    },
    getAuthStatus(state) {
      return state.isAuthenticated
    },
    getUser(state) {
      return state.user
    }
  },
  mutations: {
    onInit(state) {
      if (localStorage.getItem('authTokens') && localStorage.getItem('user')) {
        state.authTokens = JSON.parse(localStorage.getItem('authTokens'))
        state.user = JSON.parse(localStorage.getItem('user'))
        state.isAuthenticated = true
        axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ' + state.authTokens.access
      } else {
        this.commit('removeAuthTokens')
        this.commit('removeUser')
        axiosInstance.defaults.headers.common['Authorization'] = ''
      }
    },
    setAuthTokens(state, tokens, req=null) {
      state.authTokens = tokens,
      state.isAuthenticated = true,
      localStorage.setItem('authTokens', JSON.stringify(state.authTokens))
      axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ' + state.authTokens.access
    },
    removeAuthTokens(state, req=null) {
      state.authTokens = { access: '', refresh: '' }
      state.isAuthenticated = false
      localStorage.removeItem('authTokens')
      axiosInstance.defaults.headers.common['Authorization'] = ''
    },
    setUser(state, access) {
      state.user = jwtDecode(access)
      localStorage.setItem('user', JSON.stringify(state.user))
    },
    removeUser(state) {
      state.user = {}
      localStorage.removeItem('user')
    }
  },
  actions: {
    login(state, credentials) {
      return axiosInstance
        .post('auth/token/', credentials)
        .then(response => {
          console.log(`Login: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          this.commit('setAuthTokens', response.data)
          this.commit('setUser', response.data.access)
          router.push('/dashboard')
          toastMixin.fire({ title: 'Signed in Successfully' })
          return response.status
        })
        .catch(error => {
          console.error(`Login: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return error.response.status
        })
    },
    logout(state) {
      const context = { refresh: this.getters.getRefresh }
      this.commit('removeAuthTokens')
      this.commit('removeUser')
      router.push('/')
      toastMixin.fire({ title: 'Signed out Successfully' })
      return axiosInstance
        .post('auth/token/blacklist/', context)
        .then(response => {
          console.log(`Logout: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return response.status
        })
        .catch(error => {
          console.error(`Logout: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 401) { console.error('User authorization already timed out.') }
          return error.response.status
        })
    }
  },
  modules: {
  }
})
