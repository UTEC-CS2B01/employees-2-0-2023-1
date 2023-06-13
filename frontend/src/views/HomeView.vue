<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <p>The counter is: {{ count }}</p>
    <button @click="increment">Increment count</button>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  components: {},
  data() {
    return {
      count: 0,
      name: "",
      lastname: "",
    };
  },
  methods: {
    increment() {
      this.count++;
    },
  },
};
</script>
