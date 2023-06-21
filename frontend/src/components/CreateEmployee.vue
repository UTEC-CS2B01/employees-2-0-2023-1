<template>
  <div class="create-employee-form">
    <h1>Create Employee</h1>
    <form v-on:submit.prevent.stop="createEmployee">
      <div class="form-group">
        <label>First Name:</label>
        <input type="text" v-model.lazy.trim="employee.firstname" />
      </div>
      <div class="form-group">
        <label>Last Name:</label>
        <input type="text" v-model="employee.lastname" />
      </div>
      <div class="form-group">
        <label>Age:</label>
        <input type="text" v-model.number="employee.age" />
      </div>
      <div class="form-group">
        <select v-model="employee.selectDepartment">
          <option
            v-for="department in departments"
            :key="department.id"
            :value="department.id"
          >
            {{ department.name }}
          </option>
        </select>
      </div>
      <button class="submit-button" type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { createEmployee } from "@/services/employees.api.js";
import { getAllDepartments } from "@/services/departments.api.js";

export default {
  name: "CreateEmployee",
  components: {},
  mounted() {
    this.loadDepartments();
  },
  data() {
    return {
      employee: {
        firstname: "",
        lastname: "",
        age: 0,
        selectDepartment: null,
      },
      departments: [],
    };
  },
  methods: {
    async loadDepartments() {
      // Aquí usas la función importada para obtener los departamentos

      const { departments } = await getAllDepartments();
      this.departments = departments;
      console.log("Departments loaded:", this.departments); // Aquí puedes ver los departamentos en la consola
    },

    async createEmployee() {
      console.log(this.employee);
      // Aquí usas la función importada para crear el empleado
      const data = await createEmployee(this.employee);
      console.log(data);
    },
  },
};
</script>

<style>
.create-employee-form {
  padding: 0;
  margin: 0;
  width: 300px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
}

.submit-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
