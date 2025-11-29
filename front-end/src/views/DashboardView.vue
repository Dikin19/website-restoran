<script>
import Navbar from "@/components/Navbar.vue";
import Loading from "@/components/Loading.vue";
import orderService from "@/services/orderService";

export default {
  name: "DashboardView",

  components: {
    Navbar,
    Loading,
  },

  data() {
    return {
      loading: false,
      stats: {
        total_pesanan: 0,
        pesanan_pending: 0,
        pesanan_selesai: 0,
        total_pendapatan: 0,
      },
    };
  },

  computed: {
    adminName() {
      return localStorage.getItem("adminName") || "Admin";
    },
  },

  mounted() {
    this.loadStatistics();
  },

  methods: {
    async loadStatistics() {
      this.loading = true;

      try {
        const response = await orderService.getStatistics();

        if (response.data.success) {
          this.stats = response.data.data;
        }
      } catch (error) {
        console.error("Error loading statistics:", error);

      } finally {
        this.loading = false;
      }
    },

    
    formatCurrency(amount) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(amount);
    },
  },
};
</script>

<template>

  <div class="min-h-screen bg-gray-50">
    
    <Navbar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-600 mt-2">Selamat datang, {{ adminName }}! 👋</p>
      </div>


      <Loading v-if="loading" message="waiting for statistik" />


      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm">Total Pesanan</p>
              <h3 class="text-3xl font-bold mt-2">{{ stats.total_pesanan }}</h3>
            </div>
            <div class="text-4xl opacity-80">📋</div>
          </div>
        </div>


        <div
          class="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-yellow-100 text-sm">Pesanan Pending</p>
              <h3 class="text-3xl font-bold mt-2">
                {{ stats.pesanan_pending }}
              </h3>
            </div>
            <div class="text-4xl opacity-80">⏳</div>
          </div>
        </div>


        <div
          class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Pesanan Selesai</p>
              <h3 class="text-3xl font-bold mt-2">
                {{ stats.pesanan_selesai }}
              </h3>
            </div>
            <div class="text-4xl opacity-80">✅</div>
          </div>
        </div>


        <div
          class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-6 text-white shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Total Pendapatan</p>
              <h3 class="text-2xl font-bold mt-2">
                {{ formatCurrency(stats.total_pendapatan) }}
              </h3>
            </div>
            <div class="text-4xl opacity-80">💰</div>
          </div>
        </div>
      </div>


      <div class="mt-8">
        <h2 class="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Tambah Menu -->
          <router-link
            to="/menu/create"
            class="bg-white rounded-xl p-6 shadow hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="flex items-center space-x-4">
              <div class="text-4xl">➕</div>
              <div>
                <h3 class="font-semibold text-gray-900">Tambah Menu</h3>
                <p class="text-sm text-gray-600">Tambah menu baru</p>
              </div>
            </div>
          </router-link>


          <router-link
            to="/menu"
            class="bg-white rounded-xl p-6 shadow hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="flex items-center space-x-4">
              <div class="text-4xl">📜</div>
              <div>
                <h3 class="font-semibold text-gray-900">Lihat Menu</h3>
                <p class="text-sm text-gray-600">Kelola daftar menu</p>
              </div>
            </div>
          </router-link>


          <router-link
            to="/orders/create"
            class="bg-white rounded-xl p-6 shadow hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div class="flex items-center space-x-4">
              <div class="text-4xl">🛒</div>
              <div>
                <h3 class="font-semibold text-gray-900">Buat Pesanan</h3>
                <p class="text-sm text-gray-600">Tambah pesanan baru</p>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f7fafc;
}

.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* Header Dashboard */
.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 0.5rem 0;
}

.dashboard-header p {
  color: #718096;
  font-size: 1rem;
  margin: 0;
}

/* Statistik Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (min-width: 640px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Stat Card */
.stat-card {
  border-radius: 12px;
  padding: 1.5rem;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

/* Warna untuk setiap stat card */
.stat-blue {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-yellow {
  background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
}

.stat-green {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
}

.stat-purple {
  background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%);
}

/* Konten Stat Card */
.stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-label {
  font-size: 0.875rem;
  opacity: 0.9;
  margin: 0 0 0.5rem 0;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.stat-value-currency {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.stat-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

/* Quick Actions */
.quick-actions {
  margin-top: 2rem;
}

.quick-actions h2 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 1rem;
}

@media (min-width: 768px) {
  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Action Card */
.action-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
}

.action-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.action-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.action-icon {
  font-size: 2.5rem;
}

.action-card h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 0.25rem 0;
}

.action-card p {
  font-size: 0.875rem;
  color: #718096;
  margin: 0;
}
</style>
