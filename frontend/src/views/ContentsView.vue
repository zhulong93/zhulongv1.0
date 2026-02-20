<template>
  <div class="contents-view">
    <h2>今日推送</h2>
    <p class="subtitle">根据您的兴趣与底层逻辑精选</p>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="content-list">
      <article
        v-for="item in items"
        :key="item.id"
        class="content-card"
      >
        <a :href="item.url" target="_blank" rel="noopener" class="title">
          {{ item.title }}
        </a>
        <p class="source">{{ item.source }}</p>
        <p v-if="item.summary" class="summary">{{ item.summary }}</p>
        <div class="feedback">
          <span>有用吗？</span>
          <button
            v-for="s in 6"
            :key="s"
            class="score-btn"
            :class="{ active: feedbacks[item.id] === s - 1 }"
            @click="submitScore(item.id, s - 1)"
          >
            {{ s - 1 }}
          </button>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getContents, submitFeedback } from '../api'

const items = ref([])
const loading = ref(true)
const error = ref('')
const feedbacks = ref({})

onMounted(async () => {
  try {
    const res = await getContents()
    items.value = res.data
  } catch (e) {
    error.value = e.message || '加载失败'
  } finally {
    loading.value = false
  }
})

async function submitScore(id, score) {
  if (feedbacks.value[id] !== undefined) return
  try {
    await submitFeedback(id, score)
    feedbacks.value[id] = score
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
.contents-view h2 {
  font-size: 1.25rem;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: var(--text-dim);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.loading, .error {
  padding: 2rem;
  text-align: center;
  color: var(--text-dim);
}

.content-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.content-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.content-card .title {
  font-weight: 600;
  color: var(--text);
  display: block;
  margin-bottom: 0.5rem;
}

.content-card .source {
  font-size: 0.8rem;
  color: var(--text-dim);
  margin-bottom: 0.5rem;
}

.content-card .summary {
  font-size: 0.9rem;
  color: var(--text-dim);
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.feedback {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}

.score-btn {
  padding: 0.2rem 0.5rem;
  background: var(--bg-elevated);
  color: var(--text-dim);
  font-size: 0.85rem;
}

.score-btn.active {
  background: var(--accent);
  color: white;
}

.score-btn:hover:not(.active) {
  background: var(--border);
}
</style>
