const API = "http://127.0.0.1:8000";

function showPanel(id) {
  document.querySelectorAll(".panel").forEach(p =>
    p.classList.add("hidden")
  );
  document.getElementById(id).classList.remove("hidden");

  if (id !== "intake") {
    loadPatients();
  }
}

/* ===============================
   PATIENT INTAKE (LLM CALL)
================================ */
async function submitReport() {
  const patientId = document.getElementById("patientId").value;
  const report = document.getElementById("report").value;

  if (!patientId || !report) {
    alert("Patient ID and report required");
    return;
  }

  const formData = new FormData();
  formData.append("patient_id", patientId);
  formData.append("report", report);

  try {
    const res = await fetch(`${API}/patient/report`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    document.getElementById("intakeResult").innerText =
      JSON.stringify(data, null, 2);
  } catch (err) {
    alert("Backend error");
    console.error(err);
  }
}

/* ===============================
   LOAD ALL PATIENTS
================================ */
async function loadPatients() {
  const res = await fetch(`${API}/patients`);
  const patients = await res.json();

  // Doctor Panel
  document.getElementById("doctorList").innerHTML =
    patients.map(p =>
      `<div class="card">
        <b>${p.patient_id}</b><br/>
        Dept: ${p.department}<br/>
        Risk: ${p.risk_score}<br/>
        Doctor: ${p.doctor}
      </div>`
    ).join("");

  // Nurse Panel
  document.getElementById("nurseList").innerHTML =
    patients.map(p =>
      `<div class="card">
        ${p.patient_id} → Monitor vitals
      </div>`
    ).join("");

  // Admin Panel
  document.getElementById("adminStats").innerHTML =
    `<pre>${JSON.stringify(patients, null, 2)}</pre>`;
}
