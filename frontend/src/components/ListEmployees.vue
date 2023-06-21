<template>
  <div class="list-employees">
    <ul>
      <li v-for="employee in employees" :key="employee.id">
        {{ employee.firstname }} {{ employee.lastname }}
      </li>
    </ul>
  </div>
</template>

<script>
import { getAllEmployees } from "@/services/employees.api";
export default {
  name: "ListEmployees",
  data() {
    return {
      employees: [],
    };
  },
  async mounted() {
    const { employees } = await getAllEmployees();
    this.employees = employees;
  },
};
</script>

<style>
.list-departments {
  padding: 0px;
  margin: 0px;
  width: 300px;
}
</style>
