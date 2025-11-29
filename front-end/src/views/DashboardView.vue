<script>
export default {
  name: "DashboardView",

  data() {
    return {
      adminName: localStorage.getItem("adminName") || "Admin",
    };
  },

  methods: {
    handleLogout() {
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("adminId");
      localStorage.removeItem("adminName");
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="header-content">
          <div class="brand">
            <span class="logo">🍽️</span>
            <h1>Restoran Admin</h1>
          </div>
          <div class="user-info">
            <span>Halo, {{ adminName }}</span>
            <button @click="handleLogout" class="btn-logout">Logout</button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container">
        <!-- Welcome Card -->
        <div class="welcome-card">
          <h2>Selamat Datang! 👋</h2>
          <p>Anda berhasil login ke sistem manajemen restoran.</p>
        </div>

        <!-- Stats Grid -->
        <div class="stats-grid">
          <!-- Menu Card -->
          <div class="stat-card">
            <div class="stat-header">
              <h3>Menu</h3>
              <span class="icon">🍱</span>
            </div>
            <p>Kelola menu makanan dan minuman</p>
            <button class="btn-link">Lihat Menu →</button>
          </div>

          <!-- Orders Card -->
          <div class="stat-card">
            <div class="stat-header">
              <h3>Pesanan</h3>
              <span class="icon">📋</span>
            </div>
            <p>Kelola pesanan pelanggan</p>
            <button class="btn-link">Lihat Pesanan →</button>
          </div>

          <!-- Reports Card -->
          <div class="stat-card">
            <div class="stat-header">
              <h3>Laporan</h3>
              <span class="icon">📊</span>
            </div>
            <p>Lihat laporan penjualan</p>
            <button class="btn-link">Lihat Laporan →</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f3f4f6;
}

.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo {
  font-size: 2rem;
}

.brand h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info span {
  color: #4a5568;
  font-weight: 500;
}

.btn-logout {
  padding: 0.5rem 1rem;
  background-color: #e5e7eb;
  color: #1f2937;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: #d1d5db;
}

.main-content {
  padding: 2rem 0;
}

.welcome-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.welcome-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.welcome-card p {
  color: #718096;
  margin: 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.stat-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.icon {
  font-size: 2rem;
}

.stat-card p {
  color: #718096;
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
}

.btn-link {
  background: none;
  border: none;
  color: #667eea;
  font-weight: 500;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
  transition: color 0.2s;
}

.btn-link:hover {
  color: #5a67d8;
}
</style>
