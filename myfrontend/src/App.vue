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
  background: #fdfdfd;
  padding: 2.5rem 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  border: 1px solid #e0e0e0;
}

.title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  color: #1a237e;
  margin-bottom: 2rem;
  letter-spacing: 0.5px;
}

/* Tab Header */
.tab-header {
  display: flex;
  justify-content: center;
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
}

.tab-header li {
  padding: 0.75rem 2rem;
  margin: 0 0.5rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 16px;
  color: #555;
  border-bottom: 3px solid transparent;
  border-radius: 6px 6px 0 0;
  transition: all 0.25s ease;
}

.tab-header li:hover {
  background-color: #f0f4ff;
  color: #1a73e8;
}

.tab-header li.active {
  border-bottom: 3px solid #1a73e8;
  background-color: #e8f0fe;
  color: #1a73e8;
  font-weight: 600;
}

/* Tab Content */
.tab-content {
  margin-top: 2rem;
  animation: fadeIn 0.3s ease;
}

/* Smooth transition */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
