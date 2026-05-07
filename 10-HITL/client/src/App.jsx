import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [draft, setDraft] = useState("");
  const [final, setFinal] = useState("");
  async function handleSubmit() {
    const res = await fetch("http://localhost:8000/generate-email", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        query,
        thread_id: "User 1",
      }),
    });
    const response = await res?.json();
    console.log(response.draft);
    setDraft(response?.draft);
  }
  const handleResume = async (type) => {
    const res = await fetch("http://localhost:8000/resume", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        approval_status: type === "approve" ? true : false,
        thread_id: "User 1",
      }),
    });
    const response = await res?.json();
    if (response.draft) {
      setDraft(response.draft);
    } else {
      setFinal(response);
    }
  };
  return (
    <>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSubmit}>Submit</button>
      <br />
      <br />
      <br />
      <div>PLATFORM</div>
      <br />
      <br />
      {draft && (
        <div style={{ whiteSpace: "pre-line" }}>
          <p>{draft}</p>

          <br />
          <button onClick={() => handleResume("approve")}>Approve</button>
          <button onClick={() => handleResume("reject")}>Reject</button>
        </div>
      )}
      <br />
      <br />
      {final && <div style={{ whiteSpace: "pre-line" }}>{final}</div>}
    </>
  );
}

export default App;
