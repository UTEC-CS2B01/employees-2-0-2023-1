<template>
  <div class="home">
    <div v-for="dpto in allDepartments" :key="dpto.id">
      <h2>{{ dpto.name }}</h2>
      <span class="short-name-span">{{ dpto.shot_name }}</span>
      <figure>
        <img :src="require(`@/assets/${dpto.short_name}.png`)" alt="finanzas" />
      </figure>
    </div>
  </div>
</template>

<script>
import { getAllDepartments } from "@/services/departments.api";
export default {
  name: "HomeView",
  components: {},
  mounted() {
    this.loadAllDepartments();
  },
  data() {
    return {
      allDepartments: [],
    };
  },
  methods: {
    async loadAllDepartments() {
      const { success, departments } = await getAllDepartments();
      if (success) {
        this.allDepartments = departments;
      }
    },
  },
};
</script>

<style scoped>
.short-name-span {
  font-size: 12px;
  color: blue;
}
</style>
