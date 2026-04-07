<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow-sm" style="width: 100%; max-width: 480px;">

      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">
          <i class="bi bi-search me-2"></i>URL Lookup
        </h5>
      </div>

      <div class="card-body p-4">

        <!-- CutUrl Input -->
        <div class="mb-3">
          <label class="form-label fw-semibold text-secondary small text-uppercase">
            Shortened URL
          </label>
          <div class="input-group">
            <span class="input-group-text bg-white text-muted">
              <i class="bi bi-link-45deg"></i>
            </span>
            <input
              v-model="cutUrl"
              type="text"
              class="form-control"
              :placeholder="urlPlaceholder"
            />
          </div>
        </div>

        <!-- Info & Stats Actions -->
        <div class="d-flex gap-2 mb-4">
          <button :disabled="!slug" class="btn btn-outline-primary flex-fill">
            <i class="bi bi-info-circle me-2"></i>Info
          </button>
          <button :disabled="!slug" class="btn btn-outline-secondary flex-fill">
            <i class="bi bi-bar-chart-line me-2"></i>Stats
          </button>
        </div>

        <!-- Danger Zone -->
        <div class="border border-danger rounded-3 p-3">
          <p class="text-danger fw-semibold small text-uppercase mb-3">
            <i class="bi bi-exclamation-triangle-fill me-1"></i>Danger Zone
          </p>

          <div class="mb-3">
            <label class="form-label fw-semibold text-secondary small text-uppercase">
              Owner Code
            </label>
            <div class="input-group">
              <span class="input-group-text bg-white text-muted">
                <i class="bi bi-key"></i>
              </span>
              <input
                v-model="ownerCode"
                type="text"
                class="form-control"
                placeholder="Enter owner code"
              />
            </div>
          </div>

          <div class="d-grid">
            <button :disabled="!slug || !ownerCode.trim()" class="btn btn-danger">
              <i class="bi bi-slash-circle me-2"></i>Deactivate Link
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const urlPlaceholder = `${window.location.host}/abc`

const cutUrl = ref('')
const ownerCode = ref('')

const slug = computed(() => {
  const trimmed = cutUrl.value.trim()
  if (!trimmed) return ''

  try {
    const { pathname } = new URL(trimmed)
    return pathname.replace(/^\//, '') || ''
  } catch {
    return trimmed
  }
})
</script>