import { createClient, print } from 'redis';
import { promisify } from 'util';
const express = require('express');

const listProducts = [
  {Id: 1, name: 'Suitcase 250', price: 50, stock: 4},
  {Id: 2, name: 'Suitcase 450', price: 100, stock: 10},
  {Id: 3, name: 'Suitcase 650', price: 350, stock: 2},
  {Id: 4, name: 'Suitcase 1050', price: 550, stock: 5}
];

function getItemById(id) {
  return listProducts.find((item) => item.Id === id);
}

// Create an express server listening on the port 1245.
const app = express();

const PORT = 1245;

app.get('/list_products', (req,res) => {
  res.json(listProducts);
});

app.listen(PORT, () => {
  console.log(`Server is running and listening on port ${PORT}`);
})

// Create a client to connect to the Redis server
const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// Function to set in Redis the stock for the key item.ITEM_ID
function reserveStockById(itemId, stock) {
  client.set(`item.${itemId}`, stock, print);
}

// Get the reserved stock for an item in redis
async function getCurrentReservedStockById(itemId) {
  const getAsync = promisify(client.get).bind(client);
  try {
    const value = await getAsync(`item.${itemId}`);
    return value;
  } catch (err) {
    console.log(`Error getting value for ${itemId}: ${err}`);
    return 0;
  }
}

// Route to return the current product and its available stock
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId); // Parse the itemId from the URL
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ "status": "Product not found" });
  }

  // Get the reserved stock from Redis
  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = reservedStock ? product.stock - reservedStock : product.stock;

  res.json({
    itemId: product.Id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity: currentQuantity
  });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId) // Parse the itemId from the URL
  const product = getItemById(itemId);
  // Check if product exists
  if (!product) {
    return res.status(404).json({status: "Product not found"})
  }
  //  Get the current reserved stock from Redis
  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = product.stock - reservedStock;
  
  // Check if there is enough stock available
  if (availableStock <= 0) {
    return res.json({
      status: 'Not enough stock available',
      itemId: itemId
    });
  }
  
  // Reserve one item (by increasing the reserved stock)
  reserveStockById(itemId, reservedStock + 1);

  return res.json({
    status: 'Reservation confirmed',
    itemId: itemId
  });
})

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running and listening on port ${PORT}`);
});