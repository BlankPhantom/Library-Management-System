<template>
  <div class="p-4 max-w-xl mx-auto">
     <h2 class="section-title">📘 Borrow a Book</h2>

    <form @submit.prevent="borrowBook" class="form-inline">
      <!-- User Input -->
      <input
        v-model="form.user"
        type="text"
        required
        class="input"
        placeholder="Enter a User"
      />

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

    <!-- Modal -->
    <div v-if="showModal" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <h3 class="modal-title">Success</h3>
          <div class="modal-body">
            <p>✅ Borrow successful!</p>
          </div>
          <div class="modal-footer">
            <button class="btn" @click="showModal = false">OK</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      form: { user: '', book_id: '' },
      books: [],
      showModal: false
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
        this.form = { user: '', book_id: '' };
        this.fetchBooks();
        this.showModal = true; // ✅ show success modal
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
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.input {
  flex: 1 1 180px;
  min-width: 160px;
  padding: 10px 14px;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  font-size: 15px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

.input:focus {
  border-color: #4c9aff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(76, 154, 255, 0.2);
}

.btn {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: #fff;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #2563eb;
}

/* Modal Styles */
.modal-mask {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(31, 41, 55, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease;
}

.modal-wrapper {
  width: 100%;
  max-width: 420px;
  padding: 20px;
  box-sizing: border-box;
}

.modal-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 28px 24px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
  text-align: center;
  transition: all 0.3s ease;
}

.modal-title {
  font-size: 22px;
  font-weight: 700;
  color: #16a34a;
  margin-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
}

.modal-body {
  font-size: 16px;
  color: #374151;
  margin-bottom: 20px;
}

.modal-footer {
  display: flex;
  justify-content: center;
}

.modal-footer .btn {
  background-color: #16a34a;
  font-size: 15px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 8px;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background-color 0.25s ease;
}

.modal-footer .btn:hover {
  background-color: #15803d;
}

/* Animations */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    background-color: rgba(30, 30, 30, 0);
  }
  to {
    background-color: rgba(30, 30, 30, 0.5);
  }
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a237e;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

</style>
