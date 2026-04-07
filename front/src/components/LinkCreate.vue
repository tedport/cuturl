<template>
	<div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
		<div class="card shadow-sm" style="width: 100%; max-width: 480px;">

			<div class="card-header bg-primary text-white">
				<h5 class="mb-0">
					<i class="bi bi-link-45deg me-2"></i>URL Shortener
				</h5>
			</div>

			<div class="card-body p-4">
				<div class="mb-3">
					<label class="form-label fw-semibold text-secondary small text-uppercase tracking-wide">
						Long URL
					</label>
					<div class="input-group">
						<span class="input-group-text bg-white text-muted">
							<i class="bi bi-globe2"></i>
						</span>
						<input v-model="url" type="text" class="form-control"
							placeholder="https://your-very-very-long.url" />
					</div>
				</div>

				<div class="mb-3">
					<label class="form-label fw-semibold text-secondary small text-uppercase">
						Expiration Type
					</label>
					<select v-model="expirationSelectOption" class="form-select">
						<option value="noexpiry">No Expiry</option>
						<option value="maxuses">Max Uses</option>
						<option value="date">Expiration Date</option>
					</select>
				</div>

				<div class="mb-4">
					<label class="form-label fw-semibold text-secondary small text-uppercase">
						{{ expirationSelectOption === 'maxuses' ? 'Max Uses' : 'Expiration Date' }}
					</label>
					<input v-model="expirationValue" :disabled="expirationSelectOption === 'noexpiry'"
						:type="expirationType" class="form-control"
						:class="{ 'bg-light text-muted': expirationSelectOption === 'noexpiry' }"
						:placeholder="expirationSelectOption === 'maxuses' ? 'e.g. 100' : 'Pick a date'" />
					<div v-if="expirationSelectOption === 'noexpiry'" class="form-text text-muted">
						<i class="bi bi-info-circle me-1"></i>This link will never expire.
					</div>
				</div>

				<div class="d-grid">
					<button :disabled="!isValid || loading" class="btn btn-primary btn-lg" @click="submit">
						<span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
						<i v-else class="bi bi-scissors me-2"></i>
						{{ loading ? 'Shortening…' : 'Cut URL' }}
					</button>
				</div>

				<!-- Error -->
				<div v-if="error" class="alert alert-danger d-flex align-items-center mt-3 mb-0" role="alert">
					<i class="bi bi-exclamation-triangle-fill me-2 flex-shrink-0"></i>
					<span>{{ error }}</span>
				</div>

				<!-- Success result -->
				<div v-if="result" class="mt-4">
					<div class="alert alert-success mb-3">
						<div class="fw-semibold mb-1">
							<i class="bi bi-check-circle-fill me-1"></i>Link created!
						</div>
						<div class="d-flex align-items-center gap-2">
							<a :href="shortUrl" target="_blank" class="text-break">
								{{ shortUrl }}
							</a>
							<button class="btn btn-sm btn-outline-success ms-auto flex-shrink-0"
								:title="copied ? 'Copied!' : 'Copy link'"
								@click="copyShortUrl">
								<i :class="copied ? 'bi bi-check2' : 'bi bi-clipboard'"></i>
							</button>
						</div>
					</div>

					<div class="card bg-light border-0">
						<div class="card-body p-3">
							<p class="small fw-semibold text-uppercase text-secondary mb-2">
								<i class="bi bi-key me-1"></i>Owner Code
								<span class="text-danger">— save this now!</span>
							</p>
							<div class="d-flex align-items-center gap-2">
								<code class="text-break flex-grow-1">{{ result.owner_code }}</code>
								<button class="btn btn-sm btn-outline-secondary flex-shrink-0"
									:title="copiedCode ? 'Copied!' : 'Copy code'"
									@click="copyOwnerCode">
									<i :class="copiedCode ? 'bi bi-check2' : 'bi bi-clipboard'"></i>
								</button>
							</div>
							<p class="small text-muted mb-0 mt-2">
								<i class="bi bi-info-circle me-1"></i>
								You will need this code to deactivate the link later.
							</p>
						</div>
					</div>

					<ul class="list-group list-group-flush mt-3 small">
						<li class="list-group-item d-flex justify-content-between px-0">
							<span class="text-secondary">Original URL</span>
							<a :href="result.url" target="_blank" class="text-truncate ms-3" style="max-width: 240px;">
								{{ result.url }}
							</a>
						</li>
						<li class="list-group-item d-flex justify-content-between px-0">
							<span class="text-secondary">Active</span>
							<span :class="result.is_active ? 'text-success' : 'text-danger'">
								{{ result.is_active ? 'Yes' : 'No' }}
							</span>
						</li>
						<li v-if="result.expires_at" class="list-group-item d-flex justify-content-between px-0">
							<span class="text-secondary">Expires at</span>
							<span>{{ formatDate(result.expires_at) }}</span>
						</li>
						<li v-if="result.max_clicks != null" class="list-group-item d-flex justify-content-between px-0">
							<span class="text-secondary">Max uses</span>
							<span>{{ result.max_clicks }}</span>
						</li>
						<li class="list-group-item d-flex justify-content-between px-0">
							<span class="text-secondary">Created at</span>
							<span>{{ formatDate(result.created_at) }}</span>
						</li>
					</ul>
				</div>
			</div>

			<div class="card-footer text-center text-muted small py-2">
				Links are shortened instantly · No account required
			</div>

		</div>
	</div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useApiRequest } from '@/composables/useApiRequest.js'

const url = ref('')
const expirationSelectOption = ref('noexpiry')
const expirationValue = ref('')

const copied = ref(false)
const copiedCode = ref(false)

const { data: result, error, loading, request } = useApiRequest()

// Manually build the short URL using the host and the slug from the result
const shortUrl = computed(() => {
  if (!result.value?.slug) return ''
  const protocol = window.location.protocol
  const host = window.location.host
  return `${protocol}//${host}/${result.value.slug}`
})

const expirationType = computed(() => {
	const map = {
		noexpiry: 'text',
		maxuses: 'number',
		date: 'datetime-local',
	}
	return map[expirationSelectOption.value] ?? 'text'
})

const isUrlValid = computed(() => {
	try {
		new URL(url.value)
		return true
	} catch {
		return false
	}
})

const isExpirationValid = computed(() => {
	if (expirationSelectOption.value === 'noexpiry') return true

	if (expirationSelectOption.value === 'maxuses') {
		const num = Number(expirationValue.value)
		return Number.isInteger(num) && num > 0
	}

	if (expirationSelectOption.value === 'date') {
		const date = new Date(expirationValue.value)
		return !isNaN(date.getTime()) && date > new Date()
	}

	return false
})

const isValid = computed(() => isUrlValid.value && isExpirationValid.value)

async function submit() {
	const body = { url: url.value }

	if (expirationSelectOption.value === 'maxuses') {
		body.max_uses = Number(expirationValue.value)
	} else if (expirationSelectOption.value === 'date') {
		body.expires_at = new Date(expirationValue.value).toISOString()
	}

	await request('POST', '/links/', body)
}

async function copyShortUrl() {
	await navigator.clipboard.writeText(shortUrl.value)
	copied.value = true
	setTimeout(() => (copied.value = false), 2000)
}

async function copyOwnerCode() {
	await navigator.clipboard.writeText(result.value?.owner_code ?? '')
	copiedCode.value = true
	setTimeout(() => (copiedCode.value = false), 2000)
}

function formatDate(iso) {
	return new Date(iso).toLocaleString()
}
</script>