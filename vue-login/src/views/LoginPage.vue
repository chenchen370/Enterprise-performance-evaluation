<template>
  <div class="fullscreen-div">
    <div class="left-bar">
      <div class="left-img">
        <div class="header">
          <span class="welcome">欢迎使用，</span>
          <h2 class="visol">基于深度学习的企业绩效评价算法</h2>
        </div>
      </div>
      <div class="left-index">
        <img src="@/assets/img/load.png" alt="">
      </div>
    </div>

    <div class="right-bar">
      <div class="account-login">
        账号登录
      </div>
      <div>
        <img src="@/assets/img/below.png" alt="">
      </div>
      <div class="right-bar-input">
        <input v-model="username" type="text" placeholder="用户名">
      </div>
      <div class="right-bar-input">
        <input v-model="password" type="password" placeholder="密码">
      </div>
      <div class="right-bar-input code">
        <input v-model="captcha" type="text" placeholder="验证码" />
        <div class="login-code" @click="refreshCode">
          <DentifyComponent :identifyCode="identifyCode" />
        </div>
      </div>
      <div class="right-bar-input">
        <button @click="handleLogin">登录</button>
      </div>
      <div class="register-link">
        <span>没有账号？</span>
        <a @click="goToRegister">立即注册</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus'; // 引入 Element Plus 的提示组件
import { useRouter } from 'vue-router'; // 引入路由
import DentifyComponent from '@/components/DentifyComponent.vue';

const router = useRouter();

// 定义表单数据
const username = ref('');
const password = ref('');
const captcha = ref('');

// 验证码相关逻辑
const identifyCodes = '1234567890abcdefjhijklinopqrsduvwxyz'; // 随机串内容
const identifyCode = ref(''); // 验证码图片内容

// 生成验证码
const makeCode = (o, l) => {
  let code = '';
  for (let i = 0; i < l; i++) {
    code += identifyCodes[randomNum(0, identifyCodes.length)];
  }
  identifyCode.value = code;
};

// 生成随机数
const randomNum = (min, max) => {
  return Math.floor(Math.random() * (max - min) + min);
};

// 重置验证码
const refreshCode = () => {
  identifyCode.value = '';
  makeCode(identifyCodes, 4);
};

// 初始化验证码
onMounted(() => {
  refreshCode();
});

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register');
};

// 登录逻辑
const handleLogin = async () => {
  // 输入验证
  if (!username.value || !password.value || !captcha.value) {
    ElMessage.warning('账号、密码和验证码不能为空');
    return;
  }

  // 验证码校验
  if (captcha.value.toLowerCase() !== identifyCode.value.toLowerCase()) {
    ElMessage.error('验证码错误，请重新输入');
    refreshCode(); // 刷新验证码
    return;
  }

  try {
    // 发送登录请求
    const response = await axios.post('/login', null, {
      params: {
        username: username.value,
        password: password.value,
      },
    });

    // 处理响应
    if (response.data.success) {
      ElMessage.success(response.data.message);
      // 跳转到首页或其他页面
      localStorage.setItem("username", username.value);
      router.push('/index');
    } else {
      ElMessage.error(response.data.message || '登录失败，请检查账号和密码');
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

.code {
  display: flex;
  align-items: center;
  gap: 10px; /* 输入框和验证码之间的间距 */
}

.login-code {
  cursor: pointer;
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

.account-login {
  padding-top: 90px;
  font-size: 20px;
  color: #31B1ED;
  font-weight: bold;
  margin: 0;
  text-align: center;
}

.register-link {
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