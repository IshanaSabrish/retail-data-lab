
-- =====================================================
-- RETAIL DATA LAB: DATABASE SCHEMA
-- Database: retail_analytics
-- PostgreSQL 18
-- =====================================================

-- 1. DIMENSION: DATE
CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    day_of_week SMALLINT NOT NULL,
    is_weekend BOOLEAN NOT NULL,

    CONSTRAINT chk_date_day CHECK (day BETWEEN 1 AND 31),
    CONSTRAINT chk_date_month CHECK (month BETWEEN 1 AND 12),
    CONSTRAINT chk_date_quarter CHECK (quarter BETWEEN 1 AND 4),
    CONSTRAINT chk_date_weekday CHECK (day_of_week BETWEEN 1 AND 7)
);

-- 2. DIMENSION: STORE
CREATE TABLE dim_store (
    store_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_id VARCHAR(20) NOT NULL UNIQUE,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    region VARCHAR(100)
);

-- 3. DIMENSION: PRODUCT
CREATE TABLE dim_product (
    product_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL UNIQUE,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    unit_cost NUMERIC(12,2) NOT NULL,
    regular_price NUMERIC(12,2) NOT NULL,

    CONSTRAINT chk_product_cost CHECK (unit_cost >= 0),
    CONSTRAINT chk_product_price CHECK (regular_price >= 0)
);

-- 4. BRIDGE: STORE-PRODUCT
CREATE TABLE bridge_store_product (
    store_product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    store_key INTEGER NOT NULL REFERENCES dim_store(store_key),
    product_key INTEGER NOT NULL REFERENCES dim_product(product_key),
    active_from_date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    active_to_date_key INTEGER REFERENCES dim_date(date_key),

    CONSTRAINT uq_store_product UNIQUE (store_key, product_key),
    CONSTRAINT chk_active_dates CHECK (
        active_to_date_key IS NULL
        OR active_to_date_key >= active_from_date_key
    )
);

-- 5. FACT: SALES
CREATE TABLE fact_sales (
    sales_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    store_key INTEGER NOT NULL REFERENCES dim_store(store_key),
    product_key INTEGER NOT NULL REFERENCES dim_product(product_key),

    units_sold INTEGER NOT NULL DEFAULT 0,
    units_returned INTEGER NOT NULL DEFAULT 0,

    gross_sales NUMERIC(12,2) NOT NULL DEFAULT 0,
    discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    return_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    net_sales NUMERIC(12,2) NOT NULL DEFAULT 0,
    cogs NUMERIC(12,2) NOT NULL DEFAULT 0,

    CONSTRAINT uq_sales_daily
        UNIQUE (date_key, store_key, product_key),

    CONSTRAINT chk_units_sold CHECK (units_sold >= 0),
    CONSTRAINT chk_units_returned CHECK (units_returned >= 0),
    CONSTRAINT chk_gross_sales CHECK (gross_sales >= 0),
    CONSTRAINT chk_discount CHECK (discount_amount >= 0),
    CONSTRAINT chk_return_amount CHECK (return_amount >= 0),

    CONSTRAINT chk_net_sales CHECK (
        net_sales = gross_sales - discount_amount - return_amount
    )
);

-- 6. FACT: INVENTORY
CREATE TABLE fact_inventory (
    inventory_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dim_date(date_key),
    store_key INTEGER NOT NULL REFERENCES dim_store(store_key),
    product_key INTEGER NOT NULL REFERENCES dim_product(product_key),

    closing_stock INTEGER NOT NULL,

    CONSTRAINT uq_inventory_daily
        UNIQUE (date_key, store_key, product_key),

    CONSTRAINT chk_closing_stock CHECK (closing_stock >= 0)
);

-- =====================================================
-- INDEXES FOR FOREIGN KEY LOOKUPS
-- =====================================================

CREATE INDEX idx_bridge_product
    ON bridge_store_product(product_key);

CREATE INDEX idx_sales_store
    ON fact_sales(store_key);

CREATE INDEX idx_sales_product
    ON fact_sales(product_key);

CREATE INDEX idx_sales_date
    ON fact_sales(date_key);

CREATE INDEX idx_inventory_store
    ON fact_inventory(store_key);

CREATE INDEX idx_inventory_product
    ON fact_inventory(product_key);

CREATE INDEX idx_inventory_date
    ON fact_inventory(date_key);
