<template>
  <div v-if="visible" class="weilin-tools-dialog-overlay" @mousedown.self="onCancel">
    <div class="weilin-tools-dialog-content generate-image-dialog" @mousedown.stop>
      <div class="weilin-tools-dialog-header">
        <h2>{{ mode === 'regenerate' ? '重新生成预览图' : '生成标签预览图' }}</h2>
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

        <div class="form-group">
          <label>正向提示词</label>
          <textarea v-model="form.positive" class="form-textarea" rows="3"></textarea>
        </div>

        <div class="form-group">
          <label>负向提示词</label>
          <textarea v-model="form.negative" class="form-textarea" rows="2"></textarea>
        </div>
      </div>
      <div class="weilin-tools-dialog-footer">
        <button class="cancel-btn" @click="onCancel">取消</button>
        <button class="confirm-btn" @click="onGenerate" :disabled="generating">
          {{ mode === 'regenerate' ? '重新生成' : '生成' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { tagsApi } from '@/api/tags'

const props = defineProps({
  visible: { type: Boolean, default: false },
  tag: { type: Object, default: null },
  options: { type: Object, default: () => ({ checkpoints: [], samplers: [], sizes: [] }) },
  mode: { type: String, default: 'generate' }  // 'generate' | 'regenerate'
})
const emit = defineEmits(['close', 'generated'])

const generating = ref(false)

const form = reactive({
  checkpoint: '',
  sizeIndex: 0,
  sampler_name: 'euler',
  steps: 20,
  cfg: 7.0,
  seed: -1,
  positive: '',
  negative: 'worst quality, low quality, nsfw'
})

watch(() => props.visible, (v) => {
  if (v && props.tag) {
    form.positive = `${props.tag.text || ''}, masterpiece, best quality`
    form.negative = 'worst quality, low quality, nsfw'
    form.checkpoint = props.options.checkpoints?.[0]?.name || ''
    form.sampler_name = 'euler'
    form.steps = 20
    form.cfg = 7.0
    form.seed = -1
    form.sizeIndex = 0
    generating.value = false
  }
})

function onCancel() {
  if (!generating.value) {
    emit('close')
  }
}

async function onGenerate() {
  const size = props.options.sizes[form.sizeIndex] || props.options.sizes[0]
  generating.value = true
  try {
    const params = {
      checkpoint: form.checkpoint,
      width: size.width,
      height: size.height,
      sampler_name: form.sampler_name,
      steps: form.steps,
      cfg: form.cfg,
      seed: form.seed,
      positive: form.positive,
      negative: form.negative
    }
    let res
    if (props.mode === 'regenerate') {
      res = await tagsApi.regenerateTagImage(props.tag.t_uuid, params)
    } else {
      res = await tagsApi.generateTagImage(props.tag.t_uuid, params)
    }
    emit('generated', { task_id: res.data.task_id, t_uuid: props.tag.t_uuid })
    emit('close')
  } catch (err) {
    if (err.response?.status === 409) {
      alert('已有生成任务进行中')
    } else {
      alert('生成失败: ' + (err.message || '未知错误'))
    }
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.generate-image-dialog {
  width: 520px;
  max-width: 90vw;
}
.form-row {
  display: flex;
  gap: 16px;
}
.form-group-half {
  flex: 1;
}
.form-select, .form-input, .form-textarea {
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}
.form-textarea {
  resize: vertical;
}
.form-range {
  width: 100%;
}
.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
