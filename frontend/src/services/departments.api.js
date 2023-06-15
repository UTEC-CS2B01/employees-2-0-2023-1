import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/departments";

export const create = async (payload) => {
  const { data } = await axios.post(BASE_URL, payload);

  return data;
};
