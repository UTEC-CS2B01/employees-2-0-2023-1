<template>
  <div class="create-employee-form">
    <form @submit.prevent.stop="createEmployeeEvent">
      <div class="form-group">
        <label>First Name:</label>
        <input type="text" v-model="employee.firstname" />
      </div>
      <div class="form-group">
        <label>Last Name:</label>
        <input type="text" v-model="employee.lastname" />
      </div>
      <div class="form-group">
        <label>Age:</label>
        <input type="text" v-model.number="employee.age" />
      </div>
      <div>
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
import { createEmployee } from "@/services/employees.api";
import { getAllDepartments } from "@/services/departments.api";
export default {
  name: "TheNavigation",
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
      const { departments } = await getAllDepartments();
      this.departments = departments;
    },
    async createEmployeeEvent() {
      const data = await createEmployee(this.employee);
      console.log(data);
    },
  },
};
</script>

<style>
.submit-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
