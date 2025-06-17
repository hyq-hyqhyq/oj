<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="dashboard-grid">
        <div class="card manager-users-card">
          <div class="card-header-row">
            <h2>用户管理</h2>
            <div class="search-bar">
              <el-input
                v-model="searchId"
                placeholder="通过ID搜索"
                clearable
                size="small"
                style="width: 200px;"
              ></el-input>
            </div>
          </div>

          <!-- 用户列表 -->
          <table class="users-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>用户名</th>
                <th>角色</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user) in filteredUsers" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ getRoleName(user.role) }}</td>
                <td>
                  <button @click="deleteUser(user.id)" class="delete-button">删除用户</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar
  },
  name: 'ManageUsers',
  data() {
    return {
      users: [],
      searchId: '',
    };
  },
  computed: {
    filteredUsers() {
      if (this.searchId === '') {
        return this.users;
      } else {
        return this.users.filter(user => user.id.toString() === this.searchId);
      }
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('/api/manageusers')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          alert('获取用户列表失败:', error);
        });
    },
    deleteUser(user_id) {
      const userId = parseInt(user_id);
      axios.delete(`/api/manageusers`, {
        headers: {
          'session': localStorage.getItem('session'),
          'Content-Type': 'application/json'
        },
        params: {
          user_id: userId
        },
        data: {}})
        .then(() => {
          alert('删除用户成功');
          this.fetchUsers();
        })
        .catch(error => {
          alert('删除用户失败:', error);
        });
    },
    getRoleName(role) {
      switch (role) {
        case 0: return '学生';
        case 1: return '助教';
        case 2: return '教师';
        case 3: return '管理员';
        default: return '未知';
      }
    }
  }
};
</script>

<style scoped>
/* 样式保持不变 */
.main-bg {
  min-height: 100vh;
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
  display: flex;
}
.main-content {
  margin-left: 210px;
  flex: 1;
  padding: 40px 40px 40px 40px;
  min-height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}
.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.card.manager-users-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(89,174,235,0.10);
  padding: 24px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
.card.manager-users-card h2 {
  font-size: 1.18em;
  font-weight: bold;
  color: #1565c0;
  margin-bottom: 18px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 14px;
}
.card.manager-users-card h2::before {
  content: '';
  display: block;
  width: 5px;
  height: 22px;
  border-radius: 3px;
  background: linear-gradient(180deg, #42a5f5 0%, #1976d2 100%);
  position: absolute;
  left: 0;
  top: 2px;
}
.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.card-header-row h2 {
  margin-bottom: 0;
  padding-left: 14px;
}
.users-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.users-table th, .users-table td {
  border: 1px solid #ccc;
  padding: 12px;
}
.delete-button {
  background-color: #42a5f5;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 7px 18px;
  margin-right: 8px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(66,165,245,0.08);
}
button:hover {
  opacity: 0.8;
}
</style>