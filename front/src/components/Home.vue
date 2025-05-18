<template>
  <div class="video-background">
    <video
      autoplay
      muted
      loop
      playsinline
      src="@/assets/bk_vd.mp4"
    ></video>
    <div class="overlay">
      <header>
        <div class="title">SQL课程在线测评系统</div>
        <div class="buttons">
          <button @click="toggleForm('login')" class="btn">登录</button>
          <button @click="toggleForm('register')" class="btn">注册</button>
        </div>
      </header>
      <img src="@/assets/logo.png" class="logo">
      <h1>即刻开始SQL之旅</h1>
    </div>
    <transition name="slide-down">
      <div class="login-register" v-if="showForm">
        <form @submit.prevent="handleSubmit" class="form">
          <img src="@/assets/logo.png" class="logo2">
          <button type="button" class="back-btn" @click="showForm = false">返回</button>
          <input type="text" v-model="id" placeholder="请输入账号" required>
          <div v-if="!isLogin">
            <input type="text" v-model="username" placeholder="请输入姓名" required>
          </div>
          <input type="password" v-model="password" placeholder="请输入密码" required>
        <el-select v-model="role" placeholder="请选择身份" style="width: 100%; margin-top: 10px;margin-bottom: 15px;">
          <el-option label="学生" value="student" />
          <el-option label="助教" value="assistant" />
          <el-option label="教师" value="teacher" />
          <el-option label="管理员" value="admin" />
        </el-select>
          <div class="btn-group">
            <button type="submit" class="submit-btn">{{ isLogin ? '登录' : '注册' }}</button>
            <button type="button" class="switch-btn" @click="toggleForm(isLogin ? 'register' : 'login')" >
            {{ isLogin ?'没有账号？立即注册' : '已有账号？立即登录' }}</button>
          </div>        
        </form>
      </div>
    </transition>      
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      showForm: false,
      isLogin: true,
      id: '',
      username: '',
      password: '',
      role: '',
      isTyping: true,
      show:false,
    };
  },
  methods: {
    toggleForm(formType) {
      this.isLogin = formType === 'login';
      this.showForm = true;
    },
    async handleSubmit() {
      if (this.isLogin) {
        try {
          const response = await axios.post('/api/login', {
            id: parseInt(this.id),
            password: this.password,
            role: this.role,
          });
          const userID = this.id;
          const userName = response.data.username;
          const userRole = response.data.role;
          const sessionToken = response.data.session; // 获取session token

          // 将session token存储在本地存储中
          localStorage.setItem('session', sessionToken); 
          // 设置用户角色
          localStorage.setItem('userRole', userRole);
          // 设置用户ID
          localStorage.setItem('userID', userID);
          // 设置用户名
          localStorage.setItem('userName', userName);

          if (userRole === 0) {
            alert(`登录成功！id: ${this.id}\n欢迎进入在线测评平台开始刷题之旅！`)
            this.$router.push('/index');
          } else if (userRole === 1) {
            alert(`登录成功！id: ${this.id}\n欢迎回来，祝您教学顺利！`)
            this.$router.push('/teacher');
          } else if (userRole === 2) {
            alert(`登录成功！id: ${this.id}\n欢迎进入系统管理后台！`)
            this.$router.push('/admin');
          } else if (userRole === 3) {
            alert(`登录成功！id: ${this.id}\n助教您好，欢迎协助管理！`)
            this.$router.push('/assistant');
          } else {
            alert('用户身份无效，重新注册！');
          }
        } catch (error) {
          alert('登录失败：' + error.response.data.message);
        }
      } else {
        try {
          const response = await axios.post('/api/register', {
            id: parseInt(this.id),
            username: this.username,
            password: this.password,
            role: this.role
          });
          alert(response.data.message);
          this.$router.push('/');
        } catch (error) {
          if (error.response && error.response.data && error.response.data.message) {
            alert(`注册失败：` + error.response.data.message);
          } else {
            alert('注册失败！');
          }
        }
      }
    }
  }
};
</script>

<style scoped>

#app {
  font-family: 'Noto Sans', 'Microsoft YaHei UI', 'Source Code Pro', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.video-background {
  position: relative;
  width: 100%;
  height: 100vh; /* 视口高度 */
  overflow: hidden;
}

.video-background video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; 
  z-index: 0; 
}

.overlay {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

header {
  position: fixed;
  top: 0;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color:rgb(7, 12, 113);
}

.title {
  flex-grow: 1;
  text-align: left;
  font-size: 24px;
  font-weight: bold;
  color: #59aeeb;
}

.buttons {
  display: flex;
  gap: 20px; 
}

.btn {
  padding: 15px 20px; 
  border: none;
  border-radius: 10px;
  background-color: #668be3;
  color: white;
  cursor: pointer;
  font-size: 18px; 
}

.logo {
  position: relative;
  width: 350px;
  height: 300px;
}

h1 {
  font-size: 60px;
  color: #c6d5df;
}

.login-register {
  position: fixed;
  top: 0;
  right: 0;
  width: 100%;
  height: 100%;
  background-color:skyblue;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2; /* 确保在主文字层之上 */
}

.form {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 600px;
  position: relative;
}

.form .logo2{
  position: relative;
  width: 200px;
  height: 180px;
}

.form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  display:inline-block;
}

.form .btn-group{
  display: flex;
  align-items: center;  
  gap: 20px;  
}

.form .submit-btn {
  padding: 10px;
  width: 48%;
  border: none;
  border-radius: 5px;
  background-color: skyblue;
  color: white;
  cursor: pointer;
  margin-top: 10px;
}

.form .submit-btn:hover {
  background-color: #1a6ca7;
}

.form .switch-btn {
  padding: 10px;
  width: 48%;
  border: none;
  border-radius: 5px;
  background-color:skyblue;
  color: white;
  cursor: pointer;
  margin-top: 10px;
}

.form .switch-btn:hover {
  background-color: #1a6ca7;
}

.form .back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background-color:skyblue;
  color: white;
  border: none;
  border-radius: 10%;
  width: 60px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form .back-btn:hover{
  background-color: #1a6ca7;
}

/* 定义进入和离开的过渡 */
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.5s ease;
}

/* 定义进入前和离开后的状态 */
.slide-down-enter,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-100%);
}

.box {
  width: 200px;
  height: 100px;
  background: #42b983;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
}

::v-deep .el-select-dropdown__item.selected {
  background-color: #2b8cd1 !important;
  color: white !important;
}

::v-deep .el-select-dropdown__item:hover {
  background-color: #2b8cd1 !important;
  color: white !important;
}

</style>
