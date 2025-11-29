<template>
 
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",

  mounted() {
    console.log("App component mounted");
  },
};
</script>

<style scoped>
/* Custom styles untuk App component */
</style>
