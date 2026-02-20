import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/ContentsView.vue'), meta: { title: '今日推送' } },
  { path: '/memos', component: () => import('../views/MemosView.vue'), meta: { title: '备忘录' } },
  { path: '/messages', component: () => import('../views/MessagesView.vue'), meta: { title: '消息' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = to.meta?.title ? `${to.meta.title} - 烛龙` : '烛龙'
})

export default router
