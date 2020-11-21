CREATE TABLE "CRYPTOS" (
	"id"	INTEGER,
	"symbol"	TEXT UNIQUE,
	"name"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "MOVEMENTS" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"from_quantity"	REAL,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	FOREIGN KEY("from_currency") REFERENCES "CRYPTOS"("id"),
	PRIMARY KEY("id"),
	FOREIGN KEY("to_currency") REFERENCES "CRYPTOS"("id")
)