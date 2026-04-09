<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow-sm" style="width: 100%; max-width: 480px;">

      <div class="card-header bg-primary text-white">
        <h5 class="mb-0">
          <i class="bi bi-search me-2"></i>URL Lookup
        </h5>
      </div>

      <div class="card-body p-4">

        <!-- Shortened URL input -->
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
          <button
            :disabled="!slug || infoApi.loading.value"
            class="btn btn-outline-primary flex-fill"
            @click="fetchInfo"
          >
            <span v-if="infoApi.loading.value" class="spinner-border spinner-border-sm me-1" role="status"></span>
            <i v-else class="bi bi-info-circle me-2"></i>
            Info
          </button>
          <button
            :disabled="!slug || statsApi.loading.value"
            class="btn btn-outline-secondary flex-fill"
            @click="fetchStats"
          >
            <span v-if="statsApi.loading.value" class="spinner-border spinner-border-sm me-1" role="status"></span>
            <i v-else class="bi bi-bar-chart-line me-2"></i>
            Stats
          </button>
        </div>

        <!-- Shared error banner -->
        <div
          v-if="activeError"
          class="alert alert-danger d-flex align-items-center mb-3"
          role="alert"
        >
          <i class="bi bi-exclamation-triangle-fill me-2 flex-shrink-0"></i>
          <span>{{ activeError }}</span>
        </div>

        <!-- Info result -->
        <div v-if="infoApi.data.value && activePanel === 'info'" class="mb-4">
          <p class="fw-semibold text-uppercase text-secondary small mb-2">
            <i class="bi bi-info-circle me-1"></i>Link Info
          </p>
          <ul class="list-group list-group-flush small">
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Short URL</span>
              <a :href="shortUrl" target="_blank">
                {{ shortUrl }}
              </a>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Original URL</span>
              <a
                :href="infoApi.data.value.url"
                target="_blank"
                class="text-truncate ms-3"
                style="max-width: 240px;"
              >
                {{ infoApi.data.value.url }}
              </a>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Active</span>
              <span :class="infoApi.data.value.is_active ? 'text-success' : 'text-danger'">
                {{ infoApi.data.value.is_active ? 'Yes' : 'No' }}
              </span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Clicks</span>
              <span>{{ infoApi.data.value.click_count }}</span>
            </li>
            <li v-if="infoApi.data.value.expires_at" class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Expires at</span>
              <span>{{ formatDate(infoApi.data.value.expires_at) }}</span>
            </li>
            <li v-if="infoApi.data.value.max_clicks != null" class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Max uses</span>
              <span>{{ infoApi.data.value.max_clicks }}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Created at</span>
              <span>{{ formatDate(infoApi.data.value.created_at) }}</span>
            </li>
          </ul>
        </div>

        <!-- Stats result -->
        <div v-if="statsApi.data.value && activePanel === 'stats'" class="mb-4">
          <p class="fw-semibold text-uppercase text-secondary small mb-2">
            <i class="bi bi-bar-chart-line me-1"></i>Link Stats
          </p>
          <ul class="list-group list-group-flush small">
            <li class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Total clicks</span>
              <strong>{{ statsApi.data.value.total_clicks }}</strong>
            </li>
            <li v-if="statsApi.data.value.last_clicked_at" class="list-group-item d-flex justify-content-between px-0">
              <span class="text-secondary">Last clicked</span>
              <span>{{ formatDate(statsApi.data.value.last_clicked_at) }}</span>
            </li>
          </ul>

          <!-- Clicks by device -->
          <div v-if="hasEntries(statsApi.data.value.clicks_by_device)" class="mt-3">
            <p class="text-secondary small fw-semibold mb-1">By Device</p>
            <ul class="list-group list-group-flush small">
              <li
                v-for="[device, count] in sortedEntries(statsApi.data.value.clicks_by_device)"
                :key="device"
                class="list-group-item d-flex justify-content-between px-0"
              >
                <span class="text-capitalize">{{ device }}</span>
                <span>{{ count }}</span>
              </li>
            </ul>
          </div>

          <!-- Clicks by country -->
          <div v-if="hasEntries(statsApi.data.value.clicks_by_country)" class="mt-3">
            <p class="text-secondary small fw-semibold mb-1">By Country</p>
            <ul class="list-group list-group-flush small">
              <li
                v-for="[country, count] in sortedEntries(statsApi.data.value.clicks_by_country)"
                :key="country"
                class="list-group-item d-flex justify-content-between px-0"
              >
                <span>{{ country }}</span>
                <span>{{ count }}</span>
              </li>
            </ul>
          </div>
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

          <!-- Deactivate error -->
          <div
            v-if="deactivateApi.error.value"
            class="alert alert-danger d-flex align-items-center mb-3 py-2"
            role="alert"
          >
            <i class="bi bi-exclamation-triangle-fill me-2 flex-shrink-0"></i>
            <span>{{ deactivateApi.error.value }}</span>
          </div>

          <!-- Deactivated success -->
          <div
            v-if="deactivateApi.status.value === 204"
            class="alert alert-success d-flex align-items-center mb-3 py-2"
            role="alert"
          >
            <i class="bi bi-check-circle-fill me-2 flex-shrink-0"></i>
            Link successfully deactivated.
          </div>

          <div class="d-grid">
            <button
              :disabled="!slug || !ownerCode.trim() || deactivateApi.loading.value"
              class="btn btn-danger"
              @click="deactivate"
            >
              <span v-if="deactivateApi.loading.value" class="spinner-border spinner-border-sm me-2" role="status"></span>
              <i v-else class="bi bi-slash-circle me-2"></i>
              {{ deactivateApi.loading.value ? 'Deactivating…' : 'Deactivate Link' }}
            </button>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useApiRequest } from '@/composables/useApiRequest.js'

const urlPlaceholder = `${window.location.host}/abc`

const cutUrl = ref('')
const ownerCode = ref('')

const activePanel = ref(null)

const infoApi       = useApiRequest()
const statsApi      = useApiRequest()
const deactivateApi = useApiRequest()

const shortUrl = computed(() => {
  if (!result.value?.slug) return ''
  const protocol = window.location.protocol
  const host = window.location.host
  return `${protocol}//${host}/${result.value.slug}`
})

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

const activeError = computed(() => {
  if (activePanel.value === 'info')  return infoApi.error.value
  if (activePanel.value === 'stats') return statsApi.error.value
  return null
})

async function fetchInfo() {
  activePanel.value = 'info'
  await infoApi.request('GET', `/links/${slug.value}`)
}

async function fetchStats() {
  activePanel.value = 'stats'
  await statsApi.request('GET', `/links/${slug.value}/stats`)
}

async function deactivate() {
  await deactivateApi.request(
    'DELETE',
    `/links/${slug.value}?code=${encodeURIComponent(ownerCode.value.trim())}`,
  )
}

function formatDate(iso) {
  return new Date(iso).toLocaleString()
}

function hasEntries(obj) {
  return obj && Object.keys(obj).length > 0
}

function sortedEntries(obj) {
  return Object.entries(obj).sort(([, a], [, b]) => b - a)
}
</script>