<template>
  <div class="department-creation-form">
    <h1>Create Department</h1>
    <form @submit.prevent.stop="createDepartment">
      <div class="form-group">
        <label>Name:</label>
        <input type="text" v-model.lazy.trim="department.name" />
      </div>
      <div class="form-group">
        <label>Short Name:</label>
        <input type="text" v-model="department.short_name" />
      </div>
      <button class="submit-button" type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "CreateDepartment",
  components: {},
  data() {
    return {
      department: {
        name: "",
        short_name: "",
      },
    };
  },
  methods: {
    createDepartment() {
      this.$emit("new-department", this.department);
    },
  },
};
</script>
<style>
.department-creation-form {
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
