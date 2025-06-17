<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-card">
        <h1 class="index-title">{{ examName }}</h1>
        <div class="index-section exam-info-row">
          <div class="exam-info-item">开始时间: <span class="blue-text">{{ examStartTime | formatDate }}</span></div>
          <div class="exam-info-item">截止时间: <span class="blue-text">{{ examEndTime | formatDate }}</span></div>
          <div v-if="userRole == 0" class="exam-info-item">当前总分: <span class="blue-text">{{ totalScore }}</span></div>
        </div>
        <div class="index-section">
          <el-table
            :data="filteredQuestions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            class="index-table"
            border
            stripe
          >
            <el-table-column prop="id" label="ID" width="100" align="center" />
            <el-table-column prop="title" label="标题" align="center" />
            <el-table-column prop="difficulty" label="难度" width="120" align="center">
              <template slot-scope="scope">
                <span :class="getDifficultyClass(scope.row.difficulty)">{{ getDifficultyLabel(scope.row.difficulty) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default="scope">
                <button class="index-btn index-btn-success" @click="enterQuestion(scope.row.id)">进入</button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @current-change="handlePageChange"
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="[5, 10, 20, 30]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredQuestions.length"
            class="index-pagination"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'QuestionList',
  components: {
    Navbar,
  },
  data() {
    return {
      examName: '',
      examStartTime: '',
      examEndTime: '',
      questions: [],
      contestQuestions: [],
      currentPage: 1,
      pageSize: 20,
      userRole: parseInt(localStorage.getItem('userRole')),
      totalScore: 0,
    };
  },
  computed: {
    filteredQuestions() {
      return this.questions.filter(question => this.contestQuestions.includes(question.id));
    }
  },
  mounted() {
    this.fetchExamInfo();
    this.fetchContestQuestions();
    if (this.userRole == 0) {
      this.fetchTotalScore();
    }
  },
  methods: {
    fetchExamInfo() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contest`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: { contest_id: contestId }
      })
      .then(response => {
        this.examName = response.data.name;
        this.examStartTime = response.data.start_time;
        this.examEndTime = response.data.end_time;
      })
      .catch(error => {
        alert('获取考试信息失败: ' + error.response.data.message);
      });
    },
    fetchContestQuestions() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contest-question`, { params: { contest_id: contestId }})
      .then(response => {
        this.contestQuestions = response.data.questionIds;
        this.fetchQuestions();
        if (this.contestQuestions.length === 0) {
          alert("该考试没有题目");
          this.$router.push({ name: 'contest-list' });
        }
      })
      .catch(error => {
        alert("获取考试题目列表失败: " + error.response.data.message);
      });
    },
    fetchQuestions() {
      axios.get(`/api/questionlist`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
      .then(response => {
        this.questions = response.data.map(question => ({
          ...question,
          accuracy: 0
        }));
      })
      .catch(error => {
        alert("获取题目列表失败: " + error.response.data.message);
      });
    },
    fetchTotalScore() {
      const examId = this.$route.params.id;
      const studentId = localStorage.getItem('userID');
      axios.get(`/api/getscore`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          exam_id: examId,
          student_id: studentId
        }
      })
      .then(response => {
        this.totalScore = response.data.score;
      })
      .catch(error => {
        alert("获取总分失败: " + error.response.data.message);
      });
    },
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question-contest', params: { questionId: id, examId: this.$route.params.id }});
    },
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    getDifficultyLabel(difficulty) {
      switch (difficulty) {
        case 1: return '简单';
        case 2: return '中等';
        case 3: return '困难';
        case 4: return '挑战';
        case 5: return '地狱';
        default: return '未知';
      }
    },
    getDifficultyClass(difficulty) {
      switch (difficulty) {
        case 1: return 'difficulty-easy';
        case 2: return 'difficulty-medium';
        case 3: return 'difficulty-hard';
        case 4: return 'difficulty-challenge';
        case 5: return 'difficulty-hell';
        default: return '';
      }
    }
  },
  filters: {
    formatDate(date) {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleString();
    }
  }
};
</script>

<style scoped>
.index-bg {
  min-height: 100vh;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(120deg, #e0eafc 0%, #cfdef3 100%);
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  display: flex;
  flex-direction: row;
}
.index-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  margin-left: 210px;
  min-width: 0;
  min-height: 100vh;
  box-sizing: border-box;
  padding: 0 16px;
}
.index-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 123, 255, 0.08), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 36px 32px 32px 32px;
  margin-top: 32px;
  max-width: 1100px;
  width: 100%;
}
.index-title {
  text-align: center;
  font-size: 2.2rem;
  color: #1976d2;
  font-weight: 700;
  margin-bottom: 32px;
  letter-spacing: 2px;
}
.index-section {
  margin-bottom: 32px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
  background: transparent;
}
.index-section:last-child {
  border-bottom: none;
}
.exam-info-row {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: center;
  background: transparent;
  border: none;
  margin-bottom: 0;
  padding-bottom: 0;
}
.exam-info-item {
  font-size: 1.08em;
  color: #1976d2;
  font-weight: 500;
  margin: 0 10px;
}
.blue-text {
  color: #1976d2;
  font-weight: bold;
}
.index-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
  background: #f7fbff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.04);
}
.index-table th,
.index-table td {
  border: 1px solid #cfd8dc;
  padding: 12px 15px;
  text-align: center;
  font-size: 16px;
}
.index-table th {
  background-color: #e3f2fd;
  font-weight: bold;
  color: #1976d2;
}
.index-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
.index-btn {
  padding: 8px 22px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin: 0 8px 8px 0;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
}
.index-btn-success {
  background: #43a047;
  color: #fff;
}
.index-btn-success:hover {
  background: #2e7d32;
  transform: translateY(-2px);
}
.index-pagination {
  margin-top: 24px;
  text-align: center;
}
.difficulty-easy {
  background-color: #43a047;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
}
.difficulty-medium {
  background-color: #1976d2;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
}
.difficulty-hard {
  background-color: #ff9800;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
}
.difficulty-challenge {
  background-color: #8e24aa;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
}
.difficulty-hell {
  background-color: #e53935;
  color: #fff;
  padding: 5px 10px;
  border-radius: 5px;
}
@media (max-width: 1100px) {
  .index-container {
    margin-left: 0;
    padding: 0 4px;
  }
  .index-card {
    max-width: 100%;
  }
}
@media (max-width: 700px) {
  .index-card {
    padding: 18px 6px 18px 6px;
  }
  .exam-info-row {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
