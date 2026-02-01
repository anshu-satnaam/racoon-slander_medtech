const BACKEND_URL = "http://127.0.0.1:8000";

async function submitReport() {
  const patientId = document.getElementById("patientId").value;
  const report = document.getElementById("report").value;

  if (!patientId || !report) {
    alert("Patient ID and report are required");
    return;
  }

  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("result").classList.add("hidden");

  try {
    const res = await fetch(`${BACKEND_URL}/patient/report`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        patient_id: patientId,
        report: report
      })
    });

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const data = await res.json();

    document.getElementById("rPatient").innerText = data.patient_id;
    document.getElementById("rDept").innerText = data.department;
    document.getElementById("rDoctor").innerText = data.doctor;
    document.getElementById("rRisk").innerText = data.risk_score;
    document.getElementById("rSummary").innerText = data.summary;

    document.getElementById("result").classList.remove("hidden");
  } catch (err) {
    alert("Failed to connect to backend");
    console.error(err);
  } finally {
    document.getElementById("loading").classList.add("hidden");
  }
}
