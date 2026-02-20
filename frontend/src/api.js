import axios from 'axios'

// 开发时走 Vite proxy (/api)，生产时可用 VITE_API_BASE 指向 Railway
const baseURL = import.meta.env.VITE_API_BASE
  ? `${import.meta.env.VITE_API_BASE.replace(/\/$/, '')}/api`
  : '/api'

const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
})

// 用户
export const getUserProfile = () => api.get('/user/profile')

// 信息提炼
export const getContents = () => api.get('/contents')
export const submitFeedback = (contentId, score, comment) =>
  api.post(`/contents/${contentId}/feedback`, { content_id: contentId, score, comment })

// 备忘录
export const getMemos = (includeCompleted = false) =>
  api.get('/memos', { params: { include_completed: includeCompleted } })
export const getReminders = () => api.get('/memos/reminders')
export const addMemo = (data) => api.post('/memos', data)
export const completeMemo = (id) => api.post(`/memos/${id}/complete`)
export const deleteMemo = (id) => api.delete(`/memos/${id}`)

// 微信消息
export const getWeChatMessages = (priority, unreadOnly) =>
  api.get('/wechat/messages', { params: { priority, unread_only: unreadOnly } })
export const addWeChatMessage = (data) => api.post('/wechat/messages', data)
export const markMessageRead = (id) => api.post(`/wechat/messages/${id}/read`)

// 自然语言输入
export const handleInput = (text, inputType = 'text') =>
  api.post('/input', { text, input_type: inputType })

export default api
