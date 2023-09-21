-- Inserting Products
INSERT INTO store_products (slug, sku, title, describtion, unit_price, inventory, last_update, collections_id)
VALUES
  ('product-1', 'SKU001', 'Product 1', 'Description 1', 10.00, 100, '2023-09-21 12:00:00', 1),
  ('product-2', 'SKU002', 'Product 2', 'Description 2', 15.00, 150, '2023-09-22 12:00:00', 2),
  ('product-3', 'SKU003', 'Product 3', 'Description 3', 20.00, 200, '2023-09-23 12:00:00', 3);

-- Inserting Collections
INSERT INTO store_collections (title, featured_product_id)
VALUES
  ('Collection 1', 'SKU001'),
  ('Collection 2', 'SKU002'),
  ('Collection 3', 'SKU003');