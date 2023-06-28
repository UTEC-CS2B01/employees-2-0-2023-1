import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/users";

export const signUp = async (user) => {
<<<<<<< HEAD
=======
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 3944c9d (UTEC-0013 - decorator)
  try {
    const { data } = await axios.post(BASE_URL, user);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> e171a95 (UTEC-0013 - decorator)
=======
<<<<<<< HEAD
=======
>>>>>>> afc068a (UTEC-0013 - decorator)
  const { data } = await axios.post(BASE_URL, user);

  return data;
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
>>>>>>> 3944c9d (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> e4941db (UTEC-0013 - decorator)
=======
>>>>>>> 2264a0b (UTEC-0013 - decorator)
>>>>>>> ddd02cd (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> ff2be9a (UTEC-0013 - decorator)
=======
=======
>>>>>>> 3240eb4 (UTEC-0013 - decorator)
<<<<<<< HEAD
>>>>>>> afc068a (UTEC-0013 - decorator)
=======
=======
>>>>>>> 2264a0b (UTEC-0013 - decorator)
>>>>>>> e171a95 (UTEC-0013 - decorator)
>>>>>>> 3944c9d (UTEC-0013 - decorator)
};
