-- Example Oracle procedure for testing conversion

CREATE OR REPLACE PROCEDURE calculate_salary_bonus (
    p_employee_id IN NUMBER,
    p_bonus_percent IN NUMBER,
    p_bonus_amount OUT NUMBER
)
AS
    v_salary NUMBER;
    v_department VARCHAR2(50);
    v_hire_date DATE;
BEGIN
    -- Get employee information
    SELECT salary, department_name, hire_date
    INTO v_salary, v_department, v_hire_date
    FROM employees
    WHERE employee_id = p_employee_id;
    
    -- Calculate bonus
    p_bonus_amount := v_salary * (p_bonus_percent / 100);
    
    -- Add extra bonus for long-term employees
    IF SYSDATE - v_hire_date > 365 * 5 THEN
        p_bonus_amount := p_bonus_amount * 1.1;
    END IF;
    
    -- Log the calculation
    INSERT INTO bonus_log (
        employee_id,
        calculation_date,
        bonus_amount
    ) VALUES (
        p_employee_id,
        SYSDATE,
        p_bonus_amount
    );
    
    COMMIT;
    
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20001, 'Employee not found');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END calculate_salary_bonus;
/
