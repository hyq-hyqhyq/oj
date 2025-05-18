<template>
  <div>
    <Navbar />
    <div class="article-detail-page">
      <div class="article-container shadow">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-metadata">
          <span class="author">作者ID: {{ article.user_id }}</span>
          <span class="publish-time">发布时间: {{ formatDate(article.publish_time) }}</span>
        </div>
        <div class="article-content" v-html="parsedContent"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import axios from 'axios';
import marked from 'marked';

export default {
  name: 'ArticleDetail',
  components: {
    Navbar
  },
  data() {
    return {
      article: {
        id: null,
        title: '',
        content: '',
        user_id: '',
        publish_time: ''
      }
    };
  },
  mounted() {
    this.fetchArticleDetails();
  },
  methods: {
    fetchArticleDetails() {
      const articleId = this.$route.params.id;
      axios.get('/api/community', {
        headers: {
          'session': localStorage.getItem('session')
        },
        params: {
          article_id: parseInt(articleId)
        }
      })
        .then(response => {
          this.article = response.data;
        })
        .catch(error => {
          alert(`失败: ${error.response.data.message}`);
        });
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    }
  },
  computed: {
    parsedContent() {
      return marked(this.article.content);
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

body {
  font-family: 'Roboto', sans-serif;
}

.article-detail-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  min-height: 100vh;
}

.article-container {
  width: 70%;
  max-width: 1200px;
  background-color: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-container:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.article-title {
  margin-bottom: 20px;
  color: inherit;
  font-size: 2.4rem;
  text-align: center;
  word-break: break-word;
  line-height: 1.2;
}

.article-metadata {
  display: flex;
  justify-content: space-between;
  font-size: 1rem;
  color: inherit;
  margin-bottom: 20px;
}

.author, .publish-time {
  display: inline-block;
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 5px;
}

.article-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: inherit;
  text-align: justify;
}

.article-content p {
  margin-bottom: 20px;
}

.article-content h1,
.article-content h2,
.article-content h3,
.article-content h4,
.article-content h5,
.article-content h6 {
  margin-top: 20px;
  margin-bottom: 10px;
  font-weight: 400;
}

.article-content ul,
.article-content ol {
  margin-left: 20px;
}

.article-content blockquote {
  margin: 20px 0;
  padding: 10px 20px;
  background-color: #f5f5f5;
  border-left: 5px solid #ddd;
}

.article-content code {
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 3px;
}

.article-content pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}
</style>
