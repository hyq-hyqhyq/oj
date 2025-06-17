<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="card setting-card">
        <h2>用户设置</h2>
        <div class="input-group">
          <label for="username">修改用户名：</label>
          <input type="text" v-model="newUsername" placeholder="输入新用户名" />
        </div>
        <div class="input-group">
          <label for="password">修改密码：</label>
          <input type="password" v-model="newPassword" placeholder="输入新密码" />
        </div>
        <button @click="updateSettings">保存设置</button>
        <button class="back-button" @click="goBack">返回</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  components: { Navbar },
  data() {
    return {
      selectedBackground: localStorage.getItem('backgroundColor') || 'default',
      newUsername: '',
      newPassword: ''
    };
  },
  methods: {
    updateBackground() {
      localStorage.setItem('backgroundColor', this.selectedBackground);
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
      axios.post('/api/updateSettings', data, { headers: { session } })
        .then(() => {
          alert('设置已保存');
        })
        .catch(error => {
          alert('更新失败: ' + error.message);
        });
    },
    goBack() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.main-bg {
  min-height: 100vh;
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
  display: flex;
}
.main-content {
  margin-left: 210px;
  flex: 1;
  padding: 40px 0 40px 0;
  min-height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card.setting-card {
  width: 540px; 
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(89,174,235,0.10);
  padding: 32px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-width: 0;
  min-height: 0;
  margin-top: 40px; 
}
.card.setting-card h2 {
  font-size: 1.28em;
  font-weight: bold;
  color: #1565c0;
  margin-bottom: 24px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 16px;
}
.card.setting-card h2::before {
  content: '';
  display: block;
  width: 5px;
  height: 24px;
  border-radius: 3px;
  background: linear-gradient(180deg, #42a5f5 0%, #1976d2 100%);
  position: absolute;
  left: 0;
  top: 2px;
}
.input-group {
  margin-bottom: 20px;
  text-align: left;
}
.input-group label,
.theme-selector label {
  display: block;
  margin-bottom: 6px;
  color: #1976d2;
  font-weight: 500;
}
.input-group input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #bbdefb;
  border-radius: 6px;
  font-size: 1em;
  margin-top: 2px;
  margin-bottom: 2px;
  box-sizing: border-box;
  transition: border 0.2s;
}
.input-group input:focus {
  border: 1.5px solid #42a5f5;
  outline: none;
}
button {
  background-color: #2b8cd1;
  color: white;
  border: none;
  padding: 10px;
  width: 100%;
  cursor: pointer;
  margin-bottom: 10px;
  border-radius: 6px;
  font-size: 1em;
  transition: background 0.2s;
}
button:hover {
  background-color: #1a6ca7;
}
.back-button {
  background-color: #ccc;
  color: white;
  border: none;
  padding: 8px 15px;
  cursor: pointer;
  border-radius: 5px;
  width: auto;
  margin-top: 6px;
}
.back-button:hover {
  background-color: #999;
}
</style>
