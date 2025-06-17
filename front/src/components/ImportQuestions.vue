<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-card">
        <h1 class="index-title">创建题目</h1>
        <div class="index-section">
          <div class="index-form-group">
            <label class="index-label-with-bar">题目标题</label>
            <input v-model="newQuestion.title" placeholder="题目标题" class="index-input" />
          </div>
          <div class="index-form-group">
            <label class="index-label-with-bar">建表语句</label>
            <textarea v-model="newQuestion.create_code" placeholder="建表语句" class="index-textarea"></textarea>
          </div>
          <div class="index-form-group">
            <label class="index-label-with-bar">题目描述</label>
            <textarea v-model="newQuestion.description" placeholder="题目描述" class="index-textarea"></textarea>
          </div>
          <div class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">输入示例</label>
              <textarea v-model="newQuestion.input_example" placeholder="输入示例" class="index-textarea"></textarea>
            </div>
            <div class="index-form-group">
              <label class="index-label-with-bar">输出示例</label>
              <textarea v-model="newQuestion.output_example" placeholder="输出示例" class="index-textarea"></textarea>
            </div>
          </div>
          <div class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">难度</label>
              <el-select v-model="newQuestion.difficulty" placeholder="选择难度" class="index-input">
                <el-option label="1 - 简单" value="1" />
                <el-option label="2 - 中等" value="2" />
                <el-option label="3 - 困难" value="3" />
                <el-option label="4 - 挑战" value="4" />
                <el-option label="5 - 地狱" value="5" />
              </el-select>
            </div>
            <div class="index-form-group index-checkbox-group">
              <el-checkbox v-model="newQuestion.is_public" class="index-checkbox-large">
                <span class="index-label-checkbox">公开题目</span>
              </el-checkbox>
            </div>
          </div>
        </div>
        <div class="index-section">
          <h2 class="index-section-title">添加测试点</h2>
          <div v-for="(testCase, index) in testCases" :key="index" class="index-testcase-card">
            <div class="index-form-row">
              <div class="index-form-group">
                <label class="index-label-with-bar">输入数据</label>
                <textarea v-model="testCase.input_sql" placeholder="输入数据， 即向测试表插入数据的SQL语句" class="index-textarea"></textarea>
              </div>
              <div class="index-form-group">
                <label class="index-label-with-bar">输出数据</label>
                <textarea v-model="testCase.output" placeholder="输出数据，  即对应输入数据的标准输出" class="index-textarea"></textarea>
              </div>
            </div>
            <div class="index-btn-row">
              <button @click="removeTestCase(index)" class="index-btn index-btn-danger">删除测试点</button>
            </div>
          </div>
          <div class="index-btn-row">
            <button @click="addTestCase" class="index-btn index-btn-success">添加测试点</button>
          </div>
        </div>
        <div class="index-btn-row index-submit-row">
          <button @click="createQuestionWithTestCases" class="index-btn index-btn-primary">创建题目</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'ImportQuestion',
  components: {
    Navbar
  },
  data() {
    return {
      newQuestion: {
        title: '',
        create_code: '',
        description: '',
        input_example: '',
        output_example: '',
        difficulty: '1',
        answer_example: '',
        is_public: true,
        tablename: ''
      },
      testCases: [
        { input_sql: '', output: '' }
      ]
    };
  },
  methods: {
    addTestCase() {
      this.testCases.push({ input_sql: '', output: '' });
    },
    removeTestCase(index) {
      this.testCases.splice(index, 1);
    },
    createQuestionWithTestCases() {
      const teacherId = parseInt(localStorage.getItem('userID'));
      const session   = localStorage.getItem('session');
      const questionPayload = {
        ...this.newQuestion,
        teacher_id: teacherId
      };
      axios.post(
        '/api/question',
        questionPayload,
        {
          headers: {
            'session':       session,
            'Content-Type': 'application/json'
          }
        }
      )
      .then(response => {
        const questionId = response.data.question_id;
        const testCases = this.testCases.map(testCase => ({
          ...testCase,
          tablename:   this.newQuestion.tablename,
          question_id: questionId
        }));
        return axios.post(
          '/api/testcase',
          {
            test_cases:   testCases,
            question_id:  questionId
          },
          {
            headers: {
              'session':       session,
              'Content-Type': 'application/json'
            }
          }
        );
      })
      .then(response => {
        this.newQuestion = {
          title:          '',
          create_code:    '',
          description:    '',
          input_example:  '',
          output_example: '',
          difficulty:     '1',
          answer_example: '',
          is_public:      true,
          tablename:      ''
        };
        this.testCases = [{ input_sql: '', output: '' }];
        alert(`成功: ${response.data.message}`);
      })
      .catch(error => {
        const errMsg = (error.response && error.response.data && error.response.data.message) || '未知错误';
        alert(`失败: ${errMsg}`);
      });
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
  padding-bottom: 40px;
  margin: 0;
  overflow-x: hidden;
  /* 使用flex让内容在导航栏右侧区域垂直水平居中 */
  display: flex;
  flex-direction: row;
}
.index-container {
  /* 预留左侧210px导航栏空间，并在剩余空间居中 */
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
@media (max-width: 1100px) {
  .index-container {
    margin-left: 0;
    padding: 0 4px;
  }
  .index-card {
    max-width: 100%;
  }
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
/* 公开题目专用样式，无蓝边，字号更大 */
.index-checkbox-large {
  font-size: 1.25rem !important;
  min-height: 40px;
  display: flex;
  align-items: center;
}
.index-label-checkbox {
  font-size: 1.18em;
  font-weight: bold;
  color: #1565c0;
  letter-spacing: 1px;
  padding-left: 4px;
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
.index-textarea {
  min-height: 100px;
  resize: vertical;
}
.index-form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 18px;
}
.index-form-row .index-form-group {
  flex: 1;
}
.index-checkbox-group {
  display: flex;
  align-items: center;
  margin-top: 30px;
}
.index-testcase-card {
  background: #f5faff;
  border: 1px solid #e3eaf2;
  border-radius: 10px;
  padding: 18px 18px 10px 18px;
  margin-bottom: 18px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.04);
}
.index-btn-row {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}
.index-btn {
  padding: 10px 28px;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin: 0 8px;
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
  background: #1976d2;;
  color: #fff;
}
.index-btn-success:hover {
  background: #1257e1;
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