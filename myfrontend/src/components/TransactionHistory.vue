<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Transaction History</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>User</th>
          <th>Book Title</th>
          <th>Borrow Date</th>
          <th>Return Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tx in transactions" :key="tx.id">
          <td>{{ tx.id }}</td>
          <td>{{ tx.user }}</td>
          <td>{{ tx.book }}</td>
          <td>{{ formatDate(tx.borrow_date) }}</td>
          <td>{{ tx.return_date ? formatDate(tx.return_date) : 'N/A' }}</td>
          <td>{{ tx.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      transactions: []
    };
  },
  created() {
    this.loadTransactions();
  },
  methods: {
    async loadTransactions() {
      try {
        const res = await axios.get('transactions/');
        this.transactions = res.data.sort((a, b) => a.id - b.id);
      } catch (error) {
        alert('Failed to load transactions: ' + error.message);
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString(); 
    }
  }
};
</script>

<style scoped>
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 8px; border: 1px solid #ddd; text-align: left; }
</style>
