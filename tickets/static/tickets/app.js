const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
            ...(options.headers || {})
        },
        credentials: "same-origin"
    });
    if (response.status === 204) return null;
    const data = await response.json().catch(() => null);
    if (!response.ok) throw new Error(JSON.stringify(data || { detail: "Ошибка" }));
    return data;
}

const categorySelect = document.getElementById("category");
const form = document.getElementById("ticket-form");
const titleInput = document.getElementById("title");
const message = document.getElementById("message");
const list = document.getElementById("tickets-list");
const loading = document.getElementById("loading");
const filter = document.getElementById("status-filter");

let statusModal;
document.addEventListener("DOMContentLoaded", () => {
    statusModal = new bootstrap.Modal(document.getElementById('modal-status'));
});

const statusLabels = {
    'new': { text: 'Новая', class: 'bg-blue-lt' },
    'progress': { text: 'В работе', class: 'bg-warning-lt' },
    'done': { text: 'Выполнена', class: 'bg-success-lt' }
};

function showMessage(text, isError = false) {
    message.textContent = text;
    message.className = "alert " + (isError ? "alert-danger" : "alert-success");
}

function showError(context, error) {
    try {
        const errObj = JSON.parse(error.message);
        const msg = Object.values(errObj).map(v => Array.isArray(v) ? v.join(', ') : v).join(' ');
        showMessage(`${context}: ${msg}`, true);
    } catch {
        showMessage(`${context}: ${error.message}`, true);
    }
}

async function loadCategories() {
    const categories = await apiRequest("/api/categories/");
    categorySelect.replaceChildren();
    for (const cat of categories) {
        const opt = document.createElement("option");
        opt.value = cat.id;
        opt.textContent = cat.name;
        categorySelect.append(opt);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
        await apiRequest("/api/tickets/", {
            method: "POST",
            body: JSON.stringify({ title: titleInput.value, category: Number(categorySelect.value) })
        });
        titleInput.value = "";
        showMessage("Заявка успешно создана");
        await loadTickets();
    } catch (error) {
        showError("Не удалось создать заявку", error);
    }
});

async function loadTickets() {
    loading.hidden = false;
    const params = new URLSearchParams(filter.value ? { status: filter.value } : {});
    try {
        const tickets = await apiRequest("/api/tickets/" + (params.toString() ? "?" + params.toString() : ""));
        list.replaceChildren();
        if (tickets.length === 0) {
            list.innerHTML = '<p class="text-muted text-center py-3">Заявки не найдены</p>';
            return;
        }

        const table = document.createElement("table");
        table.className = "table table-vcenter card-table table-striped";
        table.innerHTML = `
            <thead>
                <tr><th>ID</th><th>Заявка</th><th>Статус</th><th class="w-1">Действия</th></tr>
            </thead>
            <tbody id="t-body"></tbody>
        `;
        list.append(table);
        const tbody = document.getElementById("t-body");

        for (const t of tickets) {
            const row = document.createElement("tr");
            const lbl = statusLabels[t.status] || { text: t.status, class: 'bg-secondary-lt' };
            row.innerHTML = `
                <td><span class="text-muted">${String(t.id).padStart(3, '0')}</span></td>
                <td><strong>${t.title}</strong><div class="text-muted small">${t.category_name}</div></td>
                <td><span class="badge ${lbl.class}">${lbl.text}</span></td>
                <td>
                    <div class="btn-list flex-nowrap">
                        <button class="btn btn-white btn-sm" onclick="openStatusModal(${t.id}, '${t.status}')">Изменить статус</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteTicket(${t.id}, '${t.title.replace(/'/g, "\\'")}')">Удалить</button>
                    </div>
                </td>
            `;
            tbody.append(row);
        }
    } catch (error) {
        showError("Не удалось загрузить заявки", error);
    } finally {
        loading.hidden = true;
    }
}

filter.addEventListener("change", loadTickets);

function openStatusModal(ticketId, currentStatus) {
    document.getElementById('modal-ticket-id').value = ticketId;
    const select = document.getElementById('modal-status-select');
    select.value = currentStatus;

    Array.from(select.options).forEach(opt => {
        opt.disabled = false;
        if (currentStatus === 'new' && opt.value === 'done') opt.disabled = true;
        if (currentStatus === 'progress' && opt.value === 'new') opt.disabled = true;
        if (currentStatus === 'done') opt.disabled = true;
    });
    statusModal.show();
}

async function submitStatusChange() {
    try {
        await apiRequest(`/api/tickets/${document.getElementById('modal-ticket-id').value}/`, {
            method: "PATCH",
            body: JSON.stringify({ status: document.getElementById('modal-status-select').value })
        });
        statusModal.hide();
        showMessage("Статус успешно изменен!");
        await loadTickets();
    } catch (error) {
        statusModal.hide();
        showError("Ошибка изменения статуса", error);
    }
}

async function deleteTicket(ticketId, ticketTitle) {
    if (!confirm(`Удалить заявку «${ticketTitle}»?`)) return;
    try {
        await apiRequest(`/api/tickets/${ticketId}/`, { method: "DELETE" });
        showMessage("Заявка успешно удалена.");
        await loadTickets();
    } catch (error) {
        showError("Не удалось удалить заявку", error);
    }
}

async function initialize() {
    try {
        await loadCategories();
        await loadTickets();
    } catch (error) {
        showMessage("Ошибка инициализации: " + error.message, true);
    }
}

initialize();

