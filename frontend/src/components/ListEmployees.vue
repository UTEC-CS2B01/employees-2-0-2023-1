<template>
    <div class="employee-list">
      <h1>List of Employees</h1>
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
    name: "EmployeeList",
    data() {
      return {
        employees: [],
      };
    },
    async mounted() {
      await this.fetchEmployees();
    },
    methods: {
      async fetchEmployees() {
        const { employees } = await getAllEmployees();
        this.employees = employees;
      },
    },
  };
  </script>
  
  <style scoped>
  .employee-list {
    padding: 0;
    margin: 0;
    width: 300px;
  }
  </style>