<template>
  <div>
    <Navbar />
    <div class="teacher-home">
      <!-- 顶部全宽欢迎卡片 -->
      <div class="card top-card">
        <h1>欢迎回来，<span class="highlight">{{ name }}</span>（教师）</h1>
        <p>您已创建 <span class="highlight">{{ questionCount }}</span> 道题，<span class="highlight">{{ contestCount }}</span> 场考试。</p>
        <div v-if="quote" class="daily-quote">每日一言：{{ quote }}</div>
        <div class="current-time">当前时间：{{ currentTime }}</div>
      </div>

      <!-- 底部两栏：我的题目 + 我的考试 -->
      <div class="bottom-container">
        <!-- 左侧 -->
        <div class="card column-card">
          <h2>我的题目</h2>
          <el-table :data="questions" style="width: 100%">
            <el-table-column prop="id" label="题目ID" align="center" />
            <el-table-column prop="title" label="标题" align="center" />
            <el-table-column prop="difficulty" label="难度" align="center" />
          </el-table>
        </div>
        <!-- 右侧 -->
        <div class="card column-card">
          <h2>我的考试</h2>
          <el-table :data="contests" style="width: 100%">
            <el-table-column prop="id" label="考试ID" align="center" />
            <el-table-column prop="start_time" label="开始时间" align="center" />
            <el-table-column prop="end_time" label="结束时间" align="center" />
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
  name: 'TeacherHome',
  components: { Navbar },
  data() {
    return {
      name: localStorage.getItem('userName'),
      questionCount: 0,
      contestCount: 0,
      questions: [],
      contests: [],
      quote: '',
      quotes: [
        "好的题目是最好的教学语言。",
        "教书育人，始于一题一解之间。",
        "每一次出题，都是一次思维的打磨。",
        "您的每一场考试，都是学生成长的阶梯。",
        "耐心引导，是教师最有力的智慧。"
      ],
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
      const teacherId = localStorage.getItem('userID');
      try {
        const qRes = await axios.get('/api/questionlist', {
          headers: { session },
          params: { teacher_id: teacherId }
        });
        this.questions = qRes.data;
        this.questionCount = this.questions.length;
      } catch (e) {
        console.error('获取题目失败', e);
      }

      try {
        const cRes = await axios.get('/api/contestlist', {
          headers: { session },
          params: {
            user_id: teacherId,
            user_role: localStorage.getItem('userRole')
          }
        });
        this.contests = cRes.data;
        this.contestCount = this.contests.length;
      } catch (e) {
        console.error('获取考试失败', e);
      }
    },
    pickQuote() {
      const index = Math.floor(Math.random() * this.quotes.length);
      this.quote = this.quotes[index];
    }
  }
};
</script>

<style scoped>
.teacher-home {
  padding: 20px;
}

/* 顶部卡片占整行 */
.top-card {
  width: 100%;
  margin-bottom: 20px;
}

/* 下方两栏平均分 */
.bottom-container {
  display: flex;
  gap: 20px;
}
.column-card {
  flex: 1;
}

/* 卡片通用样式 */
.card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 高亮样式 */
.highlight {
  color: #4A90E2;
  font-weight: bold;
}

/* 普通字体每日一言 */
.daily-quote {
  margin-top: 10px;
  font-size: 1em;
  color: #555;
  font-style: normal;
  font-weight: normal;
}

/* 当前时间样式 */
.current-time {
  margin-top: 10px;
  color: #888;
  font-size: 0.9em;
}
</style>
