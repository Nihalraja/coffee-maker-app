const BASE_URL = "http://127.0.0.1:5000";

const coffeeMenu = document.getElementById("coffee-menu");
const coffeeSelect = document.getElementById("coffee-id");
const orderForm = document.getElementById("order-form");
const orderHistory = document.getElementById("order-history");
const statusMessage = document.getElementById("status-message");
const inventoryStatus = document.getElementById("inventory-status");

function showStatusMessage(type, message) {
    Swal.fire({
        icon: type,
        title: message,
        showConfirmButton: false,
        timer: 2000
    });
}

async function fetchMenu() {
    const response = await fetch(`${BASE_URL}/menu`);
    const data = await response.json();

    coffeeMenu.innerHTML = "";
    coffeeSelect.innerHTML = "";
    data.menu.forEach(coffee => {
        const menuCard = `
            <div class="col-md-4">
                <div class="card">
                    <h5>${coffee.name}</h5>
                    <p>Price: $${coffee.price}</p>
                </div>
            </div>
        `;
        coffeeMenu.insertAdjacentHTML("beforeend", menuCard);

        const option = document.createElement("option");
        option.value = coffee.id;
        option.textContent = coffee.name;
        coffeeSelect.appendChild(option);
    });
}

async function fetchInventory() {
    const response = await fetch(`${BASE_URL}/inventory`);
    const data = await response.json();

    inventoryStatus.innerHTML = "";
    Object.entries(data.inventory).forEach(([item, quantity]) => {
        const inventoryCard = `
            <div class="col-md-3">
                <div class="card text-center">
                    <h5>${item}</h5>
                    <p>${quantity} units</p>
                </div>
            </div>
        `;
        inventoryStatus.insertAdjacentHTML("beforeend", inventoryCard);
    });
}

async function fetchOrders() {
    const response = await fetch(`${BASE_URL}/orders`);
    const data = await response.json();

    orderHistory.innerHTML = "";
    data.orders.forEach(order => {
        const listItem = `
            <li class="list-group-item">
                <strong>${order.user_name}</strong> ordered <strong>${order.quantity}</strong>x <strong>${order.coffee}</strong> for $${order.total_price}.
            </li>
        `;
        orderHistory.insertAdjacentHTML("beforeend", listItem);
    });
}

orderForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const coffeeId = parseInt(coffeeSelect.value, 10);
    const quantity = parseInt(document.getElementById("quantity").value, 10);
    const userName = document.getElementById("user-name").value.trim();

    const quarters = parseInt(document.getElementById("quarters").value, 10) || 0;
    const dimes = parseInt(document.getElementById("dimes").value, 10) || 0;
    const nickels = parseInt(document.getElementById("nickels").value, 10) || 0;
    const pennies = parseInt(document.getElementById("pennies").value, 10) || 0;

    const totalCoins = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01);

    if (!coffeeId || !quantity || !userName) {
        showStatusMessage("error", "Please fill in all fields.");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL}/menu`);
        const data = await response.json();
        const coffee = data.menu.find(coffee => coffee.id === coffeeId);

        if (!coffee) {
            showStatusMessage("error", "Coffee not found.");
            return;
        }

        const totalPrice = coffee.price * quantity;

        if (totalCoins < totalPrice) {
            showStatusMessage("error", "Not enough coins inserted.");
            return;
        }

        const orderResponse = await fetch(`${BASE_URL}/order`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                coffee_id: coffeeId,
                quantity: quantity,
                user_name: userName,
                coins: { quarters, dimes, nickels, pennies } 
            })
        });

        const orderData = await orderResponse.json();
        if (orderResponse.ok) {
            showStatusMessage("success", "Order placed successfully!");
            fetchInventory();
            fetchOrders();
        } else {
            showStatusMessage("error", orderData.error || "Failed to place order.");
        }
    } catch (error) {
        showStatusMessage("error", "Error connecting to the server.");
    }
});

(async function initializeApp() {
    await fetchMenu();
    await fetchInventory();
    await fetchOrders();
})();
