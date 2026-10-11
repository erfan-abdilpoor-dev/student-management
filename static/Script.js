const nameInput = document.getElementById("StudentName");
const ageInput = document.getElementById("StudentAge");
const codeInput = document.getElementById("StudentCode");
const fieldInput = document.getElementById("StudentField");
const button = document.getElementById("SubmitStudent");
const studentForm = document.getElementById("student-form");
const FlaskMessage = document.getElementById("flask-message");
const StudentList = document.getElementById("students-list");
const StudentCode = document.getElementById("Student-Code");
const StudentAge = document.getElementById("student-age");
const update = document.getElementById("Update");
const updateForm = document.getElementById("update-form");
const DeleteStudentCode = document.getElementById("Delete-Student-Code");
const DeleteButton = document.getElementById("Delete");

async function loadStudents () {
    try {
        const response = await fetch("/students");

        if (!response.ok) {
            throw new Error(`HTTP Error:${response.status}`);
        }

        const data = await response.json();

        StudentList.innerHTML = "";

        for(let Student of data) {
            const card = document.createElement("div");

            card.className = "student-card";

            card.innerHTML = `
                <h3>${Student.name}</h3>
                <p>Age:${Student.age}</p>
                <p>Code:${Student.code}</p>
                <p>Field:${Student.field}</p>
            `;
            StudentList.appendChild(card);
        }
    }catch (error) {
        console.log("Error:",error.message);
    }
}

DeleteButton.addEventListener("click", async function(event) {
    event.preventDefault();
    if (DeleteStudentCode.value === "") {
        console.log("Code Is Required.")
        return;
    }

    try {
        const response = await fetch("/students/" + DeleteStudentCode.value, {
        method: "DELETE"
        });


        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.Message);
        }
            FlaskMessage.className = "success";
            FlaskMessage.innerHTML = data.Message;

            loadStudents();
        
    } catch (error) {
        FlaskMessage.className = "error";
            FlaskMessage.innerHTML = error.message;
    }
});


updateForm.addEventListener("submit",async function(event) {
    event.preventDefault();
    if (StudentCode.value === "") {
        console.log("ID Is Required.")
        return;
    }

    if (StudentAge.value === "") {
        console.log("Age Is Required For Update.")
        return;
    }

    try {
        const response = await fetch("/students/" + StudentCode.value, {
            method: "PATCH",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                age:StudentAge.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.Message);
        }

        FlaskMessage.className = "success";
        FlaskMessage.innerHTML = data.Message;

        loadStudents();

    } catch (error) {
        FlaskMessage.className = "error";
        FlaskMessage.innerHTML = error.message;
    }
})


studentForm.addEventListener("submit", function(event) {
    event.preventDefault();
    
    if (nameInput.value === "") {
        console.log("Name Is Required.")
        return;
    }

    if (ageInput.value === "") {
        console.log("Age Is Required.")
        return;
    }

    if (codeInput.value === ""){
        console.log("Student Code Required.")
        return;
    }

    if (fieldInput.value === ""){
        console.log("Field Required.")
        return;
    }

    console.log(nameInput.value);
    console.log(ageInput.value);
    console.log(codeInput.value);
    console.log(fieldInput.value);
});
studentForm.addEventListener("submit",async function(event) {
    event.preventDefault();

    if (nameInput.value === "") {
        console.log("Name Is Required.");
        return;
    }

    if (ageInput.value === "") {
        console.log("Age Is Required.");
        return;
    }

    if (codeInput.value === "") {
        console.log("Code Is Required.");
        return;
    }

    if (fieldInput.value === "") {
        console.log("Field Is Required.");
        return;
    }

    try {
        const response = await fetch("/students", {
            method: "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                name:nameInput.value,
                age:ageInput.value,
                code:codeInput.value,
                field:fieldInput.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.Message);
        }
        FlaskMessage.className = "success";

        FlaskMessage.innerHTML =
            data.Message + "<br>" +
            "Name: " + data.Name + "<br>" + 
            "Age: " + data.Age + "<br>" +
            "Code:" + data.Code + "<br>" +
            "Field: " + data.Field;
        
        loadStudents();

        studentForm.reset();

        }catch (error) {
            FlaskMessage.className = "error";

            FlaskMessage.innerHTML = 
            "Something Went Wrong. " + error.message;
        }
    });