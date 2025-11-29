import { createRouter, createWebHistory } from 'vue-router'


import LoginView from '../views/LoginView.vue'
import DashboardView from '../views/DashboardView.vue'
import MenuListView from '../views/MenuListView.vue'
import MenuFormView from '../views/MenuFormView.vue'
import OrderListView from '../views/OrderListView.vue'
import OrderFormView from '../views/OrderFormView.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/menu',
    name: 'MenuList',
    component: MenuListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/menu/tambah',
    name: 'MenuAdd',
    component: MenuFormView,
    meta: { requiresAuth: true },
    alias: '/menu/create'
  },
  {
    path: '/menu/edit/:id',
    name: 'MenuEdit',
    component: MenuFormView,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'OrderList',
    component: OrderListView,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders/create',
    name: 'OrderCreate',
    component: OrderFormView,
    meta: { requiresAuth: true}
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  
  if (to.meta.requiresAuth && !isLoggedIn) {

    next({ name: 'Login' })
  } else if (to.name === 'Login' && isLoggedIn) {

    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router