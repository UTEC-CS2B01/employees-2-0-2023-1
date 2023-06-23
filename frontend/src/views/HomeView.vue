<template>
  <div class="home">
    <CreateDepartment @new-department="createDepartmentEvent" />
    <ListDepartments :departments="allDepartments" />
    <CreateEmployee />
    <ListEmployees />
  </div>
</template>

<script>
import CreateDepartment from "@/components/CreateDepartment.vue";
import ListDepartments from "@/components/ListDepartments.vue";
import CreateEmployee from "@/components/CreateEmployee.vue";
import ListEmployees from "@/components/ListEmployees.vue";

import {
  createDepartment,
  getAllDepartments,
} from "@/services/departments.api";
export default {
  name: "HomeView",
  components: {
    CreateDepartment,
    ListDepartments,
    CreateEmployee,
    ListEmployees,
  },
  mounted() {
    this.loadAllDepartments();
  },
  data() {
    return {
      selectedOption: null,
      allDepartments: [],
    };
  },
  methods: {
    async loadAllDepartments() {
      const { departments } = await getAllDepartments();
      console.log("departments: ", departments);
      this.allDepartments = departments;
      console.log("this.allDepartments: ", this.allDepartments);
    },
    async createDepartmentEvent(department) {
      const { department: { id, name } = {}, success } = await createDepartment(
        department
      );
      if (success) {
        this.allDepartments.push({ id, name });
      }
    },
  },
};
</script>

<style></style>
