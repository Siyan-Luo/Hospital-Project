-- Create the inventory table
CREATE TABLE inventory (
    name TEXT,
    reference INTEGER,
    factory TEXT,
    num INTEGER,
    lot INTEGER,
    internal_lot INTEGER,
    arrival DATE,
    expiry DATE,
    PRIMARY KEY (reference, factory, lot, internal_lot)
);

-- Create a trigger to automatically update internal_lot
CREATE TRIGGER update_internal_lot
AFTER INSERT ON inventory
BEGIN
    UPDATE inventory
    SET internal_lot = COALESCE((
        SELECT MAX(internal_lot) + 1
        FROM inventory
        WHERE reference = NEW.reference AND factory = NEW.factory AND (arrival_date != NEW.arrival_date OR lot != NEW.lot)
    ), 1)
    WHERE rowid = NEW.rowid;
END;


CREATE TABLE goods (
    name TEXT,
    reference INTEGER,
    factory TEXT,
    total_num INTEGER,
    safenumber INTEGER DEFAULT 0,
    PRIMARY KEY (reference, factory)
);

CREATE TRIGGER update_goods
AFTER INSERT ON inventory
BEGIN
    INSERT OR REPLACE INTO goods (name, reference, factory, total_num, safenumber)
    SELECT NEW.name, NEW.reference, NEW.factory, SUM(num), COALESCE(
        (SELECT safenumber FROM goods WHERE reference = NEW.reference AND factory = NEW.factory),
        0
    )
    FROM inventory
    WHERE reference = NEW.reference AND factory = NEW.factory;
END;


CREATE TRIGGER update_goods_after_update
AFTER UPDATE ON inventory
BEGIN
    -- Calculate and update the total_num for the updated (reference, factory) combination
    UPDATE goods
    SET total_num = (
        SELECT SUM(num) FROM inventory WHERE reference = NEW.reference AND factory = NEW.factory
    )
    WHERE name = NEW.name AND reference = NEW.reference AND factory = NEW.factory;
END;

CREATE TRIGGER update_goods_after_delete
AFTER DELETE ON inventory
BEGIN
    -- Calculate and update the total_num for the affected (reference, factory) combination
    UPDATE goods
    SET total_num = (
        SELECT SUM(num) FROM inventory WHERE reference = OLD.reference AND factory = OLD.factory
    )
    WHERE name = OLD.name AND reference = OLD.reference AND factory = OLD.factory;
	
   	DELETE FROM goods
    WHERE total_num IS NULL;
END;

-- Populate the table
INSERT INTO inventory (name, reference, factory, num, lot, arrival, expiry)
VALUES ('Tubes', 1234, 'PeachBio', 10, 1001, '2023-09-01', '2023-12-31');
INSERT INTO inventory (name, reference, factory, num, lot, arrival, expiry)
VALUES ('Tubes', 1234, 'PeachBio', 10, 1001, '2023-09-02', '2023-12-31');
INSERT INTO inventory (name, reference, factory, num, lot, arrival, expiry)
VALUES ('Tips', 1235, 'PearBio', 10, 1101, '2023-09-01', '2023-12-31');
INSERT INTO inventory (name, reference, factory, num, lot, arrival, expiry)
VALUES ('Tubes', 1234, 'PeachBio', 5, 1002, '2023-09-03', '2023-12-31');