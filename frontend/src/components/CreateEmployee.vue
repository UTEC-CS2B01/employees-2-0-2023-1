<template>
  <div class="create-employee-form">
    <h1>Create Employee</h1>
    <form v-on:submit.prevent.stop="createEmployee">
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
      <div class="form-group">
        <label>Departamento:</label>
        <select v-model="employee.selectDepartment">
          <option
            v-for="option in department_options"
            :key="option.id"
            :value="option.id"
          >
            {{ option.value }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label>Image:</label>
        <input type="file" v-on:change="handleFileChange" />
      </div>
      <div class="form-group">
        <button class="submit-button" type="submit">Submit</button>
      </div>
    </form>
  </div>
</template>

<script>
import { createEmployee, imgEmployee } from "@/services/employees.api";
import { getAllDepartments } from "@/services/departments.api";
export default {
  name: "CreateEmployee",
  components: {},
  async mounted() {
    const { departments } = await getAllDepartments();
    departments.forEach((department) => {
      this.department_options.push({
        id: department.id,
        value: department.name,
      });
    });
  },
  data() {
    return {
      employee: {
        firstname: "",
        lastname: "",
        age: "",
        selectDepartment: "",
      },
      department_options: [],
      id: "",
      image: "",
    };
  },
  methods: {
    async createEmployee() {
      const { id } = await createEmployee(this.employee);
      this.id = id;

      const formData = new FormData();
      formData.append("employee_id", id);
      formData.append("image", this.image);
      const { success } = await imgEmployee(formData);
      console.log(success);
    },
    async handleFileChange(event) {
      const file = event.target.files[0];
      this.image = file;
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
