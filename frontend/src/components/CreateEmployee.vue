<template>
  <div class="employee-creation-form">
    <h1>Create Employee</h1>
    <form @submit.prevent.stop="createEmployee">
      <div class="form-group">
        <label for="firstname">First Name:</label>
        <input type="text" id="firstname" v-model.lazy.trim="employee.firstname" />
      </div>
      <div class="form-group">
        <label for="lastname">Last Name:</label>
        <input type="text" id="lastname" v-model="employee.lastName" />
      </div>
      <div class="form-group">
        <label for="age">Age:</label>
        <input type="number" id="age" v-model="employee.age" />
      </div>
      <button class="submit-button" type="submit">Submit</button>
    </form>
  </div>
</template>
  
  <script>
  import { createEmployee } from "@/services/employees.api";
  
  export default {
    name: "CreateEmployee",
    data() {
      return {
        employee: {
          name: "",
          shortName: "",
        },
      };
    },
    methods: {
      async createEmployee() {
        console.log(this.employee);
        const data = await createEmployee(this.employee);
        console.log(data);
      },
    },
  };
  </script>
  
  <style scoped>
  .employee-creation-form {
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