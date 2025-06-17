<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="card submit-card">
        <div class="card-header-row">
          <h2>提交记录</h2>
          <div class="search-bar">
            <el-input
              type="text"
              class="search-field"
              v-model="searchQuery"
              placeholder="搜索题目ID..."
              clearable
            ></el-input>
          </div>
        </div>
        <div class="section-container">
          <div class="side-and-table">
            <el-menu :default-active="'1'" class="side-menu" @select="handleSelect">
              <el-menu-item index="1">所有记录</el-menu-item>
              <el-menu-item index="2">我的记录</el-menu-item>
            </el-menu>
            <el-table :data="filteredSubmissions" class="records-table" border stripe>
              <el-table-column prop="id" label="提交ID" min-width="120" align="center"></el-table-column>
              <el-table-column prop="submit_time" label="提交时间" min-width="150" align="center">
                <template slot-scope="scope">
                  {{ scope.row.submit_time | formatDate }}
                </template>
              </el-table-column>
              <el-table-column prop="question_id" label="题目ID" min-width="120" align="center"></el-table-column>
              <el-table-column v-if="currentTab === '1'" prop="student_id" label="用户ID" min-width="120" align="center"></el-table-column>
              <el-table-column v-if="currentTab === '2'" prop="submit_sql" label="提交代码" min-width="140" align="center">
                <template slot-scope="scope">
                  <el-button @click="showCode(scope.row.submit_sql)" type="success" size="small">点击查看</el-button>
                </template>
              </el-table-column>
              <el-table-column prop="status" label="结果" min-width="150" align="center">
                <template slot-scope="scope">
                  <span :style="{ color: getStatusColor(scope.row.status) }">{{ judgeResult(scope.row.status) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="pass_rate" label="得分" min-width="120" align="center"></el-table-column>
            </el-table>
          </div>
        </div>
        <el-dialog :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
          <template slot="title">
            <span>提交代码</span>
          </template>
          <pre ref="code" class="code-display">{{ codeToShow }}</pre>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">关闭</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios'; 

export default {
  name: 'Submissions',
  components: {
    Navbar
  },
  data() {
    return {
      submissions: [],
      searchQuery: '',
      dialogVisible: false,
      codeToShow: '',
      currentTab: '1'
    };
  },
  mounted() {
    this.handleSelect('1');
  },
  computed: {
    filteredSubmissions() {
      if (!this.searchQuery.trim()) {
        return this.submissions;
      } else {
        const query = this.searchQuery.trim().toLowerCase();
        return this.submissions.filter(submission =>
          submission.question_id.toString().toLowerCase().includes(query)
        );
      }
    }
  },
  methods: {
    handleSelect(index) {
      this.currentTab = index;
      if (index === '1') {
        this.fetchAll();
      } else if (index === '2') {
        this.fetchMine();
      }
    },
    fetchAll() {
      axios.get('/api/submitlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          fetchall: true
        }
      })
        .then(response => {
          this.submissions = response.data.sort((a, b) => b.id - a.id);
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    fetchMine() {
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
          alert(`失败: ${error.response.data.message}`);
        });
    },
    judgeResult(status) {
      const mapping = [
        'Pending',
        'Accepted',
        'Runtime error',
        "Wrong answer",
        "Time limit exceeded",
        "Memery limit exceeded",
      ];
      return mapping[status + 1];
    },
    getStatusColor(status) {
      const colorMapping = [
        'grey',
        'green',
        'red',
        'orange',
        'purple',
        'blue',
      ];
      return colorMapping[status + 1] || 'black';
    },
    showCode(submitSql) {
      this.codeToShow = submitSql;
      this.dialogVisible = true;
    }
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleString();
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
  padding: 40px 0 40px 0;
  min-height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card.submit-card {
  width: 1100px;
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
.card-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}
.card-header-row h2 {
  font-size: 1.35em;
  font-weight: bold;
  color: #1565c0;
  margin-bottom: 0;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  position: relative;
  padding-left: 16px;
}
.card-header-row h2::before {
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
  padding: 0;
  border-radius: 10px;
  box-shadow: none;
  /* 新增：去除原有的 block 布局 */
}

.side-and-table {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 24px;
}

.side-menu {
  width: 180px;
  border-radius: 10px;
  margin-bottom: 0;
  flex-shrink: 0;
}

.records-table {
  flex: 1;
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
.code-display {
  font-family: 'Source Code Pro', 'Consolas', 'Unifont', monospace;
  background-color: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  white-space: pre-wrap;
  overflow-x: auto;
  text-align: left;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
.dialog-footer {
  text-align: right;
}
</style>
