import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/departments";

const CONFIG = {
  headers: {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": localStorage.getItem("TOKEN"),
  },
};

export const createDepartment = async (payload) => {
  const { data } = await axios.post(BASE_URL, payload, CONFIG);

  return data;
};

export const getAllDepartments = async () => {
  const { data } = await axios.get(BASE_URL, CONFIG);

  return data;
};
