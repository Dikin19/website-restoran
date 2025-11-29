<template>
  <!-- ============================================
       ORDER FORM VIEW
       ============================================
       Halaman form untuk buat pesanan baru
  -->
  <div>
    <Navbar />

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">Buat Pesanan Baru</h1>
        <p class="text-gray-600 mt-1">Pilih menu dan isi informasi customer</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit">
        <!-- Customer Info Card -->
        <div class="card mb-6">
          <h2 class="text-xl font-bold text-gray-900 mb-4">
            Informasi Customer
          </h2>

          <!-- Nama Customer -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Nama Customer <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.nama_customer"
              type="text"
              class="input"
              placeholder="Contoh: Budi Santoso"
              required
            />
          </div>

          <!-- Catatan -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Catatan (Opsional)
            </label>
            <textarea
              v-model="form.catatan"
              rows="2"
              class="input"
              placeholder="Contoh: Tidak pakai cabe"
            ></textarea>
          </div>
        </div>

        <!-- Menu Selection Card -->
        <div class="card mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-gray-900">Pilih Menu</h2>
            <button
              type="button"
              @click="showMenuModal = true"
              class="btn btn-primary"
            >
              ➕ Tambah Item
            </button>
          </div>

          <!-- Selected Items -->
          <div v-if="selectedItems.length > 0" class="space-y-3">
            <div
              v-for="(item, index) in selectedItems"
              :key="index"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div class="flex-1">
                <h3 class="font-semibold text-gray-900">{{ item.nama }}</h3>
                <p class="text-sm text-gray-600">
                  {{ formatCurrency(item.harga) }} x {{ item.jumlah }}
                </p>
              </div>

              <!-- Quantity Controls -->
              <div class="flex items-center space-x-3 mr-4">
                <button
                  type="button"
                  @click="decreaseQuantity(index)"
                  class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                >
                  -
                </button>
                <span class="w-8 text-center font-semibold">{{
                  item.jumlah
                }}</span>
                <button
                  type="button"
                  @click="increaseQuantity(index)"
                  class="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center"
                >
                  +
                </button>
              </div>

              <!-- Subtotal & Remove -->
              <div class="text-right">
                <p class="font-bold text-primary-600">
                  {{ formatCurrency(item.harga * item.jumlah) }}
                </p>
                <button
                  type="button"
                  @click="removeItem(index)"
                  class="text-sm text-red-600 hover:text-red-800 mt-1"
                >
                  Hapus
                </button>
              </div>
            </div>

            <!-- Total -->
            <div class="pt-4 border-t flex justify-between items-center">
              <span class="text-lg font-semibold text-gray-900"
                >Total Pembayaran:</span
              >
              <span class="text-2xl font-bold text-primary-600">{{
                formatCurrency(totalHarga)
              }}</span>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-8 text-gray-500">
            <p>Belum ada menu dipilih</p>
            <p class="text-sm">Klik "Tambah Item" untuk memilih menu</p>
          </div>
        </div>

        <!-- Submit Buttons -->
        <div class="flex space-x-3">
          <button
            type="submit"
            class="btn btn-success flex-1"
            :disabled="submitting || selectedItems.length === 0"
          >
            <span v-if="submitting">Memproses...</span>
            <span v-else>💾 Buat Pesanan</span>
          </button>
          <router-link
            to="/orders"
            class="btn btn-secondary flex-1 text-center"
          >
            ✕ Batal
          </router-link>
        </div>
      </form>
    </div>

    <!-- Menu Selection Modal -->
    <div
      v-if="showMenuModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click="closeMenuModal"
    >
      <div
        class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col"
        @click.stop
      >
        <!-- Modal Header -->
        <div class="p-6 border-b flex justify-between items-center">
          <h2 class="text-2xl font-bold text-gray-900">Pilih Menu</h2>
          <button
            @click="closeMenuModal"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Filter -->
        <div class="p-4 border-b">
          <select v-model="menuFilter" @change="loadMenus" class="input">
            <option value="">Semua Kategori</option>
            <option value="Makanan">Makanan</option>
            <option value="Minuman">Minuman</option>
            <option value="Dessert">Dessert</option>
            <option value="Snack">Snack</option>
          </select>
        </div>

        <!-- Modal Body -->
        <div class="flex-1 overflow-y-auto p-6">
          <Loading v-if="loadingMenus" message="Memuat menu..." />

          <div
            v-else
            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          >
            <div
              v-for="menu in availableMenus"
              :key="menu.id"
              @click="addMenuItem(menu)"
              class="border rounded-lg p-4 hover:border-primary-500 hover:shadow-md cursor-pointer transition-all"
            >
              <div class="text-center mb-3">
                <div v-if="menu.gambar" class="h-32 mb-2">
                  <img
                    :src="`http://localhost:5000/uploads/${menu.gambar}`"
                    :alt="menu.nama"
                    class="w-full h-full object-cover rounded"
                  />
                </div>
                <div v-else class="text-5xl mb-2">🍽️</div>
              </div>
              <h3 class="font-semibold text-gray-900 mb-1">{{ menu.nama }}</h3>
              <p class="text-sm text-gray-600 mb-2 line-clamp-2">
                {{ menu.deskripsi }}
              </p>
              <div class="flex justify-between items-center">
                <span class="badge bg-primary-100 text-primary-800 text-xs">{{
                  menu.kategori
                }}</span>
                <span class="font-bold text-primary-600">{{
                  formatCurrency(menu.harga)
                }}</span>
              </div>
            </div>
          </div>

          <div
            v-if="!loadingMenus && availableMenus.length === 0"
            class="text-center py-8 text-gray-500"
          >
            Tidak ada menu tersedia
          </div>
        </div>
      </div>
    </div>

    <!-- Notification -->
    <Notification
      :show="notification.show"
      :type="notification.type"
      :message="notification.message"
      @close="notification.show = false"
    />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Loading from "@/components/Loading.vue";
