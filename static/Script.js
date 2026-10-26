
const nameInput = document.getElementById("StudentName");
const ageInput = document.getElementById("StudentAge");
const codeInput = document.getElementById("StudentCode");
const fieldInput = document.getElementById("StudentField");

const studentForm = document.getElementById("student-form");
const updateForm = document.getElementById("update-form");

const studentCodeInput = document.getElementById("Student-Code");
const studentAgeInput = document.getElementById("student-age");
const deleteCodeInput = document.getElementById("Delete-Student-Code");

const studentList = document.getElementById("students-list");
const message = document.getElementById("flask-message");
const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");
const logoutButton = document.getElementById("logout-button");

function showMessage(element, text, success = false) {
    element.textContent = text;
    element.className = success ? "success" : "error";
}

function setAuthState(isLoggedIn) {
    const managementArea = document.getElementById("management-area");
    managementArea.hidden = !isLoggedIn;

    const panelIds = [
        "add-student-panel",
        "update-student-panel",
        "delete-student-panel",
        "student-section"
    ];

    for (const id of panelIds) {
        const panel = document.getElementById(id);

        panel.hidden = !isLoggedIn;
        panel.classList.toggle("locked", !isLoggedIn);

        panel.querySelectorAll("input, button").forEach((control) => {
            control.disabled = !isLoggedIn;
        });
    }

    logoutButton.disabled = !isLoggedIn;

    document.getElementById("auth-status").textContent = isLoggedIn
        ? "You are logged in."
        : "Please log in to manage students.";
}

async function sendRequest(url, options = {}) {
    const response = await fetch(url, options);

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        const error = new Error(
            data.Message || `Request failed: ${response.status}`
        );

        error.status = response.status;
        throw error;
    }

    return data;
}

async function loadStudents() {
    try {
        const students = await sendRequest("/students");

        setAuthState(true);
        studentList.replaceChildren();

        for (const student of students) {
            const card = document.createElement("div");
            card.className = "student-card";

            const title = document.createElement("h3");
            title.textContent = student.name;

            const age = document.createElement("p");
            age.textContent = `Age: ${student.age}`;

            const code = document.createElement("p");
            code.textContent = `Code: ${student.code}`;

            const field = document.createElement("p");
            field.textContent = `Field: ${student.field}`;

            card.append(title, age, code, field);
            studentList.appendChild(card);
        }

        showMessage(
            message,
            `Loaded ${students.length} students.`,
            true
        );
    } catch (error) {
        studentList.replaceChildren();

        if (error.status === 401) {
            setAuthState(false);
            showMessage(message, "Please log in to view students.");
        } else {
            showMessage(message, error.message);
        }
    }
}

// Login
// Login
loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    try {
        const data = await sendRequest("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: document.getElementById("login-username").value,
                password: document.getElementById("login-password").value
            })
        });

        showMessage(loginMessage, data.Message, true);
        await loadStudents();
    } catch (error) {
        showMessage(loginMessage, error.message);
    }
});

// Logout
// Logout
logoutButton.addEventListener("click", async function () {
    try {
        const data = await sendRequest("/logout", {
            method: "POST"
        });

        setAuthState(false);
        studentList.replaceChildren();

        showMessage(loginMessage, data.Message, true);
        showMessage(message, "");
    } catch (error) {
        showMessage(loginMessage, error.message);

        if (error.status === 401) {
            setAuthState(false);
            studentList.replaceChildren();
        }
    }
});

// Add student
studentForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const age = Number(ageInput.value);

    if (
        !nameInput.value.trim() ||
        !ageInput.value.trim() ||
        !codeInput.value.trim() ||
        !fieldInput.value.trim()
    ) {
        showMessage(message, "Please complete all student fields.");
        return;
    }

    if (!Number.isInteger(age) || age < 0) {
        showMessage(message, "Age must be a non-negative integer.");
        return;
    }

    try {
        const data = await sendRequest("/students", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: nameInput.value.trim(),
                age: age,
                code: codeInput.value.trim(),
                field: fieldInput.value.trim()
            })
        });

        showMessage(message, data.Message, true);
        studentForm.reset();
        await loadStudents();
    } catch (error) {
        showMessage(message, error.message);
    }
});

// Update student age
updateForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const code = studentCodeInput.value.trim();
    const age = Number(studentAgeInput.value);

    if (!code || !studentAgeInput.value.trim()) {
        showMessage(message, "Student code and age are required.");
        return;
    }

    if (!Number.isInteger(age) || age < 0) {
        showMessage(message, "Age must be a non-negative integer.");
        return;
    }

    try {
        const data = await sendRequest(
            `/students/${encodeURIComponent(code)}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ age: age })
            }
        );

        showMessage(message, data.Message, true);
        await loadStudents();
    } catch (error) {
        showMessage(message, error.message);
    }
});

// Delete student
document.getElementById("Delete").addEventListener(
    "click",
    async function (event) {
        event.preventDefault();

        const code = deleteCodeInput.value.trim();

        if (!code) {
            showMessage(message, "Student code is required.");
            return;
        }

        try {
            const data = await sendRequest(
                `/students/${encodeURIComponent(code)}`,
                { method: "DELETE" }
            );

            showMessage(message, data.Message, true);
            deleteCodeInput.value = "";
            await loadStudents();
        } catch (error) {
            showMessage(message, error.message);
        }
    }
);

setAuthState(false);
