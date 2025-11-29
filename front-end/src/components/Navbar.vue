<script>
export default {
  name: "Navbar",

  computed: {
    adminName() {
      return localStorage.getItem("adminName") || "Admin";
    },
  },

  methods: {
    handleLogout() {
      // Hapus data login dari localStorage
      localStorage.removeItem("isLoggedIn");
      localStorage.removeItem("adminId");
      localStorage.removeItem("adminName");

      // Redirect ke halaman login
      this.$router.push({ name: "Login" });
    },
  },
};
</script>



<template>
  <nav class="bg-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Brand -->
        <div class="flex items-center space-x-3">
          <span class="text-3xl">🍽️</span>
          <span class="text-xl font-bold text-gray-900 hidden sm:inline"
            >Restoran Admin</span
          >
        </div>

        <!-- Navigation Links -->
        <div class="flex items-center space-x-8">
          <router-link
            to="/dashboard"
            class="text-gray-700 hover:text-primary-600 font-medium px-3 py-2 rounded-md transition-colors"
            active-class="text-primary-600 bg-primary-50"
          >
            Dashboard
          </router-link>
          <router-link
            to="/menu"
            class="text-gray-700 hover:text-primary-600 font-medium px-3 py-2 rounded-md transition-colors"
            active-class="text-primary-600 bg-primary-50"
          >
            Menu
          </router-link>
          <router-link
            to="/orders"
            class="text-gray-700 hover:text-primary-600 font-medium px-3 py-2 rounded-md transition-colors"
            active-class="text-primary-600 bg-primary-50"
          >
            Pesanan
          </router-link>
        </div>

        <!-- User Info & Logout -->
        <div class="flex items-center space-x-4">
          <span class="text-gray-700 font-medium hidden md:inline">{{
            adminName
          }}</span>
          <button
            @click="handleLogout"
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-medium transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>