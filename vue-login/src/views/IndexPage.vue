<template>
  <div data-v-app="" class="container" >
    <div class="top-bar" data-v-053af0bb="" data-v-59cd1402="">
      <button class="login-button" data-v-053af0bb="">登录</button>
    </div>
    <img alt="背景图" class="background" data-v-59cd1402="" src="@/assets/img/photo5jpg.jpg" />
    <div class="home-container" data-v-59cd1402="">
      <div class="logo-container" data-v-59cd1402="">
        <div class="easylink" data-v-59cd1402="">
          <span class="green" data-v-59cd1402="">DeepLearning</span>
          <span class="white" data-v-59cd1402="">Performance</span>
          <span class="green" data-v-59cd1402="">.ai</span>
        </div>
        <div class="title" data-v-59cd1402="">企业绩效评价</div>
      </div>
      <label class="button" data-v-59cd1402="" data-v-a2e5902b="" role="button">
        <div class="text-container" data-v-a2e5902b="">
          <div data-v-a2e5902b="">上传企业数据，</div>
          <div class="function-text-container" data-v-a2e5902b="" style="--s: 2;">
            <div class="function-text" data-v-a2e5902b="">绩效评价</div>
            <div class="function-text" data-v-a2e5902b=""> <a href="/home">结果分析</a> </div>
            <div class="function-text" data-v-a2e5902b="">模型选择</div>
          </div>
        </div>
        <input class="file-input" data-v-a2e5902b="" multiple type="file" @change="handleFileUpload" />
      </label>
    </div>

    <!-- 上传确认弹窗 -->
    <el-dialog v-model="dialogVisible" title="是否上传企业数据？" width="50%">
      <div v-if="fileContent" style="max-height: 300px; overflow-y: auto;">
        <pre>{{ fileContent }}</pre>
      </div>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="openModelSelectionDialog">确认上传</el-button>
      </template>
    </el-dialog>

    <!-- 模型选择弹窗 -->
    <el-dialog v-model="modelSelectionDialogVisible" title="选择评价模型" width="30%">
      <el-select v-model="selectedModel" placeholder="请选择模型">
        <el-option label="神经网络模型" value="neural_network"></el-option>
        <el-option label="随机森林模型" value="random_forest"></el-option>
        <el-option label="支持向量机模型" value="svm"></el-option>
      </el-select>
      <template #footer>
        <el-button @click="modelSelectionDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmUpload">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref } from 'vue';
import { ElDialog, ElButton, ElMessage, ElSelect, ElOption } from 'element-plus';
import axios from 'axios'; // 引入 axios
import router from '@/router';

export default {
  name: 'App',
  components: {
    ElDialog,
    ElButton,
    ElSelect,
    ElOption,
  },
  setup() {
    const dialogVisible = ref(false); // 控制上传确认弹窗显示
    const modelSelectionDialogVisible = ref(false); // 控制模型选择弹窗显示
    const fileContent = ref(''); // 存储文件内容
    const selectedFile = ref(null); // 存储用户选择的文件
    const selectedModel = ref(''); // 存储用户选择的模型
    const loading = ref(false); // 上传加载状态

    // 处理文件上传
    const handleFileUpload = (event) => {
      const files = event.target.files;
      if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/csv' || file.type === 'application/vnd.ms-excel') {
          selectedFile.value = file; // 保存选择的文件

          // 读取文件内容
          const reader = new FileReader();
          reader.onload = () => {
            fileContent.value = reader.result;
          };
          reader.readAsText(file);

          dialogVisible.value = true; // 显示上传确认弹窗
        } else {
          ElMessage.warning('请上传CSV或Excel文件！');
        }
      }
    };

    // 打开模型选择弹窗
    const openModelSelectionDialog = () => {
      dialogVisible.value = false; // 关闭上传确认弹窗
      modelSelectionDialogVisible.value = true; // 打开模型选择弹窗
    };

    // 上传文件并执行绩效评价
    const uploadAndEvaluate = async () => {
      if (selectedFile.value && selectedModel.value) {
        try {
          const formData = new FormData();
          formData.append('file', selectedFile.value);
          formData.append('model', selectedModel.value);

          loading.value = true; // 开始加载

          const response = await axios.post('http://localhost:8080/api/evaluate', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });

          loading.value = false; // 结束加载

          ElMessage.success('绩效评价成功！');

          // 跳转到结果页面，并传递评价结果
          router.push({
            path: '/results',
            query: {
              evaluationResult: JSON.stringify(response.data)
            }
          });
        } catch (error) {
          console.error('绩效评价失败:', error);
          ElMessage.error('绩效评价失败，请稍后重试');
        }
      }
    };

    // 确认上传并执行评价
    const handleConfirmUpload = async () => {
      modelSelectionDialogVisible.value = false; // 关闭模型选择弹窗
      await uploadAndEvaluate(); // 调用上传和评价函数
    };

    return {
      dialogVisible,
      modelSelectionDialogVisible,
      fileContent,
      selectedModel,
      loading,
      handleFileUpload,
      openModelSelectionDialog,
      handleConfirmUpload,
    };
  },
};
</script>

<style lang="less" scoped>


@import url('@/assets/css/index-cebee1c6.css');


</style>