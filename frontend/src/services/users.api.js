import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/users";

export const signUp = async (user) => {
  try {
    const { data } = await axios.post(BASE_URL, user);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
  const { data } = await axios.post(BASE_URL, user);

  return data;
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e4941db (UTEC-0013 - decorator)
=======
>>>>>>> 2264a0b (UTEC-0013 - decorator)
>>>>>>> ddd02cd (UTEC-0013 - decorator)
>>>>>>> ff2be9a (UTEC-0013 - decorator)
};
