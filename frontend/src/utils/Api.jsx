import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// --- INTERCEPTOR: Add Token to Requests Automatically ---
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token"); 
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// --- INTERCEPTOR: Handle 401 Errors ---
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized! Token expired or invalid.");
      
      // 1. Remove the invalid token
      localStorage.removeItem("token");
      
      // 2. Redirect to login to prevent infinite loops or white screens
      // Note: Using window.location.href ensures a full refresh and clears React state
      if (!window.location.pathname.includes('/auth/sign-in')) {
          window.location.href = "/auth/sign-in";
      }
    }
    return Promise.reject(error);
  }
);

export default api;