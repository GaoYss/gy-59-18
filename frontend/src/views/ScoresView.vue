<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ChevronDown, ChevronRight, Search } from 'lucide-vue-next'

import { scoreApi } from '../api/modules'
import EmptyState from '../components/EmptyState.vue'
import MessageBar from '../components/MessageBar.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { subjects } from '../constants/options'

const scores = ref([])
const loading = ref(false)
const message = reactive({ text: '', type: 'info' })
const filters = reactive({ studentName: '', subject: '' })
const expandedRow = ref(null)

function optionLabel(index) {
  return ['A', 'B', 'C', 'D'][index]
}

function toggleRow(id) {
  expandedRow.value = expandedRow.value === id ? null : id
}

async function loadScores() {
  loading.value = true
  message.text = ''
  try {
    const params = {}
    if (filters.studentName) params.studentName = filters.studentName
    if (filters.subject) params.subject = filters.subject
    scores.value = await scoreApi.list(params)
  } catch (error) {
    message.text = error.message
    message.type = 'error'
  } finally {
    loading.value = false
  }
}

onMounted(loadScores)
</script>

<template>
  <section class="panel">
    <div class="panel-heading">
      <div>
        <h3>成绩查询</h3>
        <p>按学员或科目筛选模拟考试记录。</p>
      </div>
    </div>

    <form class="toolbar" @submit.prevent="loadScores">
      <label>
        <span>学员姓名</span>
        <input v-model.trim="filters.studentName" placeholder="输入姓名检索" />
      </label>
      <label>
        <span>科目</span>
        <select v-model="filters.subject">
          <option value="">全部科目</option>
          <option v-for="subject in subjects" :key="subject">{{ subject }}</option>
        </select>
      </label>
      <button class="primary-button inline-button" type="submit">
        <Search :size="18" />
        <span>查询</span>
      </button>
    </form>

    <MessageBar :message="message.text" :type="message.type" />

    <EmptyState v-if="!loading && scores.length === 0" title="暂无成绩" description="模拟考试提交后会生成成绩。" />

    <div v-else class="table-wrap">
      <table class="scores-table">
        <thead>
          <tr>
            <th></th>
            <th>学员</th>
            <th>科目</th>
            <th>分数</th>
            <th>答对</th>
            <th>结果</th>
            <th>提交时间</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="row in scores" :key="row.id">
            <tr :class="{ 'row-expanded': expandedRow === row.id }">
              <td>
                <button
                  v-if="row.details && row.details.length"
                  class="icon-button expand-btn"
                  @click="toggleRow(row.id)"
                  type="button"
                >
                  <component :is="expandedRow === row.id ? ChevronDown : ChevronRight" :size="16" />
                </button>
              </td>
              <td>{{ row.studentName }}</td>
              <td>{{ row.subject }}</td>
              <td>{{ row.score }}</td>
              <td>{{ row.correctCount }} / {{ row.totalQuestions }}</td>
              <td><StatusBadge :status="row.passed ? '合格' : '不合格'" /></td>
              <td>{{ row.submittedAt }}</td>
            </tr>
            <tr v-if="expandedRow === row.id && row.details && row.details.length" class="detail-row">
              <td colspan="7">
                <div class="detail-list">
                  <div
                    v-for="(item, index) in row.details"
                    :key="item.questionId"
                    class="detail-item"
                  >
                    <div class="detail-header">
                      <span class="detail-title">{{ index + 1 }}. {{ item.question }}</span>
                      <span :class="['detail-status', item.correct ? 'correct' : 'wrong']">
                        {{ item.correct ? '正确' : '错误' }}
                      </span>
                    </div>
                    <div class="detail-body">
                      <div
                        v-for="(opt, optIdx) in item.options"
                        :key="opt"
                        :class="[
                          'option-row',
                          optionLabel(optIdx) === item.answer && 'option-correct',
                          optionLabel(optIdx) === item.chosen && !item.correct && 'option-wrong'
                        ]"
                      >
                        <span class="option-mark">{{ optionLabel(optIdx) }}.</span>
                        <span class="option-text">{{ opt }}</span>
                        <span v-if="optionLabel(optIdx) === item.answer" class="option-tag tag-correct">正确答案</span>
                        <span v-else-if="optionLabel(optIdx) === item.chosen" class="option-tag tag-wrong">你的选择</span>
                      </div>
                      <p v-if="!item.chosen" class="detail-note">未作答</p>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </section>
</template>
