<template>
  <div class="fullscreen-div">
    <div class="left-bar">
      <div class="left-img">
        <div class="header">
          <span class="welcome">欢迎注册，</span>
          <h2 class="visol">基于深度学习的企业绩效评价算法</h2>
        </div>
      </div>
      <div class="left-index">
        <img src="@/assets/img/load.png" alt="">
      </div>
    </div>

    <div class="right-bar">
      <div class="account-register">
        用户注册
      </div>
      <div>
        <img src="@/assets/img/below.png" alt="">
      </div>
      <div class="right-bar-input">
        <input v-model="username" type="text" placeholder="用户名">
      </div>
      <div class="right-bar-input">
        <input v-model="name" type="text" placeholder="姓名">
      </div>
      <div class="right-bar-input">
        <select v-model="gender">
          <option value="male">男</option>
          <option value="female">女</option>
        </select>
      </div>
      <div class="right-bar-input">
        <input v-model="email" type="email" placeholder="邮箱">
      </div>
      <div class="right-bar-input">
        <input v-model="age" type="number" placeholder="年龄">
      </div>
      <div class="right-bar-input">
        <input v-model="password" type="password" placeholder="密码">
      </div>
      <div class="right-bar-input">
        <input v-model="confirmPassword" type="password" placeholder="确认密码">
      </div>
      <div class="right-bar-input">
        <button @click="handleRegister">注册</button>
      </div>
      <div class="login-link">
        <span>已有账号？</span>
        <a @click="goToLogin">去登录</a>
      </div>
    </div>
  </div>
</template>






<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus'; // 引入 Element Plus 的提示组件
import { useRouter } from 'vue-router'; // 引入路由

const router = useRouter();

// 定义表单数据
const username = ref('');
const name = ref('');
const gender = ref('male');
const email = ref('');
const age = ref('');
const password = ref('');
const confirmPassword = ref('');

// 跳转到登录页面
const goToLogin = () => {
  router.push('/');
};

// 注册逻辑
const handleRegister = async () => {
  // 输入验证
  if (!username.value || !name.value || !gender.value || !email.value || !age.value || !password.value || !confirmPassword.value) {
    ElMessage.warning('所有字段不能为空');
    return;
  }

  // 密码确认
  if (password.value !== confirmPassword.value) {
    ElMessage.error('两次输入的密码不一致');
    return;
  }

  try {
    // 发送注册请求
    const response = await axios.post('/register', {
      username: username.value,
      name: name.value,
      gender: gender.value,
      email: email.value,
      age: age.value,
      password: password.value,
    });

    // 处理响应
    if (response.data.success) {
      ElMessage.success(response.data.message);
      // 注册成功后跳转到登录页面
      router.push('/');
    } else {
      ElMessage.error(response.data.message || '注册失败，请稍后重试');
    }
  } catch (error) {
    console.error('请求失败:', error);
    ElMessage.error('请求失败，请稍后重试');
  }
};
</script>

<style lang="less" scoped>
.fullscreen-div {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-image: url('@/assets/img/background.png');
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left-img {
  padding-top: 40px;
}

.left-index {
  padding-top: 20px;
}

.left-bar {
  width: 35%;
  height: 65%;
  text-align: center;
  background: #FFFFFF;
  justify-content: center;
  box-shadow: 10px 10px 10px 10px #EEF9FD;
}

.right-bar {
  width: 20%;
  height: 65%;
  background: #FFFFFF;
  box-shadow: 10px 10px 10px 10px #EEF9FD;
  padding: 20px;
  box-sizing: border-box;
}

input:focus {
  outline: none;
}

input:hover {
  width: 100%;
  border: #ADD8F3 1px solid;
  border-radius: 3px;
  height: 40px;
  background: #FFFFFF;
}

input {
  width: 100%;
  border: #ADD8F3 2px solid;
  border-radius: 4px;
  height: 40px;
  background: #F2F2F2;
  padding-right: 50px;
  box-sizing: border-box;
}

select {
  width: 100%;
  border: #ADD8F3 2px solid;
  border-radius: 4px;
  height: 40px;
  background: #F2F2F2;
  padding-right: 50px;
  box-sizing: border-box;
}

button {
  width: 100%;
  border: #ADD8F3 2px solid;
  padding-left: 20px;
  padding-right: 20px;
  border-radius: 4px;
  height: 40px;
  background: linear-gradient(to right, #53A4E5, #A7DEF9);
  color: #FFFFFF;
  font-size: 16px;
  cursor: pointer;
}

.right-bar-input {
  padding-top: 20px;
  position: relative;
}

.header {
  display: flex;
  gap: 10px;
  align-items: baseline;
  justify-content: center;
}

.welcome {
  font-size: 16px;
  color: #333;
  font-weight: bold;
}

.visol {
  font-size: 24px;
  color: #31B1ED;
  font-weight: bold;
  margin: 0;
}

.account-register {
  padding-top: 10px;
  font-size: 20px;
  color: #31B1ED;
  font-weight: bold;
  margin: 0;
  text-align: center;
}

.login-link {
  text-align: center;
  margin-top: 15px;
  font-size: 14px;
  color: #666;

  a {
    color: #31B1ED;
    cursor: pointer;
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>