<template>
  <div class="messages-view">
    <h2>消息过滤</h2>
    <p class="subtitle">三档：紧急 · 一般 · 常规</p>
    <div class="filters">
      <button
        :class="{ active: filter === null }"
        @click="filter = null"
      >
        全部
      </button>
      <button
        :class="{ active: filter === 'urgent' }"
        @click="filter = 'urgent'"
      >
        紧急
      </button>
      <button
        :class="{ active: filter === 'normal' }"
        @click="filter = 'normal'"
      >
        一般
      </button>
      <button
        :class="{ active: filter === 'routine' }"
        @click="filter = 'routine'"
      >
        常规
      </button>
    </div>
    <div class="add-form">
      <input v-model="newSender" placeholder="发送者" />
      <input v-model="newContent" placeholder="消息内容" />
      <button @click="addMessage">导入</button>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="message-list">
      <div
        v-for="msg in items"
        :key="msg.id"
        class="message-card"
        :class="[msg.priority, { unread: !msg.is_read }]"
      >
        <div class="msg-header">
          <span class="sender">{{ msg.sender }}</span>
          <span class="priority-badge">{{ priorityLabel(msg.priority) }}</span>
        </div>
        <p class="msg-content">{{ msg.content }}</p>
        <button
          v-if="!msg.is_read"
          class="read-btn"
          @click="markRead(msg.id)"
        >
          已读
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { getWeChatMessages, addWeChatMessage, markMessageRead } from '../api'

const items = ref([])
const loading = ref(true)
const filter = ref(null)
const newSender = ref('')
const newContent = ref('')

async function load() {
  loading.value = true
  try {
    const res = await getWeChatMessages(filter.value, false)
    items.value = res.data
  } finally {
    loading.value = false
  }
}

watch(filter, load)
onMounted(load)

function priorityLabel(p) {
  const map = { urgent: '紧急', normal: '一般', routine: '常规' }
  return map[p] || p
}

async function addMessage() {
  const sender = newSender.value.trim()
  const content = newContent.value.trim()
  if (!sender || !content) return
  try {
    await addWeChatMessage({ sender, content })
    newSender.value = ''
    newContent.value = ''
    load()
  } catch (e) {
    console.error(e)
  }
}

async function markRead(id) {
  try {
    await markMessageRead(id)
    load()
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
.messages-view h2 {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.filters button {
  padding: 0.4rem 0.8rem;
  background: var(--bg-card);
  color: var(--text-dim);
  border: 1px solid var(--border);
}

.filters button.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.add-form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.add-form input {
  flex: 1;
  padding: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text);
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.message-card.urgent {
  border-left: 4px solid #e94560;
}

.message-card.normal {
  border-left: 4px solid #ffd700;
}

.message-card.routine {
  border-left: 4px solid var(--border);
}

.msg-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.sender {
  font-weight: 600;
}

.priority-badge {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  background: var(--bg-elevated);
  border-radius: 4px;
}

.msg-content {
  font-size: 0.95rem;
  color: var(--text-dim);
}

.read-btn {
  margin-top: 0.5rem;
  padding: 0.3rem 0.6rem;
  background: var(--accent);
  color: white;
  font-size: 0.85rem;
}
</style>
