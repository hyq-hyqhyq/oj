<template>
  <div>
    <Navbar />
    <div class="assistant-home">
      <!-- 顶部整排欢迎卡片 -->
      <div class="card top-card">
        <h1>您好，<span class="highlight">{{ name }}</span>（助教）</h1>
        <p>您负责 <span class="highlight">{{ studentCount }}</span> 位学生。</p>
        <div class="daily-quote">每日一言：{{ quote }}</div>
        <div class="current-time">当前时间：{{ currentTime }}</div>
      </div>

      <!-- 底部左右并排 -->
      <div class="bottom-container">
        <!-- 左侧：我的学生 -->
        <div class="card left-column">
          <h2>我的学生</h2>
          <el-table :data="students" style="width: 100%" fit>
            <el-table-column prop="student_id" label="学生ID" align="center" show-overflow-tooltip />
            <el-table-column prop="username" label="用户名" align="center" show-overflow-tooltip />
          </el-table>
        </div>
        <!-- 右侧：待批阅提交 -->
        <div class="card right-column">
          <h2>待批阅提交</h2>
          <el-table :data="pendingSubmits" style="width: 100%" fit>
            <el-table-column prop="id" label="提交ID" align="center" show-overflow-tooltip />
            <el-table-column prop="student_id" label="学生ID" align="center" show-overflow-tooltip />
            <el-table-column prop="question_id" label="题目ID" align="center" show-overflow-tooltip />
            <el-table-column prop="submit_time" label="提交时间" align="center" show-overflow-tooltip />
          </el-table>
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
      currentTime: new Date().toLocaleString(),
      quote: '',
      quotes: [
        "批阅的眼神要如炬，发现每一个细节。",
        "协助不是次要，而是教育的桥梁。",
        "助教是一座灯塔，照亮学生前行的路。",
        "不只是批阅，更是守护。",
        "每一次认真审阅，都是对学生努力的尊重。"
      ]
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
        const aRes = await axios.post('/api/assistantstudents', {
          assistant_id: assistantId,
          student_ids: []
        }, { 
          headers: { session },
          params: { assistant_id: assistantId }
          });
        this.students = aRes.data;
        this.studentCount = this.students.length;
      } catch (e) {
        console.error('获取负责学生失败', e);
      }
      try {
        const sRes = await axios.get('/api/submitlist', {
          headers: { session },
          params: { fetchall: false, user_id: assistantId }
        });
        this.pendingSubmits = sRes.data.filter(s => s.status === -1);
      } catch (e) {
        console.error('获取待批阅提交失败', e);
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
.assistant-home {
  padding: 20px;
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
