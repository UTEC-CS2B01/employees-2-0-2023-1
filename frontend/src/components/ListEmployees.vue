<template>
  <div class="list-employees">
    <ul>
      <li v-for="employee in employees" :key="employee.id">
        {{ employee.firstname }} - {{ employee.lastname }} -
        {{ employee.age }} años - {{ employee.department_id }}
      </li>
    </ul>
  </div>
</template>
<script>
import { getAllEmployees } from "@/services/employees.api";
import { getAllDepartments } from "@/services/departments.api";
export default {
  name: "ListEmployees",
  data() {
    return {
      employees: [],
      departments: [],
    };
  },
  async mounted() {
    const { data } = await getAllEmployees();
    this.employees = data;

    const data2 = await getAllDepartments();
    this.departments = data2.departments;

    this.employees.forEach((employee) => {
      this.departments.forEach((department) => {
        if (employee.department_id == department.id) {
          employee.department_id = department.name;
        }
      });
    });

    console.log(this.departments);
    console.log(this.employees);
  },
};
</script>
<style>
.list-employees {
  padding: 0px;
  margin: 0px;
  width: 300px;
}
</style>
