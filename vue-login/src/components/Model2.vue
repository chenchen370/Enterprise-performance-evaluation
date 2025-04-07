<template>
  <div class="model-results">
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-else-if="error" class="error">
      Error: {{ error }}
    </div>
    
    <div v-else>
      <h2>Model Results</h2>
      
      <div class="result-section">
        <h3>Training History</h3>
        <img :src="trainingHistory" alt="Training History" v-if="trainingHistory">
      </div>
      
      <div class="result-section" v-if="errorComparison">
        <h3>Error Comparison</h3>
        <img :src="errorComparison" alt="Error Comparison">
      </div>
      
      <div class="metrics">
        <h3>Performance</h3>
        <p>Mean Absolute Percentage Error: {{ (mape * 100).toFixed(2) }}%</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const loading = ref(true)
const error = ref(null)
const trainingHistory = ref('')
const errorComparison = ref('')
const mape = ref(0)

onMounted(async () => {
  try {
    const response = await axios.post('/api/Model2')
    
    if (response.data.success) {
      trainingHistory.value = response.data.training_history + `?t=${Date.now()}`
      errorComparison.value = response.data.error_comparison ? 
        response.data.error_comparison + `?t=${Date.now()}` : ''
      mape.value = response.data.mape
    } else {
      error.value = response.data.error || 'Request failed'
    }
  } catch (err) {
    error.value = err.response?.data?.error || err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.model-results {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.result-section {
  margin-bottom: 30px;
}

.result-section img {
  width: 100%;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.metrics {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 4px;
}

.loading, .error {
  text-align: center;
  padding: 40px;
  font-size: 18px;
}

.error {
  color: #f44336;
}
</style>