<template>
  <div class="Employee-creation-form">
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
        <input type="number" v-model="employee.age" />
      </div>
      <div class="form-group">
        <label>Image:</label>
        <input type="file" v-on:change="onFileChange" />
      </div>
      <div class="form-group">
        <label>Department:</label>
        <input type="text" v-model="employee.selectDepartment" />
      </div>
      <button class="submit-botton2" type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { create } from "@/services/employees.api";

export default {
  name: "CreateEmployee",
  components: {},
  data() {
    return {
      employee: {
        firstname: "",
        lastname: "",
        age: 0,
        image: "",
        is_active: true,
        department_id: "",
      },
    };
  },

  methods: {
    async createEmployee() {
      console.log(this.employee);
      const data = await create(this.employee);
      console.log(data);
    },

    onFileChange(event) {
      const file = event.target.files[0];
      console.log(file);
    },
  },
};
</script>
<style>
.Employee-creation-form {
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

.submit-button2 {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
