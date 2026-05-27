import React, { useState, useEffect } from "react";

function Dealers() {
  const [dealers, setDealers] = useState([]);
  const [state, setState] = useState("All");
  const [states, setStates] = useState([]);
  const userName = sessionStorage.getItem("username") || null;

  const getDealers = async (filterState = "All") => {
    let url = "/djangoapp/get_dealers/";
    if (filterState !== "All") {
      url = `/djangoapp/get_dealers/${filterState}/`;
    }
    const res = await fetch(url);
    const data = await res.json();
    const dealerList = data.dealers || [];
    setDealers(dealerList);
    const uniqueStates = [...new Set(dealerList.map((d) => d.state))].sort();
    setStates(uniqueStates);
  };

  useEffect(() => {
    getDealers();
  }, []);

  const handleStateChange = (e) => {
    const val = e.target.value;
    setState(val);
    getDealers(val);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ textAlign: "center", color: "#1a1a2e" }}>Dealerships</h1>

      <div style={{ textAlign: "right", marginBottom: "10px" }}>
        {userName ? (
          <span>Welcome, <strong>{userName}</strong></span>
        ) : (
          <span>
            <a href="/login">Login</a> | <a href="/register">Register</a>
          </span>
        )}
      </div>

      <div style={{ marginBottom: "20px" }}>
        <label htmlFor="state-filter"><strong>Filter by State: </strong></label>
        <select id="state-filter" value={state} onChange={handleStateChange}>
          <option value="All">All States</option>
          {states.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#1a1a2e", color: "#fff" }}>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>ID</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Dealer Name</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>City</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>State</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Zip</th>
            <th style={{ padding: "10px", border: "1px solid #ddd" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {dealers.map((dealer) => (
            <tr key={dealer.id} style={{ background: "#fff" }}>
              <td style={{ padding: "8px", border: "1px solid #ddd", textAlign: "center" }}>{dealer.id}</td>
              <td style={{ padding: "8px", border: "1px solid #ddd" }}>{dealer.full_name}</td>
              <td style={{ padding: "8px", border: "1px solid #ddd" }}>{dealer.city}</td>
              <td style={{ padding: "8px", border: "1px solid #ddd" }}>{dealer.state}</td>
              <td style={{ padding: "8px", border: "1px solid #ddd" }}>{dealer.zip}</td>
              <td style={{ padding: "8px", border: "1px solid #ddd", textAlign: "center" }}>
                <a href={`/dealer/${dealer.id}`} style={{ color: "#e94560", fontWeight: "bold" }}>
                  Review Dealer
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dealers;
