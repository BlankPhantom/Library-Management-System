<template>
  <div>
    <h2>📚 Book List</h2>

    <!-- Add Book Form -->
    <form @submit.prevent="addBook" class="form">
      <input v-model="newBook.title" placeholder="Title" required />
      <input v-model="newBook.author" placeholder="Author" required />
      <input v-model="newBook.isbn" placeholder="ISBN" required />
      <input type="number" v-model.number="newBook.copies_available" placeholder="Copies" required />
      <button type="submit">Add Book</button>
    </form>

    <hr />

    <!-- Book List -->
    <ul>
      <li v-for="book in books" :key="book.id">
        <strong>{{ book.title }}</strong> by {{ book.author }} — {{ book.copies_available }} copies
        <button @click="deleteBook(book.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BookList',
  data() {
    return {
      books: [],
      newBook: {
        title: '',
        author: '',
        isbn: '',
        copies_available: 1,
      },
    };
  },
  methods: {
    async fetchBooks() {
      try {
        const response = await axios.get('http://localhost:8000/api/books/');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async addBook() {
      try {
        await axios.post('http://localhost:8000/api/books/', this.newBook);
        this.newBook = { title: '', author: '', isbn: '', copies_available: 1 };
        this.fetchBooks();
      } catch (error) {
        console.error('Error adding book:', error);
      }
    },
    async deleteBook(id) {
      try {
        await axios.delete(`http://localhost:8000/api/books/${id}/`);
        this.fetchBooks();
      } catch (error) {
        console.error('Error deleting book:', error);
      }
    },
  },
  mounted() {
    this.fetchBooks();
  },
};
</script>

<style scoped>
form input {
  margin: 5px;
}
</style>
