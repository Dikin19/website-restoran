<script>
import Navbar from "@/components/Navbar.vue";
import Loading from "@/components/Loading.vue";
import Pagination from "@/components/Pagination.vue";
import Notification from "@/components/Notification.vue";
import orderService from "@/services/orderService";

export default {
  name: "OrderListView",

  components: {
    Navbar,
    Loading,
    Pagination,
    Notification,
  },

  data() {
    return {
      loading: false,
      orders: [],
      filters: {
        status: "",
        limit: 10,
        page: 1,
      },
      pagination: {
        page: 1,
        limit: 10,
        total: 0,
        total_pages: 0,
      },
      showDetailModal: false,
      selectedOrder: null,
      notification: {
        show: false,
        type: "info",
        message: "",
      },
    };
  },

  mounted() {
    this.loadOrders();
  },

  methods: {
    async loadOrders() {
      this.loading = true;

      try {
        const params = {
          page: this.filters.page,
          limit: this.filters.limit,
        };

        if (this.filters.status) params.status = this.filters.status;

        const response = await orderService.getAllOrders(params);

        if (response.data.success) {
          this.orders = response.data.data;
          this.pagination = response.data.pagination;
        }
      } catch (error) {
        this.showNotification("error", "Gagal memuat data pesanan");
      } finally {
        this.loading = false;
      }
    },

    onFilterChange() {
      this.filters.page = 1;
      this.loadOrders();
    },

    onPageChange(page) {
      this.filters.page = page;
      this.loadOrders();
    },

    async viewDetail(orderId) {
      try {
        const response = await orderService.getOrderById(orderId);

        if (response.data.success) {
          this.selectedOrder = response.data.data;
          this.showDetailModal = true;
        }
      } catch (error) {
        this.showNotification("error", "Gagal memuat detail pesanan");
      }
    },

    closeDetail() {
      this.showDetailModal = false;
      this.selectedOrder = null;
    },

    async updateStatus(orderId, newStatus) {
      try {
        const response = await orderService.updateOrderStatus(
          orderId,
          newStatus
        );

        if (response.data.success) {
          this.showNotification("success", response.data.message);
          this.loadOrders();
        }
      } catch (error) {
        this.showNotification("error", "Gagal mengupdate status");
      }
    },

    async deleteOrder(order) {
      if (!confirm(`Yakin ingin menghapus pesanan #${order.id}?`)) {
        return;
      }

      try {
        const response = await orderService.deleteOrder(order.id);

        if (response.data.success) {
          this.showNotification("success", "Pesanan berhasil dihapus");
          this.loadOrders();
        }
      } catch (error) {
        this.showNotification("error", "Gagal menghapus pesanan");
      }
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(amount);
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleString("id-ID", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
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
      <div class="flex justify-between items-center mb-6">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">Daftar Pesanan</h1>
          <p class="text-gray-600 mt-1">Kelola pesanan pelanggan</p>
        </div>
        <router-link to="/orders/create" class="btn btn-primary">
          ➕ Buat Pesanan
        </router-link>
      </div>

      <!-- Filters -->
      <div class="card mb-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Status Filter -->
          <select
            v-model="filters.status"
            @change="onFilterChange"
            class="input"
          >
            <option value="">Semua Status</option>
            <option value="pending">Pending</option>
            <option value="selesai">Selesai</option>
          </select>

          <!-- Limit -->
          <select
            v-model="filters.limit"
            @change="onFilterChange"
            class="input"
          >
            <option :value="10">10 per halaman</option>
            <option :value="25">25 per halaman</option>
            <option :value="50">50 per halaman</option>
          </select>

        
          <button @click="loadOrders" class="btn btn-secondary">
            🔄 Refresh
          </button>
        </div>
      </div>


      <Loading v-if="loading" message="Memuat data pesanan..." />


      <div v-else-if="orders.length > 0" class="card overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                ID
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Customer
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Total Harga
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Tanggal
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="order in orders"
              :key="order.id"
              class="hover:bg-gray-50"
            >
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
              >
                #{{ order.id }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">
                  {{ order.nama_customer }}
                </div>
                <div v-if="order.catatan" class="text-xs text-gray-500">
                  {{ order.catatan }}
                </div>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-primary-600"
              >
                {{ formatCurrency(order.total_harga) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'badge',
                    order.status === 'selesai'
                      ? 'badge-success'
                      : 'badge-warning',
                  ]"
                >
                  {{ order.status === "selesai" ? "✅ Selesai" : "⏳ Pending" }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(order.created_at) }}
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
              >
                <button
                  @click="viewDetail(order.id)"
                  class="text-blue-600 hover:text-blue-900"
                  title="Lihat Detail"
                >
                  👁️
                </button>
                <button
                  v-if="order.status === 'pending'"
                  @click="updateStatus(order.id, 'selesai')"
                  class="text-green-600 hover:text-green-900"
                  title="Tandai Selesai"
                >
                  ✅
                </button>
                <button
                  v-else
                  @click="updateStatus(order.id, 'pending')"
                  class="text-yellow-600 hover:text-yellow-900"
                  title="Kembalikan ke Pending"
                >
                  ⏳
                </button>
                <button
                  @click="deleteOrder(order)"
                  class="text-red-600 hover:text-red-900"
                  title="Hapus"
                >
                  🗑️
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>


      <div v-else class="text-center py-12">
        <div class="text-6xl mb-4">📋</div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">
          Belum ada pesanan
        </h3>
        <p class="text-gray-600 mb-4">Mulai buat pesanan untuk customer</p>
        <router-link to="/orders/create" class="btn btn-primary">
          ➕ Buat Pesanan Pertama
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

    
    <div
      v-if="showDetailModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      @click="closeDetail"
    >
      <div
        class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <div class="p-6">
          <!-- Modal Header -->
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-gray-900">
              Detail Pesanan #{{ selectedOrder?.id }}
            </h2>
            <button
              @click="closeDetail"
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

          
          <div v-if="selectedOrder" class="space-y-4">
            <div class="grid grid-cols-2 gap-4 pb-4 border-b">
              <div>
                <p class="text-sm text-gray-600">Customer</p>
                <p class="font-semibold">{{ selectedOrder.nama_customer }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Status</p>
                <span
                  :class="[
                    'badge',
                    selectedOrder.status === 'selesai'
                      ? 'badge-success'
                      : 'badge-warning',
                  ]"
                >
                  {{ selectedOrder.status }}
                </span>
              </div>
              <div>
                <p class="text-sm text-gray-600">Tanggal</p>
                <p class="font-semibold">
                  {{ formatDate(selectedOrder.created_at) }}
                </p>
              </div>
              <div>
                <p class="text-sm text-gray-600">Total</p>
                <p class="font-semibold text-primary-600">
                  {{ formatCurrency(selectedOrder.total_harga) }}
                </p>
              </div>
            </div>

            
            <div>
              <h3 class="font-semibold text-lg mb-3">Items Pesanan</h3>
              <div class="space-y-2">
                <div
                  v-for="item in selectedOrder.items"
                  :key="item.id"
                  class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <p class="font-medium">{{ item.nama_menu }}</p>
                    <p class="text-sm text-gray-600">
                      {{ item.jumlah }} x
                      {{ formatCurrency(item.harga_satuan) }}
                    </p>
                  </div>
                  <p class="font-semibold text-primary-600">
                    {{ formatCurrency(item.subtotal) }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Catatan -->
            <div v-if="selectedOrder.catatan" class="pt-4 border-t">
              <p class="text-sm text-gray-600 mb-1">Catatan:</p>
              <p class="text-gray-900">{{ selectedOrder.catatan }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>


    <Notification
      :show="notification.show"
      :type="notification.type"
      :message="notification.message"
      @close="notification.show = false"
    />
  </div>
</template>
