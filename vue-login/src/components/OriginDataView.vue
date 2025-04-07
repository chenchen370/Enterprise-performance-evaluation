<template>
    <div>
      <!-- Element Plus 表格 -->
      <el-table :data="paginatedData" style="width: 100%">
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
  
  // 表格列（动态生成）
  const tableColumns = ref({});
  
  // 分页相关
  const currentPage = ref(1); // 当前页码
  const pageSize = ref(10); // 每页显示条数
  
  // 计算当前页的数据
  const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    console.log(tableData.value.slice(start, end))
    return tableData.value.slice(start, end);
  });
  
  // 页面挂载时发送请求
  onMounted(async () => {
    try {
      const response = await axios.post('/api/origin_data');
      response.data = eval("(" + response.data + ")");
      if (response.data.success) {
        // 更新表格数据
        tableData.value = response.data.data;
        // 动态生成列
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
    currentPage.value = 1; // 重置为第一页
  };
  </script>
  
  <style scoped>
  /* 样式可以根据需要调整 */
  </style>