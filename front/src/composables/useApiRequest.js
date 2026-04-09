import { ref } from 'vue'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''

export function useApiRequest() {
  const data    = ref(null)
  const error   = ref(null)
  const status  = ref(null)
  const loading = ref(false)

  async function request(method, path, body = undefined, headers = {}) {
    data.value    = null
    error.value   = null
    status.value  = null
    loading.value = true

    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
        },
      }

      if (body !== undefined) {
        options.body = JSON.stringify(body)
      }

      const response = await fetch(`${BASE_URL}${path}`, options)
      status.value = response.status

      if (response.status === 204) {
        data.value = null
        return null
      }

      let json = null
      let text = null
      const contentType = response.headers.get('content-type') ?? ''

      if (contentType.includes('application/json')) {
        try {
          json = await response.json()
        } catch {
          text = await response.text()
        }
      } else {
        text = await response.text()
      }

      if (!response.ok) {
        const message =
          typeof json?.detail === 'string'
            ? json.detail
            : Array.isArray(json?.detail)
              ? json.detail.map((e) => e.msg).join('; ')
              : text
                ? text
                : `Request failed with status ${response.status}`

        error.value = message
        return null
      }

      data.value = json ?? text
      return json ?? text
    } catch (err) {
      error.value = err?.message ?? 'Network error'
      return null
    } finally {
      loading.value = false
    }
  }

  return { data, error, status, loading, request }
}