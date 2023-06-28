import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/users";

export const signUp = async (user) => {
  const { data } = await axios.post(BASE_URL, user);

  return data;
};
