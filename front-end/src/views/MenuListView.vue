<script>
import Navbar from "@/components/Navbar.vue";
import Loading from "@/components/Loading.vue";
import Pagination from "@/components/Pagination.vue";
import Notification from "@/components/Notification.vue";
import menuService from "@/services/menuService";

export default {
  name: "MenuListView",

  components: {
    Navbar,
    Loading,
    Pagination,
    Notification,
  },

  data() {
    return {
      loading: false,
      menus: [],
      filters: {
        search: "",
        kategori: "",
        limit: 10,
        page: 1,
      },
      pagination: {
        page: 1,
        limit: 10,
        total: 0,
        total_pages: 0,
      },
      notification: {
        show: false,
        type: "info",
        message: "",
      },
    };
  },

  mounted() {
    this.loadMenus();
  },

  methods: {
    /**
     * Load data menu dari API
     */
    async loadMenus() {
      this.loading = true;

      try {
        const params = {
          page: this.filters.page,
          limit: this.filters.limit,
        };

        if (this.filters.search) params.search = this.filters.search;
        if (this.filters.kategori) params.kategori = this.filters.kategori;

        const response = await menuService.getAllMenus(params);

        if (response.data.success) {
          this.menus = response.data.data;
          this.pagination = response.data.pagination;
        }
      } catch (error) {
        this.showNotification("error", "Gagal memuat data menu");
      } finally {
        this.loading = false;
      }
    },

    /**
     * Handler ketika filter berubah
     */
    onFilterChange() {
      this.filters.page = 1;
      this.loadMenus();
    },

    onPageChange(page) {
      this.filters.page = page;
      this.loadMenus();
    },

    async deleteMenu(menu) {
      if (!confirm(`Yakin ingin menghapus menu "${menu.nama}"?`)) {
        return;
      }

      try {
        const response = await menuService.deleteMenu(menu.id);

        if (response.data.success) {
          this.showNotification("success", "Menu berhasil dihapus");
          this.loadMenus();
        }
      } catch (error) {
        this.showNotification("error", "Gagal menghapus menu");
      }
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(amount);
    },

    showNotification(type, message) {
      this.notification = { show: true, type, message };
    },
  },
};
</script>

<template>
  <div>
    <Navbar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header & Actions -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Daftar Menu</h1>
          <p class="text-gray-600 mt-1">Kelola menu restoran</p>
        </div>
        <router-link to="/menu/create" class="btn btn-primary">
          ➕ Tambah Menu
        </router-link>
      </div>

      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Search -->
          <input
            v-model="filters.search"
            @input="onFilterChange"
            type="text"
            placeholder="Cari nama menu..."
            class="input"
          />

          <select
            v-model="filters.kategori"
            @change="onFilterChange"
            class="input"
          >
            <option value="">Semua Kategori</option>
            <option value="Makanan">Makanan</option>
            <option value="Minuman">Minuman</option>
            <option value="Dessert">Dessert</option>
            <option value="Snack">Snack</option>
          </select>

          <select
            v-model="filters.limit"
            @change="onFilterChange"
            class="input"
          >
            <option :value="10">10 per halaman</option>
            <option :value="25">25 per halaman</option>
            <option :value="50">50 per halaman</option>
          </select>
        </div>
      </div>

      <Loading v-if="loading" message="Memuat data menu..." />

      <div
        v-else-if="menus.length > 0"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <div
          v-for="menu in menus"
          :key="menu.id"
          class="card hover:shadow-lg transition-shadow"
        >
          <div
            class="relative h-48 bg-gray-200 rounded-lg overflow-hidden mb-4"
          >
            <img
              v-if="menu.gambar"
              :src="`http://localhost:5000/uploads/${menu.gambar}`"
              :alt="menu.nama"
              class="w-full h-full object-cover"
            />
            <div
              v-else
              class="flex items-center justify-center h-full text-6xl"
            >
              🍽️
            </div>

            <div class="absolute top-2 right-2">
              <span
                :class="[
                  'badge',
                  menu.tersedia ? 'badge-success' : 'badge-danger',
                ]"
              >
                {{ menu.tersedia ? "Tersedia" : "Habis" }}
              </span>
            </div>
          </div>

          <div class="mb-4">
            <div class="flex justify-between items-start mb-2">
              <h3 class="font-bold text-lg text-gray-900">{{ menu.nama }}</h3>
              <span class="badge bg-primary-100 text-primary-800">
                {{ menu.kategori }}
              </span>
            </div>
            <p class="text-sm text-gray-600 mb-3 line-clamp-2">
              {{ menu.deskripsi || "Tidak ada deskripsi" }}
            </p>
            <p class="text-xl font-bold text-primary-600">
              {{ formatCurrency(menu.harga) }}
            </p>
          </div>

          <div class="flex space-x-2">
            <router-link
              :to="`/menu/edit/${menu.id}`"
              class="btn btn-secondary flex-1 text-center"
            >
              ✏️ Edit
            </router-link>
            <button @click="deleteMenu(menu)" class="btn btn-danger flex-1">
              🗑️ Hapus
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-12">
        <div class="text-6xl mb-4">🍽️</div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Belum ada menu</h3>
        <p class="text-gray-600 mb-4">
          Mulai tambahkan menu untuk restoran Anda
        </p>
        <router-link to="/menu/create" class="btn btn-primary">
          ➕ Tambah Menu Pertama
        </router-link>
      </div>

      <Pagination
        v-if="pagination.total > 0"
        :current-page="pagination.page"
        :total-pages="pagination.total_pages"
        :total="pagination.total"
        :limit="pagination.limit"
        @page-change="onPageChange"
      />
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