import Notification from "@/components/Notification.vue";
import menuService from "@/services/menuService";
import orderService from "@/services/orderService";

export default {
  name: "OrderFormView",

  components: {
    Navbar,
    Loading,
    Notification,
  },

  data() {
    return {
      form: {
        nama_customer: "",
        catatan: "",
      },
      selectedItems: [],
      showMenuModal: false,
      loadingMenus: false,
      availableMenus: [],
      menuFilter: "",
      submitting: false,
      notification: {
        show: false,
        type: "info",
        message: "",
      },
    };
  },

  computed: {
    totalHarga() {
      return this.selectedItems.reduce((total, item) => {
        return total + item.harga * item.jumlah;
      }, 0);
    },
  },

  methods: {
    async loadMenus() {
      this.loadingMenus = true;

      try {
        const params = { limit: 100 };
        if (this.menuFilter) params.kategori = this.menuFilter;

        const response = await menuService.getAllMenus(params);

        if (response.data.success) {
          // Filter hanya menu yang tersedia
          this.availableMenus = response.data.data.filter(
            (menu) => menu.tersedia
          );
        }
      } catch (error) {
        this.showNotification("error", "Gagal memuat menu");
      } finally {
        this.loadingMenus = false;
      }
    },

    addMenuItem(menu) {
      // Cek apakah sudah ada di selected items
      const existingIndex = this.selectedItems.findIndex(
        (item) => item.id === menu.id
      );

      if (existingIndex !== -1) {
        // Jika sudah ada, tambah quantity
        this.selectedItems[existingIndex].jumlah++;
      } else {
        // Jika belum ada, tambah item baru
        this.selectedItems.push({
          id: menu.id,
          nama: menu.nama,
          harga: menu.harga,
          jumlah: 1,
        });
      }

      this.showNotification("success", `${menu.nama} ditambahkan`);
    },

    increaseQuantity(index) {
      this.selectedItems[index].jumlah++;
    },

    decreaseQuantity(index) {
      if (this.selectedItems[index].jumlah > 1) {
        this.selectedItems[index].jumlah--;
      }
    },

    removeItem(index) {
      this.selectedItems.splice(index, 1);
    },

    closeMenuModal() {
      this.showMenuModal = false;
    },

    async handleSubmit() {
      // Validasi
      if (!this.form.nama_customer) {
        this.showNotification("error", "Nama customer wajib diisi");
        return;
      }

      if (this.selectedItems.length === 0) {
        this.showNotification("error", "Pilih minimal 1 menu");
        return;
      }

      this.submitting = true;

      try {
        // Format data untuk API
        const orderData = {
          nama_customer: this.form.nama_customer,
          catatan: this.form.catatan,
          items: this.selectedItems.map((item) => ({
            menu_id: item.id,
            jumlah: item.jumlah,
          })),
        };

        const response = await orderService.createOrder(orderData);

        if (response.data.success) {
          this.showNotification("success", "Pesanan berhasil dibuat");

          // Redirect ke order list setelah 1 detik
          setTimeout(() => {
            this.$router.push({ name: "OrderList" });
          }, 1000);
        }
      } catch (error) {
        let errorMessage = "Terjadi kesalahan";

        if (error.response && error.response.data) {
          errorMessage = error.response.data.message;
        }

        this.showNotification("error", errorMessage);
      } finally {
        this.submitting = false;
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

  watch: {
    showMenuModal(newVal) {
      if (newVal) {
        this.loadMenus();
      }
    },
  },
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
