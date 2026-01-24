// --- Configuration ---
const API_URL = "http://127.0.0.1:5000";

// --- DOM Elements ---
const overlay = document.getElementById("overlay");
const coursePopup = document.getElementById("course-popup");
const assignPopup = document.getElementById("assignment-popup");
const cardsContainer = document.querySelector(".cards-box");
const semesterSelect = document.getElementById('semester-select');

const courseForm = document.getElementById("course-form");
const assignForm = document.getElementById("assign-form");

// State Variable to track which course we are adding an assignment to
let currentCourseId = null;

// --- Event Listeners ---
if (semesterSelect) {
    semesterSelect.addEventListener('change', (e) => {
        const selectedSemester = e.target.value;
        loadData(selectedSemester);
    });
}

// Open Course Popup
document.querySelector('.add-course').addEventListener("click", () => {
    courseForm.reset();
    openPopup(coursePopup);
});

// Close Popups (X buttons and Cancel buttons)
document.querySelectorAll('.close-btn, .cancel').forEach(btn => {
    btn.addEventListener('click', closeAllPopups);
});

// Handle Course Form Submit
courseForm.addEventListener("submit", async (e) => {
    e.preventDefault(); // Stop page reload

    const courseData = {
        name: document.getElementById("course-name").value,
        semester: document.getElementById("semester").value
    };

    await createCourse(courseData);
});

// Handle Assignment Form Submit
assignForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!currentCourseId) return alert("Error: No course selected");

    // Format dates to ISO string for Python (YYYY-MM-DD)
    const startDateInput = document.getElementById("start-date").value;
    const dueDateInput = document.getElementById("end-date").value;

    const assignData = {
        course_id: currentCourseId,
        title: document.getElementById("assign-name").value,
        description: document.getElementById("assign-description").value,
        start_date: startDateInput,
        due_date: dueDateInput
    };

    await createAssignment(assignData);
});

// --- API Functions ---
window.onload = () => {
    loadData(); // Load all by default
};

// Helper to refresh the board based on semester
async function loadData(semester = null) {
    cardsContainer.innerHTML = ''; // Clear the UI

    // We must await courses first, so the cards exist before we try to put assignments in them
    await fetchCourses(semester);
    await fetchAssignments();
}

// 2. Fetch and Render Courses
async function fetchCourses(semester = null) {
    try {
        // Build URL: if semester is present, add ?semester=X
        let url = `${API_URL}/courses`;
        if (semester) {
            url += `?semester=${semester}`;
        }

        const res = await fetch(url, { credentials: 'include' });
        const courses = await res.json();

        if (courses.length === 0) {
            cardsContainer.innerHTML = '<p style="text-align:center; width:100%; margin-top:20px;">No courses found for this semester.</p>';
        } else {
            courses.forEach(course => renderCourse(course));
        }
    } catch (err) {
        console.error("Error loading courses:", err);
    }
}

// 3. Fetch and Render Assignments
async function fetchAssignments() {
    try {
        const res = await fetch(`${API_URL}/assignments`, { credentials: 'include' });
        const assignments = await res.json();

        assignments.forEach(assign => {
            renderAssignment(assign);
        });
    } catch (err) {
        console.error("Error loading assignments:", err);
    }
}

// 4. Create Course (POST)
async function createCourse(data) {
    try {
        const res = await fetch(`${API_URL}/courses`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: 'include'
        });

        if (res.ok) {
            const newCourse = await res.json();
            renderCourse(newCourse); // Add to UI immediately
            closeAllPopups();
        } else {
            alert("Failed to create course");
        }
    } catch (err) {
        console.error(err);
    }
}

// 5. Create Assignment (POST)
async function createAssignment(data) {
    try {
        const res = await fetch(`${API_URL}/assignments`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            credentials: 'include'
        });

        if (res.ok) {
            const newAssign = await res.json();
            renderAssignment(newAssign); // Add to UI immediately
            closeAllPopups();
        } else {
            const err = await res.json();
            alert("Error: " + (err.message || "Failed to add assignment"));
        }
    } catch (err) {
        console.error(err);
    }
}

