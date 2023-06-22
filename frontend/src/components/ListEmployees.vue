<template>
  <div class="list-employee"></div>
  <ul>
    <li v-for="employee in employees" :key="employee.department_id">
      {{ employee.firstname }}
    </li>
  </ul>
</template>

<script>
import { getAllEmployees } from "@/services/employees.api";
export default {
  name: "ListEmployees",
  mounted() {
    this.loadEmployees();
  },
  data() {
    return {
      employees: [],
    };
  },
  methods: {
    async loadEmployees() {
      const { employees } = await getAllEmployees();
      console.log("employees: ", employees);
      this.employees = employees;
    },
  },
};
</script>

<style></style>
