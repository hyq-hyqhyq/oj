<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="dashboard-grid">
        <!-- 个人信息卡片 -->
        <div class="card user-card">
          <h2>个人信息</h2>
          <div class="user-list">
            <div class="user-item">
              <span>昵称</span>
              <span>{{ name }}</span>
            </div>
            <div class="user-item">
              <span>身份</span>
              <span>{{ roleMap[role] }}</span>
            </div>
            <div class="user-item">
              <span>助教</span>
              <span>{{ assistantName }}</span>
            </div>
          </div>
        </div>
        <!-- 做题统计卡片 -->
        <div class="card stat-card">
          <h2>做题统计</h2>
          <div class="stat-list-grid">
            <div class="stat-item">
              <span>题目总数</span>
              <span>{{ totalQuestions }}</span>
            </div>
            <div class="stat-item">
              <span>做过题数</span>
              <span>{{ numberAnswered }}</span>
            </div>
            <div class="stat-item">
              <span>通过题数</span>
              <span>{{ pass_count }}</span>
            </div>
            <div class="stat-item">
              <span>通过率</span>
              <span>{{ correctRate }}%</span>
            </div>
          </div>
        </div>
        <!-- 最近提交卡片 -->
        <div class="card submissions-card">
          <h2>最近提交</h2>
          <el-table :data="submissions" style="width: 100%" height="220">
            <el-table-column prop="id" label="提交ID" width="80" align="center"></el-table-column>
            <el-table-column prop="question_id" label="题目ID" align="center"></el-table-column>
            <el-table-column prop="status" label="结果" align="center">
              <template slot-scope="scope">
                <span :style="{ color: getStatusColor(scope.row.status) }">{{ judgeResult(scope.row.status) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="pass_rate" label="通过率" align="center"></el-table-column>
            <el-table-column prop="submit_time" label="时间" align="center"></el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
import { Pie } from 'vue-chartjs';

export default {
  components: {
    Navbar,
    PieChart: {
      extends: Pie,
      props: ['chartData'],
      mounted() {}
    }
  },
  data() {
    return {
      name: localStorage.getItem('userName'),
      role: localStorage.getItem('userRole'),
      roleMap: { '0': '学生', '1': '老师', '2': '管理员', '3': '助教' },
      totalQuestions: 0,
      numberAnswered: 0,
      pass_count: 0,
      correctRate: 0,
      assistantName: null,
      articlesCount: 0,
      submissions: [],
      chartData: {
        labels: ['Accepted', 'Wrong Answer', 'Runtime Error', 'Time Limit Exceeded', 'Memory Limit Exceeded'],
        datasets: [{
          label: 'Statistics',
          backgroundColor: ['#4fc3f7', '#ffb74d', '#e57373', '#9575cd', '#81c784'],
          data: [0, 0, 0, 0, 0]
        }]
      }
    };
  },
  mounted() {
    this.fetchInfo();
    axios.get('/api/studentlist', {
      headers: { session: localStorage.getItem('session') }
    }).then(res => {
      const me = res.data.find(s => s.id == localStorage.getItem('userID'));
      this.assistantName = me && me.assistant_name ? me.assistant_name : '暂未分配';
    }).catch(err => {
      console.error("获取学生信息失败", err);
    });
  },
  watch: {
    chartData: {
      deep: true,
      handler() {
        this.$refs.pieChart.renderChart(this.chartData, {
          responsive: true,
          maintainAspectRatio: false
        });
      }
    }
  },
  methods: {
    fetchInfo() {
      axios.get('/api/questionlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.totalQuestions = response.data.length;
        })
        .catch(error => {
          alert("获取题目列表失败: " + error.message);
        });

      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: false,
          user_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.submissions = response.data.sort((a, b) => b.id - a.id);
        })
        .catch(error => {
          alert("获取提交列表失败: " + error);
        });

      axios.get('/api/answeredquestions', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.numberAnswered = response.data.length;
        })
        .catch(error => {
          alert("获取做过的题目数失败: " + error);
        });

      axios.get('/api/communitylist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          user_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          this.articlesCount = response.data.length;
        })
        .catch(error => {
          alert("获取发表文章数失败: " + error);
        });

      axios.get('/api/statuscount', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          student_id: localStorage.getItem('userID')
        }
      })
        .then(response => {
          const { pass_count, status_count } = response.data;
          this.pass_count = pass_count;
          this.chartData.datasets[0].data = status_count;
          if (this.totalQuestions === 0) this.correctRate = 0.0
          else this.correctRate = (this.pass_count / this.totalQuestions * 100.0).toFixed(2);
        })
        .catch(error => {
          alert("获取提交结果统计数据失败: " + error);
        });
    },
    getStatusColor(status) {
      const colorMapping = {
        0: '#43a047',
        1: '#e53935',
        2: '#fb8c00',
        3: '#8e24aa',
        4: '#1e88e5'
      };
      return colorMapping[status] || '#333';
    },
    judgeResult(status) {
      const mapping = {
        0: 'Accepted',
        1: 'Runtime Error',
        2: 'Wrong Answer',
        3: 'Time Limit Exceeded',
        4: 'Memory Limit Exceeded'
      };
      return mapping[status] || 'Unknown';
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
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 220px 220px auto;
  gap: 32px;
}
.card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(89,174,235,0.10);
  padding: 8px 24px 20px 24px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-width: 0;
  min-height: 0;
}
.card h2 {
  font-size: 1.18em;
  font-weight: bold;
  color: #1565c0;
  margin-bottom: 12px;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 14px;
}

