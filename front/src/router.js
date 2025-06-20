import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'

// Admin
import ManageUsers from '@/components/ManageUsers'

// Teacher & Students
import Index from '@/components/Index'
import ImportQuestions from '@/components/ImportQuestions'
import CreateExam from '@/components/CreateExam'
import Submit from '@/components/Submit'
import Question from "@/components/Question"
import AnswerQuestion from '@/components/AnswerQuestion.vue'
import Contest from "@/components/Contest"
import Contest_Question from "@/components/Contest_Question"
import AnswerQuestion_contest from '@/components/AnswerQuestion_contest'
import ContestStatistics from '@/components/Statistics'
import TeacherHome from '@/components/TeacherHome.vue'
import AssistantHome from '@/components/AssistantHome.vue'
import Setting from '@/components/Setting.vue'
import StudentManage from '@/components/StudentManage.vue'


Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },

    {
      path: '/admin',
      name: 'admin',
      component: ManageUsers
    },

    {
      path: '/index',
      name: 'index',
      component: Index,
    },
    {
      path: '/teacher',
      name: 'TeacherHome',
      component: TeacherHome,
    },
    {
      path: '/assistant',
      name: 'AssistantHome',
      component: AssistantHome,
    },
    {
      path: '/import',
      name: 'import',
      component: ImportQuestions
    },
    {
      path: '/create',
      name: 'create',
      component: CreateExam
    },
    {
      path: '/submit',
      name: 'submit',
      component: Submit
    },
    {
      path: '/setting',
      name: 'setting',
      component: Setting,
    },
    {
      path: '/question',
      name: 'question',
      component: Question
    },
    {
      path: '/question/:id',
      name: 'answer-question',
      component: AnswerQuestion
    },
    {
      path: '/contest',
      name: 'contest',
      component: Contest
    },
    {
      path: '/contest/question/:id',
      name: 'contest-question',
      component: Contest_Question
    },
    {
      path: '/answer-question-contest/:examId/:questionId',
      name: 'answer-question-contest',
      component: AnswerQuestion_contest
    },
    {
      path: '/contest/statistics/:id',
      name: 'contest-statistics',
      component: ContestStatistics
    },
    {
      path: '/studentmanage',
      name: 'student-manage',
      component: StudentManage
    },
  ]
})
