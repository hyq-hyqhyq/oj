<template>
  <nav class="sidebar-navbar">
    <div class="sidebar-header">
      <span class="sidebar-title">H.L.L.X  OJ</span>
    </div>
    <div class="sidebar-links">
      <router-link
        v-if="canAccessHomePage"
        :to="homePath"
        :class="['nav-link', isActive(homePath), { 'activated': isCurrentPath(homePath) }]"
        @click="handleClick(homePath)"
      >主页</router-link>
      <router-link
        v-if="canAccessCreateQuestion"
        :to="{ path: '/import' }"
        :class="['nav-link', isActive('/import'), { 'activated': isCurrentPath('/import') }]"
        @click="handleClick('/import')"
      >创建题目</router-link>
      <router-link
        v-if="canAccessCreateContest"
        :to="{ path: '/create' }"
        :class="['nav-link', isActive('/create'), { 'activated': isCurrentPath('/create') }]"
        @click="handleClick('/create')"
      >创建考试</router-link>
      <router-link
        v-if="canAccessQuestionList"
        :to="{ path: '/question' }"
        :class="['nav-link', isActive('/question'), { 'activated': isCurrentPath('/question') }]"
        @click="handleClick('/question')"
      >题目列表</router-link>
      <router-link
        v-if="canAccessContestList"
        :to="{ path: '/contest' }"
        :class="['nav-link', isActive('/contest'), { 'activated': isCurrentPath('/contest') }]"
        @click="handleClick('/contest')"
      >考试列表</router-link>
      <router-link
        v-if="canAccessSubmitRecords"
        :to="{ path: '/submit' }"
        :class="['nav-link', isActive('/submit'), { 'activated': isCurrentPath('/submit') }]"
        @click="handleClick('/submit')"
      >提交记录</router-link>
      <router-link
        v-if="canAccessUserManagement"
        :to="{ path: '/admin' }"
        :class="['nav-link', isActive('/admin'), { 'activated': isCurrentPath('/admin') }]"
        @click="handleClick('/admin')"
      >用户管理</router-link>
      <router-link
        v-if="canAccessStudentManage"
        :to="{ path: '/studentmanage' }"
        :class="['nav-link', isActive('/studentmanage'), { 'activated': isCurrentPath('/studentmanage') }]"
        @click="handleClick('/studentmanage')"
      >学生管理</router-link>
      <router-link
        :to="{ path: '/setting' }"
        class="nav-link"
        @click="handleClick('/setting')"
      >用户设置</router-link>
    </div>
    <button class="logout-button" @click="logout">退出登录</button>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Navbar',
  data() {
    return {
      nickname: '', // 初始化用户昵称
      userRole: parseInt(localStorage.getItem('userRole')) || 0, // 从本地存储中获取用户角色，默认为 0 (student)
      currentPath: ''
    };
  },
  computed: {
    canAccessHomePage() {
      return [0, 1, 3].includes(this.userRole);
    },
    canAccessCreateQuestion() {
      return this.userRole === 1 || this.userRole === 2;
    },
    canAccessCreateContest() {
      return this.userRole === 1 || this.userRole === 2;
    },
    canAccessQuestionList() {
      return [0, 1, 2, 3].includes(this.userRole);
    },
    canAccessContestList() {
      return [0, 1, 2, 3].includes(this.userRole);
    },
    canAccessSubmitRecords() {
      return [0, 1, 2, 3].includes(this.userRole);
    },
    canAccessUserManagement() {
      return this.userRole === 2;
    },
    canDeleteQuestions() {
      return this.userRole === 1;
    },
    canAccessStudentManage() {
      return this.userRole === 1; // 教师
    },
    homePath: function () {
      switch (this.userRole) {
        case 0: return '/index';
        case 1: return '/teacher';
        case 3: return '/assistant';
        default: return '/';
      }
    }
  },
  methods: {
    isActive(path) {
      return this.$route.path === path ? 'active' : '';
    },
    isCurrentPath(path) {
      return this.currentPath === path;
    },
    handleClick(path) {
      this.currentPath = path;
    },
    logout() {
      const sessionToken = localStorage.getItem('session');
      axios.delete('/api/login', {
        headers: {
          'session': sessionToken,
          'Content-Type': 'application/json'
        },
        data: {}
      })
      .then(response => {
        alert(response.data.message); // 显示成功消息
        localStorage.removeItem('session'); // 清除本地存储中的 session
        this.$router.push('/'); // 回到主页
      })
      .catch(error => {
        alert('退出登录失败: ' + error.response.data.message);
      });
    }
  },
  mounted() {
    // 在组件挂载时获取用户昵称
    this.nickname = localStorage.getItem('userName') || 'Guest';
    this.currentPath = this.$route.path;
  }
};

</script>

<style scoped>
.sidebar-navbar {
  position: fixed;
  left: 0;
  top: 0;
  width: 210px;
  height: 100vh;
  background: linear-gradient(180deg, #59aeeb 0%, #0a1a3c 100%);
  display: flex;
  flex-direction: column;
  align-items: stretch;
  z-index: 1000;
  box-shadow: 2px 0 12px rgba(0,0,0,0.08);
}

.sidebar-header {
  padding: 32px 0 18px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

.sidebar-title {
  font-size: 1.5em;
  font-weight: bold;
  color: #fff;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.sidebar-nickname {
  color: #e0e0e0;
  font-size: 1em;
  margin-bottom: 0;
}

.sidebar-links {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 24px;
  gap: 6px;
}

.nav-link {
  display: block;
  width: 100%;
  padding: 14px 0 14px 36px;
  color: #7fd0ff !important;
  text-decoration: none;
  font-size: 1.2em;
  border-left: 4px solid transparent;
  background: none;
  transition: all 0.2s;
  letter-spacing: 1px;
  border-radius: 0 20px 20px 0;
  margin-bottom: 2px;
}

.nav-link:hover, .nav-link.active, .nav-link.activated {
  background: rgba(255,255,255,0.13);
  color: white!important;
  border-left: 4px solid #59aeeb;
  font-weight: bold;
  transform: translateX(4px) scale(1.04);
}

.logout-button {
  margin: 24px 18px 32px 18px;
  padding: 12px 0;
  background: #59aeeb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.08em;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(89,174,235,0.08);
  transition: background 0.2s, color 0.2s, transform 0.2s;
}

.logout-button:hover {
  background: #59aeeb;
  color: #fff;
  transform: scale(1.05);
}

@media (max-width: 700px) {
  .sidebar-navbar {
    width: 100vw;
    height: auto;
    flex-direction: row;
    position: static;
    box-shadow: none;
  }
  .sidebar-header, .sidebar-links {
    flex-direction: row;
    align-items: center;
    padding: 0;
    margin: 0;
  }
  .sidebar-header {
    border-bottom: none;
    padding: 10px 0;
  }
  .sidebar-links {
    flex: 1;
    gap: 0;
    margin-top: 0;
  }
  .nav-link {
    padding: 10px 16px;
    border-radius: 8px;
    border-left: none;
    margin-bottom: 0;
  }
  .logout-button {
    margin: 10px;
    padding: 10px 16px;
  }
}
</style>