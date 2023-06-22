<template>
  <div class="home">
    <CreateDepartment />
    <ListDepartments />
    <CreateEmployee />
  </div>
</template>

<script>
// LLAMA A LOS COMPONENTES
import CreateDepartment from "@/components/CreateDepartment.vue";
import ListDepartments from "@/components/ListDepartments.vue";
import CreateEmployee from "@/components/CreateEmployee.vue";
export default {
  name: "HomeView",
  components: {
    CreateDepartment,
    ListDepartments,
    CreateEmployee,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style></style>
