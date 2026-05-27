import React, { useState } from "react";

function Register() {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("/djangoapp/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.status === "Authenticated") {
        setMessage("Registration successful!");
        window.location.href = "/";
      } else {
        setMessage(data.error || "Registration failed.");
      }
    } catch {
      setMessage("An error occurred.");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "60px auto", padding: 30, background: "#fff", borderRadius: 10, boxShadow: "0 4px 6px rgba(0,0,0,0.1)" }}>
      <h2 style={{ textAlign: "center", color: "#1a1a2e", marginBottom: 20 }}>Sign Up</h2>
      {message && <p style={{ color: "red", textAlign: "center" }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 15 }}>
          <label>Username</label>
          <input
            type="text"
            name="userName"
            value={form.userName}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: 10, border: "1px solid #ddd", borderRadius: 5, marginTop: 5 }}
          />
        </div>
        <div style={{ marginBottom: 15 }}>
          <label>First Name</label>
          <input
            type="text"
            name="firstName"
            value={form.firstName}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: 10, border: "1px solid #ddd", borderRadius: 5, marginTop: 5 }}
          />
        </div>
        <div style={{ marginBottom: 15 }}>
          <label>Last Name</label>
          <input
            type="text"
            name="lastName"
            value={form.lastName}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: 10, border: "1px solid #ddd", borderRadius: 5, marginTop: 5 }}
          />
        </div>
        <div style={{ marginBottom: 15 }}>
          <label>Email</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: 10, border: "1px solid #ddd", borderRadius: 5, marginTop: 5 }}
          />
        </div>
        <div style={{ marginBottom: 20 }}>
          <label>Password</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: 10, border: "1px solid #ddd", borderRadius: 5, marginTop: 5 }}
          />
        </div>
        <button
          type="submit"
          style={{ width: "100%", padding: 12, background: "#e94560", color: "#fff", border: "none", borderRadius: 5, cursor: "pointer", fontSize: 16 }}
        >
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;
