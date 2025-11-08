-- Example Oracle function for testing conversion

CREATE OR REPLACE FUNCTION get_employee_fullname (
    p_employee_id IN NUMBER
) RETURN VARCHAR2
AS
    v_first_name VARCHAR2(50);
    v_last_name VARCHAR2(50);
    v_fullname VARCHAR2(101);
BEGIN
    SELECT first_name, last_name
    INTO v_first_name, v_last_name
    FROM employees
    WHERE employee_id = p_employee_id;
    
    v_fullname := NVL(v_first_name, '') || ' ' || NVL(v_last_name, '');
    
    RETURN TRIM(v_fullname);
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RETURN 'ERROR';
END get_employee_fullname;
/

-- Example with CURSOR

CREATE OR REPLACE FUNCTION get_department_employees (
    p_department_id IN NUMBER
) RETURN NUMBER
AS
    v_count NUMBER := 0;
    CURSOR emp_cursor IS
        SELECT employee_id, first_name, last_name
        FROM employees
        WHERE department_id = p_department_id;
BEGIN
    FOR emp_rec IN emp_cursor LOOP
        v_count := v_count + 1;
    END LOOP;
    
    RETURN v_count;
END get_department_employees;
/

-- Example with sequence

CREATE OR REPLACE PROCEDURE create_new_employee (
    p_first_name IN VARCHAR2,
    p_last_name IN VARCHAR2,
    p_email IN VARCHAR2,
    p_employee_id OUT NUMBER
)
AS
BEGIN
    p_employee_id := emp_seq.NEXTVAL;
    
    INSERT INTO employees (
        employee_id,
        first_name,
        last_name,
        email,
        hire_date
    ) VALUES (
        p_employee_id,
        p_first_name,
        p_last_name,
        p_email,
        SYSDATE
    );
    
    COMMIT;
END create_new_employee;
/
