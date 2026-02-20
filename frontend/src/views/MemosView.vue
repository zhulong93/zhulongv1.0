<template>
  <div class="memos-view">
    <h2>备忘录</h2>
    <div class="add-form">
      <input v-model="newTitle" placeholder="标题" />
      <input v-model="newContent" placeholder="内容（可选）" />
      <button class="add-btn" @click="add">添加</button>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else class="memo-list">
      <div
        v-for="memo in items"
        :key="memo.id"
        class="memo-card"
        :class="{ completed: memo.is_completed }"
      >
        <div class="memo-main">
          <h3 class="memo-title">{{ memo.title }}</h3>
          <p v-if="memo.content" class="memo-content">{{ memo.content }}</p>
          <p v-if="memo.reminder_at" class="reminder">
            ⏰ {{ formatDate(memo.reminder_at) }}
          </p>
        </div>
        <div class="memo-actions">
          <button
            v-if="!memo.is_completed"
            class="complete-btn"
            @click="complete(memo.id)"
          >
            完成
          </button>
          <button class="del-btn" @click="del(memo.id)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMemos, addMemo, completeMemo, deleteMemo } from '../api'

const items = ref([])
const loading = ref(true)
const newTitle = ref('')
const newContent = ref('')

async function load() {
  loading.value = true
  try {
    const res = await getMemos(false)
    items.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(load)

function formatDate(d) {
  if (!d) return ''
  const date = new Date(d)
  return date.toLocaleString('zh-CN')
}

async function add() {
  const title = newTitle.value.trim()
  if (!title) return
  try {
    await addMemo({ title, content: newContent.value.trim() })
    newTitle.value = ''
    newContent.value = ''
    load()
  } catch (e) {
    console.error(e)
  }
}

async function complete(id) {
  try {
    await completeMemo(id)
    load()
  } catch (e) {
    console.error(e)
  }
}

async function del(id) {
  if (!confirm('确定删除？')) return
  try {
    await deleteMemo(id)
    load()
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
.memos-view h2 {
  font-size: 1.25rem;
  margin-bottom: 1rem;
}

.add-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.add-form input {
  padding: 0.6rem 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text);
}

.add-btn {
  padding: 0.6rem;
  background: var(--accent);
  color: white;
}

.memo-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.memo-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.memo-card.completed {
  opacity: 0.6;
}

.memo-title {
  font-size: 1rem;
  font-weight: 600;
}

.memo-content {
  font-size: 0.9rem;
  color: var(--text-dim);
  margin-top: 0.25rem;
}

.reminder {
  font-size: 0.8rem;
  color: var(--gold);
  margin-top: 0.25rem;
}

.memo-actions {
  display: flex;
  gap: 0.5rem;
}

.complete-btn {
  padding: 0.3rem 0.6rem;
  background: #2e7d32;
  color: white;
  font-size: 0.85rem;
}

.del-btn {
  padding: 0.3rem 0.6rem;
  background: var(--bg-elevated);
  color: var(--text-dim);
  font-size: 0.85rem;
}
</style>
