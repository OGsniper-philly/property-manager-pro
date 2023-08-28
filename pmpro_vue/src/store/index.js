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
    setAuthTokens(state, tokens) {
      state.authTokens = tokens,
      state.isAuthenticated = true,
      localStorage.setItem('authTokens', JSON.stringify(state.authTokens))
      axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ' + state.authTokens.access
    },
    removeAuthTokens(state) {
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
    },
    updateUser(state, context) {
      state.user.first_name = context.first
      state.user.last_name = context.last
      state.user.username = context.username
      state.user.email = context.email
      localStorage.setItem('user', JSON.stringify(state.user))
    }
  },
  actions: {
    // Authentication NOT required - interceptor will fail
    loginUser(state, credentials) {
      return axiosInstance
        .post('auth/token/', credentials)
        .then(response => {
          console.log(`Login: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          this.commit('setAuthTokens', response.data)
          this.commit('setUser', response.data.access)
          router.push('/dashboard')
          toastMixin.fire({ title: 'Logged in Successfully' })
          return { 'success': true }
        })
        .catch(error => {
          console.error(`Login: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 401) { 
            return { 'success': false, 'error': 'Username or password incorrect.' } 
          }
          return { 'success': false, 'error': 'Something went wrong, please try again later.' }
        })
    },
    logoutUser(state) {
      const context = { refresh: this.getters.getRefresh }
      this.commit('removeAuthTokens')
      this.commit('removeUser')
      router.push('/')
      toastMixin.fire({ title: 'Logged out Successfully' })
      return axiosInstance
        .post('auth/token/blacklist/', context)
        .then(response => {
          console.log(`Logout: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return response.status
        })
        .catch(error => {
          console.error(`Logout: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 401) { 
            console.error('User authorization already timed out.') 
          }
          return error.response.status
        })
    },
    signupUser(state, context) {
      return axiosInstance
        .post('auth/create-user/', context)
        .then(response => {
          console.log(`Signup: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            const credentials = {
                username: context.username,
                password: context.password
            }
            this.dispatch('login', credentials)
          }
          return response.data
        })
        .catch(error => {
          console.error(`Signup: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something went wrong, please try again later.']}
        })
    },
    // Authentication required - interceptor called, refresh token validity checked
    updateUser(state, context) {
      return axiosInstance
        .post('auth/update-user/', context)
        .then(response => {
          console.log(`Update User: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            this.commit('updateUser', context)
            toastMixin.fire({ title: 'Profile updated successfully.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': true } }
          console.error(`Update User: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something went wrong, please try again later.']}
        })
    },
    deleteUser(state, context) {
      return axiosInstance
        .post('auth/delete-user/', context)
        .then(response => {
          console.log(`Delete User: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            this.dispatch('logoutUser')
            toastMixin.fire({ title: 'Profile deleted successfully.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': true } }
          console.error(`Delete User: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something went wrong, please try again later.' }
        })
    },
    requestResetEmail(state, context) {
      return axiosInstance
        .post('auth/password-reset/', context)
        .then(response => {
          console.log(`Password Reset Request: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          toastMixin.fire({ title: 'Password reset email sent.' })
          return response.status
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': true } }
          console.error(`Password Reset Request: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return error.response.status
        })
    },
    resetPassword(state, context) {
      return axiosInstance
        .post('auth/password-reset/confirm/', context)
        .then(response => {
          console.log(`Password Reset: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          toastMixin.fire({ title: 'Password reset successful.' })
          router.push('/account')
          return { 'success': true }
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': true } }
          console.error(`Password Reset: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 404) {
            // Reset token has already been used
            return { 'success': false, 'errors': ['Password has already been reset. This page has expired.'] }
          } 
          return { 'success': false, 'errors': (JSON.parse(error.response.request.response)).password }
        })
    }
  },
  modules: {
  }
})
