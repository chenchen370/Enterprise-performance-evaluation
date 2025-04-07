<template>
  <div class="profit-analysis-container">
    <!-- 搜索框 -->
    <div class="search-container">
      <el-input
        v-model="stockCode"
        placeholder="请输入股票代码，例如：sh.600000"
        style="width: 300px; margin-right: 20px;"
      />
      <el-date-picker
        v-model="value2"
        type="yearrange"
        unlink-panels
        range-separator="To"
        start-placeholder="Start Year"
        end-placeholder="End Year"
        :shortcuts="shortcuts"
      />
      <el-button style="margin:60px" type="primary" @click="fetchData">查询</el-button>
    </div>

    <!-- 表格 -->
    <div v-if="isShow" class="table-container">
      <el-table :data="tableData" style="width: 100%" height="100%">
        <!-- 动态生成列 -->
        <el-table-column
          v-for="(value, key) in tableData[0]"
          :key="key"
          :prop="key"
          :label="formatLabel(key)"
          :width="getColumnWidth(key)"
        >
          <!-- 自定义列内容 -->
          <template #default="{ row }">
            <span v-if="isBillionColumn(key)">
              {{ formatBillion(row[key]) }}
            </span>
            <span v-else-if="isPercentageColumn(key)">
              {{ formatPercentage(row[key]) }}
            </span>
            <span v-else>
              {{ row[key] }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 图表 -->
    <div class="chart-container" v-if="isShow">
      <LineEChar :x-axis-data="xAxisData" :series-data="seriesData"></LineEChar>

    </div>
  </div>
</template>
  
  <script lang="ts" setup>
  import axios from 'axios'; // 引入 axios
  import { ref, onMounted, defineProps, watch } from 'vue';
  // import * as echarts from 'echarts';
  import { ElMessage } from 'element-plus';
  import { ElDatePicker } from 'element-plus';

  import LineEChar from '../components/LineEChar.vue';
  const xAxisData = ref(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
  const seriesData = ref([150, 230, 224, 218, 135, 147, 260]);
  // 定义 props
  const props = defineProps({
    defaultStockCode: {
      type: String,
      default: 'sh.600000',
    },
    defaultYearRange: {
      type: Array,
      default: () => [2017, 2020],
    },
  });
  const value2 = ref()

  const tableData = ref([])

  const isShow = ref(false)


  const shortcuts = [
    {
      text: 'This Year',
      value: [new Date(), new Date()],
    },
    {
      text: 'Last 10 years',
      value: () => {
        const end = new Date()
        const start = new Date(
          new Date().setFullYear(new Date().getFullYear() - 10)
        )
        return [start, end]
      },
    },
    {
      text: 'Next 50 years',
      value: () => {
        const start = new Date()
        const end = new Date(
          new Date().setFullYear(new Date().getFullYear() + 50)
        )
        return [start, end]
      },
    },
  ]


  // 股票代码
  const stockCode = ref(props.defaultStockCode);
  // 年份范围
  const yearRange = ref(props.defaultYearRange);
  // 图表数据
  
  // 获取数据
  const fetchData = async () => {
    const dateStrings = value2.value;
    const years = dateStrings .map(date => date.getFullYear());

    console.log(years); // 输出: [2030, 2031]

    if (!stockCode.value || !yearRange.value || yearRange.value.length !== 2) {
      ElMessage.warning('请输入股票代码并选择年份范围');
      return;
    }

    try {
      const response = await axios.post('/api/profit', {
        code: stockCode.value,
        startYear: years[0],
        endYear: years[1],
      }, {
        headers: {
          'Content-Type': 'application/json', // 设置请求头
        },
      });

      const result = response.data; // axios 返回的数据在 response.data 中
      if (result.success) {
        tableData.value = result.data;
        isShow.value = true;
      } else {
        ElMessage.error(result.message || '数据获取失败');
      }
    } catch (error) {
      ElMessage.error('请求失败，请检查网络或服务器');
      console.error(error); // 打印错误信息
    }
  };


  // 格式化列名
const formatLabel = (key) => {
  const labelMap = {
    code: '股票代码',
    MBRevenue: '主营收入',
    epsTTM: '每股收益(TTM)',
    gpMargin: '毛利率',
    liqaShare: '流通股本',
    netProfit: '净利润',
    npMargin: '净利率',
    pubDate: '发布日期',
    roeAvg: '净资产收益率(平均)',
    statDate: '统计日期',
    totalShare: '总股本',
  };
  return labelMap[key] || key; // 如果未找到映射，则返回原始 key
};

// 获取列宽
const getColumnWidth = (key) => {
  const widthMap = {
    MBRevenue: '180',
    code: '120',
    epsTTM: '120',
    gpMargin: '120',
    liqaShare: '150',
    netProfit: '150',
    npMargin: '120',
    pubDate: '150',
    roeAvg: '180',
    statDate: '150',
    totalShare: '150',
  };
  return widthMap[key] || 'auto'; // 如果未找到映射，则使用 auto
};
  
  // 判断是否是亿元单位列
  const isBillionColumn = (key) => {
    return ['MBRevenue', 'liqaShare', 'netProfit', 'totalShare'].includes(key);
  };

  // 格式化亿元单位
  const formatBillion = (value) => {
    if (!value) return '—'; // 如果值为空，显示占位符
    const num = parseFloat(value);
    if (isNaN(num)) return '—'; // 如果转换失败，显示占位符
    return (num / 100000000).toFixed(2) + ' 亿元'; // 转换为亿元并保留两位小数
  };

  // 判断是否是百分比列
  const isPercentageColumn = (key) => {
    return ['gpMargin', 'npMargin', 'roeAvg'].includes(key);
  };

  // 格式化百分比
  const formatPercentage = (value) => {
    if (!value) return '—'; // 如果值为空，显示占位符
    const num = parseFloat(value);
    if (isNaN(num)) return '—'; // 如果转换失败，显示占位符
    return (num * 100).toFixed(2) + '%'; // 转换为百分比并保留两位小数
  };


  </script>
  
  <style scoped>
.profit-analysis-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 占满整个视口高度 */
  box-sizing: border-box; /* 防止 padding 影响高度计算 */
}
  
  .search-container {
    flex: 0 0 5%; /* 占据 10% 高度 */
    display: flex;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .table-container {
    flex: 0 0 40%; /* 占据 40% 高度 */
    overflow: auto; /* 如果内容超出，显示滚动条 */
    margin-bottom: 20px;
  }
  
  .chart-container {
    flex: 0 0 50%; /* 占据 50% 高度 */
    overflow: hidden; /* 防止内容溢出 */
  }
  </style>