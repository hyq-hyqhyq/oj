<template>
  <div class="main-bg">
    <Navbar />
    <div class="main-content">
      <div class="card contest-card">
        <div class="card-header-row">
          <h2>考试列表</h2>
          <div class="filter-container">
            <el-select v-model="filterStatus" placeholder="筛选考试状态" @change="filterContests">
              <el-option label="全部" value="all"></el-option>
              <el-option label="未开始" value="not_started"></el-option>
              <el-option label="进行中" value="ongoing"></el-option>
              <el-option label="已结束" value="ended"></el-option>
            </el-select>
          </div>
        </div>
        <div class="section-container">
          <table class="el-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>教师ID</th>
                <th>开始时间</th>
                <th>结束时间</th>
                <th>状态</th>
                <th>操作</th>
                <th v-if="userRole === 0">考试成绩</th>
                <th v-if="userRole !== 0">查看答题</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="contest in filteredContests" :key="contest.id">
                <td>{{ contest.id }}</td>
                <td>{{ contest.teacher_id }}</td>
                <td>{{ formatTime(contest.start_time) }}</td>
                <td>{{ formatTime(contest.end_time) }}</td>
                <td>
                  <span :class="getStatusClass(contest.status)">{{ getStatusText(contest.status) }}</span>
                </td>
                <td>
                  <button 
                    @click="goToContestQuestions(contest.id)" 
                    :disabled="contest.status !== 'ongoing'"
                    :class="{ 'disabled-button': contest.status !== 'ongoing' }"
                  >
                    开始考试
                  </button>
                  <button 
                    @click="deleteContest(contest.id)" 
                    style="margin-left: 8px; background-color: #d9534f;"
                  >
                    删除考试
                  </button>
                </td>
                <td v-if="userRole === 0">
                  <button @click="viewMyScore(contest.id)">考试成绩</button>
                </td>
                <td v-if="userRole !== 0">
                  <button @click="viewScores(contest.id)">查看答题</button>
                </td>
              </tr>
            </tbody>
          </table>
          <el-dialog
            title="考试成绩"
            :visible.sync="scoreDialogVisible"
            width="400px"
            :before-close="() => { scoreDialogVisible = false }"
          >
            <div v-if="scoreLoading" style="text-align:center;padding:30px 0;">
              <span>正在加载成绩...</span>
            </div>
            <div v-else-if="myScore !== null">
              <p style="font-size:1.2em;text-align:center;">
                您的成绩：<span style="color:#1976d2;font-weight:bold;">{{ myScore }}</span>
              </p>
            </div>
            <div v-else style="text-align:center;color:#888;">
              暂无成绩
            </div>
            <span slot="footer" class="dialog-footer">
              <el-button @click="scoreDialogVisible = false">关闭</el-button>
            </span>
          </el-dialog>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'Contest',
  components: {
    Navbar
  },
  data() {
    return {
      contests: [],
      filteredContests: [],
      filterStatus: '',
      userRole: parseInt(localStorage.getItem('userRole')),
      scoreDialogVisible: false,
      myScore: null,
      scoreLoading: false
    };
  },
  created() {
    this.fetchContests();
  },
  methods: {
    fetchContests() {
      const userId = localStorage.getItem('userID');
      const userRole = localStorage.getItem('userRole');
      axios.get('/api/contestlist', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          user_id: userId,
          user_role: userRole
        }
      })
      .then(response => {
        this.contests = response.data.map(contest => {
          return {
            ...contest,
            status: this.getContestStatus(contest.start_time, contest.end_time)
          };
        });
        this.filteredContests = this.contests;
      })
      .catch(error => {
        alert("获取考试列表时发生错误！", error);
      });
    },
    deleteContest(contestId) {
      if (confirm("确定要删除该考试吗？")) {
        axios.delete(`/api/contest/${contestId}`, {
          headers: { 'session': localStorage.getItem('session') }
        })
        .then(() => {
          alert("考试已删除！");
          this.fetchContests();
        })
        .catch(error => {
          alert("删除失败！" + ((error.response && error.response.data && error.response.data.message) ? error.response.data.message : error.message));
        });
      }
    },
    getContestStatus(startTime, endTime) {
      const now = new Date();
      const start = new Date(startTime);
      const end = new Date(endTime);

      if (now < start) {
        return 'not_started';
      } else if (now > end) {
        return 'ended';
      } else {
        return 'ongoing';
      }
    },
    formatTime(time) {
      const date = new Date(time);
      const year = date.getFullYear();
      const month = ('0' + (date.getMonth() + 1)).slice(-2);
      const day = ('0' + date.getDate()).slice(-2);
      const hours = ('0' + date.getHours()).slice(-2);
      const minutes = ('0' + date.getMinutes()).slice(-2);

      return `${year}-${month}-${day} ${hours}:${minutes}`;
    },
    filterContests() {
      if (this.filterStatus && this.filterStatus !== 'all') {
        this.filteredContests = this.contests.filter(contest => contest.status === this.filterStatus);
      } else {
        this.filteredContests = this.contests;
      }
    },
    goToContestQuestions(contestId) {
      this.$router.push({ name: 'contest-question', params: { id: contestId } });
    },
    viewScores(contestId) {
      this.$router.push({ name: 'contest-statistics', params: { id: contestId } });
    },
    viewMyScore(contestId) {
      this.scoreDialogVisible = true;
      this.myScore = null;
      this.scoreLoading = true;
      axios.get('/api/getscore', {
        headers: { 'session': localStorage.getItem('session') },
        params: {
          exam_id: contestId,
          student_id: localStorage.getItem('userID')
        }
      })
      .then(res => {
        this.myScore = (res.data && typeof res.data.score !== 'undefined') ? res.data.score : null;
        this.scoreLoading = false;
      })
      .catch(() => {
        this.myScore = null;
        this.scoreLoading = false;
      });
    },
    getStatusText(status) {
      switch (status) {
        case 'not_started':
          return '未开始';
        case 'ongoing':
          return '进行中';
        case 'ended':
          return '已结束';
        default:
          return '';
      }
    },
    getStatusClass(status) {
      return {
        'status-not-started': status === 'not_started',
        'status-ongoing': status === 'ongoing',
        'status-ended': status === 'ended'
      };
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
.card.contest-card {
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
.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card.contest-card h2 {
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
.card.contest-card h2::before {
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
.filter-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 18px;
  margin-top: 18px;
}

.el-select {
  width: 200px;
}
.el-table {
  width: 100%;
  border-collapse: collapse;
  background: #f8fbff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(89,174,235,0.08);
  font-size: 1em;
}
th, td {
  padding: 12px 15px;
  text-align: center;
}
th {
  background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1565c0;
  font-weight: bold;
  font-size: 1.05em;
  border-bottom: 1.5px solid #90caf9;
}
td {
  background: transparent;
  color: #1976d2;
  border-bottom: 1px solid #e3f2fd;
}
tr:nth-child(even) {
  background-color: #f9f9f9;
}
.el-table tr:hover > td {
  background: #e3f2fd !important;
  transition: background 0.2s;
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
.disabled-button {
  background-color: #bdbdbd !important;
  cursor: not-allowed;
}
.status-not-started {
  background-color: #f0ad4e;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
.status-ongoing {
  background-color: #5cb85c;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
.status-ended {
  background-color: #d9534f;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
}
</style>
