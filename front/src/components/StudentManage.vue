<template>
  <div class="index-bg">
    <Navbar />
    <div class="index-container">
      <div class="index-card">
        <h1 class="index-title">学生管理（教师分配助教）</h1>
        <div class="student-columns">
          <!-- 左侧：未分配学生 -->
          <div class="student-column">
            <h2 class="index-section-title">未分配学生</h2>
            <el-table
              :data="unassignedStudents"
              border
              class="index-table"
              empty-text="暂无未分配学生"
            >
              <el-table-column prop="id" label="学生ID" align="center" />
              <el-table-column prop="username" label="学生用户名" align="center" />
              <el-table-column label="助教ID" align="center">
                <template slot-scope="{ row }">
                  <el-select
                    v-model="assistantSelections[row.id]"
                    placeholder="选择助教ID"
                    style="width: 100%"
                    @change="onAssistantSelectChange(row.id)"
                  >
                    <el-option
                      v-for="assistant in assistants"
                      :key="assistant.id"
                      :label="assistant.id"
                      :value="{ id: assistant.id, username: assistant.username }"
                    />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="助教用户名" align="center">
                <template slot-scope="{ row }">
                  <el-select
                    v-model="assistantSelections[row.id]"
                    placeholder="选择助教用户名"
                    style="width: 100%"
                    @change="onAssistantSelectChange(row.id)"
                  >
                    <el-option
                      v-for="assistant in assistants"
                      :key="assistant.id"
                      :label="assistant.username"
                      :value="{ id: assistant.id, username: assistant.username }"
                    />
                  </el-select>
                </template>
              </el-table-column>
            </el-table>
            <div class="index-btn-row">
              <button
                class="index-btn index-btn-primary"
                :disabled="!hasAssignments"
                @click="submitAssignments"
                style="margin-top: 20px"
              >提交分配</button>
            </div>
          </div>

          <!-- 右侧：已分配学生 -->
          <div class="student-column">
            <h2 class="index-section-title">已分配学生</h2>
            <el-table
              :data="assignedStudents"
              border
              class="index-table"
              empty-text="暂无已分配学生"
            >
              <el-table-column prop="id" label="学生ID" align="center" />
              <el-table-column prop="username" label="学生用户名" align="center" />
              <el-table-column prop="assistant_id" label="助教ID" align="center" />
              <el-table-column label="助教用户名" align="center">
                <template slot-scope="{ row }">
                  <span>
                    {{
                      (assistants.find(a => a.id == row.assistant_id) || {}).username || '未知助教'
                    }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column label="操作" align="center">
                <template slot-scope="{ row }">
                  <button class="index-btn index-btn-danger" style="padding:4px 16px;font-size:0.95em;" @click="removeAssignment(row.id)">删除</button>
                </template>
              </el-table-column>
            </el-table>
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
  name: 'StudentManage',
  components: { Navbar },
  data() {
    return {
      students: [],
      assistants: [],
      assignments: {},
      assistantSelections: {},
    };
  },
  computed: {
    hasAssignments() {
      return Object.keys(this.assignments).length > 0;
    },
    assignedStudents() {
      return this.students.filter(s => s.assistant_id);
    },
    unassignedStudents() {
      return this.students.filter(s => !s.assistant_id);
    }
  },
  mounted() {
    this.fetchStudents();
    this.fetchAssistants();
  },
  methods: {
    async removeAssignment(studentId) {
      try {
        await axios.delete('/api/assistantstudents', {
          headers: { session: localStorage.getItem('session') },
          data: { student_id: studentId }
        });
        this.fetchStudents();
      } catch (e) {
        alert('删除失败');
      }
    },
    async fetchStudents() {
      try {
        const res = await axios.get('/api/studentlist', {
          headers: { session: localStorage.getItem('session') }
        });
        this.students = res.data;
      } catch (e) {
        alert('获取学生列表失败');
      }
    },
    async fetchAssistants() {
      try {
        const res = await axios.get('/api/manageusers', {
          headers: { session: localStorage.getItem('session') }
        });
        this.assistants = res.data.filter(u => u.role === 3);
      } catch (e) {
        alert('获取助教列表失败');
      }
    },
    onAssistantSelectChange(studentId) {
      const selected = this.assistantSelections[studentId];
      if (selected && selected.id) {
        this.$set(this.assignments, studentId, selected.id);
      } else {
        delete this.assignments[studentId];
      }
    },
    async submitAssignments() {
      const payload = Object.entries(this.assignments).map(([student_id, assistant_id]) => ({
        student_id: parseInt(student_id),
        assistant_id
      }));

      if (payload.length === 0) {
        alert('请先选择至少一个分配');
        return;
      }

      try {
        await axios.post('/api/assistantstudents', payload, {
          headers: { session: localStorage.getItem('session') }
        });
        alert('分配成功！');
        this.assignments = {};
        this.assistantSelections = {};
        this.fetchStudents();
      } catch (e) {
        alert('提交失败');
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
  max-width: 1200px;
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
.index-section-title {
  font-size: 1.2rem;
  color: #1976d2;
  font-weight: 600;
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
.student-columns {
  display: flex;
  gap: 40px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.student-column {
  flex: 1;
  min-width: 340px;
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
  text-align: center;
  font-size: 16px;
}
.index-table th {
  background-color: #e3f2fd;
  font-weight: bold;
  color: #1976d2;
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
.index-btn-primary:disabled {
  background: #b0bec5;
  cursor: not-allowed;
}
.index-btn-primary:hover:enabled {
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
@media (max-width: 1100px) {
  .index-container {
    margin-left: 0;
    padding: 0 4px;
  }
  .index-card {
    max-width: 100%;
  }
  .student-columns {
    flex-direction: column;
    gap: 24px;
  }
}
@media (max-width: 700px) {
  .index-card {
    padding: 18px 6px 18px 6px;
  }
  .student-columns {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
