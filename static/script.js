const API_BASE = "http://127.0.0.1:8000";

// ================= TOAST =================
function showToast(msg, isError = false) {
    const toast = document.getElementById('toastMsg');
    toast.textContent = msg;
    toast.style.backgroundColor = isError ? '#b91c1c' : '#166534';
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 3000);
}

// ================= API CALL =================
async function apiCall(endpoint, method = 'GET', body = null) {
    const opts = {
        method,
        headers: { 'Content-Type': 'application/json' }
    };

    if (body) opts.body = JSON.stringify(body);

    const res = await fetch(API_BASE + endpoint, opts);

    if (!res.ok) {
        let err = "Error";
        try {
            const data = await res.json();
            err = data.detail;
        } catch {}
        throw new Error(err);
    }

    return res.json();
}

// ================= PASSENGERS =================
async function loadPassengers() {
    try {
        const data = await apiCall('/view_passenger');

        let rows = "";
        data.forEach(p => {
            rows += `
                <tr>
                    <td>${p.passenger_id}</td>
                    <td>${p.name}</td>
                    <td>${p.gender}</td>
                    <td>${p.mobile_no}</td>
                    <td>${p.email}</td>
                </tr>
            `;
        });

        document.querySelector('#passengerTable tbody').innerHTML =
            rows || `<tr><td colspan="5">No Data</td></tr>`;

    } catch (e) {
        showToast("Passenger load failed", true);
    }
}

// ================= TRAINS =================
async function loadTrains() {
    try {
        const data = await apiCall('/view_train');

        let rows = "";
        data.forEach(t => {
            rows += `
                <tr>
                    <td>${t.train_no}</td>
                    <td>${t.train_name}</td>
                </tr>
            `;
        });

        document.querySelector('#trainTable tbody').innerHTML =
            rows || `<tr><td colspan="2">No Data</td></tr>`;

    } catch (e) {
        showToast("Train load failed", true);
    }
}

// ================= RESERVATIONS =================
async function loadReservations() {
    try {
        const data = await apiCall('/view_reservations');

        let rows = "";
        data.forEach(r => {
            rows += `
                <tr>
                    <td>${r.reservation_id}</td>
                    <td>${r.class_type}</td>
                </tr>
            `;
        });

        document.querySelector('#reservationTable tbody').innerHTML =
            rows || `<tr><td colspan="2">No Data</td></tr>`;

    } catch (e) {
        showToast("Reservation load failed", true);
    }
}

// ================= TICKETS =================
async function loadTickets() {
    try {
        const data = await apiCall('/view_tickets');

        let rows = "";
        data.forEach(t => {
            rows += `
                <tr>
                    <td>${t.ticket_id}</td>
                    <td>${t.journey_date}</td>
                    <td>${t.seat_no}</td>
                    <td>${t.passenger_id}</td>
                    <td>${t.train_no}</td>
                    <td>${t.reservation_id}</td>
                </tr>
            `;
        });

        document.querySelector('#ticketTable tbody').innerHTML =
            rows || `<tr><td colspan="6">No Data</td></tr>`;

    } catch (e) {
        showToast("Ticket load failed", true);
    }
}

// ================= ADD PASSENGER =================
document.getElementById('passengerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        name: passengerName.value,
        gender: passengerGender.value,
        mobile_no: passengerMobile.value,
        email: passengerEmail.value
    };

    try {
        await apiCall('/passenger', 'POST', data);
        showToast("Passenger Added ✅");
        loadPassengers();
        e.target.reset();
    } catch (err) {
        showToast(err.message, true);
    }
});

// ================= ADD TRAIN =================
document.getElementById('trainForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        train_no: parseInt(trainNo.value),
        train_name: trainName.value
    };

    try {
        await apiCall('/add_train', 'POST', data);
        showToast("Train Added 🚆");
        loadTrains();
        e.target.reset();
    } catch (err) {
        showToast(err.message, true);
    }
});

// ================= ADD RESERVATION =================
document.getElementById('reservationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        reservation_id: parseInt(reservationId.value),
        class_type: classType.value
    };

    try {
        await apiCall('/add_reservation', 'POST', data);
        showToast("Class Added 🎫");
        loadReservations();
        e.target.reset();
    } catch (err) {
        showToast(err.message, true);
    }
});

// ================= BOOK TICKET =================
document.getElementById('ticketForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        journey_date: journeyDate.value,
        booking_date: bookingDate.value,
        seat_no: parseInt(seatNo.value),
        passenger_id: parseInt(passengerId.value),
        train_no: parseInt(ticketTrainNo.value),
        reservation_id: parseInt(ticketResId.value)
    };

    try {
        await apiCall('/add_ticket', 'POST', data);
        showToast("Ticket Booked 🎉");
        loadTickets();
        e.target.reset();
    } catch (err) {
        showToast("Booking failed: " + err.message, true);
    }
});

// ================= TAB SWITCH =================
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {

        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active-pane'));

        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active-pane');

        if (btn.dataset.tab === 'passenger-tab') loadPassengers();
        if (btn.dataset.tab === 'train-tab') loadTrains();
        if (btn.dataset.tab === 'reservation-tab') loadReservations();
        if (btn.dataset.tab === 'ticket-tab') loadTickets();
    });
});

// ================= INIT =================
loadPassengers();
loadTrains();
loadReservations();
loadTickets();