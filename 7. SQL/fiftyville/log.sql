-- theft took place on July 28, 2020 on Chamberlin Street, 10.15am. 

-- identify the crime and learn more about the details of the crime.
SELECT description FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28
AND street = "Chamberlin Street";

-- extract witness statements for clues.
SELECT transcript FROM interviews
WHERE transcript LIKE "%Courthouse%";

-- clue #1: thief got into car within 10 minutes of theft: suspect list 1.
SELECT name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020 AND month = 7 AND day = 28
AND hour = 10
AND minute > 15 AND minute <= 25
AND activity = "exit";

-- clue #2: thief withdrew money on Fifer Street before theft: suspect list 2.
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28
AND atm_location = "Fifer Street"
AND transaction_type = "withdraw");

-- clue #3.1: thief called the accomplice for less than a minute: suspect list 3.
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2020 AND month = 7 AND day = 28
AND duration < 60;
-- clue #3.2: accomplice scheduled the earliest flight out of fiftyville for the thief the next day: suspect list 4.
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id IN (SELECT id FROM flights
WHERE year = 2020 AND month = 7 AND day = 29
AND origin_airport_id IN (SELECT id FROM airports
WHERE city = "Fiftyville")
ORDER BY hour, minute DESC LIMIT 1);

-- compile all the suspect lists and find the thief: refer to below for code
-- The THIEF is: Ernest

-- find escape destination
SELECT city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE flights.id IN (SELECT flight_id FROM passengers
WHERE passport_number IN (SELECT passport_number FROM people
WHERE name = "Ernest"));
--The thief ESCAPED TO: London

-- find accomplice
SELECT name FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE year = 2020 AND month = 7 AND day = 28
AND duration < 60
AND caller IN (SELECT phone_number FROM people
WHERE name = "Ernest");
--The ACCOMPLICE is: Berthold




-- compile all the suspect lists and find the thief
SELECT name FROM people
JOIN courthouse_security_logs ON people.license_plate = courthouse_security_logs.license_plate
WHERE year = 2020 AND month = 7 AND day = 28
AND hour = 10
AND minute > 15 AND minute <= 25
AND activity = "exit"

INTERSECT

SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
WHERE account_number IN (SELECT account_number FROM atm_transactions
WHERE year = 2020 AND month = 7 AND day = 28
AND atm_location = "Fifer Street"
AND transaction_type = "withdraw")

INTERSECT

SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2020 AND month = 7 AND day = 28
AND duration < 60

INTERSECT

SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flight_id IN (SELECT id FROM flights
WHERE year = 2020 AND month = 7 AND day = 29
AND origin_airport_id IN (SELECT id FROM airports
WHERE city = "Fiftyville")
ORDER BY hour, minute DESC LIMIT 1);
-- The THIEF is: Ernest