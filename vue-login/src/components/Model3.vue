<template>
  <div class="analysis-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-else>
        <h3>训练历史</h3>
        <img :src="msePlotPath" v-if="msePlotPath" alt="训练历史图表" style="max-width: 100%;">
        
        <h3 style="margin-top: 30px;">预测误差分布</h3>
        <img :src="histogramPath" v-if="histogramPath" alt="误差分布直方图" style="max-width: 100%;">
        
        <div v-if="mape" class="mape-result">
          <h3>模型评估</h3>
          <p>平均绝对百分比误差(MAPE): {{ mape.toFixed(2) }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 数据状态
const loading = ref(true);
const error = ref('');
const msePlotPath = ref('');
const histogramPath = ref('');
const mape = ref(null);

// 自动发送请求获取数据
onMounted(async () => {
  try {
    loading.value = true;
    const response = await axios.post('/api/Model1');  // 注意去掉了/api前缀，与后端路由一致
    
    if (response.data.success) {
      // 更新图片路径，添加时间戳防止缓存
      const timestamp = new Date().getTime();
      msePlotPath.value = `${response.data.mse_plot_path}?t=${timestamp}`;
      histogramPath.value = `${response.data.histogram_path}?t=${timestamp}`;
      mape.value = response.data.mape * 100;  // 转换为百分比
    } else {
      error.value = '分析失败: ' + (response.data.error || '未知错误');
      ElMessage.error(error.value);
    }
  } catch (err) {
    error.value = '请求出错: ' + (err.response?.data?.message || err.message);
    ElMessage.error(error.value);
    console.error('请求出错:', err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.loading, .error {
  text-align: center;
  padding: 50px;
  font-size: 18px;
}

.error {
  color: #f56c6c;
}

.mape-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

h3 {
  color: #409eff;
  margin-bottom: 15px;
}
</style>