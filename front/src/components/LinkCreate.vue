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
					<button :disabled="!isValid" class="btn btn-primary btn-lg">
						<i class="bi bi-scissors me-2"></i>Cut URL
					</button>
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

const url = ref('')
const expirationSelectOption = ref('noexpiry')
const expirationValue = ref('')

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
</script>