.card h2::before {
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
.user-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 1.08em;
  text-align: left; /* 左对齐 */
}
.user-card li {
  margin-bottom: 15px;
  color: #1976d2; /* 主题蓝色，更美观 */
}
.stat-card .stat-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 2px;
}
.stat-card .stat-list-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 10px;
  margin-top: 18px;
  width: 100%;
  box-sizing: border-box;
}
.stat-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  font-size: 1em;
  font-weight: 600;
  color: #1976d2;
  background: #e3f2fd;
  border-radius: 8px;
  padding: 8px 12px;      /* 调整为和 .user-item 一致 */
  min-height: 36px;       /* 和 .user-item 视觉高度一致 */
  width: 100%;
  box-sizing: border-box;
}
.stat-item span:last-child {
  align-self: center;
  font-size: 1.08em;
  margin-top: 0;
}
.chart-card {
  align-items: center;
  justify-content: center;
}
.chart-card h2 {
  margin-bottom: 18px;
}
.submissions-card {
  grid-column: span 2;
  min-height: 220px;
}
.submissions-card h2 {
  margin-bottom: 10px;
}
@media (max-width: 1100px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(4, auto);
  }
  .submissions-card {
    grid-column: span 1;
  }
}
.user-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 18px;
  width: 100%;
  box-sizing: border-box;
}
.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1em;
  font-weight: 600;
  color: #1976d2;
  background: #e3f2fd;
  border-radius: 8px;
  padding: 5px 12px;
  width: 100%;
  box-sizing: border-box;
}

.submissions-card .el-table {
  background: #f8fbff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(89,174,235,0.08);
  overflow: hidden;
  font-size: 1em;
}

.submissions-card .el-table th {
  background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
  font-weight: bold;
  font-size: 1.05em;
  border-bottom: 1.5px solid #90caf9;
}

.submissions-card .el-table td {
  background: transparent;
  color: #1976d2;
  border-bottom: 1px solid #e3f2fd;
  padding: 8px 0;
}

.submissions-card .el-table tr:hover > td {
  background: #e3f2fd !important;
  transition: background 0.2s;
}

.submissions-card .el-table__body-wrapper {
  border-radius: 0 0 12px 12px;
  overflow: hidden;
}
</style>
