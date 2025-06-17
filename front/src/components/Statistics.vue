<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-card">
        <h1 class="index-title">学生成绩</h1>
        <div class="index-btn-row">
          <button @click="goBack" class="index-btn index-btn-primary">返回</button>
        </div>
        <table class="index-table" v-if="studentScores.length">
          <thead>
            <tr>
              <th>学生ID</th>
              <th>分数</th>
              <th>排名</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in studentScores" :key="student.id">
              <td>{{ student.id }}</td>
              <td>{{ student.score }}</td>
              <td>{{ student.rank }}</td>
            </tr>
          </tbody>
        </table>
        <div v-else style="text-align:center;color:#888;margin-top:32px;">暂无成绩数据</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';

export default {
  name: 'ContestScores',
  components: {
    Navbar
  },
  data() {
    return {
      studentScores: []
    };
  },
  created() {
    this.fetchStudentScores();
  },
  methods: {
    fetchStudentScores() {
      const contestId = this.$route.params.id;
      axios.get(`/api/contestscores`, {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          contest_id: contestId
        }
      })
      .then(response => {
        this.studentScores = response.data;
      })
      .catch(error => {
        alert("获取学生成绩时发生错误！")
        alert(error);
      });
    },
    goBack() {
      this.$router.push({ name: 'contest' });
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
  max-width: 700px;
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
.index-btn-row {
  display: flex;
  justify-content: center;
  margin-top: 10px;
  margin-bottom: 24px;
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
@media (max-width: 900px) {
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
}
</style>
