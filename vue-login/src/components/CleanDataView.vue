<template>
  <div>
    <!-- Element Plus 表格 -->
    <el-table :data="formattedPaginatedData" style="width: 100%">
      <!-- 动态生成列 -->
      <el-table-column
        v-for="(value, key) in tableColumns"
        :key="value"
        :prop="value"
        :label="value"
        width="140"
      />
    </el-table>

    <!-- Element Plus 分页 -->
    <el-pagination
      style="margin-top: 20px; text-align: right"
      background
      layout="prev, pager, next, sizes, total"
      :total="tableData.length"
      :page-size="pageSize"
      :current-page="currentPage"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// 表格数据
const tableData = ref([]);
const rawData = ref([]); // 保存原始数据

// 表格列（动态生成）
const tableColumns = ref({});

// 分页相关
const currentPage = ref(1);
const pageSize = ref(10);

// 格式化数字为4位小数
const formatNumber = (value) => {
  if (typeof value === 'number') {
    // 使用toFixed(4)并去除末尾无意义的0
    const formatted = value.toFixed(4);
    return formatted.replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.0+$/, '');
  }
  return value;
};

// 格式化整个数据对象
const formatData = (data) => {
  return data.map(row => {
    const formattedRow = {};
    for (const key in row) {
      formattedRow[key] = formatNumber(row[key]);
    }
    return formattedRow;
  });
};

// 计算当前页的数据（带格式化）
const formattedPaginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return formatData(tableData.value.slice(start, end));
});

// 页面挂载时发送请求
onMounted(async () => {
  try {
    const response = await axios.post('/api/clean_data');
    if (response.data.success) {
      rawData.value = response.data.data; // 保存原始数据
      tableData.value = response.data.data; // 初始化显示数据
      if (tableData.value.length > 0) {
        tableColumns.value = Object.keys(tableData.value[0]);
      }
    } else {
      console.error('请求失败：', response.data);
    }
  } catch (error) {
    console.error('请求出错：', error);
  }
});

// 处理页码变化
const handlePageChange = (page) => {
  currentPage.value = page;
};

// 处理每页条数变化
const handleSizeChange = (size) => {
  pageSize.value = size;
  currentPage.value = 1;
};
</script>

<style scoped>
/* 样式可以根据需要调整 */
</style>