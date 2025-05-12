<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Book Management</h2>

    <!-- Add/Edit Form -->
    <form @submit.prevent="submitBook" class="form-inline">
      <input v-model="form.title" placeholder="Title" required class="input" />
      <input v-model="form.author" placeholder="Author" required class="input" />
      <input v-model="form.isbn_number" placeholder="ISBN" required class="input" maxlength="13" @input="limitIsbn" />
      <input v-model.number="form.copies_available" placeholder="Copies" required class="input" type="number" min="1" />
      <button type="submit" class="btn">{{ editing ? 'Update' : 'Add' }}</button>
    </form>

    <!-- Book Table -->
    <table class="table mt-4">
      <thead>
        <tr><th>Title</th><th>Author</th><th>ISBN</th><th>Copies</th><th>Actions</th></tr>
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
          <h3 class="modal-title">Delete Not Allowed</h3>
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
    limitIsbn() {
      if (this.form.isbn_number.length > 13) {
        this.form.isbn_number = this.form.isbn_number.slice(0, 13);
      }
    },
    showModalWith(message) {
      this.modalMessage = message;
      this.showModal = true;
    }
  },
};
</script>

<style scoped>
.form-inline {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-bottom: 1rem;
}
.form-inline .input {
  flex: 1 1 150px;
  min-width: 120px;
}
.form-inline .btn {
  flex-shrink: 0;
  margin: 0;
  height: 100%;
}
.input {
  margin: 8px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
  font-size: 14px;
}
.btn {
  margin: 4px 4px 4px 0;
  padding: 8px 14px;
  background-color: #2c7be5;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.btn:hover {
  background-color: #1a5edb;
}
.btn.danger {
  background-color: #dc3545;
}
.btn.danger:hover {
  background-color: #b02a37;
}
.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 14px;
}
.table th, .table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}
.table thead {
  background-color: #f8f9fa;
}
.table tbody tr:nth-child(even) {
  background-color: #f4f7fb;
}
.table tbody tr:hover {
  background-color: #e9f0fb;
}
/* Modal Styles */
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
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
.modal-container {
  background-color: #fff;
  border-radius: 10px;
  padding: 24px 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 6px;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 8px;
}
.modal-body {
  font-size: 15px;
  color: #444;
  line-height: 1.4;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}
.modal-footer .btn {
  padding: 8px 14px;
  background-color: #3498db;
  border-radius: 6px;
  font-weight: 500;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}
.modal-footer .btn:hover {
  background-color: #2a7bbd;
}
/* Animations */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.98);
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
</style>
