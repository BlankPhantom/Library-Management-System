<template>
  <div class="p-4 max-w-md mx-auto">
    <h2 class="text-2xl font-bold mb-4 text-center text-orange-600">📤 Return a Book</h2>
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
        this.modalTitle = 'Success';
        this.modalMessage = '✅ Book returned!';
        this.showModal = true;
        this.borrowId = '';
      } catch {
        this.modalTitle = 'Error';
        this.modalMessage = '❌ Return failed. Check the transaction ID.';
        this.showModal = true;
      }
    }
  }
};
</script>

<style scoped>
.form-inline {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 15px;
  min-width: 200px;
  flex: 1 1 auto;
  transition: border-color 0.3s ease;
}

.input:focus {
  outline: none;
  border-color: #fb8c00;
  box-shadow: 0 0 0 3px rgba(251, 140, 0, 0.2);
}

.btn {
  padding: 10px 16px;
  background-color: #fb8c00;
  color: white;
  font-weight: bold;
  font-size: 15px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #ef6c00;
}

/* Modal */
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
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.3s ease-out;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #fb8c00;
  border-bottom: 1px solid #eee;
}

.modal-body {
  font-size: 15px;
  color: #333;
}

.modal-footer {
  text-align: right;
  margin-top: 16px;
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
</style>
