<template>
  <div class="setting">
    <!-- 设置内容居中 -->
    <div class="setting-content">
      <h1>设置</h1>

      <!-- 背景颜色选择 -->
      <div class="theme-selector">
        <label for="theme">选择背景颜色：</label>
        <el-select v-model="selectedBackground" placeholder="选择背景颜色" @change="updateBackground" size="small" style="width: 150px;">
          <el-option label="默认" value="default" />
          <el-option label="晨曦蓝" value="blue" />
          <el-option label="豆沙绿" value="green" />
          <el-option label="金秋黄" value="yellow" />
          <el-option label="烟雾灰" value="gray" />
        </el-select>
      </div>

      <!-- 修改用户名 -->
      <div class="input-group">
        <label for="username">修改用户名：</label>
        <input type="text" v-model="newUsername" placeholder="输入新用户名" />
      </div>

      <!-- 修改密码 -->
      <div class="input-group">
        <label for="password">修改密码：</label>
        <input type="password" v-model="newPassword" placeholder="输入新密码" />
      </div>

      <button @click="updateSettings">保存设置</button>

      <!-- 返回按钮 -->
      <button class="back-button" @click="goBack">返回</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedBackground: localStorage.getItem('backgroundColor') || 'default',  // 默认从 localStorage 获取背景色
      newUsername: '',
      newPassword: ''
    };
  },
  methods: {
    updateBackground() {
      // 将选择的背景颜色保存在 localStorage 中
      localStorage.setItem('backgroundColor', this.selectedBackground);
      
      // 触发页面重新渲染，确保根组件应用更新的背景色
      document.body.classList.remove('theme-default', 'theme-blue', 'theme-green', 'theme-yellow', 'theme-gray');
      document.body.classList.add(`theme-${this.selectedBackground}`);
    },
    updateSettings() {
      const session = localStorage.getItem('session');
      const userId = localStorage.getItem('userID');
      const data = {
        id: userId,
        username: this.newUsername,
        password: this.newPassword
      };

      // 调用接口更新用户设置
      axios.post('/api/updateSettings', data, { headers: { session } })
        .then(response => {
          alert('设置已保存');
        })
        .catch(error => {
          alert('更新失败: ' + error.message);
        });
    },
    goBack() {
      // 你可以根据需要修改返回逻辑，比如返回到主页
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.setting {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;  /* 改为min-height */
  background-color: transparent !important; /* 移除自身背景 */
}

.setting-content {
  width: 350px;  /* 更改为适合的宽度 */
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.theme-selector,
.input-group {
  margin-bottom: 20px;
}

button {
  background-color: #2b8cd1;
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  cursor: pointer;
  margin-bottom: 10px;
}

button:hover {
  background-color: #1a6ca7;
}

/* 返回按钮样式 */
.back-button {
  background-color: #ccc;
  color: white;
  border: none;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 5px;
}

.back-button:hover {
  background-color: #999;
}
</style>
