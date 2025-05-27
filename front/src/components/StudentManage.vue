<template>
  <div>
    <Navbar />
    <div class="student-manage">
      <h1>学生管理（教师分配助教）</h1>

      <div class="student-columns">
        <!-- 左侧：未分配学生 -->
        <div class="student-column">
          <h2>未分配学生</h2>
          <el-table
            :data="unassignedStudents"
            border
            style="width: 100%"
            empty-text="暂无未分配学生"
          >
            <el-table-column prop="id" label="学生ID" :width="leftTableWidth" align="center" />
            <el-table-column prop="username" label="学生用户名" :width="leftTableWidth" align="center" />

            <el-table-column label="助教ID" :width="leftTableWidth" align="center">
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

            <el-table-column label="助教用户名" :width="leftTableWidth" align="center">
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
          <el-button
            type="primary"
            style="margin-top: 20px"
            :disabled="!hasAssignments"
            @click="submitAssignments"
          >提交分配</el-button>
        </div>

        <!-- 右侧：已分配学生 -->
        <div class="student-column">
          <h2>已分配学生</h2>
          <el-table
            :data="assignedStudents"
            border
            style="width: 100%"
            empty-text="暂无已分配学生"
          >
            <el-table-column prop="id" label="学生ID" :width="rightTableWidth" align="center" />
            <el-table-column prop="username" label="学生用户名" :width="rightTableWidth" align="center" />
            <el-table-column prop="assistant_id" label="助教ID" :width="rightTableWidth" align="center" />
            <el-table-column label="助教用户名" :width="rightTableWidth" align="center">
              <template slot-scope="{ row }">
                <span>
                  {{
                    (assistants.find(a => a.id == row.assistant_id) || {}).username || '未知助教'
                  }}
                </span>
              </template>
            </el-table-column>
            <el-table-column label="操作" :width="tableColumnWidth" align="center">
                <template slot-scope="{ row }">
                    <el-button type="danger" size="mini" @click="removeAssignment(row.id)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
          </el-table>
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
      assistantSelections: {},  // 👈 新增联动映射
      leftTableWidth: 0,
      rightTableWidth: 0
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
    this.calculateTableColumnWidth();
    window.addEventListener('resize', this.calculateTableColumnWidth);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.calculateTableColumnWidth);
  },
  methods: {
    async removeAssignment(studentId) {
        try {
            await axios.delete('/api/assistantstudents', {
                headers: { session: localStorage.getItem('session') },
                data: { student_id: studentId }
            });
            this.fetchStudents(); // 重新加载数据，刷新“未分配”与“已分配”
        } catch (e) {
            alert('删除失败');
        }
    },
    calculateTableColumnWidth() {
      const columnEl = document.querySelector('.student-column');
      if (columnEls.length >= 2) {
        const leftWidth = columnEls[0].offsetWidth;
        const rightWidth = columnEls[1].offsetWidth;
        this.leftTableWidth = Math.floor(leftWidth / 4);
        this.rightTableWidth = Math.floor(rightWidth / 5);
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
        this.assistantSelections = {};  // 清空联动数据
        this.fetchStudents();
      } catch (e) {
        alert('提交失败');
      }
    }
  }
};
</script>

<style scoped>
.student-manage {
  padding: 20px;
}
h2 {
  color: #333;
}
.student-columns {
  display: flex;
  gap: 40px;
  margin-top: 20px;
}
.student-column {
  flex: 1;
}
</style>