// 6. Delete Course
async function deleteCourse(id, cardElement) {
    if (!confirm("Delete this course and all its assignments?")) return;

    try {
        const res = await fetch(`${API_URL}/course/${id}`, { method: "DELETE", credentials: 'include' });
        if (res.ok) {
            cardElement.remove();
        }
    } catch (err) { console.error(err); }
}

// 7. Delete Assignment
async function deleteAssignment(id, assignElement) {
    if (!confirm("Delete this assignment?")) return;

    try {
        const res = await fetch(`${API_URL}/assignments/${id}`, { method: "DELETE", credentials: 'include' });
        if (res.ok) {
            assignElement.remove();
        }
    } catch (err) { console.error(err); }
}

// --- UI Rendering Helper Functions ---

function renderCourse(course) {
    const courseCard = document.createElement("div");
    courseCard.className = 'card';
    // IMPORTANT: Store the ID in the HTML so we can find it later
    courseCard.dataset.id = course.id;

    courseCard.innerHTML = `
        <div class="card-head">
            <div>
                <i class="fa-solid fa-book-open"></i>
                <h2>${course.name} <br>
                    <small style="font-size: 12px; color: #777;">Semester: ${course.semester}</small>
                </h2>
            </div>
            <i class="fa-solid fa-trash delete-course-btn admin-only" style="cursor:pointer; color: #ff6b6b;"></i>
        </div>
        <div class="assignments-container"></div>
        <button class="add-assign-btn admin-only">+ Add Assignment</button>
    `;

    // Add Event Listener for "Add Assignment" button on this specific card
    courseCard.querySelector(".add-assign-btn").addEventListener("click", () => {
        currentCourseId = course.id; // REMEMBER THIS ID
        assignForm.reset();
        openPopup(assignPopup);
    });

    // Add Delete Listener
    courseCard.querySelector(".delete-course-btn").addEventListener("click", () => {
        deleteCourse(course.id, courseCard);
    });

    cardsContainer.appendChild(courseCard);
}

function renderAssignment(assign) {
    // Find the course card that matches the course_id
    const courseCard = document.querySelector(`.card[data-id='${assign.course_id}']`);

    // SAFETY CHECK: If we filtered the courses (e.g. showing Sem 1), 
    // but this assignment belongs to Sem 2, courseCard will be null.
    // We simply return and don't render it.
    if (!courseCard) return;

    const container = courseCard.querySelector(".assignments-container");
    const assignEl = document.createElement("div");

    // ... (Rest of your renderAssignment logic remains exactly the same) ...
    assignEl.className = "assignment";

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const dueDate = new Date(assign.due_date);
    dueDate.setHours(0, 0, 0, 0);

    let bgColor = "";
    if (today.getTime() > dueDate.getTime()) {
        bgColor = "#f8b2b2ff";
    } else if (today.getTime() === dueDate.getTime()) {
        bgColor = "#f7e8b5ff";
    } else {
        bgColor = "#afffcbff";
    }

    assignEl.style.backgroundColor = bgColor;
    assignEl.style.borderRadius = "5px";
    assignEl.style.padding = "10px";

    assignEl.innerHTML = `
        <div class="assign-details">
            <h3><i class="fa-regular fa-clock"></i> ${assign.title}</h3>
            <p>${assign.description}</p>
            <div class="time">
                <span>Start: ${assign.start_date}</span>
                <span>Due: ${assign.due_date}</span>
            </div>
        </div>
        <i class="fa-solid fa-trash delete-assign-btn admin-only" style="cursor:pointer; color: #ff6b6b; margin-left:10px;"></i>
    `;

    assignEl.querySelector(".delete-assign-btn").addEventListener("click", () => {
        deleteAssignment(assign.id, assignEl);
    });

    container.appendChild(assignEl);
}

// --- Popup Helpers ---
function openPopup(element) {
    overlay.style.display = "block";
    element.style.display = 'block';
}

function closeAllPopups() {
    overlay.style.display = "none";
    coursePopup.style.display = 'none';
    assignPopup.style.display = 'none';
    currentCourseId = null; // Reset ID
}