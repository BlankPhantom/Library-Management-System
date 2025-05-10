<template>
  <div id="app">
    <BookList />
  </div>
</template>

<script>
import BookList from './components/BookList.vue';

export default {
  name: 'App',
  components: {
    BookList,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  margin-top: 60px;
}
</style>
