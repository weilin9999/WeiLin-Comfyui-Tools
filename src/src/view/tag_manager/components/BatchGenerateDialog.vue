<template>
  <div v-if="visible" class="weilin-tools-dialog-overlay" @mousedown.self="onCancel">
    <div class="weilin-tools-dialog-content batch-generate-dialog" @mousedown.stop>
      <div class="weilin-tools-dialog-header">
        <h2>一键生成预览图 —— {{ tagCount }} 个标签</h2>
        <button class="close-btn" @click="onCancel">×</button>
      </div>
      <div class="weilin-tools-dialog-body">
        <div class="form-group">
          <label>模型</label>
          <select v-model="form.checkpoint" class="form-select">
            <option v-for="cp in options.checkpoints" :key="cp.name" :value="cp.name">
              {{ cp.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>尺寸</label>
          <select v-model="form.sizeIndex" class="form-select">
            <option v-for="(s, i) in options.sizes" :key="i" :value="i">
              {{ s.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>采样器</label>
          <select v-model="form.sampler_name" class="form-select">
            <option v-for="s in options.samplers" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>调度器</label>
          <select v-model="form.scheduler" class="form-select">
            <option v-for="s in options.schedulers" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group form-group-half">
            <label>步数: {{ form.steps }}</label>
            <input type="range" v-model.number="form.steps" min="1" max="50" class="form-range" />
          </div>
          <div class="form-group form-group-half">
            <label>CFG: {{ form.cfg }}</label>
            <input type="range" v-model.number="form.cfg" min="1" max="20" step="0.5" class="form-range" />
          </div>
        </div>

        <div class="form-group">
          <label>种子 (-1 为随机)</label>
          <input type="number" v-model.number="form.seed" class="form-input" />
        </div>

        <!-- Progress bar (only shown during generation) -->
        <div v-if="generating" class="batch-progress-section">
          <div class="batch-progress-bar-wrap">
            <div class="batch-progress-bar" :style="{ width: progressPercent + '%' }"></div>
          </div>
          <div class="batch-progress-text">{{ completedCount }} / {{ totalCount }}</div>
        </div>
      </div>
      <div class="weilin-tools-dialog-footer">
        <button class="cancel-btn" @click="onCancel" :disabled="generating">取消</button>
        <button class="confirm-btn" @click="onStartGenerate" :disabled="generating">开始生成</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { tagsApi } from '@/api/tags'

const props = defineProps({
  visible: { type: Boolean, default: false },
  tags: { type: Array, default: () => [] },
  options: { type: Object, default: () => ({ checkpoints: [], samplers: [], sizes: [] }) }
})
const emit = defineEmits(['close', 'generated'])

const generating = ref(false)
const completedCount = ref(0)
const totalCount = ref(0)

const progressPercent = computed(() => {
  if (!totalCount.value) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})

const form = reactive({
  checkpoint: '',
  sizeIndex: 0,
  sampler_name: 'euler',
  scheduler: 'normal',
  steps: 20,
  cfg: 7.0,
  seed: -1
})

watch(() => props.visible, (v) => {
  if (v) {
    form.checkpoint = props.options.checkpoints?.[0]?.name || ''
    form.sampler_name = 'euler'
    form.scheduler = 'normal'
    form.steps = 20
    form.cfg = 7.0
    form.seed = -1
    form.sizeIndex = 0
    generating.value = false
    completedCount.value = 0
    totalCount.value = 0

    // Load saved params
    try {
      const saved = JSON.parse(localStorage.getItem('weilin_tools_gen_params') || '{}')
      if (saved.checkpoint && props.options.checkpoints.some(c => c.name === saved.checkpoint)) {
        form.checkpoint = saved.checkpoint
      }
      if (saved.sizeIndex !== undefined) form.sizeIndex = saved.sizeIndex
      if (saved.sampler_name) form.sampler_name = saved.sampler_name
      if (saved.scheduler) form.scheduler = saved.scheduler
      if (saved.steps !== undefined) form.steps = saved.steps
      if (saved.cfg !== undefined) form.cfg = saved.cfg
      if (saved.seed !== undefined) form.seed = saved.seed
    } catch (e) { /* ignore */ }
  }
})

const tagCount = computed(() => {
  if (!props.tags) return 0
  return props.tags.filter(t => !t.image_status || t.image_status === 'failed').length
})

function onCancel() {
  if (!generating.value) {
    emit('close')
  }
}

async function onStartGenerate() {
  const size = props.options.sizes[form.sizeIndex] || props.options.sizes[0]
  const tagsToGenerate = props.tags.filter(t => !t.image_status || t.image_status === 'failed')
  if (!tagsToGenerate.length) {
    alert('所有标签已有预览图')
    return
  }

  generating.value = true
  totalCount.value = tagsToGenerate.length
  completedCount.value = 0

  // Save params
  try {
    localStorage.setItem('weilin_tools_gen_params', JSON.stringify({
      checkpoint: form.checkpoint,
      sizeIndex: form.sizeIndex,
      sampler_name: form.sampler_name,
      scheduler: form.scheduler,
      steps: form.steps,
      cfg: form.cfg,
      seed: form.seed,
    }))
  } catch (e) { /* ignore */ }

  const params = {
    checkpoint: form.checkpoint,
    width: size.width,
    height: size.height,
    sampler_name: form.sampler_name,
    scheduler: form.scheduler,
    steps: form.steps,
    cfg: form.cfg,
    seed: form.seed,
    positive_template: '{text}, masterpiece, best quality',
    negative: 'worst quality, low quality'
  }

  try {
    const res = await tagsApi.batchGenerateTagImages(tagsToGenerate, params)
    const taskIds = res.data?.task_ids || []

    // Emit generated event for tracking
    emit('generated', { task_ids: taskIds })

    // Poll all tasks until complete
    const pending = new Map()
    for (const item of taskIds) {
      pending.set(item.task_id, item.t_uuid)
    }

    completedCount.value = taskIds.length - pending.size
    totalCount.value = taskIds.length

    // Poll every 2 seconds until all done
    while (pending.size > 0) {
      await new Promise(r => setTimeout(r, 2000))
      for (const [taskId, tUuid] of [...pending]) {
        try {
          const statusRes = await tagsApi.getTagImageStatus(taskId)
          const data = statusRes.data || statusRes
          if (data.status === 'ready' || data.status === 'failed') {
            pending.delete(taskId)
            completedCount.value = totalCount.value - pending.size
          }
        } catch (e) {
          // keep polling
        }
      }
    }
  } catch (err) {
    alert('批量生成失败: ' + (err.message || '未知错误'))
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.batch-generate-dialog {
  width: 480px;
  max-width: 90vw;
}
.form-row {
  display: flex;
  gap: 16px;
}
.form-group-half {
  flex: 1;
}
.form-select, .form-input {
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}
.form-range {
  width: 100%;
}
.confirm-btn:disabled, .cancel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.batch-progress-section {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--weilin-prompt-ui-border-color);
}
.batch-progress-bar-wrap {
  width: 100%;
  height: 12px;
  background: var(--weilin-prompt-ui-secondary-bg);
  border-radius: 6px;
  overflow: hidden;
}
.batch-progress-bar {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 6px;
  transition: width 0.3s ease;
}
.batch-progress-text {
  text-align: center;
  font-size: 14px;
  font-weight: 600;
  margin-top: 6px;
  color: var(--weilin-prompt-ui-primary-text);
}
</style>
