<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-card">
        <h1 class="index-title">创建新考试</h1>

        <!-- 考试名称和时间部分 -->
        <div class="index-section">
          <div class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">开始时间</label>
              <input type="datetime-local" v-model="startTime" class="index-input" />
            </div>
            <div class="index-form-group">
              <label class="index-label-with-bar">截止时间</label>
              <input type="datetime-local" v-model="endTime" class="index-input" />
            </div>
          </div>
        </div>

        <!-- 添加题目部分 -->
        <div class="index-section">
          <div class="index-btn-row">
            <button @click="toggleAddQuestion" class="index-btn index-btn-primary">
              {{ showAddQuestion ? "取消添加题目" : "添加题目" }}
            </button>
          </div>
          <div v-if="showAddQuestion" class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">题目ID</label>
              <input v-model="questionId" placeholder="题目ID" class="index-input" />
            </div>
            <div class="index-form-group">
              <label class="index-label-with-bar">分值</label>
              <input v-model.number="questionScore" type="number" placeholder="分值" class="index-input" />
            </div>
            <div class="index-btn-row">
              <button @click="addQuestion" class="index-btn index-btn-success">确认添加题目</button>
            </div>
          </div>
          <table v-if="questions.length > 0" class="index-table">
            <thead>
              <tr>
                <th>题目ID</th>
                <th>分值</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(question, index) in questions" :key="index">
                <td>{{ question.id }}</td>
                <td>{{ question.score }}</td>
                <td><button @click="removeQuestion(index)" class="index-btn index-btn-danger">删除</button></td>
              </tr>
            </tbody>
          </table>
          <div class="totals" v-if="questions.length > 0">
            总题目数量: {{ questions.length }}
            总分值: {{ totalScore }}
          </div>
        </div>

        <!-- 添加学生部分 -->
        <div class="index-section">
          <div class="index-btn-row">
            <button @click="toggleAddStudent" class="index-btn index-btn-primary">
              {{ showAddStudent ? "取消添加学生" : "添加学生" }}
            </button>
          </div>
          <div v-if="showAddStudent" class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">学生ID</label>
              <input v-model="studentId" placeholder="学生ID" class="index-input" />
            </div>
            <div class="index-btn-row">
              <button @click="addStudent" class="index-btn index-btn-success">确认添加学生</button>
            </div>
          </div>
          <table v-if="students.length > 0" class="index-table">
            <thead>
              <tr>
                <th>学生ID</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in students" :key="index">
                <td>{{ student.id }}</td>
                <td><button @click="removeStudent(index)" class="index-btn index-btn-danger">删除</button></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 提交部分 -->
        <div class="index-btn-row index-submit-row">
          <button @click="submitExam" class="index-btn index-btn-primary">完成创建</button>
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
  name: 'CreateExam',
  data() {
    return {
      startTime: '',
      endTime: '',
      questionId: '',
      questionScore: '',
      studentId: '',
      questions: [],
      students: [],
      showAddQuestion: false,
      showAddStudent: false
    };
  },
  computed: {
    totalScore() {
      return this.questions.reduce((total, question) => total + parseInt(question.score), 0);
    }
  },
  methods: {
    toggleAddQuestion() {
      this.showAddQuestion = !this.showAddQuestion;
    },
    toggleAddStudent() {
      this.showAddStudent = !this.showAddStudent;
    },
    addQuestion() {
      if (this.questionId && this.questionScore) {
        this.questions.push({ id: this.questionId, score: this.questionScore });
        this.questionId = '';
        this.questionScore = '';
        this.showAddQuestion = false;
      }
    },
    removeQuestion(index) {
      this.questions.splice(index, 1);
    },
    addStudent() {
      if (this.studentId) {
        this.students.push({ id: this.studentId });
        this.studentId = '';
        this.showAddStudent = false;
      }
    },
    removeStudent(index) {
      this.students.splice(index, 1);
    },
    async validateIds() {
      const questionIds = this.questions.map(q => q.id);
      const studentIds = this.students.map(s => s.id);

      try {
        const questionCheck = await axios.post('/api/check-questions', { questionIds }, { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
        const studentCheck = await axios.post('/api/check-students', { studentIds }, { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });

        if (questionCheck.data.invalidIds.length > 0 || studentCheck.data.invalidIds.length > 0) {
          let errorMessage = '';
          if (questionCheck.data.invalidIds.length > 0) {
            errorMessage += `以下题目ID无效: ${questionCheck.data.invalidIds.join(', ')}\n`;
          }
          if (studentCheck.data.invalidIds.length > 0) {
            errorMessage += `以下学生ID无效: ${studentCheck.data.invalidIds.join(', ')}`;
          }
          alert(errorMessage);
          return false;
        }
        return true;
      } catch (error) {
        alert('验证ID时出错，请重试。');
        return false;
      }
    },
    async submitExam() {
      if (this.startTime && this.endTime) {
        const valid = await this.validateIds();
        if (!valid) return;

        try {
          const examResponse = await axios.post('/api/contest', {
            teacher_id: localStorage.getItem('userID'),
            start_time: this.startTime,
            end_time: this.endTime,
          }, { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });

          if (examResponse.status === 201) {
            const examId = examResponse.data.id;

            for (const question of this.questions) {
              await axios.post('/api/contest-question', {
                exam_id: examId,
                question_id: question.id,
                score: question.score
              }, { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
            }

            for (const student of this.students) {
              await axios.post('/api/contest-student', {
                exam_id: examId,
                student_id: student.id,
              }, { headers: { 'session': localStorage.getItem('session'), 'Content-Type': 'application/json' } });
            }

            alert('考试创建成功！');
          } else {
            alert('创建考试时出错，请重试。');
          }
        } catch (error) {
          alert('创建考试时出错，请重试。');
        }
      } else {
        alert('请填写完整的考试信息！');
      }
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
}
.index-section:last-child {
  border-bottom: none;
}
.index-section-title {
  font-size: 1.2rem;
  color: #1976d2;
  font-weight: 600;
  margin-bottom: 18px;
  letter-spacing: 1px;
}
.index-form-group {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
}
.index-form-group label {
  font-weight: 500;
  color: #1565c0;
  margin-bottom: 7px;
  font-size: 1rem;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 14px;
  letter-spacing: 0.5px;
}
.index-label-with-bar::before {
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
.index-input,
.index-textarea,
.el-select.index-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #cfd8dc;
  border-radius: 6px;
  font-size: 16px;
  background: #f7fbff;
  transition: border 0.2s;
  box-sizing: border-box;
}
.index-input:focus,
.index-textarea:focus {
  border-color: #1976d2;
  outline: none;
  background: #fff;
}
.index-form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}
.index-form-row .index-form-group {
  flex: 1;
  min-width: 220px;
}
.index-btn-row {
  display: flex;
  justify-content: center;
  margin-top: 10px;
  flex-wrap: wrap;
}
.index-btn {
  padding: 10px 28px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin: 0 8px 8px 0;
  transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
}
.index-btn-primary {
  background: #1976d2;
  color: #fff;
}
.index-btn-primary:hover {
  background: #1257e1;
  transform: translateY(-2px);
}
.index-btn-success {
  background: #43a047;
  color: #fff;
}
.index-btn-success:hover {
  background: #2e7d32;
  transform: translateY(-2px);
}
.index-btn-danger {
  background: #e53935;
  color: #fff;
}
.index-btn-danger:hover {
  background: #b71c1c;
  transform: translateY(-2px);
}
.index-submit-row {
  margin-top: 36px;
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
  padding: 10px;
  text-align: left;
  font-size: 16px;
}
.index-table th {
  background-color: #e3f2fd;
  font-weight: bold;
  color: #1976d2;
}
.totals {
  margin-top: 10px;
  font-weight: bold;
  color: #333;
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
  .index-form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>