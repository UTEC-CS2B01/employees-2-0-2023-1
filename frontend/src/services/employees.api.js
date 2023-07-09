import axios from "axios";

const BASE_URL = "http://127.0.0.1:5002/employees";

const CONFIG = {
  headers: {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": localStorage.getItem("TOKEN"),
  },
};

export const createEmployee = async (employee) => {
  const { data } = await axios.post(BASE_URL, employee, CONFIG);

  return data;
};

export const getAllEmployees = async () => {
  const { data } = await axios.get(BASE_URL, CONFIG);

  return data;
};
