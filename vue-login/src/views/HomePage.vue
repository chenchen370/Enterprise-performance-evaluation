<template>
    <div class="common-layout">
      <el-container>
        <!-- Header -->
        <el-header style="background-color: #409EFF; color: white; text-align: center; line-height: 60px;">
          基于深度学习的企业绩效评价算法
        </el-header>
  
        <el-container>
          <!-- Aside (侧边栏) -->
          <el-aside width="200px" style="background-color: #e9eef3;">
            <el-menu
              default-active="1"
              class="el-menu-vertical-demo"
              @select="handleMenuSelect"
            >
              <!-- 动态渲染菜单项 -->
              <el-menu-item
                v-for="item in menuItems"
                :key="item.id"
                :index="item.id"
              >
                <el-icon>
                  <component :is="item.icon" />
                </el-icon>
                <span>{{ item.label }}</span>
              </el-menu-item>
            </el-menu>
          </el-aside>
  
          <!-- Main (主内容区) -->
          <el-main>
            <div v-if="activeMenu === '1'">
              盈利能力分析
                <ProfitAnalysis></ProfitAnalysis>
            </div>
            <div v-if="activeMenu === '2'">
              营运能力分析
                <OperationAnalysis></OperationAnalysis>
            </div>
            <div v-if="activeMenu === '3'">
              成长能力分析
              <GrowthAnalysis></GrowthAnalysis>
            </div>
            <div v-if="activeMenu === '4'">
              偿债能力分析
              <BalanceAnalysis></BalanceAnalysis>
              
            </div>

            <div v-if="activeMenu === '5'">
              <TOPSISAnalysis></TOPSISAnalysis>
              
            </div>

          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>

<script setup>
import { ref } from 'vue';
import {
  Menu as IconMenu,
  Document,
  Setting,
  Money,
  Compass,
} from '@element-plus/icons-vue';

import ProfitAnalysis from '../components/ProfitAnalysis.vue';
import OperationAnalysis from '../components/OperationAnalysis.vue';
import GrowthAnalysis from '../components/GrowthAnalysis.vue';
import BalanceAnalysis from '../components/BalanceAnalysis.vue';

import TOPSISAnalysis from '../components/TOPSISAnalysis.vue'

// 菜单项数据
const menuItems = [
  { id: '1', label: '盈利能力分析', icon: IconMenu },
  { id: '2', label: '营运能力分析', icon: Document },
  { id: '3', label: '成长能力分析', icon: Setting },
  { id: '4', label: '偿债能力分析', icon: Money },
  { id: '5', label: '熵权TOPSIS绩效评价', icon: Compass }, 
];





// 当前选中的菜单项
const activeMenu = ref('1');

// 处理菜单选择
const handleMenuSelect = (index) => {
  activeMenu.value = index;
};
</script>

<style scoped>
.common-layout {
  height: 100vh; /* 占满整个视口高度 */
}

.el-container {
  height: 100%; /* 继承父容器的高度 */
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #e9eef3;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.el-menu {
  border-right: none; /* 移除侧边栏菜单的边框 */
}

.el-menu-item {
  margin: 10px 0;
}

.el-menu-item.is-active {
  background-color: #ecf5ff; /* 选中菜单项的背景色 */
  color: #409EFF; /* 选中菜单项的文字颜色 */
}
</style>