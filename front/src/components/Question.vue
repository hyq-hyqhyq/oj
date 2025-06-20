<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="card question-card">
        <h2>题目列表</h2>
        <div class="section-container">
          <el-table
            :data="filteredQuestions.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
            style="width: 100%"
            border
            stripe
          >
            <el-table-column prop="id" label="ID" width="100" align="center" />
            <el-table-column prop="title" label="标题" align="center" />
            <el-table-column label="操作" width="150" align="center">
              <template #default="scope">
                <el-button @click="enterQuestion(scope.row.id)" type="success" size="small">进入</el-button>
                <el-button
                  v-if="canDeleteQuestions"
                  @click="deleteQuestion(scope.row.id)"
                  type="danger"
                  size="small"
                >
                  删除
                </el-button>
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
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios';

export default {
  name: 'QuestionList',
  components: {
    Navbar
  },
  data() {
    return {
      questions: [],
      currentPage: 1,
      pageSize: 20,
      searchQuery: '',
      filterType: 'all', // 默认显示全部
      randomMode: false,
      randomQuestionId: null,
      userId: localStorage.getItem('userID'), // 获取 userId
    };
  },
  computed: {
    canDeleteQuestions() {
      return localStorage.getItem('userRole') === '1'; // 判断是否为教师角色
    },
    filteredQuestions() {
      // 根据搜索和筛选条件过滤题目
      return this.questions.filter(question => 
        this.filterQuestion(question)
      );
    }
  },
  mounted() {
    this.fetchQuestions();
  },
  methods: {
    // 获取题目列表
    fetchQuestions() {
      axios.get(`/api/questionlist`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: this.userId
        }
      })
      .then(response => {
        this.questions = response.data.map(question => ({
          ...question
        }));
      })
      .catch(error => {
        alert("获取题目列表失败:", error);
      });
    },
    // 根据筛选条件过滤题目
    filterQuestion(question) {
      const matchesSearch = question.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      const matchesPublic = question.is_public;
      if (this.filterType === 'all') {
        return matchesSearch && matchesPublic;
      } else {
        return question.difficulty == this.filterType && matchesSearch && matchesPublic;
      }
    },
    // 进入题目详情
    enterQuestion(id) {
      this.$router.push({ name: 'answer-question', params: { id: id } });
    },
    // 删除题目
    deleteQuestion(questionId) {
      const userId = localStorage.getItem('userID');  // 获取当前用户的ID
      if (confirm("确定要删除该题目吗？")) {
        axios.delete(`/api/question/${questionId}`, {
          headers: {
            'session': localStorage.getItem('session')  // 确保传递 session
          },
          params: {
            user_id: userId  // 传递当前用户ID
          }
        })
        .then(response => {
          alert("题目已删除！");
          this.fetchQuestions();  // 刷新题目列表
        })
        .catch(error => {
          const errorMessage = error.response && error.response.data && error.response.data.message
            ? error.response.data.message
            : error.message;
          alert("删除失败！" + errorMessage);
        });
      }
    },

    // 处理分页
    handlePageChange(newPage) {
      this.currentPage = newPage;
    },
    randomQuestion() {
      const publicQuestions = this.questions.filter(question => question.is_public);
      const randomIndex = Math.floor(Math.random() * publicQuestions.length);
      this.randomQuestionId = publicQuestions[randomIndex].id;
      this.randomMode = true;
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
      return {
        'difficulty-easy': difficulty === 1,
        'difficulty-medium': difficulty === 2,
        'difficulty-hard': difficulty === 3,
        'difficulty-challenge': difficulty === 4,
        'difficulty-hell': difficulty === 5,
      };
    },
    refreshPage() {
      location.reload();
    }
  }
}
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
  padding: 40px 0 40px 0;
  min-height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card.question-card {
  width: 1000px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(89,174,235,0.10);
  padding: 24px 28px 28px 28px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-width: 0;
  min-height: 0;
  margin-top: 40px;
}
.card.question-card h2 {
  font-size: 1.35em;
  font-weight: bold;
  color: #1565c0;
  margin-bottom: 18px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 16px;
}
.card.question-card h2::before {
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
.section-container {
  background-color: #ffffff;
  padding: 20px 0 0 0;
  border-radius: 10px;
  box-shadow: none;
}
.el-table {
  background: #f8fbff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(89,174,235,0.08);
  overflow: hidden;
  font-size: 1em;
}
.el-table th {
  background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
  font-weight: bold;
  font-size: 1.05em;
  border-bottom: 1.5px solid #90caf9;
}
.el-table td {
  background: transparent;
  color: #1976d2;
  border-bottom: 1px solid #e3f2fd;
  padding: 8px 0;
}
.el-table tr:hover > td {
  background: #e3f2fd !important;
  transition: background 0.2s;
}
.el-pagination {
  margin-top: 18px;
  text-align: right;
}
.create-question-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.section-container {
  margin-bottom: 20px;
  background-color: #ffffff;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.header-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #007bff;
  font-weight: bold;
}

.button-bar {
  text-align: center;
  margin-bottom: 20px;
}

.button-bar .random-button,
.button-bar .refresh-button {
  margin-left: 10px;
}

.search-bar {
  display: flex;
  flex-direction: column; /* 纵向排列 */
  margin-bottom: 20px;
}

.search-input {
  max-width: 100%;
  flex: 1;
  margin-bottom: 20px;
}

.difficulty-filter {
  display: flex;
  align-items: center;
}

.search-tip {
  margin-left: 10px;
  margin-right: 10px;
  color: #666;
  white-space: nowrap; /* 防止文字换行 */
}

.filter-select {
  width: 100px;
}

.el-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px 15px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  color: #333;
  font-weight: bold;
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 16px;
}

td {
  text-align: center;
  font-family: 'Arial', sans-serif;
  font-size: 14px;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}

.difficulty-easy {
  background-color: green;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-medium {
  background-color: blue;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hard {
  background-color: orange;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-challenge {
  background-color: purple;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.difficulty-hell {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.completed-true {
  background-color: green;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}

.completed-false {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>