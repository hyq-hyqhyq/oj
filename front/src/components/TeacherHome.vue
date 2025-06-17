<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="dashboard-grid">
        <div class="card teacher-home-card">
          <div class="teacher-home">
            <div class="card top-card">
              <h2>教师首页</h2>
              <h1>欢迎回来，教师<span class="highlight">{{ name }}</span></h1>
            </div>
            <div class="bottom-container">
              <div class="card column-card">
                <h2>我的题目</h2>
                <el-table :data="questions" style="width: 100%">
                  <el-table-column prop="id" label="题目ID" align="center" />
                  <el-table-column prop="title" label="标题" align="center" />
                  <el-table-column prop="difficulty" label="难度" align="center" />
                </el-table>
              </div>
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
.card.teacher-home-card {
  background: transparent;
  border-radius: 18px;
  box-shadow: none;
  padding: 24px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  width: 100%;
  max-width: 1240px;
  margin: 0 auto;
}
.card.teacher-home-card h2 {
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
.card.teacher-home-card h2::before {
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
  gap: 5px;
  flex-wrap: wrap;
  justify-content: space-between;
}
.column-card {
  flex: 1;
  width: 100%;
  min-width: 260px;
  max-width: 600px;
  margin: 0 10px;
  background: none;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  display: flex;
  flex-direction: column;
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

@media (max-width: 1200px) {
  .card.teacher-home-card {
    max-width: 90vw;
  }
  .bottom-container {
    flex-direction: column;
    gap: 16px;
  }
  .column-card {
    max-width: 100%;
    margin: 0;
  }
}
@media (max-width: 700px) {
  .card.teacher-home-card {
    max-width: 98vw;
    padding: 12px 6px;
  }
}
</style>
