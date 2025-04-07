<template>
    <div>
      <!-- 图表容器 -->
      <div ref="chartDom" style="width: 100%; height: 400px;"></div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted, onUnmounted, watch } from 'vue';
  import * as echarts from 'echarts/core';
  import { GridComponent, GridComponentOption } from 'echarts/components';
  import { LineChart, LineSeriesOption } from 'echarts/charts';
  import { UniversalTransition } from 'echarts/features';
  import { CanvasRenderer } from 'echarts/renderers';
  
  // 注册 ECharts 组件
  echarts.use([GridComponent, LineChart, CanvasRenderer, UniversalTransition]);
  
  // 定义 ECharts 配置类型
  type EChartsOption = echarts.ComposeOption<
    GridComponentOption | LineSeriesOption
  >;
  
  // 定义 props
  const props = defineProps({
    xAxisData: {
      type: Array as () => string[],
      required: true,
    },
    seriesData: {
      type: Array as () => number[],
      required: true,
    },
  });
  
  // 图表 DOM 元素引用
  const chartDom = ref<HTMLElement | null>(null);
  let myChart: echarts.ECharts | null = null;
  
  // 初始化图表
  const initChart = () => {
    if (!chartDom.value) return;
  
    // 初始化 ECharts 实例
    myChart = echarts.init(chartDom.value);
  
    // 配置项
    const option: EChartsOption = {
      xAxis: {
        type: 'category',
        data: props.xAxisData, // 使用父组件传递的 xAxisData
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          data: props.seriesData, // 使用父组件传递的 seriesData
          type: 'line',
        },
      ],
    };
  
    // 设置配置项并渲染图表
    myChart.setOption(option);
  };
  
  // 监听窗口大小变化，调整图表大小
  const resizeChart = () => {
    if (myChart) {
      myChart.resize();
    }
  };
  
  // 监听 props 变化，更新图表
  watch(
    () => [props.xAxisData, props.seriesData],
    () => {
      if (myChart) {
        myChart.setOption({
          xAxis: {
            data: props.xAxisData,
          },
          series: [
            {
              data: props.seriesData,
            },
          ],
        });
      }
    },
    { deep: true }
  );
  
  // 在组件挂载后初始化图表
  onMounted(() => {
    initChart();
    window.addEventListener('resize', resizeChart);
  });
  
  // 在组件卸载时移除事件监听
  onUnmounted(() => {
    window.removeEventListener('resize', resizeChart);
  });
  </script>
  
  <style scoped>
  /* 可以根据需要添加样式 */
  </style>