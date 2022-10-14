
DROP TABLE IF EXISTS agent CASCADE;
DROP TABLE IF EXISTS item CASCADE;
DROP TABLE IF EXISTS part_bin CASCADE;
DROP TABLE IF EXISTS storage CASCADE;
DROP TABLE IF EXISTS action CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;

DROP PROCEDURE IF EXISTS proc_simulate_order;
DROP PROCEDURE IF EXISTS proc_use_item;
DROP PROCEDURE IF EXISTS proc_fill_bin;
DROP PROCEDURE IF EXISTS proc_modify_bin;

CREATE TABLE agent (
	ID INTEGER PRIMARY KEY,
	name VARCHAR(50) NOT NULL);

CREATE TABLE item (
	ID SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	item_desc VARCHAR(256) NULL,
	item_type INTEGER NOT NULL,
	item_subtype INTEGER NULL,
	partn VARCHAR(50) NULL,
	manufacturer VARCHAR(50) NULL,
	notes VARCHAR(1024) NULL,
	supplier_id INTEGER NOT NULL);
	
CREATE TABLE part_bin (
	ID SERIAL PRIMARY KEY,
	location_code VARCHAR(50) NOT NULL,
	item_id INTEGER NULL,
	position VARCHAR(50) NOT NULL,
	qty INTEGER NOT NULL,
	max_qty INTEGER NOT NULL);

CREATE TABLE storage (
	ID INTEGER PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	location VARCHAR(50) NOT NULL,
	address VARCHAR(50) NULL);

CREATE TABLE action (
	ID SERIAL PRIMARY KEY,
	action_type INTEGER NOT NULL,
	agent_id INTEGER NOT NULL,
	datetime TIMESTAMP NOT NULL,
	qty INTEGER NOT NULL,
	bin_id INTEGER NOT NULL,
	price DECIMAL(8,2),
	supplier_id INTEGER NULL,
	po_num INTEGER NULL,
	via VARCHAR(50) NULL,
	reason VARCHAR(50) NULL,
	item_id INTEGER NULL);

CREATE TABLE supplier (
	ID INTEGER PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	contact VARCHAR(50) NULL);

CREATE TABLE types (ID SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE subtypes (ID SERIAL PRIMARY KEY, name VARCHAR(50));

-- do all the foreign keys once the tables are created
ALTER TABLE item ADD CONSTRAINT item_supplier_id_fk FOREIGN KEY (supplier_id) REFERENCES supplier (ID);
ALTER TABLE part_bin ADD CONSTRAINT part_bin_item_id_fk FOREIGN KEY (item_id) REFERENCES item (ID);
ALTER TABLE action ADD CONSTRAINT action_agent_id_fk FOREIGN KEY (agent_id) REFERENCES agent (ID);
ALTER TABLE action ADD CONSTRAINT action_part_bin_id_fk FOREIGN KEY (bin_id) REFERENCES part_bin (ID);
ALTER TABLE action ADD CONSTRAINT action_supplier_id_fk FOREIGN KEY (supplier_id) REFERENCES supplier (ID);

CREATE OR REPLACE FUNCTION fn_get_item_info(item_id INTEGER)
RETURNS SETOF record
LANGUAGE SQL
AS $$
	SELECT item.id,item.name,
	item_desc, item_type, item_subtype,
	partn, manufacturer,
	notes, s.name AS supplier_name 
	FROM item 
		LEFT JOIN supplier s ON s.id = item.supplier_id
		WHERE item.id = item_id;
$$;

CREATE PROCEDURE proc_simulate_order(bin_id integer, i_id integer, cnt integer, price decimal(8,2), supplier integer)
LANGUAGE SQL
AS $$ 
	-- post the initial order action
	INSERT INTO action (action_type, agent_id, datetime, qty, bin_id, price, supplier_id, item_id)VALUES(0, 0, CURRENT_TIMESTAMP, cnt, bin_id, price*cnt, supplier, i_id);
	-- post the reciept of the order
	INSERT INTO action (action_type, agent_id, datetime, qty, bin_id, via, item_id)VALUES(1, 0, CURRENT_TIMESTAMP, cnt, bin_id, 'FedEx', i_id);
	-- update the bin with the ordered amount
	UPDATE part_bin SET qty = qty + cnt, item_id=i_id WHERE ID=bin_id;
$$;

CREATE PROCEDURE proc_use_item(bin_id integer, cnt integer)
LANGUAGE plpgsql
AS $$
	DECLARE 
	itid INTEGER := 0;
	BEGIN
	SELECT INTO itid item_id FROM part_bin WHERE ID=bin_id;
	-- post the dispense
	INSERT INTO action (action_type, agent_id, datetime, qty, bin_id, item_id)VALUES(2, 0, CURRENT_TIMESTAMP, cnt, bin_id, itid);
	-- update the bin with the ordered amount
	UPDATE part_bin SET qty = qty - cnt WHERE ID=bin_id;
	END;
$$;

CREATE PROCEDURE proc_fill_bin(bin_id integer, iid integer, cnt integer, maxq integer)
LANGUAGE SQL
AS $$
	-- post the dispense
	INSERT INTO action (action_type, agent_id, datetime, qty, bin_id, item_id)VALUES(4, 0, CURRENT_TIMESTAMP, cnt, bin_id, iid);
	-- update the bin with the ordered amount
	UPDATE part_bin SET qty = qty+cnt, item_id=iid, max_qty=maxq WHERE ID=bin_id;
$$;

CREATE PROCEDURE proc_modify_bin(bin_id integer, iid integer, cnt integer)
LANGUAGE SQL
AS $$
	-- post the dispense
	INSERT INTO action (action_type, agent_id, datetime, qty, bin_id, item_id)VALUES(4, 0, CURRENT_TIMESTAMP, cnt, bin_id, iid);
	-- update the bin with the ordered amount
	UPDATE part_bin SET qty = cnt WHERE ID=bin_id;
$$;