<template>
  <div class="app-container">
    <div class="menu">
      <TheNavigation />
    </div>
    <router-view />
  </div>
</template>

<script>
import TheNavigation from "@/views/TheNavigation.vue";
export default {
  name: "App",
  components: {
    TheNavigation,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.app-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.menu {
  position: fixed;
  top: 0;
  left: 0;
  padding: 0px;
}
</style>
