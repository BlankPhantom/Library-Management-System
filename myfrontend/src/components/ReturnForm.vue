<template>
  <div class="p-6 max-w-lg mx-auto">
    <h2 class="section-title"> 📤 Return a Book</h2>

    <form @submit.prevent="returnBook" class="form-inline">
      <input
        v-model="borrowId"
        placeholder="Enter Transaction ID"
        required
        class="input"
        type="number"
        min="1"
      />
      <button type="submit" class="btn">Return</button>
    </form>

    <!-- Modal -->
    <div v-if="showModal" class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <h3 class="modal-title">{{ modalTitle }}</h3>
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
      borrowId: '',
      showModal: false,
      modalTitle: '',
      modalMessage: ''
    };
  },
  methods: {
    async returnBook() {
      try {
        await axios.post(`return/${this.borrowId}/`);
        this.modalTitle = '✅ Success';
        this.modalMessage = 'Book has been successfully returned!';
        this.showModal = true;
        this.borrowId = '';
      } catch (error) {
        const status = error.response?.status;

        if (status === 404) {
          this.modalTitle = '❌ Transaction Not Found';
          this.modalMessage = 'The transaction ID you entered does not exist.';
        } else if (status === 400) {
          this.modalTitle = '⚠️ Already Returned';
          this.modalMessage = 'This transaction has already been marked as returned.';
        } else {
          this.modalTitle = '❌ Error';
          this.modalMessage = 'An unexpected error occurred. Please try again.';
        }

        this.showModal = true;
      }
    }
  }
};
</script>

<style scoped>
.form-inline {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 1rem;
}

.input {
  padding: 12px 14px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  min-width: 240px;
  flex: 1 1 auto;
  background-color: #fefefe;
  transition: border-color 0.3s ease;
}

.input:focus {
  outline: none;
  border-color: #fb8c00;
  box-shadow: 0 0 0 3px rgba(251, 140, 0, 0.25);
}

.btn {
  padding: 12px 20px;
  background-color: #fb8c00;
  color: white;
  font-weight: bold;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #ef6c00;
}

/* Modal Styles */
.modal-mask {
  position: fixed;
  z-index: 9999;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
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
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.15);
  animation: slideUp 0.3s ease-out;
  text-align: center;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #fb8c00;
  margin-bottom: 12px;
}

.modal-body {
  font-size: 16px;
  color: #333;
}

.modal-footer {
  margin-top: 18px;
  display: flex;
  justify-content: center;
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

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
.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a237e;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e2e8f0;
  padding-bottom: 0.5rem;
}
</style>
