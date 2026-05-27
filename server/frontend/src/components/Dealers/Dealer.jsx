import React, { useState, useEffect } from "react";

function Dealer({ dealerId }) {
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const userName = sessionStorage.getItem("username") || null;

  useEffect(() => {
    const id = dealerId || window.location.pathname.split("/").pop();
    fetch(`/djangoapp/dealer/${id}/`)
      .then((r) => r.json())
      .then((data) => setDealer(data.dealer));

    fetch(`/djangoapp/reviews/dealer/${id}/`)
      .then((r) => r.json())
      .then((data) => setReviews(data.reviews || []));
  }, [dealerId]);

  if (!dealer) return <p>Loading...</p>;

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#1a1a2e" }}>{dealer.full_name}</h1>
      <p><strong>City:</strong> {dealer.city}, {dealer.state}</p>
      <p><strong>Address:</strong> {dealer.address}, {dealer.zip}</p>

      <div style={{ textAlign: "right" }}>
        {userName ? (
          <a href={`/postreview/${dealer.id}`} style={{ background: "#e94560", color: "#fff", padding: "8px 16px", borderRadius: "5px", textDecoration: "none" }}>
            Write a Review
          </a>
        ) : (
          <a href="/login">Login to Write a Review</a>
        )}
      </div>

      <h2 style={{ marginTop: "30px" }}>Reviews</h2>
      {reviews.length === 0 ? (
        <p>No reviews yet.</p>
      ) : (
        reviews.map((r) => (
          <div key={r.id} style={{ background: "#f9f9f9", padding: "15px", marginBottom: "15px", borderRadius: "8px", border: "1px solid #eee" }}>
            <p><strong>{r.reviewer_name}</strong> — {r.purchase_date}</p>
            <p>{r.review}</p>
            <p>
              <span style={{ color: r.sentiment === "positive" ? "green" : r.sentiment === "negative" ? "red" : "#888" }}>
                {r.sentiment === "positive" ? "👍 Positive" : r.sentiment === "negative" ? "👎 Negative" : "😐 Neutral"}
              </span>
            </p>
            {r.purchase && <p><em>Purchased: {r.car_year} {r.car_make} {r.car_model}</em></p>}
          </div>
        ))
      )}
    </div>
  );
}

export default Dealer;
