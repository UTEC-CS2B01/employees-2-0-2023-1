<template>
  <div>
    <h1>Sign Up!</h1>
    <form @submit.prevent.stop="signUpEvent">
      <div>
        <label>Username:</label>
        <input type="text" v-model="user.username" />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="user.password" />
      </div>
      <div>
        <label>Confirmation Password:</label>
        <input type="password" v-model="user.confirmationPassword" />
      </div>
      <button class="submit-button" type="submit">Submit</button>
    </form>
    <div class="user-message-error" v-if="errorList.lenght> 0">
      <ul>
        <li v-for="error in errorList" :key="error">
          {{ error }}
        </li> 
      </ul>
    </div>
    <div v-else>
      <h1>Sign Up!</h1>
      <p>Thank you for signing up!</p>
    </div>
  </div>
  
</template>


<script>
import { signUp } from "@/services/users.api";
export default {
  name: "SignUp",
  data() {
    return {
      user: {
        username: "",
        password: "",
        confirmationPassword: "",
      },
    };
  },
  methods: {
    async signUpEvent() {
      const response = await signUp(this.user);
      console.log("response: ", response);
    },
  },
};
</script>

<style>
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="password"] {
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
