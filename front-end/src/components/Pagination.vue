<script>
export default {
  name: "Pagination",

  props: {
    /**
     * Halaman saat ini
     */
    currentPage: {
      type: Number,
      required: true,
    },

    /**
     * Total halaman
     */
    totalPages: {
      type: Number,
      required: true,
    },

    /**
     * Total data
     */
    total: {
      type: Number,
      required: true,
    },

    /**
     * Limit per halaman
     */
    limit: {
      type: Number,
      required: true,
    },
  },

  computed: {
    /**
     * Item pertama di halaman ini
     */
    startItem() {
      return (this.currentPage - 1) * this.limit + 1;
    },

    /**
     * Item terakhir di halaman ini
     */
    endItem() {
      const end = this.currentPage * this.limit;
      return end > this.total ? this.total : end;
    },

    /**
     * Halaman yang ditampilkan (max 5 halaman)
     */
    visiblePages() {
      const pages = [];
      const maxVisible = 5;

      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
      let end = Math.min(this.totalPages, start + maxVisible - 1);

      // Adjust start jika end sudah mentok
      if (end - start < maxVisible - 1) {
        start = Math.max(1, end - maxVisible + 1);
      }

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      return pages;
    },
  },

  methods: {
    /**
     * Ke halaman tertentu
     */
    goToPage(page) {
      if (page !== this.currentPage) {
        this.$emit("page-change", page);
      }
    },

    /**
     * Ke halaman sebelumnya
     */
    goToPrevious() {
      if (this.currentPage > 1) {
        this.goToPage(this.currentPage - 1);
      }
    },

    /**
     * Ke halaman selanjutnya
     */
    goToNext() {
      if (this.currentPage < this.totalPages) {
        this.goToPage(this.currentPage + 1);
      }
    },
  },
};
</script>

<template>
  <div class="flex items-center justify-between mt-6">
    <div class="text-sm text-gray-600">
      Menampilkan {{ startItem }} - {{ endItem }} dari {{ total }} data
    </div>

    <div class="flex space-x-2">
      <button
        @click="goToPrevious"
        :disabled="currentPage === 1"
        class="px-3 py-1 border rounded-md text-sm"
        :class="
          currentPage === 1
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-white text-gray-700 hover:bg-gray-50'
        "
      >
        Previous
      </button>

      <button
        v-for="page in visiblePages"
        :key="page"
        @click="goToPage(page)"
        class="px-3 py-1 border rounded-md text-sm"
        :class="
          page === currentPage
            ? 'bg-primary-600 text-white'
            : 'bg-white text-gray-700 hover:bg-gray-50'
        "
      >
        {{ page }}
      </button>

      <button
        @click="goToNext"
        :disabled="currentPage === totalPages"
        class="px-3 py-1 border rounded-md text-sm"
        :class="
          currentPage === totalPages
            ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
            : 'bg-white text-gray-700 hover:bg-gray-50'
        "
      >
        Next
      </button>
    </div>
  </div>
</template>
