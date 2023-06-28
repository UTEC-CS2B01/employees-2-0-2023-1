import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/users";

export const signUp = async (user) => {
<<<<<<< HEAD
  try {
    const { data } = await axios.post(BASE_URL, user);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
=======
  const { data } = await axios.post(BASE_URL, user);

  return data;
>>>>>>> 2264a0b (UTEC-0013 - decorator)
};
