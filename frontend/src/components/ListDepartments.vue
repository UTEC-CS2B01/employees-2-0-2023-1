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
export default {
  name: "ListDepartments",
  props: {
    departments: {
      type: [],
      required: true,
    },
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
