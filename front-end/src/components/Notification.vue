<template>
  <transition name="fade">
    <div
      v-if="show"
      :class="['notification', typeClass]"
      class="fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg text-white cursor-pointer"
      style="min-width: 300px; max-width: 500px"
      @click="close"
    >
      <div class="flex items-center">
        <!-- Icon -->
        <div class="flex-shrink-0">
          <span class="text-2xl">{{ icon }}</span>
        </div>

        <!-- Message -->
        <div class="ml-3 flex-1">
          <p class="text-sm font-medium">{{ message }}</p>
        </div>

        <!-- Close Button -->
        <button @click="close" class="ml-4 text-white hover:text-gray-200">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </button>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Notification",

  props: {
    /**
     * Apakah notification ditampilkan
     */
    show: {
      type: Boolean,
      default: false,
    },

    /**
     * Tipe notification: 'success', 'error', 'warning', 'info'
     */
    type: {
      type: String,
      default: "info",
      validator: (value) =>
        ["success", "error", "warning", "info"].includes(value),
    },

    /**
     * Pesan yang ditampilkan
     */
    message: {
      type: String,
      required: true,
    },

    /**
     * Durasi tampil (ms), 0 = tidak auto close
     */
    duration: {
      type: Number,
      default: 3000,
    },
  },

  computed: {
    /**
     * Class CSS berdasarkan tipe
     */
    typeClass() {
      const classes = {
        success: "bg-green-500",
        error: "bg-red-500",
        warning: "bg-yellow-500",
        info: "bg-blue-500",
      };
      return classes[this.type] || classes.info;
    },

    /**
     * Icon berdasarkan tipe
     */
    icon() {
      const icons = {
        success: "✅",
        error: "❌",
        warning: "⚠️",
        info: "ℹ️",
      };
      return icons[this.type] || icons.info;
    },
  },

  watch: {
    /**
     * Auto close setelah duration
     */
    show(newVal) {
      if (newVal && this.duration > 0) {
        setTimeout(() => {
          this.close();
        }, this.duration);
      }
    },
  },

  methods: {
    /**
     * Close notification
     */
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
/* Fade Transition */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
