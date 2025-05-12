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
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  font-size: 14px;
  background-color: #fff;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.table thead {
  background-color: #f1f5f9;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table th, .table td {
  padding: 12px 14px;
  border: 1px solid #e2e8f0;
  text-align: left;
  color: #000000;
}

.table tbody tr:nth-child(even) {
  background-color: #f9fbfd;
}

.table tbody tr:hover {
  background-color: #eef3fb;
  transition: background 0.3s ease;
}

</style>
