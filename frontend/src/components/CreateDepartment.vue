<template>
  <div>
    <h1>Create Department</h1>
    <form @submit.prevent.stop="createDepartment">
      <div>
        <label>Name:</label>
        <input type="text" v-model="department.name" />
      </div>
      <div>
        <label>Short Name:</label>
        <input type="text" v-model="department.short_name" />
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { create } from "@/services/departments.api";

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
    async createDepartment() {
      console.log(this.department);
      const data = await create(this.department);
      console.log(data);
    },
  },
};
</script>
<style></style>
