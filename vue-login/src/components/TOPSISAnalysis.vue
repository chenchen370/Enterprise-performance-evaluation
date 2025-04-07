<template>
  <div class="container">
    <div class="sidebar">
      <div style="height: 300px; max-width: 600px">
<div  :disabled="activeStep === 0" @click="prevStep"><el-icon><ArrowUpBold /></el-icon></div>
        <el-steps direction="vertical" :active="activeStep" @step-click="handleStepClick">
          <el-step title="原始数据展示" />
          <el-step title="清理数据" />
          <el-step title="相对贴近度比较分析" />
          <el-step title="模型1" />
          <el-step title="模型2" />
          <el-step title="模型3" />
        </el-steps>
<div :disabled="activeStep === views.length - 1" @click="nextStep"><el-icon><ArrowDownBold /></el-icon></div>
      </div>
    </div>

    <div class="main">
      <!-- 动态渲染组件 -->
      <component :is="currentView" />


    </div>
  </div>
</template>

<script setup>
import {
ArrowUpBold,
ArrowDownBold,
} from '@element-plus/icons-vue';
import { ref, computed } from 'vue';
import OriginDataView from '../components/OriginDataView.vue';
import CleanDataView from '../components/CleanDataView.vue';
import AnalysisView from '../components/AnalysisView.vue';
import Model1 from './Model1.vue';
import Model2 from './Model2.vue';
// 默认 activeStep 为 0，表示从第一个步骤开始
const activeStep = ref(0);

// 组件映射
const views = [
  OriginDataView,  // 对应 activeStep = 0
  CleanDataView, // 对应 activeStep = 1
  AnalysisView,// 对应 activeStep = 2 
  Model1,
  Model2,
  Model1,

];

// 计算属性，根据 activeStep 返回对应的组件
const currentView = computed(() => views[activeStep.value]);

// 点击步骤时触发
const handleStepClick = (index) => {
  activeStep.value = index;
};

// 上一步逻辑
const prevStep = () => {
  if (activeStep.value > 0) {
    activeStep.value--;
  }
};

// 下一步逻辑
const nextStep = () => {
  if (activeStep.value < views.length - 1) {
    activeStep.value++;
  }
};


</script>

<style>
.container {
  width: 100%;
  height: 100%;
  display: flex;
}

.sidebar {
  width: 20%;
}

.main {
  width: 80%;
  display: flex;
  flex-direction: column;
}

.button-group {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}
</style>