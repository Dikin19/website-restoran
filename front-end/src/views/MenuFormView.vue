<script>
import Navbar from "@/components/Navbar.vue";
import Loading from "@/components/Loading.vue";
import Notification from "@/components/Notification.vue";
import menuService from "@/services/menuService";

export default {
  name: "MenuFormView",

  components: {
    Navbar,
    Loading,
    Notification,
  },

  data() {
    return {
      loading: false,
      submitting: false,
      isEditMode: false,
      menuId: null,
      form: {
        nama: "",
        deskripsi: "",
        harga: "",
        kategori: "",
      },
      imageFile: null,
      imagePreview: null,
      existingImage: null,
      notification: {
        show: false,
        type: "info",
        message: "",
      },
    };
  },

  mounted() {
    // Cek apakah edit mode (ada parameter id di URL)
    if (this.$route.params.id) {
      this.isEditMode = true;
      this.menuId = parseInt(this.$route.params.id);
      this.loadMenuData();
    }
  },

  methods: {
    /**
     * Load data menu untuk edit
     */
    async loadMenuData() {
      this.loading = true;

      try {
        const response = await menuService.getMenuById(this.menuId);

        if (response.data.success) {
          const menu = response.data.data;
          this.form = {
            nama: menu.nama,
            deskripsi: menu.deskripsi || "",
            harga: menu.harga,
            kategori: menu.kategori,
          };

          if (menu.gambar) {
            this.existingImage = menu.gambar;
            this.imagePreview = `http://localhost:5000/uploads/${menu.gambar}`;
          }
        }
      } catch (error) {
        this.showNotification("error", "Gagal memuat data menu");
        this.$router.push({ name: "MenuList" });
      } finally {
        this.loading = false;
      }
    },

    /**
     * Handle file upload
     */
    handleFileChange(event) {
      const file = event.target.files[0];

      if (!file) return;

      // Validasi ukuran file (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        this.showNotification("error", "Ukuran file maksimal 5MB");
        return;
      }

      if (!file.type.startsWith("image/")) {
        this.showNotification("error", "File harus berupa gambar");
        return;
      }

      this.imageFile = file;

      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },

    removeImage() {
      this.imageFile = null;
      this.imagePreview = null;
      // Jangan hapus existingImage saat edit mode, hanya reset preview
      if (!this.isEditMode) {
        this.existingImage = null;
      }
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
    },

    async handleSubmit() {
      // Validasi form
      if (!this.form.nama || !this.form.nama.trim()) {
        this.showNotification("error", "Nama menu wajib diisi");
        return;
      }

      if (!this.form.harga) {
        this.showNotification("error", "Harga menu wajib diisi");
        return;
      }

      if (!this.form.kategori) {
        this.showNotification("error", "Kategori menu wajib diisi");
        return;
      }

      // Validasi harga
      const harga = parseFloat(this.form.harga);
      if (isNaN(harga) || harga <= 0) {
        this.showNotification("error", "Harga harus berupa angka positif");
        return;
      }

      this.submitting = true;

      try {
        // Buat FormData untuk support upload file
        const formData = new FormData();
        formData.append("nama", this.form.nama.trim());
        formData.append("deskripsi", this.form.deskripsi.trim() || "");
        formData.append("harga", harga.toString());
        formData.append("kategori", this.form.kategori);

        // Tambahkan gambar jika ada file baru
        if (this.imageFile) {
          formData.append("gambar", this.imageFile);
        }

        // Debug: Log FormData content
        console.log("Submitting form:");
        for (let [key, value] of formData.entries()) {
          console.log(`${key}:`, value);
        }

        let response;

        if (this.isEditMode) {
          console.log(`Updating menu ID: ${this.menuId}`);
          response = await menuService.updateMenu(this.menuId, formData);
        } else {
          console.log("Creating new menu");
          response = await menuService.createMenu(formData);
        }

        console.log("Server response:", response.data);

        if (response.data.success) {
          this.showNotification(
            "success",
            response.data.message ||
              (this.isEditMode
                ? "Menu berhasil diupdate"
                : "Menu berhasil ditambahkan")
          );

          // Redirect ke menu list setelah 1.5 detik
          setTimeout(() => {
            this.$router.push({ name: "MenuList" });
          }, 1500);
        } else {
          this.showNotification(
            "error",
            response.data.message || "Gagal menyimpan menu"
          );
        }
      } catch (error) {
        console.error("Error submitting menu:", error);
        console.error("Error details:", {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
        });

        let errorMessage = "Terjadi kesalahan saat menyimpan menu";

        if (error.response) {
          if (error.response.data && error.response.data.message) {
            errorMessage = error.response.data.message;
          } else if (error.response.status === 401) {
            errorMessage = "Sesi login telah berakhir, silakan login kembali";
            setTimeout(() => {
              localStorage.removeItem("isLoggedIn");
              this.$router.push({ name: "Login" });
            }, 2000);
          } else if (error.response.status === 400) {
            errorMessage = "Data yang dikirim tidak valid";
          } else if (error.response.status === 404) {
            errorMessage = "Menu tidak ditemukan";
          } else if (error.response.status === 500) {
            errorMessage = "Terjadi kesalahan server, coba lagi nanti";
          }
        } else if (error.request) {
          errorMessage =
            "Tidak dapat terhubung ke server. Pastikan backend sedang berjalan.";
        }

        this.showNotification("error", errorMessage);
      } finally {
        this.submitting = false;
      }
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

    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ isEditMode ? "Edit Menu" : "Tambah Menu Baru" }}
        </h1>
        <p class="text-gray-600 mt-1">
          {{
            isEditMode
              ? "Perbarui informasi menu"
              : "Isi form untuk menambah menu"
          }}
        </p>
      </div>

      <Loading v-if="loading" message="Memuat data..." />

      <form v-else @submit.prevent="handleSubmit" class="card">
        <!-- Preview Gambar -->
        <div v-if="imagePreview" class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Preview Gambar
          </label>
          <div
            class="relative w-full h-64 bg-gray-100 rounded-lg overflow-hidden"
          >
            <img
              :src="imagePreview"
              alt="Preview"
              class="w-full h-full object-cover"
            />
            <button
              type="button"
              @click="removeImage"
              class="absolute top-2 right-2 bg-red-500 text-white px-3 py-1 rounded-lg hover:bg-red-600"
            >
              ✕ Hapus
            </button>
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Gambar Menu (Opsional)
          </label>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileChange"
            class="input"
          />
          <p class="text-xs text-gray-500 mt-1">
            Format: JPG, PNG, GIF. Maksimal 5MB
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Nama Menu <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.nama"
            type="text"
            class="input"
            placeholder="Contoh: Nasi Goreng Spesial"
            required
          />
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Deskripsi
          </label>
          <textarea
            v-model="form.deskripsi"
            rows="3"
            class="input"
            placeholder="Deskripsi menu..."
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4 mb-4">
          <!-- Harga -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Harga <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.harga"
              type="number"
              min="0"
              step="1000"
              class="input"
              placeholder="25000"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Kategori <span class="text-red-500">*</span>
            </label>
            <select v-model="form.kategori" class="input" required>
              <option value="">Pilih Kategori</option>
              <option value="Makanan">Makanan</option>
              <option value="Minuman">Minuman</option>
              <option value="Dessert">Dessert</option>
              <option value="Snack">Snack</option>
            </select>
          </div>
        </div>

        <div class="flex space-x-3 pt-4 border-t">
          <button
            type="submit"
            class="btn btn-primary flex-1"
            :disabled="submitting"
          >
            <span v-if="submitting">Menyimpan...</span>
            <span v-else
              >💾 {{ isEditMode ? "Update Menu" : "Simpan Menu" }}</span
            >
          </button>
          <router-link to="/menu" class="btn btn-secondary flex-1 text-center">
            ✕ Batal
          </router-link>
        </div>
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
