<template>
  <div class="home">
    <select v-model="selectedOption">
      <option
        v-for="option in optionsLists"
        :key="option.id"
        :value="option.id"
      >
        {{ option.value }}
      </option>
    </select>

    {{ selectedOption }}

    <CreateDepartment />
    <ListDepartments />
    <CreateEmployee />
    <ListEmployees />
  </div>
</template>

<script>
import CreateDepartment from "@/components/CreateDepartment.vue";
import ListDepartments from "@/components/ListDepartments.vue";
import CreateEmployee from "@/components/CreateEmployee.vue";
import ListEmployees from "@/components/ListEmployees.vue";

export default {
  name: "HomeView",
  components: {
    CreateDepartment,
    ListDepartments,
    CreateEmployee,
    ListEmployees,
  },
  data() {
    return {
      selectedOption: null,
      optionsLists: [
        {
          id: 1,
          value: "option 1",
        },
        {
          id: 2,
          value: "option 2",
        },
        {
          id: 3,
          value: "option 3",
        },
        {
          id: 4,
          value: "option 4",
        },
        {
          id: 5,
          value: "option 5",
        },
        {
          id: 6,
          value: "option 6",
        },
      ],
    };
  },
  methods: {},
};
</script>

<style></style>
