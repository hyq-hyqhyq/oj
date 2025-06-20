<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="dashboard-grid">
        <div class="card assistant-card">
          <h2>助教首页</h2>
          <!-- 原有内容保持不变，直接放在这里 -->
          <div>
            <!-- 顶部整排欢迎卡片 -->
            <div class="card top-card">
              <h1>您好，<span class="highlight">{{ name }}</span>（助教）</h1>
              <p>您负责 <span class="highlight">{{ studentCount }}</span> 位学生。</p>
            </div>

            <!-- 底部左右并排 -->
            <div class="bottom-container">
              <!-- 左侧：我的学生 -->
              <div class="card left-column">
                <h2>我的学生</h2>
                <el-table :data="students" style="width: 100%" fit>
                  <el-table-column prop="student_id" label="学生ID" align="center" show-overflow-tooltip />
                  <el-table-column prop="username" label="学生用户名" align="center" show-overflow-tooltip />
                </el-table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'AssistantHome',
  components: { Navbar },
  data() {
    return {
      name: localStorage.getItem('userName'),
      studentCount: 0,
      students: [],
      pendingSubmits: [],
      currentTime: new Date().toLocaleString()
    };
  },
  mounted() {
    this.fetchInfo();
    this.pickQuote();
    setInterval(() => {
      this.currentTime = new Date().toLocaleString();
    }, 1000);
  },
  methods: {
    async fetchInfo() {
      const session = localStorage.getItem('session');
      const assistantId = localStorage.getItem('userID');
      try {
        const aRes = await axios.get('/api/assistantstudents', {
          headers: { session },
          params: { assistant_id: assistantId }
          });
        this.students = aRes.data;
        this.studentCount = this.students.length;
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error('获取负责学生失败', e);
      }
    },
    pickQuote() {
      const idx = Math.floor(Math.random() * this.quotes.length);
      this.quote = this.quotes[idx];
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
  margin-left: 210px; /* 预留给Navbar */
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
.card.assistant-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(89,174,235,0.10);
  padding: 24px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}
.card.assistant-card h2 {
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
.card.assistant-card h2::before {
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

/* 顶部整排 */
.top-card {
  width: 100%;
  margin-bottom: 20px;
}

/* 底部左右结构 */
.bottom-container {
  display: flex;
  gap: 20px;
}
.left-column,
.right-column {
  flex: 1;
}

/* 卡片统一样式 */
.card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* 高亮名 */
.highlight {
  color: #4A90E2;
  font-weight: bold;
}

/* 每日一言 */
.daily-quote {
  margin-top: 10px;
  font-size: 16px;
  color: #333;
  font-weight: normal;
}

/* 时间 */
.current-time {
  margin-top: 10px;
  color: #666;
}
</style>
