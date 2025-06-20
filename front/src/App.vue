<template>
  <div id="app" :class="currentThemeClass">
    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    currentThemeClass() {
      return `theme-${localStorage.getItem('backgroundColor') || 'default'}`;
    }
  }
};
</script>

<style>
#app {
  font-family: 'Noto Sans', 'Microsoft YaHei UI', 'Source Code Pro', sans-serif;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 20px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

/* 主题背景颜色样式 */
.theme-default {
  background-color: #ffffff;  /* 默认白色 */
  color: #000;
}

.theme-blue {
  background-color: #dce2f1;  /* 蓝色 */
  color: #fff;
}

.theme-green {
  background-color: #e3edcd;  /* 绿色 */
  color: #000;
}

.theme-yellow {
  background-color: #faf9de;  /* 黄色 */
  color: #000;
}

.theme-gray {
  background-color: #eaeaef;  /* 灰色 */
  color: #000;
}
</style>
