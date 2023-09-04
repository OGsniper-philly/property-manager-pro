import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

import HomeView from '../views/Home.vue'
import LoginView from '../views/Login.vue'
import SignUpView from '../views/SignUp.vue'
import DashboardView from '../views/Dashboard.vue'
import AccountView from '../views/Account.vue'
import ResetPasswordView from '../views/ResetPassword.vue'
import ConnectView from '../views/ConnectView.vue'
import LL_ManageProperties from '../views/Landlord/LL_ManageProperties.vue'
import LL_Connect from '../views/Landlord/LL_Connect.vue'
import TN_Connect from '../views/Tenant/TN_Connect.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/account/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/account',
    name: 'account',
    component: AccountView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/connect',
    name: 'connect',
    component: ConnectView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/landlord/manage-properties',
    name: 'LandlordManageProperties',
    component: LL_ManageProperties,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/landlord/connect',
    name: 'LandlordConnect',
    component: LL_Connect,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/tenant/connect',
    name: 'TenantConnect',
    component: TN_Connect,
    meta: {
      requireLogin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.getters.getAuthStatus) {
    next({ name: 'login'});
  } else if ((to.name =='login' || to.name == 'signup') && store.getters.getAuthStatus) {
    next({ name: 'account'});
  } else {
    next()
  }
})

export default router
