import { createRouter, createWebHistory } from 'vue-router';

// 路由懒加载
const Login = () => import('../views/LoginPage.vue');
const Register = () => import('../views/RegisterPage.vue');
const Index = () => import('../views/IndexPage.vue');
const Home = () => import('../views/HomePage.vue');
const Demo = () => import('../views/Demo.vue');
const ProfitAnalysis = () => import('../components/ProfitAnalysis.vue');

export const routes = [
  {
    path: '/',
    redirect: '/login', // 默认重定向到登录页
  },
  {
    name: 'login',
    path: '/login',
    component: Login,
  },
  {
    name: 'register',
    path: '/register',
    component: Register,
  },
  {
    name: 'index',
    path: '/index',
    component: Index,
  },
  {
    name: 'demo',
    path: '/demo',
    component: Demo,
  },
  {
    name: 'home',
    path: '/home',
    component: Home,
    children: [
      {
        path: 'profit-analysis', // 子路由使用相对路径
        name: 'ProfitAnalysis',
        component: ProfitAnalysis,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 历史模式
  routes,
  scrollBehavior() {
    return { left: 0, top: 0 }; // 每次路由切换时滚动到页面顶部
  },
});

// 全局路由守卫
// router.beforeEach((to, from, next) => {
//   // 示例：检查用户是否登录
//   const isAuthenticated = localStorage.getItem('token'); // 假设 token 存储在 localStorage
//   if (to.name !== 'login' && !isAuthenticated) {
//     // 如果用户未登录且目标路由不是登录页，则重定向到登录页
//     next({ name: 'login' });
//   } else {
//     next(); // 否则允许导航
//   }
// });

export default router;