<template>
  <div class="create-employee-form">
    <form>
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
        <select v-model="employee.selectedDepartment">
          <option></option>
        </select>
      </div>
    </form>
  </div>
</template>

<script></script>

<style></style>
