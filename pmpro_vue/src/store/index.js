import { createStore } from 'vuex'
import router from '@/router'
import jwtDecode from 'jwt-decode'
import HttpStatus from 'http-status-codes'
import toastMixin from '@/services/alerts'
import axios from 'axios'
import axiosInstance from '@/services/api'


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
    getAuthStatus(state) {
      return state.isAuthenticated
    },
    getUser(state) {
      return state.user
    },
    getLandlordStatus(state) {
      console.assert(state.isAuthenticated)
      return state.user.is_landlord
    },
    getRefresh(state) {
      console.assert(state.isAuthenticated)
      return state.authTokens.refresh
    },
    getUserExpiry(state) {
      console.assert(state.isAuthenticated)
      return state.user.exp
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
        this.commit('removeUserObject')
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
    setUserObject(state, access) {
      state.user = jwtDecode(access)
      localStorage.setItem('user', JSON.stringify(state.user))
    },
    removeUserObject(state) {
      state.user = {}
      localStorage.removeItem('user')
    },
    updateUserObject(state, context) {
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
      return axios
        .post('auth/token/', credentials)
        .then(response => {
          console.log(`Login: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          this.commit('setAuthTokens', response.data)
          this.commit('setUserObject', response.data.access)
          router.push('/dashboard')
          toastMixin.fire({ title: 'Logged in Successfully' })
          return { 'success': true }
        })
        .catch(error => {
          console.error(`Login: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 401) { 
            return { 'success': false, 'error': 'Username or password incorrect.' } 
          }
          return { 'success': false, 'error': 'Something during login went wrong, please try again later.' }
        })
    },
    logoutUser(state) {
      const context = { refresh: this.getters.getRefresh }
      this.commit('removeAuthTokens')
      this.commit('removeUserObject')
      router.push('/')
      toastMixin.fire({ title: 'Logged out Successfully' })
      return axios
        .post('auth/token/blacklist/', context)
        .then(response => {
          console.log(`Logout: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return { 'success': true }
        })
        .catch(error => {
          console.error(`Logout: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 401) { 
            console.error('User authorization already timed out.')
            return { 'success': true }
          }
          return { 'success': false, 'error': 'Something during logout went wrong, please try again later.' }
        })
    },
    signupUser(state, context) {
      return axios
        .post('auth/create-user/', context)
        .then(response => {
          console.log(`Signup: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            const credentials = {
                username: context.username,
                password: context.password
            }
            this.dispatch('loginUser', credentials)
          }
          return response.data
        })
        .catch(error => {
          console.error(`Signup: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during signup went wrong, please try again later.']}
        })
    },
    resetPassword(state, context) {
      return axios
        .post('auth/password-reset/confirm/', context)
        .then(response => {
          console.log(`Password Reset: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          toastMixin.fire({ title: 'Password reset successful.' })
          router.push('/account')
          return { 'success': true }
        })
        .catch(error => {
          console.error(`Password Reset: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          if (error.response.status == 404) {
            // Reset token has already been used
            return { 'success': false, 'errors': ['Password has already been reset. This page has expired.'] }
          } 
          return { 'success': false, 'errors': (JSON.parse(error.response.request.response)).password }
        })
    },
    // Authentication required - interceptor called, refresh token validity checked
    updateUser(state, context) {
      return axiosInstance
        .post('auth/update-user/', context)
        .then(response => {
          console.log(`Update User: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            this.commit('updateUserObject', context)
            toastMixin.fire({ title: 'Profile updated successfully.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Update User: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during user update went wrong, please try again later.']}
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
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Delete User: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something during user delete went wrong, please try again later.' }
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
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Password Reset Request: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return error.response.status
        })
    },
    createProperty(state, context) {
      return axiosInstance
        .post('base/create-property/', context)
        .then(response => {
          console.log(`Create Property: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: `${context['address']} property created successfully.` })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Create Property: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during property creation went wrong, please try again later.']}
        })
    },
    sendPropertyInvite(state, context) {
      return axiosInstance
        .post('connect/create-invitation/', context)
        .then(response => {
          console.log(`Create Invitation: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: `${context['property_address']} to @${context['tenant_username']} invite sent.`, timer:3000 })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Create Invitation: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during property invite went wrong, please try again later.']}
        })
    },
    getProperties(state) {
      return axiosInstance
        .get('base/get-properties/')
        .then(response => {
          console.log(`Get Properties: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return { 'success': true, 'data': response.data }
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Get Properties: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during property fetch went wrong, please try again later.']}
        })
    },
    getTenants(state, context) {
      return axiosInstance
        .post('base/get-tenants/', context)
        .then(response => {
          console.log(`Get Tenants: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return { 'success': true, 'data': response.data }
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Get Tenants: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during tenant fetch went wrong, please try again later.']}
        })
    },
    getInvitations(state) {
      return axiosInstance
        .get('connect/get-invitations/')
        .then(response => {
          console.log(`Get Invitations: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          return { 'success': true, 'data': response.data }
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Get Invitations: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during invitation fetch went wrong, please try again later.']}
        })
    },
    acceptInvitation(state, context) {
      return axiosInstance
        .post('connect/accept-invitation/', context)
        .then(response => {
          console.log(`Accept Invitation: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: `Accepted invite to ${context.address}.`, timer:3000 })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Accept Invitation: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'errors': ['Something during invitation accept went wrong, please try again later.']}
        })
    },
    leaveProperty(state, context) {
      return axiosInstance
        .post('base/leave-property/', context)
        .then(response => {
          console.log(`Leave Property: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: 'Property left successfully.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Leave Property: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something during property leave went wrong, please try again later.' }
        })
    },
    deleteInvitation(state, context) {
      return axiosInstance
        .post('connect/delete-invitation/', context)
        .then(response => {
          console.log(`Delete Invitation: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: 'Invitation deleted.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Delete Invitation: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something during invitation delete went wrong, please try again later.' }
        })
    },
    removeTenant(state, context) {
      return axiosInstance
        .post('base/remove-tenant/', context)
        .then(response => {
          console.log(`Remove Tenant: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: `${context.username} removed.` })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Remove Tenant: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something during tenant removal went wrong, please try again later.' }
        })
    },
    deleteProperty(state, context) {
      return axiosInstance
        .post('base/delete-property/', context)
        .then(response => {
          console.log(`Delete Property: ${response.status} - ${HttpStatus.getStatusText(response.status)}`)
          if (response.data.success) {
            toastMixin.fire({ title: 'Property deleted.' })
          }
          return response.data
        })
        .catch(error => {
          if (error.code == "ERR_CANCELED") { return { 'success': false, 'errors': [] } }
          console.error(`Delete Property: ${error.response.status} - ${HttpStatus.getStatusText(error.response.status)}`)
          return { 'success': false, 'error': 'Something during property delete went wrong, please try again later.' }
        })
    }
  },
  modules: {
  }
})
