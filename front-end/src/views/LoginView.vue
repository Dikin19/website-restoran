<script>
import authService from "@/services/authService";

export default {
  name: "LoginView",

  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      loading: false,
      errorMessage: "",
    };
  },

  methods: {
    async handleLogin() {
      this.loading = true;
      this.errorMessage = "";

      try {
        const response = await authService.login(this.form);

        if (response.data.success) {
          const admin = response.data.data.admin;
          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("adminId", admin.id);
          localStorage.setItem("adminName", admin.nama_lengkap);

          this.$router.push({ name: "Dashboard" });
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = "Terjadi kesalahan. Silakan coba lagi.";
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Header -->
      <div class="login-header">
        <div class="icon">🍽️</div>
        <h1 class="title">Restoran</h1>
        <p class="subtitle">Login untuk mengelola restoran</p>
      </div>

      
      <form @submit.prevent="handleLogin" class="login-form">
      
        <div class="form-group">
          <label class="form-label">Username</label>
          <input
            v-model="form.username"
            type="text"
            class="form-input"
            placeholder="Masukkan username"
            required
          />
        </div>

      
        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            class="form-input"
            placeholder="Masukkan password"
            required
          />
        </div>

       
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

       
        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="loading">Loading...</span>
          <span v-else>Login</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 2.5rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.subtitle {
  color: #718096;
  font-size: 0.95rem;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #4a5568;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #cbd5e0;
}

.error-message {
  padding: 0.875rem 1rem;
  background-color: #fed7d7;
  color: #c53030;
  border-radius: 8px;
  font-size: 0.875rem;
  border-left: 4px solid #c53030;
}

.btn-login {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 0.5rem;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .login-card {
    padding: 2rem 1.5rem;
  }

  .title {
    font-size: 1.75rem;
  }

  .icon {
    font-size: 3rem;
  }
}
</style>
