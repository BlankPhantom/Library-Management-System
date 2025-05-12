<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-2xl font-bold mb-4 text-center">📘 Borrow a Book</h2>

    <form @submit.prevent="borrowBook" class="form-inline">
      <!-- User Dropdown -->
      <select v-model="form.user" required class="input">
        <option disabled value="">Select User</option>
        <option v-for="u in users" :key="u.id" :value="u.username">{{ u.username }}</option>
      </select>

      <!-- Book Dropdown -->
      <select v-model="form.book_id" required class="input">
        <option disabled value="">Select Book</option>
        <option
          v-for="b in books"
          :key="b.id"
          :value="b.id"
          :disabled="b.copies_available === 0"
        >
          {{ b.title }} ({{ b.copies_available }} copies)
        </option>
      </select>

      <button type="submit" class="btn">Borrow</button>
    </form>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      form: { user: '', book_id: '' },
      users: [
        { id: 1, username: 'alice' },
        { id: 2, username: 'bob' },
        { id: 3, username: 'charlie' },
        { id: 4, username: 'diana' },
        { id: 5, username: 'edward' },
        { id: 6, username: 'frank' },
        { id: 7, username: 'grace' },
        { id: 8, username: 'hannah' },
        { id: 9, username: 'ian' },
        { id: 10, username: 'julia' }
      ],
      books: []
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    async fetchBooks() {
      try {
        const res = await axios.get('books/');
        this.books = res.data;
      } catch (error) {
        console.error('Failed to load books:', error);
      }
    },
    async borrowBook() {
      try {
        await axios.post('borrow/', this.form);
        alert('✅ Borrow successful!');
        this.form = { user: '', book_id: '' };
        this.fetchBooks();
        this.$emit('borrowed'); 
      } catch (error) {
        const msg = error.response?.data?.error || '❌ Borrow failed.';
        alert(msg);
        console.error('Borrow error:', error);
      }
    }
  }
};
</script>

<style scoped>
.form-inline {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
}

.input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  flex: 1 1 auto;
  min-width: 150px;
}

.btn {
  padding: 10px 20px;
  background: #2563eb;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #1d4ed8;
}
</style>
