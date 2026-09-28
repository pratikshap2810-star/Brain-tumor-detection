import { createContext, useContext, useState } from "react";
import client from "./api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("user");

    if (!raw || raw === "undefined" || raw === "null") {
      return null;
    }

    try {
      return JSON.parse(raw);
    } catch {
      localStorage.removeItem("user");
      localStorage.removeItem("access_token");
      return null;
    }
  });

  async function login(email, password) {
    const res = await client.post("/auth/login", {
      email,
      password,
    });

    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("user", JSON.stringify(res.data.user));

    setUser(res.data.user);

    return res.data.user;
  }

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setUser(null);
  }

  const authValue = {
    user,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={authValue}>
      {children}
    </AuthContext.Provider>
  );
}

const useAuth = () => {
  return useContext(AuthContext);
};

export { useAuth };