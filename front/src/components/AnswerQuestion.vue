<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-main-content">
        <div class="index-card">
          <h1 class="index-title">{{ question.title }}</h1>
          <div class="index-section">
            <h2 class="index-section-title">题目介绍</h2>
            <div class="index-desc">{{ question.description }}</div>
          </div>
          <div class="index-form-row">
            <div class="index-form-group">
              <label class="index-label-with-bar">示例输入</label>
              <pre v-html="highlightedCode(question.input_example, 'sql')" class="index-code"></pre>
            </div>
            <div class="index-form-group">
              <label class="index-label-with-bar">示例输出</label>
              <pre v-html="highlightedCode(question.output_example, 'sql')" class="index-code"></pre>
            </div>
          </div>
          <div class="index-section">
            <h2 class="index-section-title">建表语句</h2>
            <pre v-html="highlightedCode(question.create_code, 'sql')" class="index-code"></pre>
          </div>
          <div class="index-section">
            <h2 class="index-section-title">做题区域</h2>
            <el-input
              type="textarea"
              v-model="userAnswer"
              placeholder="在这里编写你的SQL代码..."
              class="index-textarea"
            ></el-input>
            <div class="index-btn-row">
              <el-button
                type="primary"
                @click="submitAnswer"
                class="index-btn index-btn-primary"
              >
                提交代码
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <div class="index-sidebar">
        <div class="index-card">
          <h2 class="index-section-title">题目信息</h2>
          <div class="index-info-list">
            <p><strong>题目ID：</strong>{{ question.id }}</p>
            <p><strong>题目难度：</strong>{{ getDifficultyLabel(question.difficulty) }}</p>
            <p><strong>已完成？</strong> {{ question.completed ? '是' : '否' }}</p>
            <p><strong>通过率：</strong> {{ question.accuracy }}%</p>
            <p><strong>完成率：</strong> {{ question.completion_rate }}%</p>
            <p><strong>提交数：</strong> {{ question.submission_count }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      question: {
        title: '',
        create_code: '',
        description: '',
        input_example: '',
        output_example: '',
        difficulty: 1,
        answer_example: '',
        is_public: true,
        completed: false,
        accuracy: null,
        completion_rate: null,
        submission_count: null,
        id: ''
      },
      userAnswer: '',
      userid: localStorage.getItem('userID'),
      userRole: localStorage.getItem('userRole'),
      submitResult: null
    };
  },
  mounted() {
    this.fetchQuestion();
  },
  methods: {
    fetchQuestion() {
      const questionId = this.$route.params.id;
      axios.get(`/api/question`, {
        headers: {
          'session': localStorage.getItem('session'),
        },
        params: {
          question_id: questionId,
          student_id: this.userid
        }
      })
      .then(response => {
        this.question = response.data;
      })
      .catch(error => {
        alert(`获取题目信息失败: ${error.response.data.message}`);
      });
    },
    submitAnswer() {
      axios.post(`/api/submit`, { 
        student_id: localStorage.getItem('userID'),
        exam_id: null,
        submit_sql: this.userAnswer,
        submit_time: new Date().toISOString(),
        question_id: this.$route.params.id,
      }, {
        headers: {
          'session': localStorage.getItem('session'),
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        const submit_id = response.data.submit_id;
        return axios.post('/api/judge', {
          submit_sql: this.userAnswer,
          question_id: this.$route.params.id,
          create_code: this.question.create_code,
          submit_id: submit_id
        }, {
          headers: {
            'session': localStorage.getItem('session'),
            'Content-Type': 'application/json'
          }
        });
      })
      .then(response => {
        this.submitResult = response.data.result;
        alert(`判题结果: ${JSON.stringify(this.submitResult)}`);
      })
      .catch(error => {
        alert(`提交答案失败: ${error.response.data.message}`);
      });
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
    highlightedCode(code, language) {
      if (!code) return '';
      return hljs.highlight(code, { language }).value;
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
  flex-direction: row;
  align-items: flex-start;
  justify-content: center;
  margin-left: 210px;
  min-width: 0;
  min-height: 100vh;
  box-sizing: border-box;
  padding: 32px 16px 0 16px;
  gap: 32px;
}
.index-main-content {
  flex: 3;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.index-sidebar {
  flex: 1;
  min-width: 260px;
  max-width: 320px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}
.index-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 123, 255, 0.08), 0 1.5px 6px rgba(0,0,0,0.04);
  padding: 32px 28px 28px 28px;
  margin-bottom: 0;
  width: 100%;
  box-sizing: border-box;
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
  margin-bottom: 24px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}
.index-section:last-child {
  border-bottom: none;
}
.index-section-title {
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
.index-section-title::before {
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
.index-form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 18px;
}
.index-form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.index-label-with-bar {
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
.index-desc {
  font-size: 16px;
  color: #666;
  line-height: 1.7;
  margin-bottom: 0;
  white-space: pre-wrap;
}
.index-code {
  background: #f5f5f5;
  border-radius: 5px;
  padding: 10px;
  font-family: 'Source Code Pro', monospace;
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-x: auto;
  font-size: 15px;
  color: #333;
}
.index-textarea {
  width: 100%;
  min-height: 180px;
  margin-top: 18px;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #cfd8dc;
  border-radius: 6px;
  background: #f7fbff;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.06);
  transition: border 0.2s;
  resize: vertical;
}
.index-textarea:focus {
  border-color: #1976d2;
  outline: none;
  background: #fff;
}
.index-btn-row {
  display: flex;
  justify-content: center;
  margin-top: 18px;
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
.index-info-list p {
  font-size: 15px;
  color: #444;
  margin: 10px 0;
  line-height: 1.6;
}
@media (max-width: 1100px) {
  .index-container {
    margin-left: 0;
    padding: 0 4px;
    flex-direction: column;
    gap: 0;
  }
  .index-main-content, .index-sidebar {
    max-width: 100%;
  }
}
@media (max-width: 900px) {
  .index-container {
    flex-direction: column;
    gap: 0;
  }
  .index-main-content, .index-sidebar {
    max-width: 100%;
  }
}
@media (max-width: 700px) {
  .index-card {
    padding: 18px 6px 18px 6px;
  }
  .index-container {
    flex-direction: column;
    gap: 0;
    padding: 0 2px;
  }
  .index-main-content, .index-sidebar {
    max-width: 100%;
    min-width: 0;
  }
  .index-form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
