<script>
import authService from "@/services/authService";
import Notification from "@/components/Notification.vue";

export default {
  name: "LoginView",

  components: {
    Notification,
  },

  data() {
    return {
      form: {
        username: "",
        password: "",
      },
      loading: false,
      errors: {
        username: "",
        password: "",
      },
      notification: {
        show: false,
        type: "info",
        message: "",
      },
    };
  },

  methods: {
    validateForm() {
      this.errors = {
        username: "",
        password: "",
      };

      let isValid = true;

      if (!this.form.username || this.form.username.trim() === "") {
        this.errors.username = "Username wajib diisi";
        isValid = false;
      } else if (this.form.username.length < 3) {
        this.errors.username = "Username minimal 3 karakter";
        isValid = false;
      }

      if (!this.form.password || this.form.password.trim() === "") {
        this.errors.password = "Password wajib diisi";
        isValid = false;
      } else if (this.form.password.length < 6) {
        this.errors.password = "Password minimal 6 karakter";
        isValid = false;
      }

      if (!isValid) {
        this.showNotification("error", "Mohon lengkapi form dengan benar");
      }

      return isValid;
    },

    async handleLogin() {
      if (!this.validateForm()) {
        return;
      }

      this.loading = true;

      try {
        const response = await authService.login(this.form);

        if (response.data.success) {
          const admin = response.data.data.admin;
          localStorage.setItem("isLoggedIn", "true");
          localStorage.setItem("adminId", admin.id);
          localStorage.setItem("adminName", admin.nama_lengkap);

          this.showNotification(
            "success",
            `Selamat datang, ${admin.nama_lengkap}!`
          );

          setTimeout(() => {
            this.$router.push({ name: "Dashboard" });
          }, 1000);
        }
      } catch (error) {
        let errorMsg = "Terjadi kesalahan. Silakan coba lagi.";

        if (error.response && error.response.data) {
          errorMsg = error.response.data.message || errorMsg;
        }

        this.showNotification("error", errorMsg);
      } finally {
        this.loading = false;
      }
    },

    showNotification(type, message) {
      this.notification = { show: true, type, message };
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
            :class="['form-input', { 'input-error': errors.username }]"
            placeholder="Masukkan username"
            @input="errors.username = ''"
          />
          <span v-if="errors.username" class="error-text">
            {{ errors.username }}
          </span>
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <input
            v-model="form.password"
            type="password"
            :class="['form-input', { 'input-error': errors.password }]"
            placeholder="Masukkan password"
            @input="errors.password = ''"
          />
          <span v-if="errors.password" class="error-text">
            {{ errors.password }}
          </span>
        </div>

        <button type="submit" class="btn-login" :disabled="loading">
          <span v-if="loading">⏳ Loading...</span>
          <span v-else>🔐 Login</span>
        </button>
      </form>
    </div>

    <Notification
      :show="notification.show"
      :type="notification.type"
      :message="notification.message"
      @close="notification.show = false"
    />
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

.input-error {
  border-color: #fc8181;
  background-color: #fff5f5;
}

.input-error:focus {
  border-color: #f56565;
  box-shadow: 0 0 0 3px rgba(245, 101, 101, 0.1);
}

.error-text {
  color: #e53e3e;
  font-size: 0.8rem;
  font-weight: 500;
  margin-top: 0.25rem;
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
