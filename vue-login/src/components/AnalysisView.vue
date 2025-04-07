<template>
  <div class="analysis-container">
    <!-- 标题 -->
    <h2 style="text-align: center; margin-bottom: 20px;">股票TOPSIS分析结果</h2>
    
    <!-- 图表展示区域 -->
    <div class="chart-container">
      <img :src="chartUrl" v-if="chartUrl" alt="股票评级分布图" style="max-width: 100%;">
      <el-skeleton :rows="5" animated v-else />
    </div>
    
    <!-- 分析结果表格 -->
    <div class="table-container">
      <el-table 
        :data="paginatedData" 
        border
        style="width: 100%; margin-top: 20px;"
        v-loading="loading"
        highlight-current-row
      >
        <el-table-column prop="股票代码" label="股票代码" width="120" sortable />
        <el-table-column prop="相对贴近度" label="相对贴近度" width="120" sortable>
          <template #default="{ row }">
            {{ Number(row.相对贴近度).toFixed(4) }}
          </template>
        </el-table-column>
        <el-table-column prop="分类" label="评级分类" width="120" sortable>
          <template #default="{ row }">
            <el-tag :type="getTagType(row.分类)" :class="'tag-' + row.分类.toLowerCase()">
              {{ row.分类 }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        style="margin-top: 20px;"
        background
        layout="prev, pager, next, sizes, total"
        :total="analysisData.length"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>
    
    <!-- 统计信息 -->
    <div class="stats-container" v-if="stats">
      <el-card shadow="hover" style="margin-top: 20px;">
        <template #header>
          <div style="font-weight: bold;">分类统计</div>
        </template>
        <div class="stat-item" v-for="(count, category) in stats.category_counts" :key="category">
          <el-tag :type="getTagType(category)" size="small">{{ category }}</el-tag>
          <span class="stat-count">{{ count }} 只股票</span>
        </div>
        <div style="margin-top: 10px; font-weight: bold;">
          总计: <strong>{{ stats.total_stocks }}</strong> 只股票
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

// 数据状态
const analysisData = ref([]);
const chartUrl = ref('');
const stats = ref(null);
const loading = ref(false);

// 分页相关
const currentPage = ref(1);
const pageSize = ref(10);

// 获取标签样式 - 修复type验证问题
const getTagType = (category) => {
  const types = {
    '很好': 'success',
    '好': 'primary',
    '良好': 'info',  // 将空字符串改为'info'
    '差': 'warning',
    '很差': 'danger'
  };
  return types[category] || 'info';  // 默认返回'info'而不是空字符串
};

// 分页处理
const handlePageChange = (page) => {
  currentPage.value = page;
};

const handleSizeChange = (size) => {
  pageSize.value = size;
  currentPage.value = 1;
};

// 计算当前页数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return analysisData.value.slice(start, end);
});

// 自动发送请求获取数据
onMounted(async () => {
  try {
    loading.value = true;
    const response = await axios.post('/api/AnalysisTopsis');
    
    if (response.data.success) {
      analysisData.value = response.data.analysis_result;
      chartUrl.value = response.data.chart_url;
      stats.value = response.data.stats;
    } else {
      console.error('分析失败:', response.data.error);
      ElMessage.error('分析失败: ' + response.data.error);
    }
  } catch (error) {
    console.error('请求出错:', error);
    ElMessage.error('请求出错: ' + error.message);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.analysis-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.chart-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.table-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stats-container {
  margin-top: 20px;
}

.stat-item {
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.stat-count {
  margin-left: 10px;
}

/* 自定义标签样式 */
.tag-很好 {
  font-weight: bold;
}
.tag-好 {
  font-weight: 500;
}
.tag-良好 {
  color: #666;
}
.tag-差 {
  font-style: italic;
}
.tag-很差 {
  text-decoration: underline;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .analysis-container {
    padding: 10px;
  }
  
  .chart-container,
  .table-container {
    padding: 15px;
  }
  
  .el-table-column {
    width: auto !important;
  }
}
</style>