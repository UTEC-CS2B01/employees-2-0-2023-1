<template>
  <div class="list-departments">
    <ul>
      <li v-for="department in departments" :key="department.id">
        {{ department.name }}
      </li>
    </ul>
  </div>
</template>

<script>
import { getAllDepartments } from "@/services/departments.api";
export default {
  name: "ListDepartments",
  data() {
    return {
      departments: [], // propiedad
    };
  },
  async mounted() {
    const { departments } = await getAllDepartments();
    this.departments = departments;
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
