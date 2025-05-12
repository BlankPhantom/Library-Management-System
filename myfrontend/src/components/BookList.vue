<template>
  <div class="p-4">
    <h2 class="section-title">📖 Book Management</h2>

    <!-- Add/Edit Form -->
    <form @submit.prevent="submitBook" class="form-inline">
      <input v-model="form.title" placeholder="Title" required class="input" />
      <input v-model="form.author" placeholder="Author" required class="input" />
      <input
        v-model="form.isbn_number"
        placeholder="ISBN (13 digits)"
        required
        class="input"
        maxlength="13"
        inputmode="numeric"
        pattern="[0-9]*"
        @input="filterIsbnInput"
      />
      <input
        v-model.number="form.copies_available"
        placeholder="Copies"
        required
        class="input"
        type="number"
        min="1"
      />
      <button type="submit" class="btn">{{ editing ? 'Update' : 'Add' }}</button>
    </form>

    <!-- Book Table -->
    <table class="table mt-4">
      <thead>
        <tr><th>TITLE</th><th>AUTHOR</th><th>ISBN</th><th>COPIES</th><th>ACTIONS</th></tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.title }}</td>
          <td>{{ book.author }}</td>
          <td>{{ book.isbn_number }}</td>
          <td>{{ book.copies_available }}</td>
          <td>
            <button @click="editBook(book)" class="btn">Edit</button>
            <button @click="promptDelete(book)" class="btn danger">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Confirm Delete Modal -->
    <div v-if="showConfirmModal" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <h3 class="modal-title">Confirm Deletion</h3>
          <div class="modal-body">
            <p>Are you sure you want to delete "<strong>{{ selectedBook?.title }}</strong>"?</p>
          </div>
          <div class="modal-footer">
            <button class="btn danger" @click="confirmDelete">Yes, Delete</button>
            <button class="btn" @click="cancelDelete">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Modal -->
    <div v-if="showModal" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <h3 class="modal-title">Error</h3>
          <div class="modal-body">
            <p>{{ modalMessage }}</p>
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
      books: [],
      form: {
        id: null,
        title: '',
        author: '',
        isbn_number: '',
        copies_available: 1,
      },
      editing: false,
      showModal: false,
      modalMessage: '',
      showConfirmModal: false,
      selectedBook: null
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    async fetchBooks() {
      const res = await axios.get('books/');
      this.books = res.data;
    },
    async submitBook() {
      if (this.form.copies_available < 1) {
        this.showModalWith('Copies must be at least 1.');
        return;
      }
      if (!/^\d{13}$/.test(this.form.isbn_number)) {
        this.showModalWith('ISBN must be exactly 13 numeric digits.');
        return;
      }

      try {
        if (this.editing) {
          await axios.put(`books/${this.form.id}/`, this.form);
        } else {
          await axios.post('books/', this.form);
        }
        this.resetForm();
        this.fetchBooks();
      } catch (error) {
        this.showModalWith('Failed to save book.');
      }
    },
    filterIsbnInput(e) {
      this.form.isbn_number = e.target.value.replace(/\D/g, '').slice(0, 13);
    },
    editBook(book) {
      this.form = { ...book };
      this.editing = true;
    },
    promptDelete(book) {
      this.selectedBook = book;
      this.showConfirmModal = true;
    },
    cancelDelete() {
      this.selectedBook = null;
      this.showConfirmModal = false;
    },
    async confirmDelete() {
      try {
        await axios.delete(`books/${this.selectedBook.id}/`);
        this.fetchBooks();
      } catch (error) {
        const msg = error.response?.data?.error || 'Failed to delete book.';
        this.showModalWith(msg);
      } finally {
        this.selectedBook = null;
        this.showConfirmModal = false;
      }
    },
    resetForm() {
      this.form = { id: null, title: '', author: '', isbn_number: '', copies_available: 1 };
      this.editing = false;
    },
    showModalWith(message) {
      this.modalMessage = message;
      this.showModal = true;
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
  margin-bottom: 1.5rem;
}

.form-inline .input {
  flex: 1 1 180px;
  min-width: 150px;
  padding: 10px;
  border: 1px solid #cbd5e0;
  border-radius: 8px;
  font-size: 15px;
  background-color: #f9f9f9;
  transition: border 0.3s;
}

.form-inline .input:focus {
  outline: none;
  border-color: #4c9aff;
  box-shadow: 0 0 0 3px rgba(76, 154, 255, 0.2);
}

.form-inline .btn {
  padding: 10px 16px;
  font-weight: 600;
  border-radius: 8px;
  font-size: 14px;
  height: 100%;
}

/* Table */
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 24px;
  font-size: 14px;
}

.table td > .btn {
  margin-right: 6px;
}

.table th,
.table td {
  padding: 12px 10px;
  border: 1px solid #e2e8f0;
  text-align: left;
}

.table thead {
  background-color: #f1f5f9;
}

.table tbody tr:nth-child(even) {
  background-color: #f9fbfd;
}

.table tbody tr:hover {
  background-color: #eef3fb;
}

/* Buttons */
.btn {
  background-color: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 9px 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #2563eb;
}

.btn.danger {
  background-color: #ef4444;
}

.btn.danger:hover {
  background-color: #dc2626;
}

/* Modal */
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(30, 30, 30, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeIn 0.3s ease-out;
}

.modal-wrapper {
  max-width: 420px;
  width: 90%;
  padding: 20px;
}

.modal-container {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease-out;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 8px;
  margin-bottom: 12px;
}

.modal-body {
  font-size: 15px;
  color: #374151;
  margin-bottom: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.modal-footer .btn {
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
}

.modal-footer .btn.danger {
  background-color: #ef4444;
}

.modal-footer .btn.danger:hover {
  background-color: #dc2626;
}

/* Animations */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
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
