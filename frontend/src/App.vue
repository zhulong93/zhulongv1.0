<template>
  <div class="app">
    <header class="header">
      <h1 class="logo">烛龙</h1>
      <p class="tagline">AI数字分身</p>
      <nav class="nav">
        <router-link to="/" active-class="active">今日推送</router-link>
        <router-link to="/memos" active-class="active">备忘录</router-link>
        <router-link to="/messages" active-class="active">消息</router-link>
      </nav>
    </header>
    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <div class="input-bar">
      <input
        v-model="inputText"
        type="text"
        placeholder="输入文字或指令..."
        @keyup.enter="onSubmit"
      />
      <button class="send-btn" @click="onSubmit">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { handleInput } from './api'

const router = useRouter()
const inputText = ref('')

async function onSubmit() {
  const text = inputText.value.trim()
  if (!text) return
  try {
    const res = await handleInput(text)
    const intent = res.data?.intent
    if (intent === 'contents') router.push('/')
    else if (intent === 'memo') router.push('/memos')
    else if (intent === 'wechat') router.push('/messages')
  } catch (e) {
    console.error(e)
  }
  inputText.value = ''
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-bottom: 70px;
}

.header {
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 1rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.logo {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--gold);
  letter-spacing: 0.1em;
}

.tagline {
  font-size: 0.85rem;
  color: var(--text-dim);
  margin-top: 0.2rem;
}

.nav {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
}

.nav a {
  color: var(--text-dim);
  font-size: 0.95rem;
}

.nav a.active {
  color: var(--accent);
}

.main {
  flex: 1;
  padding: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 1.5rem;
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  display: flex;
  gap: 0.5rem;
}

.input-bar input {
  flex: 1;
  padding: 0.6rem 1rem;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  color: var(--text);
}

.input-bar input::placeholder {
  color: var(--text-dim);
}

.send-btn {
  padding: 0.6rem 1.2rem;
  background: var(--accent);
  color: white;
  font-weight: 500;
}

.send-btn:hover {
  background: var(--accent-dim);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
