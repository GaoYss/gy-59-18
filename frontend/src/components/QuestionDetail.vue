<script setup>
import { ref } from 'vue'
import { ChevronDown, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  },
  collapsible: {
    type: Boolean,
    default: true
  }
})

const expanded = ref(!props.collapsible)

function toggle() {
  if (props.collapsible) {
    expanded.value = !expanded.value
  }
}

function optionLabel(index) {
  return ['A', 'B', 'C', 'D'][index]
}
</script>

<template>
  <div class="detail-item">
    <button
      v-if="collapsible"
      class="detail-toggle"
      type="button"
      @click="toggle"
    >
      <component :is="expanded ? ChevronDown : ChevronRight" :size="16" />
      <span>{{ index + 1 }}. {{ item.question }}</span>
      <span :class="['detail-status', item.correct ? 'correct' : 'wrong']">
        {{ item.correct ? '正确' : '错误' }}
      </span>
    </button>
    <div v-else class="detail-header">
      <span class="detail-title">{{ index + 1 }}. {{ item.question }}</span>
      <span :class="['detail-status', item.correct ? 'correct' : 'wrong']">
        {{ item.correct ? '正确' : '错误' }}
      </span>
    </div>

    <div v-if="!collapsible || expanded" class="detail-body">
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
        <span v-if="optionLabel(optIdx) === item.chosen" :class="['option-tag', item.correct ? 'tag-correct' : 'tag-wrong']">你的选择</span>
        <span v-if="optionLabel(optIdx) === item.answer && optionLabel(optIdx) !== item.chosen" class="option-tag tag-correct">正确答案</span>
      </div>
      <p v-if="!item.chosen" class="detail-note">未作答</p>
    </div>
  </div>
</template>
