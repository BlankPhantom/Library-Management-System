<template>
  <div class="container">
    <h1 class="title">📚 Library Management System</h1>

    <!-- Tabs -->
    <ul class="tab-header">
      <li
        v-for="tab in tabs"
        :key="tab"
        :class="{ active: currentTab === tab }"
        @click="currentTab = tab"
      >
        {{ tab }}
      </li>
    </ul>

    <!-- Tab Content -->
    <div class="tab-content">
      <BookList v-if="currentTab === 'Books'" />
      <div v-if="currentTab === 'Borrow'">
        <!-- 🔁 Emit event to parent -->
        <BorrowForm @borrowed="refreshTransactions" />
        <!-- 🔁 Use ref to call refresh -->
        <TransactionHistory ref="tx" />
      </div>
      <ReturnForm v-if="currentTab === 'Return'" />
    </div>
  </div>
</template>


<script>
import BookList from './components/BookList.vue';
import BorrowForm from './components/BorrowForm.vue';
import ReturnForm from './components/ReturnForm.vue';
import TransactionHistory from './components/TransactionHistory.vue';

export default {
  data() {
    return {
      currentTab: 'Books',
      tabs: ['Books', 'Borrow', 'Return'],
    };
  },
  components: {
    BookList,
    BorrowForm,
    ReturnForm,
    TransactionHistory,
  },
   methods: {
    refreshTransactions() {
      this.$refs.tx?.loadTransactions();  
    }
  }
};

</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 2rem auto;
  background: #fff;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-radius: 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.tab-header {
  display: flex;
  justify-content: center;
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem 0;
  border-bottom: 2px solid #ccc;
}

.tab-header li {
  margin: 0 1rem;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  font-weight: 500;
  color: #555;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
}

.tab-header li:hover {
  color: #1a73e8;
}

.tab-header li.active {
  border-bottom: 3px solid #1a73e8;
  color: #1a73e8;
  font-weight: 600;
}

.tab-content {
  margin-top: 1rem;
}
</style>
